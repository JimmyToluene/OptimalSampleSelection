from itertools import combinations
import random
import time

samples = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

k = 6  # Size of groups to form
j = 5
s = 4  # Size of combinations to be covered

class KGroup(tuple):
    score = 0
    cover = []

j_groups = list(combinations(samples, j))
k_groups = [KGroup(k) for k in list(combinations(samples, k))]

k_groups_chosen = list()

while j_groups:
    best_score = -1
    best_k_group = None
    for k_group in k_groups:
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

    for cover in best_k_group.cover:
        j_groups.remove(cover)

    k_groups_chosen.append(best_k_group)
    k_groups.remove(best_k_group)

print(*k_groups_chosen, sep='\n')








