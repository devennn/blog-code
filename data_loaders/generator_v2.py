import os
import math
import numpy as np
from pathlib import Path

from cv2 import cv2
from tensorflow.keras.utils import Sequence, to_categorical


def create_files():
    work_dir = Path(".").parent.absolute()

    data_path = os.path.join(work_dir, "data/training_set")
    f = open("train_set.txt", "w+")
    
    for label in os.listdir(data_path):
        label_path = os.path.join(data_path, label)
        for fname in os.listdir(label_path):
            f_path = os.path.join("data/training_set", label, fname)
            f.write("{}\t{}\n".format(f_path, label))

    data_path = os.path.join(work_dir, "data/test_set")
    f = open("test_set.txt", "w+")
    
    for label in os.listdir(data_path):
        label_path = os.path.join(data_path, label)
        for fname in os.listdir(label_path):
            f_path = os.path.join("data/test_set", label, fname)
            f.write("{}\t{}\n".format(f_path, label))


class Custom_ImageGenerator(Sequence):
    def __init__(self, data_filenames, labels, label_encode, batch_size, image_size):
        self.data_filenames = data_filenames
        self.labels = labels
        self.label_encode = label_encode
        self.batch_size = batch_size
        self.image_size = image_size
        self.work_dir = Path(".").parent.absolute()

    def __len__(self):
        return (np.ceil(len(self.data_filenames) / self.batch_size)).astype(np.int)

    def __getitem__(self, idx):
        data_batch = self.data_filenames[idx * self.batch_size : (idx+1) * self.batch_size]
        data_labels_batch = self.labels[idx * self.batch_size : (idx+1) * self.batch_size]

        temp = []
        for img_path in data_batch:
            img = cv2.imread(os.path.join(self.work_dir, img_path))
            img = cv2.resize(img, self.image_size)
            img = img / 255.
            temp.append(img)
        
        encoded_label = [self.label_encode[label] for label in data_labels_batch]

        processed_img_batch = np.array(temp)
        encoded_label_batch = np.array(to_categorical(encoded_label))

        return processed_img_batch, encoded_label_batch


if __name__ == "__main__":

    # create_files()

    label_encode = {"cats" : 0, "dogs" : 1}

    with open("train_set.txt", "r") as f:
        data = f.readlines()
    
    img_path_list, label_list = [], []
    for d in data:
        img_path, label = d.strip().split('\t')
        img_path_list.append(img_path)
        label_list.append(label)

    train_gen = Custom_ImageGenerator(img_path_list, label_list, label_encode, batch_size=64, 
                                        image_size=(224, 224))

    with open("test_set.txt", "r") as f:
        data = f.readlines()
    
    img_path_list, label_list = [], []
    for d in data:
        img_path, label = d.strip().split('\t')
        img_path_list.append(img_path)
        label_list.append(label)

    test_gen = Custom_ImageGenerator(img_path_list, label_list, label_encode, batch_size=64, 
                                        image_size=(224, 224))

    for idx, (img, label) in enumerate(test_gen):
        print(img)