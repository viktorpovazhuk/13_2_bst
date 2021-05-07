"""
File: linkedbst.py
Author: Ken Lambert
Linked Binary Search Tree
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            repres = ""
            if node != None:
                repres += recurse(node.right, level + 1)
                repres += "| " * level
                repres += str(node.data) + "\n"
                repres += recurse(node.left, level + 1)
            return repres

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            # if top is not None:
            #     print(top.data)
            if top.left is None and top.right is None:
                # print("None")
                return 0
            return 1 + max(height1(child)
                           for child in filter(None, [top.left, top.right]))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        vertex = len(self)
        return self.height() < 2 * log(vertex + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lyst = []

        def compare(top):
            if low <= top.data <= high:
                lyst.append(top.data)
            if LinkedBST.is_leaf(top):
                return

            if low < top.data < high:
                for child in LinkedBST.children(top):
                    compare(child)
            elif top.data <= low and top.right is not None:
                compare(top.right)
            elif top.data >= high and top.left is not None:
                compare(top.left)

        if self._root is not None:
            compare(self._root)
        return lyst

    @staticmethod
    def is_leaf(vertex):
        """Check if vertex is leaf"""
        return list(LinkedBST.children(vertex)) == []

    @staticmethod
    def children(vertex):
        """Return vertex children"""
        return filter(None, [vertex.left, vertex.right])

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        tree = [vertex for vertex in self.inorder()]

        def rebuild(subtree):
            if len(subtree) < 3:
                for vertex in subtree:
                    self.add(vertex)
                return

            pivot = len(subtree) // 2
            self.add(subtree[pivot])
            rebuild(subtree[:pivot])
            rebuild(subtree[pivot + 1:])

        self.clear()
        rebuild(tree)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                # print("!")
                return node.data
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                return None
            else:
                return recurse(node.right)
                # End of recurse

        # Tree is empty, so return None
        if self.isEmpty():
            return None
        # Otherwise, search for the item's spot
        else:
            return recurse(self._root)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        def recurse(previous, current):
            if current.data >= item:
                if not previous:
                    return None
                else:
                    return previous.data
            elif current.right is None:
                return current.data
            else:
                return recurse(current, current.right)

        if self.isEmpty():
            return None

        return recurse(None, self._root)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """


if __name__ == "__main__":
    # l = LinkedBST([1, 4, 2, 5])
    # print(l.height())
    # # print(l)
    # print(l.is_balanced())

    l2 = LinkedBST([1, 3, 2, 4, 5, 6])
    # print(l2)
    l2.rebalance()
    print(l2)
    print(l2.successor(5))
    print(l2.predecessor(6))
    print(l2.range_find(3, 5))

    l3 = LinkedBST([7])
    print(l3.predecessor(6))
