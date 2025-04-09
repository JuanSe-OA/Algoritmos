from utils import obtener_anio_valido

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class TreeSort:
    def insert(self, root, key):
        if root is None:
            return Node(key)
        if (obtener_anio_valido(key), key['autor']) < (obtener_anio_valido(root.val), root.val['autor']):
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def inorder_traversal(self, root, sorted_list):
        if root:
            self.inorder_traversal(root.left, sorted_list)
            sorted_list.append(root.val)
            self.inorder_traversal(root.right, sorted_list)

    def ordenar(self, arr):
        if not arr:
            return arr
        root = None
        for item in arr:
            root = self.insert(root, item)
        sorted_list = []
        self.inorder_traversal(root, sorted_list)
        return sorted_list