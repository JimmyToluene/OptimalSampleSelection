from itertools import combinations
from gurobipy import Model, GRB, quicksum

def setup_model(elements, j, k):
    model = Model("SetCover")
    model.setParam("MIPFocus", 1)
    model.setParam("Method", 0)
    model.setParam("Threads", 10)  # 使用4个线程
    model.setParam("Heuristics", 1)  # 优先寻找可行解
    model.setParam("Cuts", 3)  # 强化割平面生成
    j_subsets = list(combinations(elements, j))
    k_subsets = list(combinations(elements, k))

    # 创建决策变量
    x = model.addVars(k_subsets, vtype=GRB.BINARY, name="x")

    # 目标是最小化选中的 k-subsets 的数量
    model.setObjective(quicksum(x[sub] for sub in k_subsets), GRB.MINIMIZE)

    # 为每个 j-subset 添加覆盖约束
    for j_sub in j_subsets:
        model.addConstr(quicksum(x[k_sub] for k_sub in k_subsets if set(j_sub).issubset(k_sub)) >= 1, name=f"cover_{j_sub}")

    return model, x

def ida_star_search(model, x, max_depth):
    best_solution = None

    def search(depth, current_depth=0):
        nonlocal best_solution
        if current_depth > depth:
            return
        model.optimize()
        if model.status == GRB.OPTIMAL:
            current_solution = model.objVal
            if best_solution is None or current_solution < best_solution:
                best_solution = current_solution
                print(f"New best solution with {current_solution} subsets at depth {current_depth}")
            if current_depth < depth:
                # 增加约束来深化搜索
                search(depth, current_depth + 1)

    for depth in range(1, max_depth + 1):
        print(f"Searching at depth {depth}")
        search(depth)

    return best_solution

# 使用示例
elements = range(1, 14)  # 示例元素集合
j = 5  # j-subset 大小
k = 6  # k-subset 大小
model, x = setup_model(elements, j, k)
best_cover = ida_star_search(model, x, max_depth=1)
print(f"Best cover found uses {best_cover} k-subsets.")

