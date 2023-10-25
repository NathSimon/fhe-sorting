from concrete.ml.sklearn.neighbors import KNeighborsClassifier
import concrete.fhe as cnp
from concrete import fhe
import numpy
import time
from random import randint

configuration = fhe.Configuration(
    show_graph=False,
    show_progress=True,
    progress_title="Sorting:",
    enable_unsafe_features=True
)

@fhe.compiler({"x": "encrypted"})
def topk_sorting(x):
    n_neighbors = len(x)
    """Argsort in FHE.

    Time complexity: O(nlog²(k))

    Args:
        x (numpy.ndarray): The quantized input values
        labels (numpy.ndarray): The labels of the training data-set

    Returns:
        numpy.ndarray: The argsort.
    """

    def gather1d(x, indices):
        """Select elements from the input array `x` using the provided `indices`.

        Args:
            x (numpy.ndarray): The encrypted input array
            indices (numpy.ndarray): The desired indexes

        Returns:
            numpy.ndarray: The selected encrypted indexes.
        """
        arr = []
        for i in indices:
            arr.append(x[i])
        enc_arr = cnp.array(arr)
        return enc_arr

    def scatter1d(x, v, indices):
        """Rearrange elements of `x` with values from `v` at the specified `indices`.

        Args:
            x (numpy.ndarray): The encrypted input array in which items will be updated
            v (numpy.ndarray): The array containing values to be inserted into `x`
                at the specified `indices`.
            indices (numpy.ndarray): The indices indicating where to insert the elements
                from `v` into `x`.

        Returns:
            numpy.ndarray: The updated encrypted `x`
        """
        for idx, i in enumerate(indices):
            x[i] = v[idx]
        return x

    comparisons = numpy.zeros(x.shape)
    #labels = labels + cnp.zeros(labels.shape)

    n, k = x.size, n_neighbors
    # Determine the number of stages for a sequence of length n
    ln2n = int(numpy.ceil(numpy.log2(n)))

    # Stage loop
    for t in range(ln2n - 1, -1, -1):
        # p: Determines the range of indexes to be compared in each pass.
        p = 2**t
        # r: Offset that adjusts the range of indexes to be compared and sorted in each pass
        r = 0
        # d: Comparison distance in each pass
        d = p
        # Number of passes for each stage
        for bq in range(ln2n - 1, t - 1, -1):
            with cnp.tag(f"Stage_{t}_pass_{bq}"):
                q = 2**bq
                # Determine the range of indexes to be compared
                range_i = numpy.array(
                    [i for i in range(0, n - d) if i & p == r and comparisons[i] < k]
                )
                if len(range_i) == 0:
                    # Edge case, for k=1
                    continue

                # Select 2 bitonic sequences `a` and `b` of length `d`
                # a = x[range_i]: first bitonic sequence
                # a_i = idx[range_i]: Indexes of a_i elements in the original x
                a = gather1d(x, range_i)
                # a_i = gather1d(idx, range_i)
                # b = x[range_i + d]: Second bitonic sequence
                # b_i = idx[range_i + d]: Indexes of b_i elements in the original x
                b = gather1d(x, range_i + d)
                # b_i = gather1d(idx, range_i + d)

                #labels_a = gather1d(labels, range_i)  #
                #labels_b = gather1d(labels, range_i + d)  # idx[range_i + d]

                with cnp.tag("diff"):
                    # Select max(a, b)
                    diff = b - a

                with cnp.tag("max_value"):
                    max_x = a + numpy.maximum(0, diff)

                with cnp.tag("swap_max_value"):
                    # Swap if a > b
                    # x[range_i] = max_x(a, b): First bitonic sequence gets min(a, b)
                    x = scatter1d(x, a + b - max_x, range_i)
                    # x[range_i + d] = min(a, b): Second bitonic sequence gets max(a, b)
                    x = scatter1d(x, max_x, range_i + d)

                # Update labels array according to the max value
                # with cnp.tag("max_label"):
                #     is_a_greater_than_b = diff > 0
                #     max_labels = labels_a + (labels_b - labels_a) * is_a_greater_than_b

                # with cnp.tag("swap_max_label"):
                #     labels = scatter1d(labels, labels_a + labels_b - max_labels, range_i)
                #     labels = scatter1d(labels, max_labels, range_i + d)

                # Update
                with cnp.tag("update"):
                    comparisons[range_i + d] = comparisons[range_i + d] + 1
                    # Reduce the comparison distance by half
                    d = q - p
                    r = p

    return x


sample = [(numpy.random.randint(0, 2**4)) for _ in range(20)]
array = numpy.array(sample)
print("unsorted values = ", array)

inputset = [[(numpy.random.randint(0, 2**4)) for _ in range(20)] for _ in range(30)]
inpuset = numpy.array(inputset)

print("compiling...")
time_start = time.time()
circuit = topk_sorting.compile(inputset, configuration)
time_end = time.time()
total_time = time_end - time_start
print("compiled in : ", total_time)

print("encrypting and running...")
time_start = time.time()
result = circuit.encrypt_run_decrypt(sample)
time_end = time.time()
print("time = ", time_end - time_start)

print("homomorphic result = ", result)
print("python result = ", topk_sorting(array))

circuit.server.save("compiled_circuits/server_topk_sort_chunked.zip")
circuit.server.save("../server/circuits/server_topk_sort_chunked.zip")

