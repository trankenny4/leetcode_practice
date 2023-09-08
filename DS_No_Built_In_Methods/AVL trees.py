import random
from queue_and_stack import Queue, Stack
from bst_solution import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ---------------------------------------------------------------------- #

    def add(self, value: object) -> None:
        """Add value to the tree."""

        newly_inserted_node = self._add(value)
        parent = newly_inserted_node.parent

        while parent is not None:
            self._rebalance(parent)
            parent = parent.parent

    def _add(self, value: object) -> AVLNode:
        """Add node to tree and return for balancing purposes."""

        # bst module talks about the "key" and "value", students might bring it up
        # the key is used for comparison purposes only
        # for us, the key is the value contained in any given node

        parent = None
        node = self._root
        while node is not None:
            parent = node
            if value < node.value:
                node = node.left
            elif value > node.value:  # duplicates allowed in BST; are placed in right subtree
                node = node.right
            else:
                # duplicates not allowed in AVL
                return node

        # difference between bst and this version:
        #   need to set parent pointer and return the newly inserted node
        newly_inserted_node = AVLNode(value)

        if parent is None:
            self._root = newly_inserted_node
        elif value < parent.value:
            parent.left = newly_inserted_node
        else:
            parent.right = newly_inserted_node

        newly_inserted_node.parent = parent
        return newly_inserted_node

    def remove(self, value: object) -> bool:
        """
        Attempt to remove given node from Tree.
        Return True if successful, False if not.
        """
        node, parent = self._get_first_node_and_parent(value)

        # if node with value wasn't found
        if not node:
            return False

        # node has been found, now for the fun part
        # remove node has none, one or two subtrees

        if not node.left and not node.right:
            self._remove_no_subtrees(parent, node)  # use bst implementation

        elif not node.left or not node.right:
            self._remove_one_subtree(parent, node)  # use bst implementation

        else:
            # need to update parent pointers and return lowest-modified node
            # during the following removal, so have to override bst method
            parent = self._remove_two_subtrees(parent, node)

        while parent is not None:
            self._rebalance(parent)
            parent = parent.parent

        return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """Remove given node that has two subtrees and return lowest-modified node."""

        successor, inorder_parent = self._get_successor_and_parent(remove_node)

        # First put everything below remove-node in proper place,
        self._update_children(remove_node, successor, inorder_parent)

        # and then attach successor to tree.
        # The remove node's parent can simply point to fully-set-up successor.
        self._replace_node(remove_parent, remove_node, successor)

        # successor needs its parent updated to point to the removal-node parent
        successor.parent = remove_parent

        # return the lowest-modified node
        if successor is remove_node.right:
            return successor

        return inorder_parent

    @staticmethod
    def _update_children(
            remove_node: AVLNode, successor: AVLNode, inorder_parent: AVLNode) -> None:
        """
        Update inorder successor and inorder successor's parent.
        Update new children's .parent property to point to their new parents.
        """

        # bst pseudocode are the comments to the right of the code      #
        # avl thought process: update child pointer,                    #
        #                      then update that child's parent pointer  #

        # successor should never have a left,
        # so attach remove-node's left unconditionally
        successor.left = remove_node.left               # s.left ← n.left
        successor.left.parent = successor

        if successor is not remove_node.right:          # if s is not n.right:

            # assign whether or not successor has a right subtree
            inorder_parent.left = successor.right       # ps.left ← s.right

            # if it had one, make it point to the inorder parent
            if inorder_parent.left:
                inorder_parent.left.parent = inorder_parent

            successor.right = remove_node.right         # s.right ← n.right
            successor.right.parent = successor

    # Balance methods - They're discussed in this order in the modules #

    # module version: right - left
    def _balance_factor(self, parent: AVLNode) -> int:
        """Return the balance factor of the given node."""
        left = self._get_height(parent.left) if parent else -1
        right = self._get_height(parent.right) if parent else -1
        return right - left

    # everywhere else in world version: left - right
    '''
    def _balance_factor(self, parent: AVLNode) -> int:
        """Return the balance factor of the given node"""
        left = self._get_height(parent.left) if parent else -1
        right = self._get_height(parent.right) if parent else -1
        return left - right
    '''

    @staticmethod
    def _get_height(node: AVLNode) -> int:
        """Return height of given node."""

        # Some students want to return 0 if the node is None
        # As stated in the module, they should return -1 if it's None
        return node.height if node else -1

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """Rotate left around the given node."""
        child = node.right
        node.right = child.left

        if node.right:
            node.right.parent = node

        child.left = node
        node.parent = child

        self._update_height(node)
        self._update_height(child)

        # if debugging, at this point it will look like everything except
        # the root of the tree has vanished. Not the case! Keep going!
        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """Rotate right around the given node."""
        child = node.left
        node.left = child.right

        if node.left:
            node.left.parent = node

        child.right = node
        node.parent = child

        self._update_height(node)
        self._update_height(child)

        # if debugging, at this point it will look like everything except
        # the root of the tree has vanished. Not the case! Keep going!
        return child

    def _update_height(self, node: AVLNode) -> None:
        """Update height of node by comparing left and right subtrees."""

        # add 1 to account for the node itself
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """Balance subtree at given root."""

        # adapted from module's pseudocode
        # module uses right_child_height - left_child_height

        if self._balance_factor(node) < -1:

            # if True, this will be a LR rotation
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node

            # if above was False, this is a LL

            # actual implementation (not included in pseudocode)
            # needs to save parent - can do here or in the rotate method
            previous_parent = node.parent
            new_root = self._rotate_right(node)  # newSubTreeRoot ← rotateRight(n)
            new_root.parent = previous_parent    # newSubtreeRoot.parent ← n.parent

            # n.parent.left or n.parent.right ← newSubtreeRoot
            self._replace_node(previous_parent, node, new_root)

        elif self._balance_factor(node) > 1:

            # if True, this will be a RL rotation
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node

            # if above was False, this is a RR

            previous_parent = node.parent
            new_root = self._rotate_left(node)  # newSubtreeRoot ← rotateLeft(n)
            new_root.parent = previous_parent   # newSubtreeRoot.parent ← n.parent

            # n.parent.left or n.parent.right ← newSubtreeRoot
            self._replace_node(previous_parent, node, new_root)

        else:
            self._update_height(node)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
