def is_isomorphic(s, t):
    """
    :type s: str
    :type t: str

    :rtype: bool
    """

    letter_dict = {}
    ind = 0
    test = str()
    for i in s:
        if i not in letter_dict.keys() and t[ind] not in letter_dict.values():
            letter_dict[i] = t[ind]
        if i in letter_dict.keys() and t[ind] == letter_dict[i]:
            test = test + (t[ind])
        ind = ind + 1

    if test == t:
        return True
    else:
        return False


# https://leetcode.com/problems/reverse-linked-list/
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def reverseList(head):
    """
    :type head: ListNode
    :rtype: ListNode
    """
    if head is None:
        return None
    current_node = head
    next_node = head.next
    head.next = None
    while next_node is not None:
        next_next = next_node.next
        next_node.next = current_node
        current_node = next_node
        next_node = next_next
    return current_node


# Given an array of integers, find if the array contains any duplicates.
# Your function should return true if any value appears at least twice
# in the array, and it should return false if every element is distinct.
def containsDuplicate(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    nums_dict = {}
    for i in nums:
        if i in nums_dict:
            nums_dict[i] = nums_dict[i] + 1
            return True
        else:
            nums_dict[i] = 1
    return False


# Write an algorithm to determine if a number is "happy".
# A happy number is a number defined by the following process:
# Starting with any positive integer, replace the number by the
# sum of the squares of its digits, and repeat the process until
# the number equals 1 (where it will stay), or it loops endlessly
# in a cycle which does not include 1. Those numbers for which
# this process ends in 1 are happy numbers.
# Input: 19
# Output: true
# Explanation:
# 12 + 92 = 82
# 82 + 22 = 68
# 62 + 82 = 100
# 12 + 02 + 02 = 1

def isHappy(n):
    """
    :type n: int
    :rtype: bool
    """
    strn = str(n)
    temp = 0
    while True:
        temp = 0
        for i in strn:
            temp = temp + int(i) ** 2
            print(temp)
        if int(temp) == 1:
            return True
        if int(temp) != 1 and len(str(temp)) == 1:
            return False
        strn = str(temp)


def romanToInt(s: str) -> int:
    roman_int = {'I': 1,
                 'V': 5,
                 'X': 10,
                 'L': 50,
                 'C': 100,
                 'D': 500,
                 'M': 1000
                 }
    decimal = 0
    for i in range(len(s)):
        if i + 1 < len(s):
            if roman_int[s[i]] < roman_int[s[i + 1]]:
                decimal = decimal - roman_int[s[i]]
            else:
                decimal = decimal + roman_int[s[i]]
        else:
            decimal = decimal + roman_int[s[i]]
    return decimal


def numIslands(grid) -> int:
    count, island = 0, 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != grid[i][j + 1]:
                count += 1
            if grid[i][j] != grid[i][j - 1]:
                count += 1
            if grid[i][j] != grid[i + 1][j]:
                count += 1
            if grid[i][j] != grid[i - 1][j]:
                count += 1
            if count == 4:
                island += 1
    return island


def main():
    # s = 'apple'
    # t = 'ellpa'
    # print(is_isomorphic(s, t))
    # node5 = ListNode(5)
    # node4 = ListNode(4)
    # node3 = ListNode(3)
    # node2 = ListNode(2)
    # node1 = ListNode(1)
    # node1.next = node2
    # node2.next = node3
    # node3.next = node4
    # node4.next = node5

    # newnode = reverseList(node1)
    # newnode = node1
    # print(newnode.val)
    # while newnode.next is not None:
    #     print(newnode.next.val)
    #     newnode = newnode.next
    #
    # print(isHappy(1111111))
    print(romanToInt("MCMXC"))
    # print(romanToInt("IV"))
    grid = [["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"]]
    print(grid[0][0])
    print(numIslands(grid))


if __name__ == "__main__":
    main()
