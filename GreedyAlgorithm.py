from itertools import combinations
from collections import defaultdict
import time

class Greedy:
    cover = defaultdict(set)
    cover_by = defaultdict(set)

    @staticmethod
    def MainAlgorithm(samples, k, j, s):
        k_groups = set(combinations(samples, k))
        j_groups = set(combinations(samples, j))

        print(f"k-group count: {len(k_groups)}")
        print(f"j-group count: {len(j_groups)}")
        init_begin = time.time()
        k_groups_chosen = []

        for j_group in j_groups:
            Greedy.cover_by[j_group] = Greedy.generate_cover_by(j_group, samples, k, s)
            for k_group in Greedy.cover_by[j_group]:
                Greedy.cover[k_group].add(j_group)

        init_end = time.time()
        print(f"Init complete; Elapsed time: {init_end-init_begin}s")

        iter = 0
        while j_groups:
            best_k_group = max(Greedy.cover, key=lambda x: len(Greedy.cover[x]))
            j_groups = j_groups.difference(Greedy.cover[best_k_group])
            Greedy.remove_covered(best_k_group)
            k_groups.remove(best_k_group)
            Greedy.cover.pop(best_k_group)
            k_groups_chosen.append(best_k_group)
            iter += 1

        print(" ** RESULT ** ")
        print(*k_groups_chosen, sep='\n')
        print(f"count = {len(k_groups_chosen)}")
        cover_end = time.time()
        print(f"Cover complete; Elapsed time: {cover_end - init_begin}s")
        return k_groups_chosen

    @staticmethod
    def remove_covered(best_k_group):
        for j_group in Greedy.cover[best_k_group]:
            for k_group in Greedy.cover_by[j_group]:
                if k_group != best_k_group:
                    Greedy.cover[k_group].remove(j_group)

    @staticmethod
    def generate_cover_by(j_group, samples, k, s):
        s_groups = [s_group for s_group in combinations(j_group, s)]
        k_groups = set()
        for s_group in s_groups:
            remained = [x for x in samples if x not in s_group]
            tails = list(combinations(remained, k-s))
            for tail in tails:
                k_groups.add(tuple(sorted(s_group + tail)))
        return k_groups