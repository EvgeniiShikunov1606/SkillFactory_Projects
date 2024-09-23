class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def in_order_traversal(self):
        result = []
        self._in_order_traversal_recursive(self.root, result)
        return result

    def _in_order_traversal_recursive(self, node, result):
        if node:
            self._in_order_traversal_recursive(node.left, result)
            result.append(node.value)
            self._in_order_traversal_recursive(node.right, result)

    def pre_order_traversal(self):
        result = []
        self._pre_order_traversal_recursive(self.root, result)
        return result

    def _pre_order_traversal_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._pre_order_traversal_recursive(node.left, result)
            self._pre_order_traversal_recursive(node.right, result)

    def post_order_traversal(self):
        result = []
        self._post_order_traversal_recursive(self.root, result)
        return result

    def _post_order_traversal_recursive(self, node, result):
        if node:
            self._post_order_traversal_recursive(node.left, result)
            self._post_order_traversal_recursive(node.right, result)
            result.append(node.value)

    def find(self, value):
        return self._find_recursive(self.root, value)

    def _find_recursive(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._find_recursive(node.left, value)
        else:
            return self._find_recursive(node.right, value)

    def height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return 0
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return max(left_height, right_height) + 1


tree = BinaryTree()

elements = [50, 30, 70, 20, 40, 60, 80]
for el in elements:
    tree.insert(el)

print(f"In-order: {tree.in_order_traversal()}")
print(f"Pre-order: {tree.pre_order_traversal()}")
print(f"Post-order: {tree.post_order_traversal()}")

search_values = [20, 30, 90]
results = {val: tree.find(val) for val in search_values}
print(f"Поиск результатов: {results}")

print(f"Высота дерева: {tree.height()}")
