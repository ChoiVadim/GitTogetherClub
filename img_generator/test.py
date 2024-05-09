"""
20 3
6 78 61 90 87 72 50 84 98 15 24 5 100 80 24 59 28 79 6 96
"""


def main():
    n = 20
    k = 3
    arr = [6, 78, 61, 90, 87, 72, 50, 84, 98, 15, 24, 5, 100, 80, 24, 59, 28, 79, 6, 96]
    sorted_arr = sorted(arr, reverse=True)
    arr_len = len(arr)

    print(f"{arr_len=}")
    print(f"{sorted_arr=}")

    # 20 // 3 = 6

    divided_arr = []

    for i in range(k):
        start = i * arr_len // k  # 1 * 20 // 3 = 6
        end = (i + 1) * arr_len // k  # (2 * 20) // 3 = 13

        if i == k - 1:
            end = arr_len

        divided_arr.append(sorted_arr[start:end])

    print(f"{divided_arr=}")

    max_sum = 0

    for i in range(0, k - 1):
        min_score = min(divided_arr[i])
        max_score = max(divided_arr[i + 1])
        sum_diff = max_score - min_score
        max_sum = max(max_sum, sum_diff)

    print(f"Maximum sum of differences: {max_sum}")


if __name__ == "__name__":
    main()
