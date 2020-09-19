import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.applications.mobilenet import MobileNet

from generator_v2 import Custom_ImageGenerator

def get_model(input_shape, num_output_class):

    base_model = MobileNet(weights='imagenet', include_top=False,
                        input_shape=input_shape)
    x = base_model.output
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(64, activation='relu')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dense(128, activation='relu')(x)
    x = keras.layers.BatchNormalization()(x)
    output_layer = keras.layers.Dense(num_output_class, activation='softmax')(x)
    model = keras.models.Model(inputs=base_model.inputs, outputs=output_layer)

    for layer in base_model.layers:
        layer.trainable = False

    model.compile(keras.optimizers.Adam(0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

    return model

if __name__ == "__main__":

    label_encode = {"cats" : 0, "dogs" : 1}
    batch_size = 8
    image_size = (224, 224)
    input_shape=(224, 224, 3)
    num_output_class = len(label_encode)

    # Get All data
    with open("train_set.txt", "r") as f:
        data = f.readlines()
    np.random.shuffle(data)
    
    img_path_list, label_list = [], []
    for d in data:
        img_path, label = d.strip().split('\t')
        img_path_list.append(img_path)
        label_list.append(label)

    train_gen = Custom_ImageGenerator(img_path_list, label_list, label_encode, batch_size=batch_size, 
                                        image_size=image_size)

    with open("test_set.txt", "r") as f:
        data = f.readlines()
    np.random.shuffle(data)
    
    img_path_list, label_list = [], []
    for d in data:
        img_path, label = d.strip().split('\t')
        img_path_list.append(img_path)
        label_list.append(label)

    test_gen = Custom_ImageGenerator(img_path_list, label_list, label_encode, batch_size=batch_size, 
                                        image_size=image_size)
    
    for id, (img, label) in enumerate(train_gen):
        print(img.shape, "===", label.shape)
        break

    for id, (img, label) in enumerate(test_gen):
        print(img.shape, "===", label.shape)
        break

    # Define model
    model = get_model(input_shape, num_output_class)

    # Train
    model.fit_generator( 
            train_gen,
            steps_per_epoch=len(train_gen),
            epochs=10,
            verbose=1,
            validation_data=test_gen,
            validation_steps=len(test_gen),
            shuffle=True
        )