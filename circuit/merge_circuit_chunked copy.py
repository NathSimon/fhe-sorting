from concrete import fhe
import numpy as np
import time

configuration = fhe.Configuration(
    show_graph=False,
    show_progress=True,
    progress_title="Sorting:",
    enable_unsafe_features=True
)

def merge(left, right):
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left
    result = []
    index_left = index_right = 0
    while len(result) < len(left) + len(right):
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1
        if index_right == len(right):
            result += left[index_left:]
            break
        if index_left == len(left):
            result += right[index_right:]
            break
    return result


@fhe.compiler({"array": "encrypted"})
def function(array):
    if len(array) < 2:
        return array
    midpoint = len(array) // 2  
    return merge( #doenst work
        left=function(array[:midpoint]),
        right=function(array[midpoint:]))

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

bubble_circuit.server.save("compiled_circuits/server_merge_sort_chunked.zip")
bubble_circuit.client.save("../server/circuits/server_merge_sort_chunked.zip")