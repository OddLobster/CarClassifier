import cv2
import tensorflow as tf
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import numpy as np
import cv2
import os
import PIL

from sklearn.model_selection import train_test_split



label_lookup = []
def createModel():
    global label_lookup
    num_labels = len(label_lookup)
    model = tf.keras.models.Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(300, 300, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    # model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_labels, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def getData():
    global label_lookup
    folder = "data"
    imgs = os.listdir(folder)
    num_imgs = len(imgs)
    print("Number of images:", num_imgs)
    data_y = []
    data_x = []
    for i, name in enumerate(imgs):
        if i >= num_imgs:
            break
        if "error" in name:
            continue
        pil_image = PIL.Image.open(folder + "/" + name).convert('RGB') 
        img = np.asarray(pil_image)[:, :, ::-1].copy() 
        data_x.append(img)
        data_y.append(name.split("_")[0])
        # cv2.imshow(f"{name} Image", img)
        # cv2.waitKey(0)
    data_x = np.array(data_x)
    label_lookup = []
    for y in data_y:
        if y not in label_lookup:
            label_lookup.append(y)
    data_y = [label_lookup.index(y) for y in data_y]
    data_y = tf.keras.utils.to_categorical(np.array(data_y))
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2, random_state=42)
    return x_train, x_test, y_train, y_test 

def main():
    x_train, x_test, y_train, y_test  = getData()

    model = createModel()
    model.fit(x_train, y_train, epochs=100)
    model.evaluate(x_test, y_test)


if __name__ == "__main__":
    main()