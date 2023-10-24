from concrete import fhe
import numpy as np
import time
from random import randint

configuration = fhe.Configuration(
    show_graph=False,
    show_progress=True,
    progress_title="Sorting:",
    enable_unsafe_features=True
)

@fhe.compiler({"array": "encrypted"})
def function(array):
    if len(array) < 2:
        return array
    low, same, high = [], [], []
    pivot = array[randint(0, len(array) - 1)]
    for item in array: #doenst work
        if item < pivot:
            low.append(item)
        elif item == pivot:
            same.append(item)
        elif item > pivot:
            high.append(item)
    return function(low) + same + function(high)

sample = [(np.random.randint(0, 2**4)) for _ in range(20)]
print("unsorted values = ", sample)

inputset = [[(np.random.randint(0, 2**4)) for _ in range(20)] for _ in range(30)]

print("compiling...")
time_start = time.time()
bubble_circuit = function.compile(inputset, configuration)
time_end = time.time()
total_time = time_end - time_start
print("compiled in : ", total_time)

print("encrypting and running...")
time_start = time.time()
result = bubble_circuit.encrypt_run_decrypt(sample)
time_end = time.time()
print("time = ", time_end - time_start)

print("homomorphic result = ", result)
print("python result = ", function(sample))

bubble_circuit.server.save("compiled_circuits/server_quick_sort_chunked.zip")
bubble_circuit.client.save("../server/circuits/server_quick_sort_chunked.zip")