import os
from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def get_generator(data_path, batch_size, image_size, label_type, training=True):

    if training:
        datagen = ImageDataGenerator(
            width_shift_range=0.1, height_shift_range=0.1,
            shear_range=0.2, zoom_range=0.2, horizontal_flip=True,
            rescale=1. / 255.0
        )
        shuffle=True
    else:
        datagen = ImageDataGenerator(
            rescale=1. / 255.0
        )
        shuffle=False

    data_flow = datagen.flow_from_directory(
        directory=data_path, batch_size=batch_size,
        target_size=image_size, class_mode=label_type,
        shuffle=shuffle
    )

    return data_flow


if __name__ == "__main__":

    work_dir = Path(".").parent.absolute()
    
    data_path = os.path.join(work_dir, "data/training_set")
    training_data = get_generator(data_path, batch_size=64, image_size=(224, 224), 
                                    label_type='categorical')

    data_path = os.path.join(work_dir, "data/test_set")
    test_data = get_generator(data_path, batch_size=32, image_size=(224, 224), 
                                    label_type='categorical', training=False)

    for idx, (img, label) in enumerate(test_data):
        print(img)
