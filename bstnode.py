"""
File: bstnode.py
Author: Ken Lambert
"""

class BSTNode(object):
    """Represents a node for a linked binary search tree."""

    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right

    # def is_leaf(self):
    #     return list(self.children()) == []
    #
    # def children(self):
    #     return filter(None, [self.left, self.right])
