# Transfer data from voc format to COCO format
# Zhang Le 
# Aug 2020

#coding=utf-8
import xml.dom.minidom
from enum import Enum
import time, configparser
import cv2, os, re, json, sys
from configparser import ConfigParser

ROOT_PATH = os.path.split(os.path.realpath(__file__))[0]

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
  if  (cfg.get('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.DEBUG.value):
    print("find name of getBbox: " + filename)
  cfilename = "";
  dom = xml.dom.minidom.parse(cfg.get('path', 'data_path') + filename)

  # get the element
  root = dom.documentElement
  if root.hasAttribute("filename"):
    cfilename = root.getAttribute("filename")

  tables = root.getElementsByTagName("table")
  dataList = []
  segmentationList = []

  def getMaxXY(itemList):
    maxX = 0
    maxY = 0
    for item in itemList:
      if int(item.split(',')[0]) > maxX:
        maxX = int(item.split(',')[0])
      if int(item.split(',')[1]) > maxY:
        maxY = int(item.split(',')[1])
    return maxX, maxY
  
  def getMinXY(itemList):
    minX = int(itemList[0].split(',')[0])
    minY = int(itemList[0].split(',')[1])
    for item in itemList:
      if int(item.split(',')[0]) < minX:
        maxX = int(item.split(',')[0])
      if int(item.split(',')[1]) < minY:
        maxY = int(item.split(',')[1])
    return minX, minY
  
  for table in tables:
    Coord = table.getElementsByTagName("Coords")[0].getAttribute("points")
    # get x, y, width, height
    xmax, ymax  = getMaxXY(Coord.split(' '))
    x, y = getMinXY(Coord.split(' '))
    width = xmax - x
    height = ymax - y
    data = {}
    data["x"] = x
    data["y"] = y
    data["width"] = width
    data["height"] = height
    dataList.append(data)
    keypoint = []
    segmentation = []
    for item in Coord.split(' '):
      kx = int(item.split(',')[0])
      keypoint.append(kx)
      segmentation.append(kx)
      ky = int(item.split(',')[1])
      keypoint.append(ky)
      segmentation.append(ky)
      v = 2
      keypoint.append(v)
    data["keypoint"] = keypoint
    data["segmentation"] = segmentation
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
    annotation["category_id"] = 1
    annotation["area"] = bbox["width"] * bbox["height"]
    annotation["bbox"] = [bbox["x"], bbox["y"], bbox["width"], bbox["height"]]
    annotation["bbox_mode"] = 2
    annotation["iscrowd"] = 0
    annotation["segmentation"] = [bbox["segmentation"]]
    annotation["num_keypoints"] = len(bbox["keypoint"]) // 3
    annotation["keypoints"] = bbox["keypoint"]
    annotations.append(annotation)
  return(image)

def getImgSize(filename):
  img = cv2.imread(cfg.get('path', 'data_path') + filename)
  print(cfg.get('path', 'data_path') + filename)
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
  info["version"] = cfg.get('version', 'DATA_VERSION')
  info["description"] = "description"
  info["contributor"] = "contributor"
  info["url"] = ""
  info["date_created"] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

  # generate category
  categories = []
  category = {}
  category["id"] = 1
  category["name"] = "table"
  category["supercategory"] = "table"
  categories.append(category)

  images = []

  files= os.listdir(cfg.get('path', 'data_path'))
  count = 0;
  for (index,file) in enumerate(files):
    imgfile = re.match(".*.xml$", file.lower())
    if (imgfile == None):
      (image) = createCocoItem(file, index)
      images.append(image)
      if (cfg.get('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.LOG.value):
        print(str(count) + ' ' + file + ' has been added into annotation json file...')
        count = count + 1;
      if  (cfg.get('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.DEBUG.value):
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
  with open(cfg.get('path', 'FILE_PATH') + cfg.get('path', 'COCODatasetFileName'), 'w') as f:
    json.dump(data, f)
    if (cfg.get('debug', 'DEBUG_LEVEL') == DEBUG_LEVEL.LOG.value):
      print('data has been written into file : ' + cfg.get('path', 'FILE_PATH') + cfg.get('path', 'COCODatasetFileName'))

# main function 
# write the config file
data_path = input("input data path for image data and annotation:\n")
file_path = input("input coco file path:\n")
file_name = input("input coco file name: for example : coco.json:\n")
cfg = ConfigParser()
configPath = os.path.join(ROOT_PATH, 'config1.ini')
cfg.read(configPath)
cfg.set('path', 'data_path', data_path)
cfg.set('path', 'file_path', file_path)
cfg.set('path', 'COCODatasetFileName', file_name)
# cfg.set('version', 'DATA_VERSION', '1.0')
cfg.write(sys.stdout)
a = cfg.get('version', 'DATA_VERSION')
print(a)

generateCoCoDataset()
