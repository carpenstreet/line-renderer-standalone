import os
import pathlib

from PIL import Image
from torchvision import transforms
import torch
import timm
import numpy as np
from typing import List, Any
import torch.nn as nn
import random
import glob
import re

### VARIABLES ###

# For Pre-processing
custom_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# Model
class Network(nn.Module):
    def __init__(self, model_name, p=0.25):
        super(Network, self).__init__()
        self.model = timm.create_model(model_name, pretrained=True, num_classes=3, drop_rate=0.2)

    def forward(self, img):
        return self.model(img)


# For Post-processing
FIRST_ELEM_MAX = 6
FIRST_ELEM_STEP_SIZE = 0.5

SECOND_ELEM_MAX = 1
SECOND_ELEM_STEP_SIZE = 0.1

THIRD_ELEM_MAX = 1
THIRD_ELEM_STEP_SIZE = 0.1


### END OF VARIABLES###

def fix_everything(random_seed):
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed(random_seed)
    torch.cuda.manual_seed_all(random_seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    np.random.seed(random_seed)
    random.seed(random_seed)


def compute(img_paths: List[str], model_ckpt: str, model_name: str):
    # Set device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # Get Model
    model = get_model(model_ckpt, model_name).to(device)
    # Get Image
    img = get_image_tensors(img_paths).to(device)
    # Feed Image into Model
    model.eval()
    with torch.no_grad():
        out = model(img).detach().cpu().numpy()
    return post_process(out)


def get_image_tensors(img_paths: List[str]):
    return torch.cat([custom_transform(Image.open(img_path).convert("RGB")).unsqueeze(0) for img_path in img_paths],
                     dim=0)


def get_model(model_ckpt: str, model_name: str):
    model = Network(model_name)
    try:
        model.load_state_dict(torch.load(model_ckpt))
    except Exception as e:
        keys = torch.load(model_ckpt)
        new_keys = {k[7:]: v for k, v in keys.items()}
        model.load_state_dict(new_keys)
        print(e)

    return model


def post_process(pred):
    pred[pred > 1] = 1
    pred[pred < 0] = 0

    # Since first element minimum is 1:
    pred[:, 0] = np.round(pred[:, 0] * FIRST_ELEM_MAX / FIRST_ELEM_STEP_SIZE) * FIRST_ELEM_STEP_SIZE
    pred[:, 0][pred[:, 0] < 1] = 1

    pred[:, 1] = np.round(pred[:, 1] * SECOND_ELEM_MAX / SECOND_ELEM_STEP_SIZE) * SECOND_ELEM_STEP_SIZE
    pred[:, 2] = np.round(pred[:, 2] * THIRD_ELEM_MAX / THIRD_ELEM_STEP_SIZE) * THIRD_ELEM_STEP_SIZE

    return [{
        "width": pred[idx][0].item(),
        "dynamics": pred[idx][1].item(),
        "jitter": pred[idx][2].item()
    } for idx in range(len(pred))]


def get_WDJ_values(img_paths):
    """
    img_paths is a list of image filenames - but image filename should have a specific formatting.
    i.e. one element could be './data/LineStyleData_0/w1.5d0.1j0.1png
    """
    values = []
    for img_title in img_paths:
        matches = re.findall(r'[0-9]+\.?[0-9]*', img_title.split("/")[-1])
        label = [float(x) for x in matches]
        values.append(label)
    return values


def usage(img_path: str) -> list[dict[str, Any]]:
    MODEL_NAME = "convnext_small"  # This is fixed, for now.
    img_paths = [img_path]
    model_ckpt = os.path.join(pathlib.Path(__file__).parent.resolve(), "FINAL_MODEL.pth")
    return compute(
        img_paths=img_paths, model_ckpt=model_ckpt, model_name=MODEL_NAME
    )
