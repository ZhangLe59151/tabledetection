# Varify Transfer data from voc format to COCO format
# Zhang Le 
# Aug 2020

import json
import cv2
import numpy as np
import matplotlib.pyplot as plt


FILE_PATH = "data/"
DATA_PATH = "data/testData/"
FILENAME = "coco.json"

def plt_img_boxes(src_img, obj_boxes, font_width=None, plot_seq_number=False, names=None):
  boxes = np.array(obj_boxes).reshape(-1, 4)
  img = src_img.copy()
  try:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  except:
    pass
  size = max(img.shape[:2])
  font_width = max(1, size // 70) if font_width is None else font_width
  colors = [0, 255]
  for idx, box in enumerate(boxes):
    box = box.astype(int)
    cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (colors[idx % len(colors)], colors[(idx+1) % len(colors)], 0), font_width)
    if plot_seq_number:
      cv2.putText(img, str(idx), (box[2], box[3]), cv2.FONT_HERSHEY_SIMPLEX, font_width * 0.3, (255, 0, 0), font_width)
    if names:
      cv2.putText(img, str(names[idx]), (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, font_width * 0.3, (255, 0, 0), font_width)
  plt.figure(figsize = (15, 15))
  plt.imshow(img, aspect='equal')
  plt.show()
        
def plt_img_pts(src_img, pts, groundtruth=None, font_width=None, plot_seq_number=True, names=None):
  pts = np.array(pts).reshape(-1, 2)
  img = src_img.copy()
  try:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  except:
    pass
  size = max(img.shape[:2])
  font_width = max(1, size // 70) if font_width is None else font_width
  for idx in range(pts.shape[0]):
    p = pts[idx]
    p = p.astype(int)
    cv2.circle(img, tuple(p), 3, (0, 255, 0), 10)
    if groundtruth is not None:
      anno_p = groundtruth[idx]
      anno_p = anno_p.astype(int)
      cv2.circle(img, tuple(anno_p), 3, (255, 255, 0), 10)
    if plot_seq_number:
      cv2.putText(img, str(idx), tuple(p), cv2.FONT_HERSHEY_SIMPLEX, font_width * 0.3, (255, 0, 0), 8)
#             if groundtruth is not None:
#                 cv2.putText(img, str(idx), tuple(anno_p), cv2.FONT_HERSHEY_SIMPLEX, font_width * 0.3, (255, 0, 0), 3)
    if names:
      cv2.putText(img, str(names[idx]), tuple(p), cv2.FONT_HERSHEY_SIMPLEX, font_width * 0.3, (255, 0, 0), 10)
  plt.figure(figsize = (15, 15))
  plt.imshow(img, aspect='equal')
  plt.show()
    


with open(FILE_PATH+FILENAME) as f:
  data = f.read()
  j = json.loads(data)
  for index, item in enumerate(j["images"][:10]):
    print(item["id"])
    bboxs = []
    for b in j["annotations"]:
      if (b["image_id"] == item["id"]):
        bbox = (b["bbox"][0], b["bbox"][1], b["bbox"][0] + b["bbox"][2], b["bbox"][1] + b["bbox"][3])
        bboxs.append(bbox)
    print(bboxs)
    img = cv2.imread(DATA_PATH + item["filename"])
    plt_img_boxes(img, bboxs, font_width=None, plot_seq_number=False, names=None)
