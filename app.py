import torch
from zoedepth.utils.misc import get_image_from_url, colorize
from PIL import Image
from torchvision.transforms import ToTensor
from flask import Flask, request, Response
import base64
from io import BytesIO

import os
import matplotlib.pyplot as plt


app = Flask(__name__, static_url_path='', static_folder='templates')

zoe = torch.hub.load(".", "ZoeD_K", source="local", pretrained=True)


@app.route("/depth", methods=['POST'])
def depth():
    base64_string = request.json.get('img')
    name = request.json.get('name')

    image_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(image_data))
    orig_size = img.size
    X = ToTensor()(img)
    X = X.unsqueeze(0).to('cpu')

    print("X.shape", X.shape)
    print("predicting")

    out = zoe.infer_pil(img)

    print("output.shape", out.shape)
    pred = Image.fromarray(colorize(out))
    # Stack img and pred side by side for comparison and save
    pred = pred.resize(orig_size, Image.ANTIALIAS)
    stacked = Image.new("RGB", (orig_size[0], orig_size[1]))
    stacked.paste(pred, (0, 0))

    path = f"./output/{name}.png"
    stacked.save(path)
    return path


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8124)
