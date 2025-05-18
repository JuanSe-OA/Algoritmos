from ..utils import obtener_anio_valido

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class TreeSort:
    def insert(self, root, key):
        if root is None:
            return Node(key)

        current = root
        while True:
            if (obtener_anio_valido(key), key['author']) < (obtener_anio_valido(current.val), current.val['author']):
                if current.left is None:
                    current.left = Node(key)
                    break
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = Node(key)
                    break
                else:
                    current = current.right
        return root

    def inorder_traversal(self, root, sorted_list):
        stack = []
        current = root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            sorted_list.append(current.val)
            current = current.right

    def ordenar(self, arr):
        if not arr:
            return arr
        root = None
        for item in arr:
            root = self.insert(root, item)
        sorted_list = []
        self.inorder_traversal(root, sorted_list)
        return sorted_list
