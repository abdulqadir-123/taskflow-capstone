from algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} - expected {expected}, got {result}")


# 1. insertion_sort - empty list
records = []
result = insertion_sort(records, "id")
check(
    "insertion_sort empty list",
    records,
    []
)


# 2. insertion_sort - single element
records = [{"id": 1}]
insertion_sort(records, "id")
check(
    "insertion_sort single element",
    records,
    [{"id": 1}]
)


# 3. insertion_sort - normal list
records = [
    {"id": 3},
    {"id": 1},
    {"id": 2},
]
insertion_sort(records, "id")
check(
    "insertion_sort normal list",
    records,
    [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]
)


# 4. binary_search - first index
records = [
    {"id": 1},
    {"id": 2},
    {"id": 3},
    {"id": 4},
    {"id": 5},
]
check(
    "binary_search first index",
    binary_search(records, 1, "id"),
    0
)


# 5. binary_search - last index
check(
    "binary_search last index",
    binary_search(records, 5, "id"),
    4
)


# 6. binary_search - middle index
check(
    "binary_search middle index",
    binary_search(records, 3, "id"),
    2
)


# 7. binary_search - absent value
check(
    "binary_search absent value",
    binary_search(records, 99, "id"),
    -1
)


# 8. insertion_sort_count
records = [
    {"id": 3},
    {"id": 1},
    {"id": 2},
]

result = insertion_sort_count(records, "id")

if records == [
    {"id": 1},
    {"id": 2},
    {"id": 3},
] and type(result) is int and result > 0:
    print("PASS: insertion_sort_count")
else:
    print("FAIL: insertion_sort_count")


# 9. binary_search_count
records = [
    {"id": 1},
    {"id": 2},
    {"id": 3},
    {"id": 4},
    {"id": 5},
]

result = binary_search_count(records, 3, "id")

if (
    result["index"] == 2
    and type(result["comparison_count"]) is int
    and result["comparison_count"] > 0
):
    print("PASS: binary_search_count")
else:
    print("FAIL: binary_search_count")


# 10. linear_search_count - absent value
result = linear_search_count(records, 99, "id")

if (
    result["index"] == -1
    and result["comparison_count"] == len(records)
):
    print("PASS: linear_search_count absent")
else:
    print("FAIL: linear_search_count absent")


print("\nAlgorithm checks completed.")