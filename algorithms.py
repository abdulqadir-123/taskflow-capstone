from collections import Counter
from time import perf_counter

def normalize(s: str) -> str:
    return " ".join(s.lower().split())

def search_tasks(tasks, query: str):
    """Linear substring search. Time: O(n*m) worst-case for n tasks."""
    q = normalize(query)
    if not q:
        return tasks
    return [
        t for t in tasks
        if q in normalize(t.title) or q in normalize(t.description or "")
    ]
def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0 and records[j][key] > current[key]:
            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current
        def binary_search(sorted_records, target_value, key):
    low = 0
    high = len(sorted_records) - 1

    while low <= high:
        mid = (low + high) // 2
        value = sorted_records[mid][key]

        if value == target_value:
            return mid
        elif value < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return -1
def linear_search(records, target_value, key):
    for i, record in enumerate(records):
        if record[key] == target_value:
            return i
        def insertion_sort_count(records, key):
    comparisons = 0

    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if records[j][key] <= current[key]:
                break

            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return comparisons


def binary_search_count(sorted_records, target_value, key):
    low = 0
    high = len(sorted_records) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        if sorted_records[mid][key] == target_value:
            return {
                "index": mid,
                "comparison_count": comparisons,
            }

        if sorted_records[mid][key] < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return {
        "index": -1,
        "comparison_count": comparisons,
    }


def linear_search_count(records, target_value, key):
    comparisons = 0

    for i, record in enumerate(records):
        comparisons += 1

        if record[key] == target_value:
            return {
                "index": i,
                "comparison_count": comparisons,
            }

    return {
        "index": -1,
        "comparison_count": comparisons,
    }

def merge_sort(tasks, key=lambda x: x.id):
    """Stable merge sort. Time O(n log n), extra space O(n)."""
    if len(tasks) <= 1:
        return tasks[:]
    mid = len(tasks) // 2
    left = merge_sort(tasks[:mid], key)
    right = merge_sort(tasks[mid:], key)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

def task_statistics(tasks):
    status = Counter(t.status for t in tasks)
    priority = Counter(t.priority for t in tasks)
    total = len(tasks)
    done = status.get("done", 0)
    return {
        "total": total,
        "completed": done,
        "completion_percent": round((done / total) * 100, 2) if total else 0,
        "by_status": dict(status),
        "by_priority": dict(priority),
    }

def benchmark(tasks, repeats=50):
    start = perf_counter()
    for _ in range(repeats):
        search_tasks(tasks, "task")
    search_ms = (perf_counter() - start) * 1000 / repeats

    start = perf_counter()
    for _ in range(repeats):
        merge_sort(tasks, key=lambda x: x.id)
    sort_ms = (perf_counter() - start) * 1000 / repeats

    return {
        "items": len(tasks),
        "repeats": repeats,
        "linear_search_avg_ms": round(search_ms, 4),
        "merge_sort_avg_ms": round(sort_ms, 4),
    }
