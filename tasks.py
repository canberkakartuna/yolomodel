import torch
from PIL import Image
import io
import os

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # for PIL/cv2/np inputs and NMS
model.eval()


def prediction(img_bytes, filename):
    print('started...')
    img = Image.open(io.BytesIO(img_bytes))
    imgs = [img]  # batched list of images
    results = model(imgs, size=640)  # includes NMS
    results.save('./static/')
    os.rename('./static/image0.jpg', f'./static/{filename}.jpg')
    res_rows = []
    for rows in results.pandas().xyxy[0][['name', 'confidence']].itertuples():
        # Create list for the current row
        res_rows.append([rows.name, rows.confidence])
    return list(results.pandas().xyxy[0][['name', 'confidence']].columns), res_rows

