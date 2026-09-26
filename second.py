import random
import unittest
import math

def func_upper(x):
    return 3 * math.sin(x) + 5


def func_lower(x):
    return -2 * math.cos(x) + 3


def random_point(range_x, range_y):
    x = random.random() * (range_x[1] - range_x[0]) + range_x[0]
    y = random.random() * (range_y[1] - range_y[0]) + range_y[0]
    return x, y


def monte_carlo_approximation(n_points, func_u, func_l, range_x, range_y):

    true_area = (range_x[1] - range_x[0]) * (range_y[1] - range_y[0])

    points_in = 0

    for i in range(n_points):
        point = random_point(range_x, range_y)

        if func_l(point[0]) < point[1] < func_u(point[0]):
            points_in += 1

    return points_in / n_points * true_area


class MonteCarloApproximation(unittest.TestCase):
    x_range = (1, 2)
    y_range = (1, 8)
    
    true_value = 5.005
    
    def test_find_optimal_n_points(self):
        curr_n_points = 10
        
        approximate_value = monte_carlo_approximation(curr_n_points, func_upper, func_lower, self.x_range, self.y_range)
        
        while not math.isclose(approximate_value, self.true_value, abs_tol=0.0001): #иначе оно никогда не сойдется
            curr_n_points += 100
            
            approximate_value = monte_carlo_approximation(curr_n_points, func_upper, func_lower, self.x_range, self.y_range)
            
            print(f"Кол-во точек: {curr_n_points}, вычисленное значение: {approximate_value}")
            
        self.assertAlmostEqual(approximate_value, self.true_value, delta=0.0001)
        
        print(f"Подходящее значение n: {curr_n_points}, вычисленное: {approximate_value}")

