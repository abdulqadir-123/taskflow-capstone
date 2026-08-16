from .algorithms import insertion_sort, binary_search, linear_search


def insertion_sort_count(records, key):
    comparison_count = 0

    for i in range(1, len(records)):
        current = records[i]
        current_value = current[key]
        j = i - 1

        while j >= 0:
            comparison_count += 1

            if records[j][key] <= current_value:
                break

            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return comparison_count


def binary_search_count(sorted_records, target_value, key):
    low = 0
    high = len(sorted_records) - 1
    comparison_count = 0

    while low <= high:
        mid = (low + high) // 2
        comparison_count += 1

        if sorted_records[mid][key] == target_value:
            return {
                "index": mid,
                "comparison_count": comparison_count
            }

        if sorted_records[mid][key] < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return {
        "index": -1,
        "comparison_count": comparison_count
    }


def linear_search_count(records, target_value, key):
    comparison_count = 0

    for i, record in enumerate(records):
        comparison_count += 1

        if record[key] == target_value:
            return {
                "index": i,
                "comparison_count": comparison_count
            }

    return {
        "index": -1,
        "comparison_count": comparison_count
    }


def make_tasks(size):
    return [
        {
            "id": i,
            "title": f"Task {i}",
            "priority": (i % 4) + 1,
            "due_date": f"2026-12-{(i % 28) + 1:02d}"
        }
        for i in range(size, 0, -1)
    ]


def run_benchmark():
    sizes = [10, 500, 3000]

    print("\nTaskFlow Section 2 - Algorithm Benchmark")
    print("=" * 60)

    for size in sizes:
        records = make_tasks(size)

        insertion_records = [dict(x) for x in records]

        insertion_count = insertion_sort_count(
            insertion_records,
            "id"
        )

        sorted_records = [dict(x) for x in insertion_records]

        target = size // 2

        binary_result = binary_search_count(
            sorted_records,
            target,
            "id"
        )

        linear_result = linear_search_count(
            records,
            target,
            "id"
        )

        print(f"\nData size: {size}")
        print(f"Insertion sort comparisons: {insertion_count}")
        print(
            f"Binary search: index={binary_result['index']}, "
            f"comparisons={binary_result['comparison_count']}"
        )
        print(
            f"Linear search: index={linear_result['index']}, "
            f"comparisons={linear_result['comparison_count']}"
        )


if __name__ == "__main__":
    run_benchmark()