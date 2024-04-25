from itertools import combinations
from collections import defaultdict
import time

def remove_covered(best_k_group):
    for j_group in cover[best_k_group]:
        for k_group in cover_by[j_group]:
            if k_group != best_k_group:
                cover[k_group].remove(j_group)

def generate_cover_by(j_group, samples, k, s):
    s_groups = [s_group for s_group in list(combinations(j_group, s))]

    k_groups = set()
    for s_group in s_groups:
        remained = [x for x in samples if x not in s_group]
        tails = list(combinations(remained, k-s))
        for tail in tails:
            k_groups.add(tuple(sorted(s_group + tail)))

    return k_groups


samples = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
k = 7
j = 5
s = 3

cover = defaultdict(set)
cover_by = defaultdict(set)

k_groups = set([k for k in list(combinations(samples, k))])
j_groups = set([j for j in list(combinations(samples, j))])

print(f"k-group count: {len(k_groups)}")
print(f"j-group count: {len(j_groups)}")

k_groups_chosen = []

# Init cover and cover_by sets
init_begin = time.time()

# METHOD 1: check against each pair; very slow
#for k_group in k_groups:
#    cover[k_group] = set()
#    for j_group in j_groups:
#        if len(set(j_group) & set(k_group)) >= s:
#            cover[k_group].add(j_group)
#            cover_by[j_group].add(k_group)

# METHOD 2: direct generate 
for j_group in j_groups:
    cover_by[j_group] = generate_cover_by(j_group, samples, k, s)
    for k_group in cover_by[j_group]:
        cover[k_group].add(j_group)

# Debug 
#for k_group in k_groups:
#    print(f"k: {k_group}, cover: {cover[k_group]}")
#for j_group in j_groups:
#    print(f"j: {j_group}, cover_by: {cover_by[j_group]}")

init_end = time.time()
print(f"Init complete; Elapsed time: {init_end-init_begin}s")

iter = 0
while j_groups:
    #print(f" -- iter {iter} -- ")
    #print(f"Remained j-groups: {len(j_groups)}")

    best_k_group = max(cover, key=lambda x: len(cover[x]))

    j_groups = set(j_groups).difference(cover[best_k_group])
    remove_covered(best_k_group)
    k_groups.remove(best_k_group)
    cover.pop(best_k_group)
    k_groups_chosen.append(best_k_group)

    iter += 1

print(" ** RESULT ** ")
print(*k_groups_chosen, sep='\n')
print(f"count = {len(k_groups_chosen)}")

cover_end = time.time()
print(f"Cover complete; Elapsed time: {cover_end - init_begin}s")