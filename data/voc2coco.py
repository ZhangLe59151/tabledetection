# Transfer data from voc format to COCO format
# Zhang Le 
# Aug 2020

#coding=utf-8
import xml.dom.minidom
from enum import Enum
import datetime
import cv2

class nodeType(Enum):
  ATTRIBUTE_NODE = 'ATTRIBUTE_NODE'

DATA_VERSION = "1.0"
DATA_PATH = "data/testData/"

# function to get param for bbox
def getBbox(filename):
  # open the xml document
  cfilename = "";
  dom = xml.dom.minidom.parse(DATA_PATH + 'cTDaR_t00000.xml')

  # get the element
  root = dom.documentElement
  if root.hasAttribute("filename"):
    cfilename = root.getAttribute("filename")

  table = root.getElementsByTagName("table")[0]
  Coord = table.getElementsByTagName("Coords")[0].getAttribute("points")

  # get x, y, width, height
  x = int(Coord.split(' ')[3].split(',')[0])
  y = int(Coord.split(' ')[3].split(',')[1])
  width = int(Coord.split(' ')[1].split(',')[0]) - x
  height = y -  int(Coord.split(' ')[1].split(',')[1])

  data = {}
  data["x"] = x
  data["y"] = y
  data["width"] = width
  data["height"] = height
  return data

def createCocoItem(filename, bbox):
  # generate info 
  info = {}
  info["year"] = 2020
  info["version"] = DATA_VERSION
  info["description"] = "description"
  info["contributor"] = "contributor"
  info["url"] = ""
  info["date_created"] = datetime.date.today()

  # generate image
  image = {}
  image["id"] = 1
  image["width"] = getImgSize('cTDaR_t00000.jpg')["width"]
  image["height"] = getImgSize('cTDaR_t00000.jpg')["height"]
  image["filename"] = filename
  image["license"] = 1
  image["flickr_url"] = ""
  image["coco_url"] = ""
  image["date_captured"] = datetime.date.today()

  # generate license
  licensee = {}
  licensee["id"] = 1
  licensee["name"] = filename
  licensee["url"] = ""

  # generate annotation
  annotation = {}
  annotation["id"] = 1
  annotation["image_id"] = 1
  annotation["category_id"] = 0
  annotation["area"] = 1
  annotation["bbox"] = [bbox["x"], bbox["y"], bbox["width"], bbox["height"]]
  annotation["iscrowd"] = 0

  return(info, image, annotation, licensee)

def getImgSize(filename):
  img = cv2.imread(DATA_PATH + filename)
  (width, height, depth) = img.shape
  data = {}
  data["width"] = width
  data["height"] = height
  return data

data = {}
infos = []
images = []
annotations = []
licenses = []
(info, image, annotation, licensee) = createCocoItem('',getBbox(''))
infos.append(info)
images.append(image)
annotations.append(annotation)
licenses.append(licensee)
data["info"]: infos
data["images"] = images
data["annotations"] = annotations
data["licenses"] = licenses

print(data)
