from cv2 import cv2
import numpy as np
import abc

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras

class DataLoader(keras.utils.Sequence):

    __metaclass__ = abc.ABCMeta

    def __init__(self, filenames, labels, char_list, batch_size, training, image_size=(32, 128)):
        self.filenames = filenames
        self.labels = labels
        self.char_list = char_list
        self.batch_size = batch_size
        self.training = training
        self.w = image_size[0]
        self.h = image_size[1]
        self.max_label_len = 0

    def __len__(self):
        return (np.ceil(len(self.filenames) / self.batch_size)).astype(np.int)

    def __getitem__(self, idx):
        data_batch = self.filenames[idx * self.batch_size: (idx + 1) * self.batch_size]
        label_batch = self.labels[idx * self.batch_size: (idx + 1) * self.batch_size]

        X, y = self._generate_data(data_batch, label_batch)

        return X, y

    def _preprocess_image(self, img, w, h):
        if w < self.w:
            add_zeros = np.ones((self.w - w, h)) * 255.0
            img = np.concatenate((img, add_zeros))

        if h < self.h:
            add_zeros = np.ones((self.w, self.h - h)) * 255.0
            img = np.concatenate((img, add_zeros), axis=1)

        img = np.expand_dims(img, axis=2)

        # Normalize Images
        img = img / 255.0

        return img

    def encode_to_labels(self, txt, char_list):
        # encoding each output word into digits
        dig_lst = []
        for _, char in enumerate(txt):
            try:
                dig_lst.append(char_list.index(char))
            except:
                print(char)

        return dig_lst
    
    @abc.abstractmethod
    def _generate_data(self, data_batch, label_batch):
        # Method to generate batches of data
        pass


class TrainGenerator(DataLoader):

    def _generate_data(self, data_batch, label_batch):
        batch_imgs, batch_labels, input_len, label_len = [], [], [], []
        for img_path, label in zip(data_batch, label_batch):
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            # Preprocess image
            w, h = img.shape
            if h > self.h or w > self.w:
                continue

            img = self._preprocess_image(img, w, h)

            # compute maximum length of the text
            label = label.strip()
            if len(label) > self.max_label_len:
                self.max_label_len = len(label)

            label = self.encode_to_labels(label, self.char_list)

            batch_imgs.append(img)
            batch_labels.append(label)
            input_len.append(self.w - 1)
            label_len.append(len(label))

        batch_labels = pad_sequences(batch_labels, maxlen=self.max_label_len, padding='post', value=len(self.char_list))

        batch_imgs = np.array(batch_imgs).astype('float32')
        batch_labels = np.array(batch_labels).astype('float32')
        inputs_len = np.array(input_len).astype('float32')
        labels_len = np.array(label_len).astype('float32')

        return [batch_imgs, batch_labels, inputs_len, labels_len], batch_labels


class ValidationGenerator(DataLoader):

    def _generate_data(self, data_batch, label_batch):
        batch_imgs, batch_labels, input_len, label_len = [], [], [], []
        for img_path, label in zip(data_batch, label_batch):
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            # Preprocess image
            w, h = img.shape
            if h > self.h or w > self.w:
                continue

            img = self._preprocess_image(img, w, h)

            # compute maximum length of the text
            label = label.strip()
            if len(label) > self.max_label_len:
                self.max_label_len = len(label)

            label = self.encode_to_labels(label, self.char_list)

            batch_imgs.append(img)
            batch_labels.append(label)
            input_len.append(self.w - 1)
            label_len.append(len(label))

        batch_labels = pad_sequences(batch_labels, maxlen=self.max_label_len, padding='post', value=len(self.char_list))

        batch_imgs = np.array(batch_imgs).astype('float32')
        batch_labels = np.array(batch_labels).astype('float32')
        inputs_len = np.array(input_len).astype('float32')
        labels_len = np.array(label_len).astype('float32')

        return [batch_imgs, batch_labels, inputs_len, labels_len], [np.zeros(len(batch_imgs))]