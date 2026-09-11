def feasible_subsets(required, capacity, local_caps=None):
    n = len(required)
    local_caps = local_caps or [float("inf")] * n
    out = []
    for mask in range(1 << n):
        subset = [i for i in range(n) if mask & (1 << i)]
        if all(required[i] <= local_caps[i] for i in subset):
            total = sum(required[i] for i in subset)
            if total <= capacity + 1e-12:
                out.append(subset)
    return out

def unavoidable_replacement(demand, source_capacity, required, shared_capacity, local_caps=None):
    subsets = feasible_subsets(required, shared_capacity, local_caps)
    preserved = 0.0
    for s in subsets:
        preserved = max(preserved, sum(source_capacity[i] for i in s))
    return max(0.0, demand - preserved)
