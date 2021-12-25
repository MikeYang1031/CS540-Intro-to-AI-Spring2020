"""
    File name: keras_cnn.py
    Author: Zonglin Yang
    Project: P10
    course: cs540 Spring2020
    credit: Piazza
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras


def get_dataset(training=True):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = np.expand_dims(train_images, axis=3)
    test_images = np.expand_dims(test_images, axis=3)

    if training:
        return train_images, train_labels
    else:
        return test_images, test_labels


def build_model():
    model = tf.keras.Sequential()
    model.add(keras.layers.Conv2D(64, 3, activation='relu', input_shape=(28, 28, 1)))
    model.add(keras.layers.Conv2D(32, 3, activation='relu'))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def train_model(model, train_img, train_lab, test_img, test_lab, T):
    train_lab = keras.utils.to_categorical(train_lab)
    test_lab = keras.utils.to_categorical(test_lab)
    model.fit(train_img, train_lab, validation_data=(test_img, test_lab), epochs=T)


def predict_label(model, images, index):
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    predictions = model.predict(images)
    # get predicted labels for image at given index
    predicted_labels = [(predictions[index][i], class_names[i]) for i in range(len(predictions[index]))]
    # sort by highest probability
    predicted_labels.sort(reverse=True, key=lambda tup: tup[0])

    for i in range(3):
        print('{}: {:.2f}%'.format(predicted_labels[i][1], predicted_labels[i][0] * 100))


# tests
# (train_images, train_labels) = get_dataset()
# (test_images, test_labels) = get_dataset(False)
# print(train_images.shape)
# print(test_images.shape)
# model = build_model()
# keras.utils.plot_model(model, to_file='model.png')
# train_model(model, train_images, train_labels, test_images, test_labels, 5)
# predict_label(model, test_images, 6)