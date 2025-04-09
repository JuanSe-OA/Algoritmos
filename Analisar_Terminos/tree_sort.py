def tree_sort(frecuencias):
    """Implementación de Tree Sort con árbol binario"""
    items = list(frecuencias.items())
    
    class Node:
        def __init__(self, key):
            self.left = None
            self.right = None
            self.key = key
    
    def insert(root, key):
        if root is None:
            return Node(key)
        if (-key[1], key[0]) < (-root.key[1], root.key[0]):
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
        return root
    
    def inorder_traversal(root, result):
        if root:
            inorder_traversal(root.left, result)
            result.append(root.key)
            inorder_traversal(root.right, result)
    
    if not items:
        return {}
    
    root = None
    for item in items:
        root = insert(root, item)
    
    sorted_items = []
    inorder_traversal(root, sorted_items)
    return dict(sorted_items)