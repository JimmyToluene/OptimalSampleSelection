from itertools import combinations
from collections import defaultdict
import time
from tkinter import ttk

import interface


class Greedy:
    cover = defaultdict(set)
    cover_by = defaultdict(set)
    s_group_generated_k_groups_dp = defaultdict(set)

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

        begin_group = len(j_groups)
        while j_groups:
            execute_group = len(j_groups)
            best_k_group = max(Greedy.cover, key=lambda x: len(Greedy.cover[x]))
            j_groups = j_groups.difference(Greedy.cover[best_k_group])
            Greedy.remove_covered(best_k_group)
            k_groups.remove(best_k_group)
            Greedy.cover.pop(best_k_group)
            k_groups_chosen.append(best_k_group)

        print(" ** RESULT ** ")
        print(*k_groups_chosen, sep='\n')
        print(f"count = {len(k_groups_chosen)}")
        cover_end = time.time()
        elapsed_time= cover_end - init_begin
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
        s_groups = [s_group for s_group in list(combinations(j_group, s))]

        k_groups = set()
        for s_group in s_groups:
            if s_group in Greedy.s_group_generated_k_groups_dp:
                k_groups = k_groups | Greedy.s_group_generated_k_groups_dp[s_group]

            else:
                remained = [x for x in samples if x not in s_group]
                tails = list(combinations(remained, k-s))
                k_groups_generated = set()
                for tail in tails:
                    k_group = tuple(sorted(s_group + tail))
                    k_groups_generated.add(k_group)
                k_groups = k_groups | k_groups_generated
                Greedy.s_group_generated_k_groups_dp[s_group] = k_groups_generated

        return k_groups