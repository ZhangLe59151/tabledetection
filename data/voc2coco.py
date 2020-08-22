# Transfer data from voc format to COCO format
# Zhang Le 
# Aug 2020

#coding=utf-8
import xml.dom.minidom
from enum import Enum
import datetime
import cv2, os, re

class nodeType(Enum):
  ATTRIBUTE_NODE = 'ATTRIBUTE_NODE'

class DEBUG_LEVEL(Enum):
  RUNTIME = 'RUNTIME',
  DEBUG = 'DEBUG',
  LOG = 'LOG'

DATA_VERSION = "1.0"
DATA_PATH = "data/testData/"
DEBUG_STATUS = DEBUG_LEVEL.DEBUG.value

# function to get param for bbox
def getBbox(filename):
  # open the xml document
  cfilename = "";
  dom = xml.dom.minidom.parse(DATA_PATH + filename)

  # get the element
  root = dom.documentElement
  if root.hasAttribute("filename"):
    cfilename = root.getAttribute("filename")

  table = root.getElementsByTagName("table")[0]
  Coord = table.getElementsByTagName("Coords")[0].getAttribute("points")

  # get x, y, width, height
  '''
  x = int(Coord.split(' ')[3].split(',')[0])  # to do - check the max of width and height
  y = int(Coord.split(' ')[3].split(',')[1])
  width = int(Coord.split(' ')[1].split(',')[0]) - x 
  height = y - int(Coord.split(' ')[1].split(',')[1])
  '''

  x = min([int(Coord.split(' ')[0].split(',')[0]), int(Coord.split(' ')[1].split(',')[0]), int(Coord.split(' ')[2].split(',')[0]), int(Coord.split(' ')[3].split(',')[0])])
  y = max([int(Coord.split(' ')[0].split(',')[1]), int(Coord.split(' ')[1].split(',')[1]), int(Coord.split(' ')[2].split(',')[1]), int(Coord.split(' ')[3].split(',')[1])])
  width = max([int(Coord.split(' ')[0].split(',')[0]), int(Coord.split(' ')[1].split(',')[0]), int(Coord.split(' ')[2].split(',')[0]), int(Coord.split(' ')[3].split(',')[0])]) - x
  height = y - int(Coord.split(' ')[1].split(',')[1])

  data = {}
  data["x"] = x
  data["y"] = y
  data["width"] = width
  data["height"] = height
  return data

def createCocoItem(imgfilename):
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
  imgsize = getImgSize(imgfilename)
  image["id"] = 1
  image["width"] = imgsize["width"]   # to-do optimize 
  image["height"] = imgsize["height"]
  image["filename"] = imgfilename
  image["license"] = 1
  image["flickr_url"] = ""
  image["coco_url"] = ""
  image["date_captured"] = datetime.date.today()

  # generate license
  licensee = {}
  licensee["id"] = 1
  licensee["name"] = imgfilename
  licensee["url"] = ""

  # generate annotation
  annotationFilename = imgfilename.replace('.jpg', '.xml')
  bbox = getBbox(annotationFilename)
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
  (height, width, depth) = img.shape
  data = {}
  data["width"] = width
  data["height"] = height
  return data

def generateCoCoDataset():
  data = {}
  infos = []
  images = []
  annotations = []
  licenses = []
  files= os.listdir(DATA_PATH)
  for file in files:
    imgfile = re.match(".*.jpg$", file.lower())
    if (imgfile):
      (info, image, annotation, licensee) = createCocoItem(file)
      infos.append(info)
      images.append(image)
      annotations.append(annotation)
      licenses.append(licensee)
      if (DEBUG_STATUS == DEBUG_LEVEL.LOG.value):
        print(file + 'has been added into annotation json file...')
      if  (DEBUG_STATUS == DEBUG_LEVEL.DEBUG.value):
        temp = {}
        temp["info"] = infos
        temp["images"] = images
        temp["annotations"] = annotations
        temp["licenses"] = licenses
        print(file + ':')
        print(temp)
  # (info, image, annotation, licensee) = createCocoItem('')
  # infos.append(info)
  # images.append(image)
  # annotations.append(annotation)
  # licenses.append(licensee)
  data["info"] = infos
  data["images"] = images
  data["annotations"] = annotations
  data["licenses"] = licenses
  return data

generateCoCoDataset()
