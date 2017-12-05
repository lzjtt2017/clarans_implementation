import math
import random

import numpy as np
from tqdm import tqdm

random.seed()

# Komentarze i opis struktur danych w komentarzach
# Raport w pdf, w nim wykres czasu działania dla różnych ilości danych, dla różnych wartości numlocal i maxneighbor
# Obsługa polygonów + określić dla nich miarę grupowania - może jest w artykule. Wyniki działania na przykładowych danych.


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cluster = None


class Clarans(object):

    # Punkt 1
    def __init__(self, points, numlocal, maxneighbor, number_of_medoids):
        self.points = points
        self.point_indices = len(points)
        self.numlocal = numlocal
        self.maxneighbor = maxneighbor
        self.mincost = 1000000000
        self.number_of_medoids = number_of_medoids

        self.local_best_medoids = []
        self.best_medoids = []
        self.distance_matrix = np.asmatrix(np.zeros((self.number_of_medoids, self.point_indices)))

    def run(self):
        pbar = tqdm(total=self.numlocal)

        i = 1
        while i <= self.numlocal:
            pbar.update(1)
            self.distance_matrix.fill(0)
            self.local_best_medoids = []

            # Punkt 2
            temp_medoids = self.get_random_medoids()
            self.set_distances(temp_medoids)
            self.assign_to_clasters(temp_medoids)
            cost = self.get_total_distance(temp_medoids)

            # Punkt 3
            j = 1
            while j <= self.maxneighbor:

                # Punkt 4
                new_medoid_index = self.get_random_neighbor(temp_medoids)
                self.replace_random_medoid(temp_medoids, new_medoid_index)
                self.update_distance_matrix_for_new_medoid(temp_medoids, new_medoid_index)
                self.assign_to_clasters(temp_medoids)
                new_cost = self.get_total_distance(temp_medoids)

                # Punkt 5
                if new_cost < cost:
                    self.local_best_medoids = temp_medoids.copy()
                    cost = new_cost
                    j = 1
                    continue
                else:

                    # Punkt 6
                    j += 1
                    if j <= self.maxneighbor:
                        continue

                    # Punkt 7
                    elif cost < self.mincost:
                        self.mincost = cost
                        self.best_medoids = self.local_best_medoids.copy()

                    # Punkt 8
                    i += 1
                    if i > self.numlocal:
                        self.set_distances(self.best_medoids)
                        self.assign_to_clasters(self.best_medoids)
                        return self.best_medoids, self.points
                    else:
                        break
        pbar.close()

    def get_random_medoids(self):
        return random.sample(range(self.point_indices), self.number_of_medoids)

    @staticmethod
    def get_distance(pointA, pointB):
        return math.sqrt((pointA.x - pointB.x) ** 2 + (pointA.y - pointB.y) ** 2)

    def set_distances(self, medoids_indices):
        for medoid_index in medoids_indices:
            for point_index in range(self.point_indices):
                self.distance_matrix[medoids_indices.index(medoid_index), point_index] = \
                    self.get_distance(self.points[medoid_index], self.points[point_index])

    def assign_to_clasters(self, medoids_indices):
        for point_index, point in enumerate(self.points):
            d = 1000000000
            idx = point_index
            for medoid_index in medoids_indices:
                distance = self.distance_matrix[medoids_indices.index(medoid_index), point_index]
                if distance < d:
                    d = distance
                    idx = medoid_index
            point.cluster = idx

    def get_total_distance(self, medoids_indices):
        tot_dist = 0
        for point_index, point in enumerate(self.points):
            tot_dist += self.distance_matrix[medoids_indices.index(point.cluster), point_index]
        return tot_dist

    def get_random_neighbor(self, medoids_indices):
        new_medoid_index = random.randrange(0, self.point_indices, 1)
        while new_medoid_index in medoids_indices:
            new_medoid_index = random.randrange(0, self.point_indices, 1)

        return new_medoid_index

    def replace_random_medoid(self, medoids_indices, new_medoid_index):
        medoids_indices[random.randrange(0, len(medoids_indices))] = new_medoid_index

    def update_distance_matrix_for_new_medoid(self, medoids_indices, new_medoid_index):
        for point_index in range(self.point_indices):
            self.distance_matrix[medoids_indices.index(new_medoid_index), point_index] = \
                self.get_distance(self.points[new_medoid_index], self.points[point_index])
