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
    seen = {}
    while True:
        if temp in seen:
            seen[temp] += 1
            if int(temp) == 1:
                return True
            if seen[temp] > 1:
                return False
        else:
            seen[temp] = 1
        temp = 0

        for i in strn:
            temp = temp + int(i) ** 2
        print(temp)

        strn = str(temp)

    return False

# Given a linked list, determine if it has a cycle in it.
#
# To represent a cycle in the given linked list, we use an
# integer pos which represents the position (0-indexed) in
# the linked list where tail connects to. If pos is -1,
# then there is no cycle in the
# linked list.
#
# Example 1:
#
# Input: head = [3,2,0,-4], pos = 1
# Output: true
# Explanation: There is a cycle in the linked list, where tail connects to the second node.
# Example 2:
#
# Input: head = [1,2], pos = 0
# Output: true
# Explanation: There is a cycle in the linked list, where tail connects to the first node
# Example 3:
#
# Input: head = [1], pos = -1
# Output: false
# Explanation: There is no cycle in the linked list.

def hasCycle(head):
    """
    :type head: ListNode
    :rtype: bool
    """

def main():
    s = 'apple'
    t = 'ellpa'
    print(is_isomorphic(s, t))
    node5 = ListNode(5)
    node4 = ListNode(4)
    node3 = ListNode(3)
    node2 = ListNode(2)
    node1 = ListNode(1)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5

    newnode = reverseList(node1)
    # newnode = node1
    print(newnode.val)
    while newnode.next is not None:
        print(newnode.next.val)
        newnode = newnode.next

    print(isHappy(1111111))

if __name__ == "__main__":
    main()
