from concurrent.futures import ProcessPoolExecutor
import itertools
from collections import defaultdict
import random
import time  # Import the time module to measure running time

def thread_worker(k_groups, j_groups_set, s):
    result = defaultdict(list)
    for k_group in k_groups:
        k_set = set(k_group)
        cover_count = 0
        for j_set in j_groups_set:
            if len(j_set & k_set) >= s:
                cover_count += 1
        if cover_count > 0:
            result[cover_count].append(k_group)
    return result

def find_optimal_k_groups_multithreaded(samples, k, j, s, num_threads=12):
    start_time = time.time()  # Start the timer

    k_groups = list(itertools.combinations(samples, k))
    j_groups = list(itertools.combinations(samples, j))
    j_groups_set = [set(g) for g in j_groups]
    k_groups_chosen = []

    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        while j_groups_set:
            # Split k_groups into chunks for each thread
            chunks = [k_groups[i::num_threads] for i in range(num_threads)]
            futures = [executor.submit(thread_worker, chunk, j_groups_set, s) for chunk in chunks]

            k_group_scores = defaultdict(list)
            for future in futures:
                result = future.result()
                for key, value in result.items():
                    k_group_scores[key].extend(value)

            if not k_group_scores:
                break

            max_cover = max(k_group_scores)
            chosen_k_group = random.choice(k_group_scores[max_cover])
            k_groups_chosen.append(chosen_k_group)

            # Update remaining j_groups
            chosen_k_set = set(chosen_k_group)
            j_groups_set = [j_set for j_set in j_groups_set if len(j_set & chosen_k_set) < s]

    elapsed_time = time.time() - start_time  # Calculate the elapsed time
    print(f"Samples number:{len(samples)},k:{k},j:{j},s:{s}")
    print(f"Execution time: {elapsed_time:.5f} seconds")
    print(f"The number of chosen group:{len(k_groups_chosen)}")
    return k_groups_chosen

if __name__ == "__main__":
    samples = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]  # Adjusted for your use case
    k = 7
    j = 5
    s = 3

    result = find_optimal_k_groups_multithreaded(samples, k, j, s)
    print("Optimal k-group with highest coverage:", result)
