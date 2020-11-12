import torch
from torchvision import transforms, datasets
from PIL import Image
from io import BytesIO

def image_to_bytes(image:Image):
  imgByteArr = BytesIO()
  image.save(imgByteArr,format='jpeg')
  return imgByteArr.getvalue()

ops = [ BytesIO,
        Image.open,
        transforms.Scale(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        transforms.ToPILImage(),
        image_to_bytes
        ]
