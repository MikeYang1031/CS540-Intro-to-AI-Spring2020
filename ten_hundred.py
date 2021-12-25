"""
    File name: ten_hundred.py
    Author: Zonglin Yang
    Project: P7
    course: cs540 Spring2020
    credit: Piazza
"""
import csv
import numpy as np


# takes in a string with a path to a CSV file formatted as in the link above, and returns the data in a single
# structure.
def load_data(filepath):
    data = []
    with open(filepath) as f:
        for d in csv.DictReader(f):
            d.pop("Lat")
            d.pop("Long")
            for k in list(d.keys())[2:]:
                d[k] = int(d[k])
            data.append(d)
    return data


# takes in one row from the data loaded from the previous function, calculates the corresponding x, y values for
# that region as specified in the video, and returns them in a single structure.
def calculate_x_y(time_series):
    l = list(time_series.items())[::-1]
    last = l[0][1]
    x, y = None, None
    for i in range(len(l)):
        if l[i][1] <= last / 10:
            x = i
            break

    for i in range(len(l)):
        if type(l[i][1]) is str:
            break
        if l[i][1] <= last / 100:
            y = i
            break
    return x if x else None, y - x if y else None


# performs single linkage hierarchical agglomerative clustering on the regions with the (x,y) feature representation,
# and returns a data structure representing the clustering.
def hac(dataset):
    def euclidean(i, j):  # calculate the l2 distance
        x, y = dataset[i], dataset[j]  # two points
        return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5

    def min_distance(c1, c2):  # calculate min distance between points from cluster c1 and cluster c2
        ds = []
        for x in cluster[c1]:
            for y in cluster[c2]:
                ds.append(distance[(x, y)])  # calculate all distance
        return min(ds)  # return the min distance as the distance of two cluster , ie, the single

    cluster = {i: [i] for i in range(len(dataset))}
    distance = {}
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            distance[(i, j)] = euclidean(i, j)  # *pre calculate the distance of any two points
            # I think it is a good way to enhance performance

    result = []
    nc = len(dataset)
    while len(cluster) > 1:  # while there is not only one cluster
        keys = list(cluster)
        keys.sort()

        min_pair = None
        closest_d = float('inf')
        # the HAC Algo in slice 19
        for k1 in keys:
            for k2 in keys:
                if k2 <= k1:
                    continue
                d = min_distance(k1, k2)  # calculate distance between clusters
                if d < closest_d:
                    closest_d = d  # update the closest distance and closest cluster pair
                    min_pair = [k1, k2]

        a, b = min_pair
        cluster[nc] = cluster.pop(a)
        cluster[nc].extend(cluster.pop(b))  # assign a new cluster id of the combination of two cluster
        result.append([a, b, closest_d, len(cluster[nc])])  # add a new row of result
        nc += 1
    return np.array(result)  # convert to numpy


if __name__ == '__main__':
    data = load_data("time_series_covid19_confirmed_global.csv")
    xy = [calculate_x_y(d) for d in data]
    xy = [d for d in xy if d[1] is not None]
    from scipy.cluster.hierarchy import linkage

    result = hac(xy)
    print(result)
