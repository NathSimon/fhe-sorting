import random
import sys
import numpy as np

# Generate a list of integers from 1 to N
numbers = [(np.random.randint(0, 2**4)) for _ in range(20)]

# Shuffle the list
random.shuffle(numbers)

# Define the output file name
filename = f"unsorted_numbers.txt"

output_file = filename

# Write the shuffled numbers to the output file
with open(output_file, "w") as file:
    for num in numbers:
        file.write(str(num) + "\n")

print(f"Shuffled numbers from 1 to {20} saved to {output_file}")