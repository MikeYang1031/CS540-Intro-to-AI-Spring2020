""" author: Zonglin Yang
    source: cs540 P5 2020 Spring
    email: zyang439@wisc.edu
    credit help to: Suyan Qu
"""

import numpy as np
from scipy.io import loadmat
from scipy.linalg import eigh
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    dataset = loadmat(filename)
    x = dataset['fea'].astype(np.float32)
    x = x - np.mean(x, axis=0)
    return x


def get_covariance(dataset):
    n = len(dataset)
    x = dataset
    S = np.dot(np.transpose(x), x)
    S = S / (n - 1)
    return S


def get_eig(S, m):
    value, vector = eigh(S)
    index = np.argsort(value)
    value = value[index[-m:]]
    vector = vector[:, index[-m:]]
    value = np.diag(value)
    return value, vector


def project_image(image, U):
    x = image
    temp = np.zeros_like(U)

    for i in range(U.shape[1]):
        u = U[:, i]
        a = np.dot(np.transpose(u), x)
        temp[:, i] = a * u
    projected = np.sum(temp, axis=1)
    return projected


def display_image(orig, proj):
    orig = np.rot90(np.reshape(orig, (32, 32)), axes=(1, 0))
    proj = np.rot90(np.reshape(proj, (32, 32)), axes=(1, 0))

    fig, (ax1, ax2) = plt.subplots(1, 2)

    im1 = ax1.imshow(orig, aspect='equal')
    fig.colorbar(im1, ax=ax1)
    ax1.set_title("Original")

    im2 = ax2.imshow(proj, aspect='equal')
    fig.colorbar(im2, ax=ax2)
    ax2.set_title("Projection")

    plt.show()


# # for test
# if __name__ == '__main__':
#     dataset = load_and_center_dataset('./YaleB_32x32.mat')
#     S = get_covariance(dataset)
#     _, U = get_eig(S, 2)
#     projection = project_image(dataset[399], U)
#     display_image(dataset[399], projection)
