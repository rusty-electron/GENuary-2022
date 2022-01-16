import numpy as np

TOPPLE_LIMIT = 3

class Sandpile:
    def __init__(self, data, topple = True):
        self.data = np.array(data)
        assert len(self.data.shape) == 2, "size of dims must be 2"
        self.dims = self.row_count, self.col_count = self.data.shape
        self.to_topple = [] # for keep track of potential topple locations in future iterations
        if topple:
            self.topple_all()

    def topple_once(self):
        if len(self.to_topple) == 0: # if to_topple list is empty, check the entire data array for topple locations
            for r in range(self.row_count):
                for c in range(self.col_count):
                    if self.data[r, c] > TOPPLE_LIMIT:
                        current_pair = (r, c)
                        self.distribute_values(current_pair)
        # else:
        #     for pair in self.to_topple:
        #         if self.data[pair[0], pair[1]] > TOPPLE_LIMIT:
        #             self.distribute_values(pair)

    def topple_all(self):
        while np.sum(self.data > TOPPLE_LIMIT) > 0:
            self.topple_once()

    def distribute_values(self, current_pair):
        # if current_pair in self.to_topple and self.data[current_pair] <= TOPPLE_LIMIT:
        #     self.to_topple.remove(current_pair)
        x, y = current_pair
        if x + 1 < self.row_count:
            self.data[x + 1, y] += 1
        if x - 1 >= 0:
            self.data[x - 1, y] += 1
        if y + 1 >= 0:
            self.data[x, y + 1] += 1
        if y - 1 < self.col_count:
            self.data[x, y - 1] += 1

        self.data[current_pair] -= TOPPLE_LIMIT + 1
        # if current_pair not in self.to_topple and self.data[current_pair] > TOPPLE_LIMIT:
        #     self.to_topple.append(current_pair)

    def __add__(self, other):
        sum_pile = Sandpile(self.data + other.data)
        return sum_pile

    def __str__(self):
        return np.array2string(self.data)

if __name__ == "__main__":
    pile_a = Sandpile([[3, 3, 3], [3, 3, 3], [3, 3, 3]])
    pile_b = Sandpile([[3, 3, 3], [3, 1, 3], [3, 3, 3]])
    pile_c = pile_a + pile_b
    print(pile_c)
