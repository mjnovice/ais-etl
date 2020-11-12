This is a sample demonstration to allow any generic user transformation to happen.

# How to provide your own set of data tranforming functions ? 

1. The file `trans.py` gives a sample of how one can add in the functions.

```
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
```

2. Post writing this, one needs to make entries in `requirements.txt` to be able to successfully run the
transforming operations.

3. Build the docker image for the transforming operations, and push it to some repository.

4. Now, one can initiate the ETL container by going through the steps https://github.com/NVIDIA/aistore/blob/master/etl/README.md

# What is novel about this ? 

- It is a POC of attempting to introduce generic 'lambda' functions like operations in place of writing the entire transformer from scratch.
- In future the attempt is to make pipelines of these operations, where each operation runs preferably in a separate container.
