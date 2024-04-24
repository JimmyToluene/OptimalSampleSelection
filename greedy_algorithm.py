from itertools import combinations
import random
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

class KGroup(tuple):
    score = 0
    cover = []

def worker(k_subgroup):
    best_score = -1
    best_k_group = None
    for k_group in k_subgroup:
        k_group.score = 0
        k_group.cover = []
        for j_group in j_groups:
            # if the size of intersection >= s
            interesc = set(j_group).intersection(k_group) 
            if len(interesc) >= s:
                k_group.score += 1
                k_group.cover.append(j_group)
        if k_group.score > best_score:
            best_score = k_group.score
            best_k_group = k_group
    return best_k_group

samples = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

k = 6 # Size of groups to form
j = 5
s = 5  # Size of combinations to be covered

thread_count = 8

j_groups = list(combinations(samples, j))
k_groups = [KGroup(k) for k in list(combinations(samples, k))]

k_groups_chosen = list()

print(f"j_group count={len(j_groups)}")
print(f"k_group count={len(k_groups)}")

if __name__ == '__main__':
    iter = 0
    while j_groups:
        start = time.time()

        # Split k_groups into subgroups
        k_subgroup_size = int(len(k_groups) / thread_count)
        k_subgroups = [k_groups[i:i+k_subgroup_size] for i in range(0, len(k_groups), k_subgroup_size)]

        for sg in k_subgroups:
            p = Process(target=worker, args=sg)
            p.start()
            p.join()


        #with ThreadPoolExecutor() as executor:
        #    futures = [executor.submit(worker, k_subgroup) for k_subgroup in k_subgroups]
        #    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

        #results = [future.result() for future in futures]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        best_k_group = max(results, key=lambda x : x.score)

        for cover in best_k_group.cover:
            j_groups.remove(cover)

        k_groups_chosen.append(best_k_group)
        k_groups.remove(best_k_group)

        print(f" -- iter {iter} -- ")
        print(f"duration={time.time() - start}")
        print(f"cover={len(best_k_group.cover)}")
        print(f"remained={len(j_groups)}")
        print('\n')

        iter += 1

    print(*k_groups_chosen, sep='\n')








