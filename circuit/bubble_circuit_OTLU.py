from concrete import fhe
import numpy as np
import time

configuration = fhe.Configuration(
    show_graph=True,
    show_progress=True,
    progress_title="Sorting:",
    comparison_strategy_preference=fhe.ComparisonStrategy.ONE_TLU_PROMOTED,
    enable_unsafe_features=True
)

@fhe.compiler({"array": "encrypted"})
def function(array):
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            cmp = array[j] > array[j + 1]
            tmp = array[j]
            array[j] = array[j + 1] * cmp + array[j] * (1 - cmp)
            array[j + 1] = array[j + 1] * (1 - cmp) + tmp * cmp
            already_sorted = False
        if already_sorted:
            break
    return array

sample = [(np.random.randint(0, 2**4)) for _ in range((20))]
sample = np.array(sample)
print("unsorted values = ", sample)

inputset = [[(np.random.randint(0, 2**4)) for _ in range(20)] for _ in range(30)]
inputset = np.array(inputset)

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

time_start = time.time()
python_result = function(sample)
time_end = time.time()
print("python time = ", time_end - time_start)

print("homomorphic result = ", result)
print("python result = ", python_result)

bubble_circuit.server.save("compiled_circuits/server_bubble_sort_OTLU.zip")
bubble_circuit.server.save("../server/circuits/server_bubble_sort_OTLU.zip")