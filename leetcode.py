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
    print(head)
    if head.next is not None:
        print(head.next)
        return reverseList(head.next)

https://leetcode.com/problems/reverse-linked-list/

def main():
    s = 'apple'
    t = 'ellpa'
    print(is_isomorphic(s, t))
    ListNode()

    print(reverseList(lis))


if __name__ == "__main__":
    main()
