import numpy as np
import os
from glob import glob
from PIL import Image
import torch
from torch.utils import data
import cv2

class word2vec1(data.dataset.Dataset):
  def __init__(self, classes_file, transform):
    predicate_binary_mat = np.load('vec_array.npy')
    self.predicate_binary_mat = predicate_binary_mat
    self.transform = transform
    class_to_index = dict()
    with open('Data/classes.txt') as f:
      index = 0
      for line in f:
        class_name = line.split('\t')[1].strip()
        class_to_index[class_name] = index
        index += 1
    self.class_to_index = class_to_index

    img_names = []
    img_index = []
    with open('Data/{}'.format(classes_file)) as f:
      for line in f:
        class_name = line.strip().split('\t')[1] 
        FOLDER_DIR = os.path.join('Data/JPEGImages', class_name)
        file_descriptor = os.path.join(FOLDER_DIR, '*.jpg')
        files = glob(file_descriptor)

        class_index = class_to_index[class_name]
        count = 0
        for file_name in files:
            img_names.append(file_name)
            img_index.append(class_index)
            count += 1
    self.img_names = img_names
    self.img_index = img_index

  def __getitem__(self, index):
    im = Image.open(self.img_names[index])
    if im.getbands()[0] == 'L':
      im = im.convert('RGB')
    if self.transform:
      im = self.transform(im)
    if im.shape != (3,224,224):
      print(self.img_names[index])

    im_index = self.img_index[index]
    im_predicate = self.predicate_binary_mat[im_index,:]
    return im, im_predicate, self.img_names[index], im_index

  def __len__(self):
    return len(self.img_names)

if __name__ == '__main__':
    dataset = word2vec1('testclasses.txt')