import numpy as np

class Solution():

    ID = 0

    def __init__(self, n_sprinklers, width, height):
        """
        :param n_sprinklers: number of sprinklers in our solution
        """
        Solution.ID += 1
        self.sol_id = Solution.ID
        self.n_sprinklers = n_sprinklers

        self.width = width
        self.height = height

        self.fitness = 0
        self.sprinklers1, self.sprinklers2 = self.generate_sprinklers_random()

    # Play with the distributions later
    def generate_sprinklers_random(self):

        sprinklers_coords1, sprinklers_coords2 = [], []
        for _ in range(self.n_sprinklers):
            sprinklers_coords1.append(int(np.random.uniform(low=0, high=self.width)))
            sprinklers_coords2.append(int(np.random.uniform(low=0, high=self.height)))

        return sprinklers_coords1, sprinklers_coords2

    def generate_sprinklers_wiser(self):

        sprinklers_coords1, sprinklers_coords2 = [], []

        for i in range(self.n_sprinklers - 1):

            q_x = (i * (self.width // self.n_sprinklers), (i + 1) * (self.width // self.n_sprinklers))
            random_y = np.random.randint(0, self.n_sprinklers - 1)
            q_y = (random_y * (self.height // self.n_sprinklers), (random_y + 1) * (self.height // self.n_sprinklers))

            sprinklers_coords1.append(int(np.random.uniform(low=q_x[0], high=q_x[1])))
            sprinklers_coords2.append(int(np.random.uniform(low=q_y[0], high=q_x[1])))

        return sprinklers_coords1, sprinklers_coords2

    def __repr__(self):
        return f"id: {self.sol_id}"

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness