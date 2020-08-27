# Transfer data from voc format to COCO format
# Zhang Le 
# Aug 2020

#coding=utf-8
import xml.dom.minidom
from enum import Enum
import time
import cv2, os, re, json

class nodeType(Enum):
  ATTRIBUTE_NODE = 'ATTRIBUTE_NODE'

class DEBUG_LEVEL(Enum):
  RUNTIME = 'RUNTIME',
  DEBUG = 'DEBUG',
  LOG = 'LOG'

DATA_VERSION = "1.0"
# DATA_PATH = "data/testData/"
# DATA_PATH = "/home/hungnguyen/ZhangLe/data/ICDAR2019_cTDaR/training/TRACKA/ground_truth/"
DATA_PATH = "/home/hungnguyen/ZhangLe/data/ICDAR2019_cTDaR/verify/"
# FILE_PATH = "data/"
FILE_PATH = "/home/hungnguyen/ZhangLe/tabledetection/data/"
COCODatasetFileName = 'coco_v.json'
DEBUG_STATUS = DEBUG_LEVEL.LOG.value
AID = 0
annotations = []

# function to get param for bbox
def getBbox(filename):
  # open the xml document
  if  (DEBUG_STATUS == DEBUG_LEVEL.DEBUG.value):
    print("find name of getBbox: " + filename)
  cfilename = "";
  dom = xml.dom.minidom.parse(DATA_PATH + filename)

  # get the element
  root = dom.documentElement
  if root.hasAttribute("filename"):
    cfilename = root.getAttribute("filename")

  tables = root.getElementsByTagName("table")
  dataList = []
  for table in tables:
    Coord = table.getElementsByTagName("Coords")[0].getAttribute("points")
    # get x, y, width, height
    x = min([int(Coord.split(' ')[0].split(',')[0]), int(Coord.split(' ')[1].split(',')[0]), int(Coord.split(' ')[2].split(',')[0]), int(Coord.split(' ')[3].split(',')[0])])
    y = min([int(Coord.split(' ')[0].split(',')[1]), int(Coord.split(' ')[1].split(',')[1]), int(Coord.split(' ')[2].split(',')[1]), int(Coord.split(' ')[3].split(',')[1])])
    width = max([int(Coord.split(' ')[0].split(',')[0]), int(Coord.split(' ')[1].split(',')[0]), int(Coord.split(' ')[2].split(',')[0]), int(Coord.split(' ')[3].split(',')[0])]) - x
    height = max([int(Coord.split(' ')[0].split(',')[1]), int(Coord.split(' ')[1].split(',')[1]), int(Coord.split(' ')[2].split(',')[1]), int(Coord.split(' ')[3].split(',')[1])]) - y
    data = {}
    data["x"] = x
    data["y"] = y
    data["width"] = width
    data["height"] = height
    dataList.append(data)
  return dataList

def createCocoItem(imgfilename, id):
  global AID
  # generate image
  image = {}
  imgsize = getImgSize(imgfilename)
  image["id"] = id
  image["width"] = imgsize["width"]   # to-do optimize 
  image["height"] = imgsize["height"]
  image["file_name"] = imgfilename
  image["license"] = 1
  image["flickr_url"] = ""
  image["coco_url"] = ""
  image["date_captured"] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

  # generate annotation
  annotationFilename = imgfilename.split('.')[0]+".xml"
  bboxList = getBbox(annotationFilename)
  for (index, bbox) in enumerate(bboxList):
    annotation = {}
    annotation["id"] = AID
    AID = AID + 1
    annotation["image_id"] = id
    annotation["category_id"] = 0
    annotation["area"] = 1
    annotation["bbox"] = [bbox["x"], bbox["y"], bbox["width"], bbox["height"]]
    annotation["iscrowd"] = 0
    annotations.append(annotation)
  return(image)

def getImgSize(filename):
  img = cv2.imread(DATA_PATH + filename)
  (height, width, depth) = img.shape
  data = {}
  data["width"] = width
  data["height"] = height
  return data

def generateCoCoDataset():
  data = {}
  # generate info 
  info = {}
  info["year"] = 2020
  info["version"] = DATA_VERSION
  info["description"] = "description"
  info["contributor"] = "contributor"
  info["url"] = ""
  info["date_created"] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

  # generate category
  categories = []
  category = {}
  category["id"] = 0
  category["name"] = "table"
  category["supercategory"] = "table"
  categories.append(category)

  images = []

  files= os.listdir(DATA_PATH)
  count = 0;
  for (index,file) in enumerate(files):
    imgfile = re.match(".*.xml$", file.lower())
    if (imgfile == None):
      (image) = createCocoItem(file, index)
      images.append(image)
      if (DEBUG_STATUS == DEBUG_LEVEL.LOG.value):
        print(str(count) + ' ' + file + ' has been added into annotation json file...')
        count = count + 1;
      if  (DEBUG_STATUS == DEBUG_LEVEL.DEBUG.value):
        temp = {}
        temp["images"] = images
        print(file + ':')
        print(temp)
  # (info, image, annotation, licensee) = createCocoItem('')
  # infos.append(info)
  # images.append(image)
  # annotations.append(annotation)
  # licenses.append(licensee)
  data["info"] = info
  data["images"] = images
  data["annotations"] = annotations
  data["categories"] = categories
  writeToFile(data)

def writeToFile(data):
  with open(FILE_PATH + COCODatasetFileName, 'w') as f:
    json.dump(data, f)
    if (DEBUG_STATUS == DEBUG_LEVEL.LOG.value):
      print('data has been written into file : ' + FILE_PATH + COCODatasetFileName)

# main function 
generateCoCoDataset()
