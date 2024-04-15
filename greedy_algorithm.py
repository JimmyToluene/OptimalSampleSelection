from itertools import combinations
import random

samples = [1, 2, 3, 4, 5, 6, 7]

k = 6  # Size of groups to form
j = 5
s = 5  # Size of combinations to be covered

k_groups = list(combinations(samples, k))
j_groups = list(combinations(samples, j))

k_groups_chosen = list()
k_group_score = dict() 
k_group_cover_list = dict(list())

while j_groups:
    # Step 1: For each k_group, calculate its score
    for k_group in k_groups:
        k_group_score[k_group] = 0
        k_group_cover_list[k_group] = list() 
        for j_group in j_groups:
            # if the size of intersection >= s
            if len(set(j_group).intersection(k_group)) >= s:
                k_group_score[k_group] += 1
                k_group_cover_list[k_group].append(j_group)

    # Step 2: Select the group with the max score and mark those covered
    best_k_group = max(k_group_score, key=k_group_score.get)
    max_score = k_group_score[best_k_group]
    best_k_groups = [k for (k, v) in k_group_score.items() if v == max_score]
    rand_best_k_group = random.choice(best_k_groups)
    # Remove j_group the are covered
    j_groups = set(j_groups).difference(k_group_cover_list[rand_best_k_group])

    k_group_score.pop(rand_best_k_group)
    k_groups.remove(rand_best_k_group)
    k_groups_chosen.append(rand_best_k_group)

print(*k_groups_chosen, sep='\n')








