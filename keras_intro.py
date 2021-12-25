"""
    File name: keras_intro.py
    Author: Zonglin Yang
    Project: P9
    course: cs540 Spring2020
    credit: Piazza
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Activation, Softmax
from tensorflow.keras.losses import SparseCategoricalCrossentropy
import matplotlib.pyplot as plt

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


# Takes an optional boolean argument and returns the data as described in the specifications.
def get_dataset(training=True):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    if training:
        return train_images, train_labels
    else:
        return test_images, test_labels


# Takes the dataset and labels produced by the previous function and prints several statistics about the data; does
# not return anything.
def print_stats(images, labels):
    class_num = [0] * 10

    print(len(images))
    # get canvas size
    print('{}x{}'.format(len(images[0]), len(images[0][0])))
    # get number of images corresponding to the class labels
    for x in labels:
        class_num[x] += 1

    for i in range(len(class_names)):
        print('{}. {} - {}'.format(i, class_names[i], class_num[i]))


# Takes a single image as an array of pixels and displays an image; does not return anything.
def view_image(image, label):
    fig, ax = plt.subplots()
    ax.set_title(label)

    # show image and color bar
    bar = ax.imshow(image, aspect='equal')
    fig.colorbar(bar, ax=ax)
    plt.show()


# Takes no arguments and returns an untrained neural network as described in the specifications.
def build_model():
    model = keras.Sequential([
        Flatten(input_shape=(28, 28)),
        Dense(128, activation=Activation('relu')),
        Dense(10)
    ])
    model.compile(
        optimizer='adam',
        loss=SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    return model


# Takes the model produced by the previous function and the images and labels produced by the first function and
# trains the data for T epochs; does not return anything.
def train_model(model, images, labels, T):
    model.fit(x=images, y=labels, epochs=T)


# Takes the trained model produced by the previous function and the test image/labels, and prints the evaluation
# statistics as described below (displaying the loss metric value if and only if the optional parameter has not been
# set to False).
def evaluate_model(model, images, labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(images, labels)

    if show_loss:
        print('Loss: {:.2f}'.format(test_loss))
    else:
        print('Accuracy: {:.2f}%'.format(test_accuracy * 100))


# Takes the trained model and test images, and prints the top 3 most likely labels for the image at the given index,
# along with their probabilities.
def predict_label(model, images, index):
    # add softmax layer before predictions
    model.add(Softmax())
    predictions = model.predict(images)

    # get predicted labels for image at given index
    predicted_labels = [(predictions[index][i], class_names[i]) for i in range(len(predictions[index]))]
    # sort by highest probability
    predicted_labels.sort(reverse=True, key=lambda tup: tup[0])

    # get rid of the softmax layer to avoid duplicate
    model.pop()

    for i in range(3):
        print('{}: {:.2f}%'.format(predicted_labels[i][1], predicted_labels[i][0] * 100))


if __name__ == '__main__':
    (train_images, train_labels) = get_dataset()
    (test_images, test_labels) = get_dataset(False)
    #
    print_stats(train_images, train_labels)
    print_stats(test_images, test_labels)
    #
    view_image(train_images[100], class_names[train_labels[100]])
    view_image(test_images[2200], class_names[test_labels[2200]])
    view_image(test_images[6324], class_names[test_labels[6324]])
    view_image(test_images[7777], class_names[test_labels[7777]])
    #
    model = build_model()
    #
    train_model(model, train_images, train_labels, 5)
    #
    evaluate_model(model, test_images, test_labels, show_loss=False)
    evaluate_model(model, test_images, test_labels)
    #
    # model.add(Softmax())
    predict_label(model, test_images, 2200)
    predict_label(model, test_images, 6324)
    predict_label(model, test_images, 7777)