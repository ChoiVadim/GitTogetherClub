import time


def containsDuplicate(nums):
    # Time complexity: O(n)
    # Space complexity: O(n)
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def containsDuplicate_sort(nums):
    # Time complexity: O(nlogn)
    # Space complexity: O(1)
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False


def main():
    print(containsDuplicate([1, 2, 3, 1]))  # True
    print(containsDuplicate([1, 2, 3, 4]))  # False
    print(containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))  # True
    print(containsDuplicate_sort([1, 2, 3, 1]))  # True
    print(containsDuplicate_sort([1, 2, 3, 4]))  # False
    print(containsDuplicate_sort([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))  # True


if __name__ == "__main__":
    main()
