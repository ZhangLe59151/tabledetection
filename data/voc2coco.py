# Transfer data from voc format to COCO format
# Zhang Le 
# Aug 2020

#coding=utf-8
import xml.dom.minidom
from enum import Enum
import time, configparser
import cv2, os, re, json, sys
from configparser import ConfigParser

class nodeType(Enum):
  ATTRIBUTE_NODE = 'ATTRIBUTE_NODE'

class DEBUG_LEVEL(Enum):
  RUNTIME = 'RUNTIME',
  DEBUG = 'DEBUG',
  LOG = 'LOG'

def getParameter(p1, p2):
  config = configparser.ConfigParser()
  config.read('config.ini')
  # data_path = "data/testData/"
  # data_path = "/home/hungnguyen/ZhangLe/data/ICDAR2019_cTDaR/training/TRACKA/ground_truth/"
  # data_path = "/home/hungnguyen/ZhangLe/data/ICDAR2019_cTDaR/verify/"
  Parameter = config.get(p1, p2)
  # FILE_PATH = "data/"
  # FILE_PATH = "/home/hungnguyen/ZhangLe/tabledetection/data/"
  # FILE_PATH = config.get('path', 'FILE_PATH')
  # COCODatasetFileName = 'coco.json' 
  # COCODatasetFileName = 'coco_v.json' 
  COCODatasetFileName = config.get('path', 'COCODatasetFileName')
  # DEBUG_STATUS = DEBUG_LEVEL.LOG.value
  DEBUG_STATUS = config.get('debug', 'DEBUG_LEVEL')
  return Parameter

AID = 0
annotations = []

# function to get param for bbox
def getBbox(filename):
  # open the xml document
  if  (getParameter('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.DEBUG.value):
    print("find name of getBbox: " + filename)
  cfilename = "";
  dom = xml.dom.minidom.parse(getParameter('path', 'data_path') + filename)

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
  img = cv2.imread(getParameter('path', 'data_path') + filename)
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
  info["version"] = getParameter('version', 'DATA_VERSION')
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

  files= os.listdir(getParameter('path', 'data_path'))
  count = 0;
  for (index,file) in enumerate(files):
    imgfile = re.match(".*.xml$", file.lower())
    if (imgfile == None):
      (image) = createCocoItem(file, index)
      images.append(image)
      if (getParameter('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.LOG.value):
        print(str(count) + ' ' + file + ' has been added into annotation json file...')
        count = count + 1;
      if  (getParameter('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.DEBUG.value):
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
  with open(getParameter('path', 'FILE_PATH') + getParameter('path', 'COCODatasetFileName'), 'w') as f:
    json.dump(data, f)
    if (getParameter('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.LOG.value):
      print('data has been written into file : ' + getParameter('path', 'FILE_PATH') + getParameter('path', 'COCODatasetFileName'))

# main function 
# write the config file
data_path = input("input data path for image data and annotation:\n")
file_path = input("input coco file path:\n")
file_name = input("input coco file name: for example : coco.json:\n")
cfg = ConfigParser()
cfg.read('config.ini')
cfg.set('path', 'data_path', data_path)
cfg.set('path', 'file_path', file_path)
cfg.set('path', 'COCODatasetFileName', file_name)
cfg.write(sys.stdout)
a = cfg.get('path', 'data_path')
print(a)

generateCoCoDataset()
