import numpy as np

class Area():
    
    """
    Author: Anton Masiukevich
    """

    
    def __init__(self, width=50, height=100, sprinkler_rad=7):

        self.width = width
        self.height = height
        self.sprinkler_rad = sprinkler_rad

        self.clear_area()


    def add_sprinkle(self, sprinkle_coords):
        # try:

        # lower_range_x, upper_range_x, lower_range_y, upper_range_y = 0, 0, 0, 0
        lower_range_x = sprinkle_coords[0] - self.sprinkler_rad
        upper_range_x = sprinkle_coords[0] + self.sprinkler_rad + 1

        lower_range_y = sprinkle_coords[1] - self.sprinkler_rad
        upper_range_y = sprinkle_coords[1] + self.sprinkler_rad + 1

        if lower_range_x < 0:
            lower_range_x = 0
        if upper_range_x > self.width:
            upper_range_x = self.width
        if lower_range_y < 0:
            lower_range_y = 0
        if upper_range_y > self.height:
            upper_range_y = self.height


        for y_i in range(lower_range_y, upper_range_y):
            for x_i in range(lower_range_x, upper_range_x):
                check_value = np.linalg.norm(np.array(sprinkle_coords) - np.array([x_i, y_i]))
                if check_value < self.sprinkler_rad or np.isclose(check_value, self.sprinkler_rad):
                    self.area_matrix[y_i][x_i] = 1


    def clear_area(self):
        self.area_matrix = np.zeros(shape=(self.height, self.width), dtype=int)

    def visualize_area(self):
        for i in range(self.height):
            string_to_print = ""
            for j in range(self.width):
                string_to_print += str(self.area_matrix[i][j])
            print(string_to_print)

    def calc_sprinkled_ratio(self):
        return 100 * np.mean(self.area_matrix)

    def get_total_area(self):
        return self.width * self.height
