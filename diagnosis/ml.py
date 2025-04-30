# diagnosis/ml.py

import os
import numpy as np
from PIL import Image
from ultralytics import YOLO
from django.conf import settings

# —————————————————————————————————————————————
# Configuration
# —————————————————————————————————————————————
WEIGHTS_PATH     = os.path.join(settings.BASE_DIR, 'ml_models', 'best.pt')
MODEL            = YOLO(WEIGHTS_PATH)

# the two pathology classes we care about (normalized)
TARGET_LABELS    = {'cavity', 'pleural effusion'}

# your thresholds & boosting parameters
BASE_CONF_THRESH = 0.3    # filter out very low confidences
DECISION_THRESH  = 0.5    # boosted must reach this to call pathology
BOOST_GAMMA      = 0.6    # power-law exponent
CONF_BOOST_FACTOR= 1.1    # small linear boost after gamma

def run_ai_model(image_file):
    """
    Runs test-time augmentation + YOLO inference on the uploaded X-ray.
    Returns (label, confidence) where label ∈ {"Cavity","Pleural Effusion","No Findings"}.
    """

    # 1) load image once
    img = Image.open(image_file).convert('RGB')

    # 2) small TTA: identity, flip, slight rotations
    tta_fns = [
        lambda x: x,
        lambda x: x.transpose(Image.FLIP_LEFT_RIGHT),
        lambda x: x.rotate(10,  expand=False),
        lambda x: x.rotate(-10, expand=False),
    ]

    # 3) gather per-run best confidences for each class
    cav_confs = []
    eff_confs = []

    for fn in tta_fns:
        aug = fn(img)
        results = MODEL.predict(source=aug, conf=BASE_CONF_THRESH, device='cpu')
        det = results[0]

        best_cav = 0.0
        best_eff = 0.0

        # inspect each box
        for cid, cf in zip(det.boxes.cls.cpu().numpy(),
                           det.boxes.conf.cpu().numpy()):
            lbl = results[0].names[int(cid)].lower().replace('_',' ')
            if lbl == 'cavity':
                best_cav = max(best_cav, float(cf))
            elif lbl == 'pleural effusion':
                best_eff = max(best_eff, float(cf))

        cav_confs.append(best_cav)
        eff_confs.append(best_eff)

    # 4) if nothing seen at all, return clean
    if max(cav_confs + eff_confs) == 0.0:
        return 'No Findings', 1.0

    # 5) pick the raw best per class across TTA
    raw_cav = float(np.max(cav_confs))
    raw_eff = float(np.max(eff_confs))

    # 6) boost them
    boosted_cav = min(raw_cav ** BOOST_GAMMA * CONF_BOOST_FACTOR, 1.0)
    boosted_eff = min(raw_eff ** BOOST_GAMMA * CONF_BOOST_FACTOR, 1.0)

    # 7) make decision
    if boosted_cav < DECISION_THRESH and boosted_eff < DECISION_THRESH:
        # neither strong enough
        return 'No Findings', max(boosted_cav, boosted_eff)

    # otherwise pick whichever is stronger
    if boosted_cav > boosted_eff:
        return 'Cavity', boosted_cav
    else:
        return 'Effusion', boosted_eff
