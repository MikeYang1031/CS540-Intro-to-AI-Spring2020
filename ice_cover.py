""" author: Zonglin Yang
    name: P8 ice_cover
    source: cs540 P8 2020 Spring
    email: zyang439@wisc.edu
    credit help to: piazza
"""
import csv
import math
import numpy as np
import random


# takes no argument and returns the data as described below in an n_by_2 array
def get_dataset():
    with open("icetime.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        dataset = []
        for row in reader:
            dataset.append([int(row[0].split("-")[0]), int(row[1])])
        return dataset


# Takes the dataset as produced by the previous function and prints several 
# statistics about the data; does not return anything.
def print_stats(dataset):
    print(len(dataset))
    # format to 2 digits after decimal point
    print(round(np.mean(dataset, axis=0)[1], 2))
    print(round(np.std(dataset, axis=0)[1], 2))


# Calculates and returns the mean squared error on the dataset given fixed 
# betas.
def regression(beta_0, beta_1, dataset=get_dataset()):
    number = 0
    for x, y in dataset:
        number += (beta_0 + beta_1 * x - y) ** 2
    number = number / len(dataset)

    return number


# Performs a single step of gradient descent on the MSE and returns the 
# derivative values as a tuple.
def gradient_descent(beta_0, beta_1, dataset=get_dataset()):
    i = 0
    j = 0
    for x, y in dataset:
        i += beta_0 + beta_1 * x - y
    i = i * (2 / len(dataset))

    for x, y in dataset:
        j += (beta_0 + beta_1 * x - y) * x
    j = j * (2 / len(dataset))

    return i, j


# Performs T iterations of gradient descent starting at (beta_0, beta_1) = 
# (0,0) with the given parameter and prints the results; does not return 
# anything.
def iterate_gradient(T, eta, dataset=get_dataset()):
    beta_0 = 0
    beta_1 = 0

    for i in range(0, T):
        vec1, vec2 = gradient_descent(beta_0, beta_1, dataset)
        beta_0 -= eta * vec1
        beta_1 -= eta * vec2
        MSE = regression(beta_0, beta_1, dataset)

        print(i+1, round(beta_0, 2), round(beta_1, 2), round(MSE, 2))


# Using the closed-form solution, calculates and returns the values of beta_0
# and beta_1 and the corresponding MSE as a three-element tuple.
def compute_betas():
    dataset = get_dataset()
    means = np.mean(dataset, axis=0)
    x_mean = means[0]
    y_mean = means[1]
    numerator = 0
    denominator = 0
    for point in dataset:
        if point[0] - x_mean != 0:
            numerator += (point[0] - x_mean) * (point[1] - y_mean)
            denominator += math.pow((point[0] - x_mean), 2)

    beta_1 = numerator / denominator
    beta_0 = y_mean - beta_1 * x_mean
    MSE = regression(beta_0, beta_1)

    return beta_0, beta_1, MSE


# Using the closed-form solution betas, return the predicted number of ice 
# days for that year.
def predict(year):
    beta_0, beta_1, MSE = compute_betas()
    predicted = beta_0 + beta_1 * year

    return predicted


# Normalizes the data before performing gradient descent, prints results as in 
# iterate_gradient().
def iterate_normalized(T, eta):
    dataset = get_dataset()

    n_data0 = [dataset[i][0] for i in range(len(dataset))]
    n_mean = np.mean(n_data0)
    n_std = np.std(n_data0)

    normalized_dataset = [[(dataset[i][0] - n_mean) / n_std, dataset[i][1]] for i in range(len(dataset))]

    # call the iterate_gradient function to print new output
    iterate_gradient(T, eta, dataset=normalized_dataset)


# Performs stochastic gradient descent, prints results as in function
# iterate_gradient().
def sgd(T, eta):
    dataset = get_dataset()
    beta_0 = 0
    beta_1 = 0

    n_data = [dataset[i][0] for i in range(len(dataset))]
    n_mean = np.mean(n_data)
    n_std = np.std(n_data)

    normalized_dataset = [[(dataset[i][0] - n_mean) / n_std, dataset[i][1]] for i in range(len(dataset))]

    for i in range(0, T):
        # randomly choose item for approximate the gradient using only
        random_xy = random.choice(normalized_dataset)

        vec1 = 2 * (beta_0 + beta_1 * random_xy[0] - random_xy[1])
        vec2 = vec1 * random_xy[0]

        beta_0 = beta_0 - eta * vec1
        beta_1 = beta_1 - eta * vec2
        MSE = regression(beta_0, beta_1, dataset = normalized_dataset)

        print(i+1, round(beta_0, 2), round(beta_1, 2), round(MSE, 2))

