# ---------------------------------------
# Lab2 Log 3430 winter 2020
# The purpose of this piece of code is to help you unit test some methods as required in Lab 2 assignment
# Binary Search Tree
# Noureddine Kerzazi
# ---------------------------------------

# The class Stack is used only to count the amount of node. used within the size method
class Stack(object):
    def __init__(self):
        self.items = []

    def __len__(self):
        return self.size()

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        s = ""
        for i in range(len(self.items)):
            s += str(self.items[i].value) + "-"
        return s


class node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = node(value)
        else:
            self._insert(value, self.root)

    # Insert a new node. This function is recursive
    def _insert(self, value, cur_node):
        if value < cur_node.value:
            if cur_node.left is None:
                cur_node.left = node(value)
                cur_node.left.parent = cur_node  # point out the parent
            else:
                self._insert(value, cur_node.left)
        elif value > cur_node.value:
            if cur_node.right is None:
                cur_node.right = node(value)
                cur_node.right.parent = cur_node  # point out the parent
            else:
                self._insert(value, cur_node.right)
        else:
            print("This Value is already in the tree!!!")

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, cur_node):
        if cur_node is not None:
            self._print_tree(cur_node.left)
            print(str(cur_node.value))
            self._print_tree(cur_node.right)

    def height(self):
        if self.root is not None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, cur_node, cur_height):
        if cur_node is None:
            return cur_height
        left_height = self._height(cur_node.left, cur_height + 1)
        right_height = self._height(cur_node.right, cur_height + 1)
        return max(left_height, right_height)

        # recursive version to calculate the size of the Tree

    def size_(self):
        if node is None:
            return 0
        return 1 + self.size_(node.left) + self.size_(node.right)

    # iterative version to calculate the size of the Tree
    def size(self):
        if self.root is None:
            return 0

        stack = Stack()
        stack.push(self.root)
        size = 1
        while stack:
            node = stack.pop()
            if node.left:
                size += 1
                stack.push(node.left)
            if node.right:
                size += 1
                stack.push(node.right)
        return size

    def is_bst_satisfied(self):
        if self.root:
            is_satisfied = self._is_bst_satisfied(self.root, self.root.value)

            if is_satisfied is None:
                return True
            return False

        return True

    def _is_bst_satisfied(self, cur_node, value):
        if cur_node.left:
            if value > cur_node.left.value:
                return self._is_bst_satisfied(cur_node.left, cur_node.left.value)
            else:
                return False
            if cur_node.right:
                if data < cur_node.right.value:
                    return self._is_bst_satisfied(cur_node.right, cur_node.right.value)
                else:
                    return False

    # This function returns the node given a value
    def find(self, value):
        if self.root is not None:
            return self._find(value, self.root)
        else:
            return None

    def _find(self, value, cur_node):
        if value == cur_node.value:
            return cur_node
        elif value < cur_node.value and cur_node.left is not None:
            return self._find(value, cur_node.left)  # recursive progression direction left
        elif value > cur_node.value and cur_node.right is not None:
            return self._find(value, cur_node.right)  # recursive progression direction right

    # delete a node passing a value
    def delete_value(self, value):
        return self.delete_node(self.find(value))

    # delete a node passing a node
    def delete_node(self, node):

        if node == None or self.search(node.value) == None:
            print("Node to be deleted not found in the tree!")
            return None

        # This sub function returns the node with min value in tree rooted at input node
        def min_value_node(n):
            current = n
            while current.left is not None:
                current = current.left  # the min is always left according to the BST property
            return current

        # This sub function returns the number of children for the specified node
        def how_many_children(n):
            nb_children = 0
            if n.left is not None:
                nb_children += 1
            if n.right is not None:
                nb_children += 1
            return nb_children

        # The parent of the node we want to delete
        node_parent = node.parent

        # Get the number of children of the node to be deleted
        node_children = how_many_children(node)

        # 3 cases occur when deleting a node
        # CASE 1 (node has no children)
        if node_children == 0:
            if node_parent is not None:
                # remove the ref to the parent node
                if node_parent.left == node:
                    node_parent.left = None
                else:
                    node_parent.right = None
            else:
                self.root = None  # deleted the root node means deleting the entire tree.

        # CASE 2 (node has a single child)
        if node_children == 1:
            # get the single child node in a temporary variable
            if node.left is not None:
                tmp_child = node.left
            else:
                tmp_child = node.right
            if node_parent is not None:
                # replace the node to be deleted with its child
                if node_parent.left == node:
                    node_parent.left = tmp_child
                else:
                    node_parent.right = tmp_child
            else:
                self.root = tmp_child

            tmp_child.parent = node_parent

        # CASE 3 (node has two children)
        if node_children == 2:
            # find the min value at the right
            successor = min_value_node(node.right)
            node.value = successor.value
            self.delete_node(successor)

    def search(self, value):
        if self.root is not None:
            return self._search(value, self.root)
        else:
            return False

    def _search(self, value, cur_node):
        if value == cur_node.value:
            return True
        elif value < cur_node.value and cur_node.left is not None:
            return self._search(value, cur_node.left)
        elif value > cur_node.value and cur_node.right is not None:
            return self._search(value, cur_node.right)
        return False

    def reversetree(self):
        print("    7     ")
        print("  /   \     ")
        print(" 6      8     ")
        print("         \     ")
        print("          12     ")
        print("        /    \  ")
        print("      11      18")
        print("---------inverted tree-----------")
        print("        7     ")
        print("      /   \     ")
        print("     8      6     ")
        print("    /")
        print("   12 ")
        print("  /  \          ")
        print("18    11     ")

        if self.root is not None:
            return self._reversetree(self.root)
        else:
            return None

    def _reversetree(self, cur_node):
        if cur_node is None:
            return None
        else:
            cur_node.left, cur_node.right = cur_node.right, cur_node.left
            self._reversetree(cur_node.left)
            self._reversetree(cur_node.right)
            return cur_node

    # @classmethod
    # def build_tree(cls, tree, num_elements, maximum_int):
    #     from random import randint
    #     for _ in range(num_elements):
    #         cur_elem = randint(0, maximum_int)
    #         tree.insert(cur_elem)
    #     return tree

    # -------------------------
    # def main():
    #     tree = BST()
    #     BST.build_tree(tree, 100, 1000)

    # if __name__ == '__main__':
    #     main()


