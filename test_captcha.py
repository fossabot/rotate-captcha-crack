import argparse

import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision.transforms import functional as F

from rotate_captcha_crack.common import device
from rotate_captcha_crack.dataset import strip_circle_border
from rotate_captcha_crack.dataset.helper import DEFAULT_NORM
from rotate_captcha_crack.model import RotNet, WhereIsMyModel

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", "-i", type=int, default=-1, help="Use which index")
    opts = parser.parse_args()

    with torch.no_grad():
        model = RotNet(train=False)
        model_path = WhereIsMyModel(model).with_index(opts.index).model_dir / "best.pth"
        print(f"Use model: {model_path}")
        model.load_state_dict(torch.load(str(model_path)))
        model = model.to(device=device)
        model.eval()

        img = Image.open("datasets/tieba/1615096444.jpg")
        img = img.convert('RGB')
        img_ts = F.to_tensor(img)
        img_ts = strip_circle_border(img_ts)
        img_ts = DEFAULT_NORM(img_ts)
        img_ts = img_ts.to(device=device)

        predict = model.predict(img_ts)
        degree = predict * 360
        print(f"Predict degree: {degree:.4f}°")

    img = img.rotate(
        -degree, resample=Image.Resampling.BILINEAR, fillcolor=(255, 255, 255)
    )  # use neg degree to recover the img
    plt.figure("debug")
    plt.imshow(img)
    plt.show()
