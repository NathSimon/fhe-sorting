from concrete import fhe
import numpy as np
import time

configuration = fhe.Configuration(
    show_graph=False,
    show_progress=True,
    progress_title="Sorting:",
    enable_unsafe_features=True
)

@fhe.compiler({"array": "encrypted"})
def function(array):
    for i in range(1, len(array)):
        key_item = array[i]      
        j = i - 1        
        
        for k in range(j, -1, -1):  
            cmp = array[j] > key_item
            array[j + 1] = array[j] * cmp + key_item * (1 - cmp)
            j = (j-1)*(cmp) + j*(1 - cmp)
            k = 0*(1 - cmp)

        array[j + 1] = key_item #doenst work
    return array

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

bubble_circuit.server.save("compiled_circuits/server_insertion_sort_chunked.zip")
bubble_circuit.client.save("../server/circuits/server_insertion_sort_chunked.zip")