# ---------------------------------------------
# ---The main to test methods------------------
# Build randomly a tree of 100 nodes
# Duplicate values are invalid

def build_tree(tree, num_elements=100, maximum_int=1000):
    from random import randint
    for _ in range(num_elements):
        cur_elem = randint(0, maximum_int)
        tree.insert(cur_elem)
    return tree


def build_nonBTS_tree(tree):
    print("Invoke building a non BTS Tree")
    tree.root = node(1)
    tree.root.left = node(3)
    tree.root.right = node(2)
    print(tree.is_bst_satisfied())


# # pour tester le code
# tree = BST()
# tree1 = build_tree(tree)

# # BST.print_tree(build_nonBTS_tree(tree))
# # tree1.print_tree()

# print("**************")
# print("The height of the Tree1 is :" + str(tree1.height()))
# print("The size of the Tree1 is   :" + str(tree1.size()))

# print("***%%%%%%%%%%%%% test search a node Build a non Random small tree*")
# tree2 = BST()
# tree2.insert(7)
# tree2.insert(6)
# tree2.insert(8)
# tree2.insert(12)
# tree2.insert(11)
# tree2.insert(18)

# tree2.print_tree()

# print("**************")
# print("The height of the Tree2 is :" + str(tree2.height()))
# print("The size of the Tree2 is   :" + str(tree2.size()))

# print("Does tree2  satisfy the BST property ? ", tree2.is_bst_satisfied())

# print("***%%%%%%%%%%%%% deleting a node  *")
# print("--deleting the root")
# tree2.delete_value(7)
# # tree2.delete_value(6) #uncomment to test other cases
# # tree2.delete_value(18) #uncomment to test other cases
# # tree2.delete_value(8) #uncomment to test other cases
# # tree2.delete_value(12) #uncomment to test other cases
# tree2.print_tree()

# print("the result of the first search 11  is: ", tree2.search(11))
# print("the result of the second search 37 is: ", tree2.search(37))

# print("---------------Reverse the Tree")
# tree2.reversetree()
# tree2.print_tree()
