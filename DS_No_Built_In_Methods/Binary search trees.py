import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None    # pointer to root of left subtree
        self.right = None   # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """Binary Search Tree class"""

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """Add value to the tree."""

        # bst module talks about the "key" and "value", students might bring it up
        # the key is used for comparison purposes only
        # for us, the key is the value contained in any given node

        parent = None
        node = self._root
        while node is not None:
            parent = node
            if value < node.value:
                node = node.left
            else:  # duplicates allowed in BST; are placed in right subtree
                node = node.right

            # duplicates not allowed in AVL

        if parent is None:
            self._root = BSTNode(value)
        elif value < parent.value:
            parent.left = BSTNode(value)
        else:
            parent.right = BSTNode(value)

        # in AVL, want to return the "newly inserted node"
        # and have to update parent references

    def remove(self, value: object) -> bool:
        """
        Attempt to remove given node from Tree.
        Return True if successful, False if not.
        """

        # since BST can have duplicates, students may find a node with
        # the matching value, but it won't be the very first occurrence
        # of that value, and so they'll fail the Gradescope test
        remove_node, remove_parent = self._get_first_node_and_parent(value)

        # if node with value wasn't found
        if not remove_node:
            return False

        # remove-node has been found, now for the fun part
        # it has none, one or two subtrees

        if not remove_node.left and not remove_node.right:
            self._remove_no_subtrees(remove_parent, remove_node)

        elif not remove_node.left or not remove_node.right:
            self._remove_one_subtree(remove_parent, remove_node)

        else:
            self._remove_two_subtrees(remove_parent, remove_node)

        return True

    def _get_first_node_and_parent(self, value: object) -> (BSTNode, BSTNode):
        """Find first matching value in BST and return the node and its parent."""

        # If not found, node will be None when returned and
        # this can be checked against later.
        node, parent = self._root, None

        while node is not None:

            if value < node.value:
                parent = node
                node = node.left
            elif value > node.value:
                parent = node
                node = node.right
            else:
                return node, parent

        return node, parent

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """Remove node that has no subtrees."""

        # replace leaf with None
        self._replace_node(remove_parent, remove_node)

    def _replace_node(self, parent: BSTNode, child: BSTNode, replacement: BSTNode = None) -> None:
        """
        Determine if child is parent's left or right,
        and replace with the given node.
        """
        if parent:
            if parent.left is child:
                parent.left = replacement
            else:
                parent.right = replacement

        # if no parent, in bst or avl, then we're dealing with the root
        else:
            self._root = replacement

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """Remove node that has one subtree."""

        # update pn to point to n’s child instead of n #

        # if deleting root
        if not remove_parent:

            # replace with remove node's subtree
            if remove_node.left:
                self._root = self._root.left
            else:
                self._root = self._root.right

        # Figure out if remove_node is the left or right child of remove_parent.
        # remove_parent then points past remove_node to one of remove_node's subtrees,
        # which removes the node.
        elif remove_parent.left is remove_node:
            self._replace_parent_left_child(remove_parent, remove_node)
        else:
            self._replace_parent_right_child(remove_parent, remove_node)

    @staticmethod
    def _replace_parent_left_child(remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Replace remove_parent's left child with either
        the remove node's left or right subtree, whichever isn't None.
        """
        if remove_node.left:
            remove_parent.left = remove_node.left
        else:
            remove_parent.left = remove_node.right

    @staticmethod
    def _replace_parent_right_child(remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Replace remove_parent's right child with either
        the remove node's left or right subtree, whichever isn't None.
        """
        if remove_node.left:
            remove_parent.right = remove_node.left
        else:
            remove_parent.right = remove_node.right

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """Remove node that has two subtrees."""

        # bst pseudocode are the comments to the right of the code #

        successor, inorder_parent = self._get_successor_and_parent(remove_node)

        # attach remove-node's subtree to successor
        successor.left = remove_node.left                  # s.left ← n.left

        if successor is not remove_node.right:             # if s is not n.right:
            inorder_parent.left = successor.right          # ps.left ← s.right
            successor.right = remove_node.right            # s.right ← n.right

        # pseudocode: update pn to point to s instead of n
        # update parent to point to successor instead of removal-node
        self._replace_node(remove_parent, remove_node, successor)

    @staticmethod
    def _get_successor_and_parent(parent: BSTNode) -> (BSTNode, BSTNode):
        """Return inorder successor and its parent."""

        successor = parent.right
        while successor.left:
            parent = successor
            successor = successor.left

        return successor, parent

    def contains(self, value: object) -> bool:
        """Return True if value is in tree, False if not."""

        node = self._root
        while node:
            if node.value == value:
                return True
            node = node.left if value < node.value else node.right
        return False

    # def contains(self, value: object) -> bool:
    #     """
    #     Returns TRUE / FALSE if value is in the tree
    #     """
    #     """ RECURSIVE IMPLEMENTATION WITH HELPER METHOD """
    #     return self._contains_helper(self._root, value)
    #
    # def _contains_helper(self, cur_node, value):
    #     """ Helper method for the recursive contains() """
    #     # base case - reached end of subtree, no value found
    #     if not cur_node:
    #         return False
    #     # base case - current node == value -> return true
    #     if cur_node.value == value:
    #         return True
    #
    #     # recursively search in the left subtree
    #     if self._contains_helper(cur_node.left, value):
    #         return True
    #     # if not found in left -> recursively search in the right subtree
    #     return self._contains_helper(cur_node.right, value)

    def inorder_traversal(self) -> Queue:
        """
        Perform inorder traversal of the tree and return queue of visited nodes.
        """
        visited, s = Queue(), Stack()

        node = self._root
        while node or not s.is_empty():
            if node:
                s.push(node)
                node = node.left
            else:
                node = s.pop()
                visited.enqueue(node.value)
                node = node.right
        return visited

    # def inorder_traversal(self, cur_node=None, visited=None) -> Queue:
    #     """
    #     Perform inorder traversal of the tree and return queue of visited nodes
    #     """
    #     """ RECURSIVE IMPLEMENTATION WITH NO HELPER METHODS """
    #     if not visited:
    #         # first call to function -> create queue to store visited nodes
    #         # and initiate recursive calls starting with the root node
    #         return self.inorder_traversal(self._root, Queue())
    #
    #     # base case - reached the end of current subtree -> backtrack
    #     if not cur_node:
    #         return visited
    #
    #     # recursive case -> sequence of steps for in-order traversal:
    #     # visit left subtree, store current node value, visit right subtree
    #     self.inorder_traversal(cur_node.left, visited)
    #     visited.enqueue(cur_node.value)
    #     self.inorder_traversal(cur_node.right, visited)
    #     return visited

    def find_min(self) -> object:
        """Find and return smallest value in a subtree."""

        if not self._root:
            return

        node = self._root
        while node.left:
            node = node.left

        return node.value

    # def find_min(self) -> object:
    #    """ Finds smallest item in a subtree. """
    #    """ RECURSIVE IMPLEMENTATION """
    #
    #    if not self._root:
    #        return
    #
    #    return self._find_min(self._root)
    #
    # def _find_min(self, node: TreeNode) -> object:
    #    """ Private, recursive version of public method.  """
    #    if not node.left:
    #        return node
    #
    #    return self._find_min(node.left)

    def find_max(self) -> object:
        """Find and return largest value in a subtree."""

        if not self._root:
            return

        node = self._root
        while node.right:
            node = node.right

        return node.value

    # def find_max(self) -> object:
    #    """ Finds largest item in a subtree. """
    #    """ RECURSIVE IMPLEMENTATION """
    #
    #    if not self._root:
    #        return
    #
    #    return self._find_max(self._root)
    #
    # def _find_max(self, node: TreeNode) -> object:
    #    """ Private, recursive version of public method."""
    #
    #    if not node.right:
    #        return node
    #
    #    return self._find_max(node.right)

    def is_empty(self) -> bool:
        """Return True if tree is empty, False if not."""
        return not self._root

    def make_empty(self) -> None:
        """Make the tree empty."""
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
