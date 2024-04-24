from itertools import combinations
from itertools import filterfalse
import time
import matplotlib.pyplot as plt
import numpy as np

class KGroup(tuple):
    cover = set()

class JGroup(tuple):
    cover_by = set()

def remove_covered(best_k_group):
    for j_group in best_k_group.cover:
        for k_group in j_group.cover_by:
            if k_group != best_k_group:
                k_group.cover.remove(j_group)

samples = [1,2,3,4,5]
k = 4
j = 3
s = 3

k_groups = set([KGroup(k) for k in list(combinations(samples, k))])
j_groups = set([JGroup(j) for j in list(combinations(samples, j))])

print(f"k-group count: {len(k_groups)}")
print(f"j-group count: {len(j_groups)}")

k_groups_chosen = []

# Init cover and cover_by sets
init_begin = time.time()

for j_group in j_groups:
    j_group.cover_by = set()

for k_group in k_groups:
    k_group.cover = set()

for k_group in k_groups:
    k_group.cover = set()
    for j_group in j_groups:
        # Don't need to check against all j's
        # Directly generate cover list from k
        if len(set(j_group).intersection(k_group)) >= s:
            k_group.cover.add(j_group)
            j_group.cover_by.add(k_group)

#for k_group in k_groups:
#    if j == s:
#        k_group.cover = [JGroup(j) for j in set(combinations(k_group, j))]
#        for j_group in k_group.cover:
#            j_groups.remove(j_group)
#            j_group.cover_by.add(k_group)
#            j_groups.add(j_group)
#            #j_groups[j_group].cover_by.add(k_group)
#    else:
#        pass

#for k_group in k_groups:
#    print(f"k: {k_group}, cover: {k_group.cover}")
#for j_group in j_groups:
#    print(f"j: {j_group}, cover_by: {j_group.cover_by}")

init_end = time.time()
print(f"Init complete; Elapsed time: {init_end-init_begin}s")

iter = 0
while j_groups:
    print(f" -- iter {iter} -- ")
    print(f"Remained j-groups: {len(j_groups)}")
    best_k_group = max(k_groups, key=lambda k: len(k.cover))
    j_groups = set(j_groups).difference(best_k_group.cover)
    remove_covered(best_k_group)
    k_groups.remove(best_k_group)
    k_groups_chosen.append(best_k_group)

    #xpoints = np.array(range(len(k_groups)))
    #ypoints = np.array([len(k_group.cover) for k_group in k_groups])
    #plt.plot(xpoints, ypoints)
    #plt.show()

    iter += 1

print(*k_groups_chosen, sep='\n')

cover_end = time.time()
print(f"Cover complete; Elapsed time: {cover_end - init_begin}s")