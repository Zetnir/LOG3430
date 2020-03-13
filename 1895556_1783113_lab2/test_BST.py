import unittest
import unittest.mock
import os
from BST import BST
from BST import Stack
from BST import node
from unittest.mock import MagicMock, Mock
# Voir les assertions possibles ici
# https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
class TestBST(unittest.TestCase):
    def setUp(self):
        self.bst = BST()

    #Question 2 :

    def test_when_value_for_deleted_node_is_None_should_return_None(self):
        self.assertIsNone(self.bst.delete_node(None))

    def test_when_value_for_deleted_node_is_Node_but_value_is_not_in_tree_should_return_None(self):
        self.value = 20
        self.node = node(self.value)
        self.assertIsNone(self.bst.delete_node(self.node))

    def test_when_value_for_deleted_node_is_Node_in_tree_with_no_parent_and_no_child_should_set_root_to_None(self):
        self.value = 20
        self.bst.insert(self.value)
        self.bst.delete_node(self.bst.root)
        self.assertIsNone(self.bst.root)

    def test_when_value_for_deleted_node_is_Node_in_tree_with_no_parent_and_right_child_should_set_root_to_right_child(self):
        self.value = 20
        self.right_value = 25
        self.bst.insert(self.value)
        self.bst.insert(self.right_value)
        self.bst.delete_node(self.bst.root)
        self.assertEqual(self.bst.root.value, self.right_value)

    def test_when_value_for_deleted_node_is_Node_in_tree_with_no_parent_and_left_child_should_set_root_to_left_child(self):
        self.value = 20
        self.left_value = 15
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.bst.delete_node(self.bst.root)
        self.assertEqual(self.bst.root.value, self.left_value)

    def test_when_value_for_deleted_node_is_Node_in_tree_with_no_parent_and_two_child_should_set_root_to_min_right_child_node_and_call_delete_node_using_said_node(self):
        self.value = 20
        self.left_value = 15
        self.right_value = 25
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.bst.insert(self.right_value)
        self.bst.delete_node(self.bst.root)
        self.assertIsNone(self.bst.root.right)
        self.assertEqual(self.bst.root.value, self.right_value)

    def test_when_value_for_deleted_node_is_left_child_of_its_parent_and_has_no_child_should_set_parents_left_child_to_None(self):
        self.parent_value = 30
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.bst.insert(self.value)
        self.parent_node.left = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.left)
        self.assertIsNone(self.bst.root.parent.left)

    def test_when_value_for_deleted_node_is_left_child_of_its_parent_and_has_right_child_should_set_parents_left_child_to_right_child(self):
        self.parent_value = 30
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.right_value = 25
        self.bst.insert(self.value)
        self.bst.insert(self.right_value)
        self.parent_node.left = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.left)
        self.assertEqual(self.bst.root.parent.left.value, self.right_value)

    def test_when_value_for_deleted_node_is_left_child_of_its_parent_and_has_left_child_should_set_parents_left_child_to_left_child(self):
        self.parent_value = 30
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.left_value = 15
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.parent_node.left = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.left)
        self.assertEqual(self.bst.root.parent.left.value, self.left_value)

    def test_when_value_for_deleted_node_is_left_child_of_its_parent_and_has_two_child_should_set_node_to_min_right_child_node_and_call_delete_node_using_said_node(self):
        self.parent_value = 30
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.left_value = 15
        self.right_value = 25
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.bst.insert(self.right_value)
        self.parent_node.left = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.left)
        self.assertEqual(self.bst.root.parent.left.value, self.right_value)
        self.assertIsNone(self.bst.root.right)

    def test_when_value_for_deleted_node_is_right_child_of_its_parent_and_has_no_child_should_set_parents_right_child_to_None(self):
        self.parent_value = 10
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.bst.insert(self.value)
        self.parent_node.right = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.right)
        self.assertIsNone(self.bst.root.parent.right)

    def test_when_value_for_deleted_node_is_right_child_of_its_parent_and_has_right_child_should_set_parents_right_child_to_right_child(self):
        self.parent_value = 10
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.right_value = 25
        self.bst.insert(self.value)
        self.bst.insert(self.right_value)
        self.parent_node.right = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.right)
        self.assertEqual(self.bst.root.parent.right.value, self.right_value)

    def  test_when_value_for_deleted_node_is_right_child_of_its_parent_and_has_left_child_should_set_parents_right_child_to_left_child(self):
        self.parent_value = 10
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.left_value = 15
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.parent_node.right = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.right)
        self.assertEqual(self.bst.root.parent.right.value, self.left_value)

    def test_when_value_for_deleted_node_is_right_child_of_its_parent_and_has_two_child_should_set_node_to_min_right_child_node_and_call_delete_node_using_said_node(self):
        self.parent_value = 10
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.left_value = 15
        self.right_value = 25
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.bst.insert(self.right_value)
        self.parent_node.right = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.right)
        self.assertEqual(self.bst.root.parent.right.value, self.right_value)
        self.assertIsNone(self.bst.root.right)

    #Question 3
    def test_PathA(self):
        self.parent_value = 30
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.bst.insert(self.value)
        self.parent_node.left = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.left)
        self.assertIsNone(self.bst.root.parent.left)

    def test_PathB(self):
        self.parent_value = 30
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.left_value = 15
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.parent_node.left = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.left)
        self.assertEqual(self.bst.root.parent.left.value, self.left_value)

    def test_PathC(self):
        self.parent_value = 10
        self.parent_node = node(self.parent_value)
        self.value = 20
        self.left_value = 15
        self.right_value = 25
        self.bst.insert(self.value)
        self.bst.insert(self.left_value)
        self.bst.insert(self.right_value)
        self.parent_node.right = self.bst.root
        self.bst.root.parent = self.parent_node
        self.bst.delete_node(self.bst.root.parent.right)
        self.assertEqual(self.bst.root.parent.right.value, self.right_value)
        self.assertIsNone(self.bst.root.right)

if __name__ == '__main__':
    unittest.main()




