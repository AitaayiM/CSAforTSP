import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import numpy as np

class CrowSearch:
    def __init__(self, n, cities, distance):
        self.n = n
        self.cities = cities
        self.distance = distance
        self.current_solution = [0] * cities
        self.best_solution = [0] * cities

    def search(self):
        # Initialize crows/solutions
        for i in range(self.n):
            self.current_solution = self.generate_random_solution()
            if self.get_fitness(self.current_solution) < self.get_fitness(self.best_solution):
                self.best_solution = self.current_solution.copy()

        temp_solution = [0] * self.cities
        r1, r2 = 0, 0
        temp_fitness, new_fitness = 0, 0
        while True:
            for i in range(self.n):
                temp_solution = self.current_solution.copy()
                r1 = random.randint(0, self.cities - 1)
                r2 = random.randint(0, self.cities - 1)
                # Swap cities in solution
                temp = temp_solution[r1]
                temp_solution[r1] = temp_solution[r2]
                temp_solution[r2] = temp
                temp_fitness = self.get_fitness(temp_solution)
                new_fitness = self.get_fitness(self.current_solution)
                if temp_fitness < new_fitness:
                    self.current_solution = temp_solution
                    if temp_fitness < self.get_fitness(self.best_solution):
                        self.best_solution = temp_solution
                # Check if best solution is good enough
                threshold = 75
                if self.get_fitness(self.best_solution) <= threshold:
                    print("estimated cost: "+str(self.get_fitness(self.best_solution)))
                    return

    def generate_random_solution(self):
        solution = [0] * self.cities
        added = [False] * self.cities
        r = 0
        for i in range(self.cities):
            r = random.randint(0, self.cities - 1)
            while added[r]:
                r = random.randint(0, self.cities - 1)
            solution[i] = r
            added[r] = True
        return solution

    def get_fitness(self, solution):
        fitness = 0
        for i in range(self.cities - 1):
            fitness += self.distance[solution[i]][solution[i + 1]]
        return fitness

# Example usage:
if __name__ == '__main__':
    n = 100 # Number of crows/solutions
    # Coordonnées des villes
    all_coordinates = [(33, 1),
                        (14, 1),
                        (8, 22),
                        (14, 12),
                        (5, 3),
                        (19, 2),
                        (8, 12),
                        (12, 20)]
    cities = len(all_coordinates) # Number of cities
    # Coordonnées des villes
    x_coordinates = np.zeros((cities, 1))
    y_coordinates = np.zeros((cities, 1))
    city_distances = np.zeros((cities, cities))
    for i in range(cities):
        for j in range(cities):
            x1, y1 = all_coordinates[i]
            x2, y2 = all_coordinates[j]
            x_coordinates[i] = x1
            y_coordinates[i] = y1
            if i==j:
                city_distances[i][j]=99999
            else:
                city_distances[i][j] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    solver = CrowSearch(n, cities, city_distances)
    solver.search()
    print("Best solution found:", solver.best_solution)
    # Draw the cities
    fig, ax = plt.subplots()
    for i in range(cities):
        ax.add_patch(Circle((x_coordinates[i], y_coordinates[i]), radius=0.75, color='b'))
        ax.text(x_coordinates[i], y_coordinates[i], str(i), ha='center', va='center')

    ax.set_aspect('equal')
    ax.set_xlim(0, max(x_coordinates) + 1)
    ax.set_ylim(0, max(y_coordinates) + 1)

    # Draw the best path
    best_path = solver.best_solution
    for i in range(cities - 1):
        start = best_path[i]
        end = best_path[i + 1]
        ax.plot([x_coordinates[start], x_coordinates[end]], [y_coordinates[start], y_coordinates[end]], 'r')
    plt.show()
