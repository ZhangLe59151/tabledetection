# Transfer data from voc format to COCO format
# Zhang Le 
# Aug 2020

import sys
from configparser import ConfigParser
from data import voc2coco

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
voc2coco.generateCoCoDataset()