# diagnosis/ml.py

import torchvision.transforms as T
from ultralytics import YOLO
from PIL import Image
from django.conf import settings
import os

# 1) Path to your weights file: PROJECT_ROOT/ml_models/yolov11.pt
WEIGHTS_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'yolov11.pt')

# 2) Load model once at import time
MODEL = YOLO(WEIGHTS_PATH)

# 3) Preprocessing transforms
TRANSFORMS = T.Compose([
    T.Resize((640, 640)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
])

def run_ai_model(image_file):
    """
    Runs inference on a PIL-uploaded image file.
    Returns one of: 'No Findings', 'PTB', or 'Pending'.
    """
    # Open & convert to RGB
    img = Image.open(image_file).convert('RGB')
    # Transform & add batch dimension
    tensor = TRANSFORMS(img).unsqueeze(0)  # [1,C,H,W]

    # Run YOLO inference
    results = MODEL.predict(source=tensor, conf=0.25, device='cpu')
    det = results[0]

    # No boxes → No Findings
    if det.boxes.shape[0] == 0:
        return 'No Findings'

    # Check for PTB class (assumes class index 0 → PTB)
    classes = det.boxes.cls.cpu().numpy().astype(int)
    if 0 in classes:
        return 'PTB'

    # Otherwise fallback
    return 'Pending'
