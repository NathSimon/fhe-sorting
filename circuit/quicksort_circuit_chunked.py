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
    i = 0
    for j in range(0, len(array)):
        cmp = array[j] <= array[len(array) - 1]
        tmp = array[i]
        array[i] = array[j] * cmp + array[i] * (1 - cmp)
        array[j] = array[j] * (1 - cmp) + tmp * cmp
        #i += cmp
    return array

# @fhe.compiler({"array": "encrypted"})
# def function(array):
#     if len(array) <= 1:
#         return array

#     stack = [(0, len(array) - 1)]

#     while stack:
#         low, high = stack.pop()

#         if low < high:
#             pivot = array[high]
#             i = low - 1

#             for j in range(low, high):
#                 cmp = array[j] <= pivot
#                 #i += 1
#                 #i+=cmp
#                 #i = i * cmp + (i - 1) * (1 - cmp)
#                 tmp = array[i]
#                 array[i] = array[j] * cmp + array[i] * (1 - cmp)
#                 array[j] = array[j] * (1 - cmp) + tmp * cmp
                
#             tmp = array[i + 1]
#             array[i + 1] = array[high]
#             array[high] = tmp
            
#             pivot_index = i + 1

#             if pivot_index - low < high - pivot_index:
#                 stack.append((low, pivot_index - 1))
#                 stack.append((pivot_index + 1, high))
#             else:
#                 stack.append((pivot_index + 1, high))
#                 stack.append((low, pivot_index - 1))

#     return array

sample = [(np.random.randint(0, 2**4)) for _ in range(20)]
print("unsorted values = ", sample)

#inputset = [[(np.random.randint(0, 2**4)) for _ in range(20)] for _ in range(30)]

#print("compiling...")
#time_start = time.time()
#bubble_circuit = function.compile(inputset, configuration)
#time_end = time.time()
#total_time = time_end - time_start
#print("compiled in : ", total_time)

#print("encrypting and running...")
#time_start = time.time()
#result = bubble_circuit.encrypt_run_decrypt(sample)
#time_end = time.time()
#print("time = ", time_end - time_start)

#print("homomorphic result = ", result)
print("python result = ", function(sample))

#bubble_circuit.server.save("compiled_circuits/server_quick_sort_chunked.zip")
#bubble_circuit.client.save("../server/circuits/server_quick_sort_chunked.zip")