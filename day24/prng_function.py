import time
import math

import matplotlib.pyplot as plt

def prng(seed = None, num_range = 256):
    if seed == None:
        seed = int(time.time() * 1000)
    current_state = (1 << 127) | seed
    random_value = 0

    no_of_bits = math.log2(num_range)
    if int(no_of_bits) != no_of_bits:
        no_of_bits = int(no_of_bits) + 1
    else:
        no_of_bits = int(no_of_bits)

    for i in range(no_of_bits): # 8 bits for values in range 0-255
        newbit = (current_state ^ (current_state >> 1) ^ (current_state >> 2) ^ (current_state >> 7)) & 1
        current_state = (current_state >> 1) | (newbit << 127)
        random_value = random_value | (newbit << (no_of_bits - i - 1))
    return random_value % num_range

def plot_distribution(iterations = 1000000):
    occurences = dict()
    for _ in range(iterations):
        value = prng()
        current_record = occurences.get(value, 0)
        current_record += 1

        occurences[value] = current_record

    plt.figure()
    plt.bar(occurences.keys(), occurences.values())
    plt.ylabel("frequency")
    plt.xlabel("generated numbers")
    plt.show()

if __name__ == "__main__":
    plot_distribution()
