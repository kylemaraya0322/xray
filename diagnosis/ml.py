# diagnosis/ml.py

import os
import numpy as np
from PIL import Image
from ultralytics import YOLO
from django.conf import settings

# —————————————————————————————————————————————
# Configuration
# —————————————————————————————————————————————
# Path to your YOLO weights file
WEIGHTS_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'best.pt')

# Load the model once at import time
MODEL = YOLO(WEIGHTS_PATH)

# PTB labels to look for (normalized to lowercase + spaces)
PTB_LABELS = {'pleural effusion', 'cavity'}

# Per‐run confidence threshold (low to catch faint detections)
BASE_CONF_THRESH = 0.3

# Final decision threshold on boosted confidence
DECISION_THRESH = 0.5

# Exponent for power‐law boosting (<1 boosts mid‐range scores)
BOOST_GAMMA = 0.6

# Small linear boost factor after gamma
CONF_BOOST_FACTOR = 1.1


def run_ai_model(image_file):
    """
    Runs test‐time augmentation (TTA) + YOLO inference on the uploaded X-ray.
    Returns a tuple (label, confidence):
      - ('No Findings', 1.0) if no PTB cues in any TTA run
      - ('PTB', boosted_conf) if boosted best confidence >= DECISION_THRESH
      - ('No Findings', boosted_conf) otherwise
    """
    # 1) Open image as PIL once
    img = Image.open(image_file).convert('RGB')

    # 2) Define a small suite of augmentations
    tta_fns = [
        lambda x: x,
        lambda x: x.transpose(Image.FLIP_LEFT_RIGHT),
        lambda x: x.rotate(10, expand=False),
        lambda x: x.rotate(-10, expand=False),
        # (you can add more photometric augs here)
    ]

    # 3) Run inference on each augmented image and record best PTB confidence
    confs = []
    for fn in tta_fns:
        aug = fn(img)
        results = MODEL.predict(source=aug, conf=BASE_CONF_THRESH, device='cpu')
        det = results[0]

        run_best = 0.0
        # iterate boxes to find PTB labels
        for cid, cf in zip(det.boxes.cls.cpu().numpy(),
                           det.boxes.conf.cpu().numpy()):
            lbl = results[0].names[int(cid)].lower().replace('_', ' ')
            if lbl in PTB_LABELS:
                run_best = max(run_best, float(cf))
        confs.append(run_best)

    # 4) If absolutely no PTB seen => No Findings @ 100%
    if all(c == 0.0 for c in confs):
        return 'No Findings', 1.0

    # 5) Otherwise take the single best confidence
    best = float(np.max(confs))

    # 6) Apply gamma (power‐law) & linear boost, clamp to 1.0
    boosted = min(best ** BOOST_GAMMA * CONF_BOOST_FACTOR, 1.0)

    # 7) Final decision
    if boosted >= DECISION_THRESH:
        return 'PTB', boosted
    return 'No Findings', boosted
    