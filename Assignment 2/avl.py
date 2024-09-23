from node import Node

class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0


    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balancefactor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def revaluate_height(self, p):
        p.height = 1 + max(self.height(p.left), self.height(p.right))

    def is_balanced(self, p):
        return abs(self.balancefactor(p)) <= 1


    def rebalance(self, node):
        while node is not None:
            self.revaluate_height(node)
            balance = self.balancefactor(node)

            if balance > 1:
                if self.balancefactor(node.left) < 0:
                    self.rotateleft(node.left)
                self.rotateright(node)

            elif balance < -1:
                if self.balancefactor(node.right) > 0:
                    self.rotateright(node.right)
                self.rotateleft(node)

            node = node.parent

    def rotateleft(self, z):
        y = z.right
        z.right = y.left
        if y.left is not None:
            y.left.parent = z
        y.parent = z.parent
        if z.parent is None:
            self.root = y
        elif z == z.parent.left:
            z.parent.left = y
        else:
            z.parent.right = y
        y.left = z
        z.parent = y

        self.revaluate_height(z)
        self.revaluate_height(y)

    def rotateright(self, z):
        y = z.left
        z.left = y.right
        if y.right is not None:
            y.right.parent = z
        y.parent = z.parent
        if z.parent is None:
            self.root = y
        elif z == z.parent.right:
            z.parent.right = y
        else:
            z.parent.left = y
        y.right = z
        z.parent = y

        self.revaluate_height(z)
        self.revaluate_height(y)

    def insert(self, key, value):
        node = Node(key, value)

        if self.root is None:
            self.root = node
            self.size += 1
            return
        current = self.root
        parent = None

        while current is not None:
            parent = current
            if node.key > current.key:
                current = current.right
            else:
                current = current.left

        if node.key > parent.key:
            parent.right = node
        else:
            parent.left = node

        node.parent = parent
        self.size += 1

        self.rebalance(node)


    def search(self, key):
        current = self.root
        while current is not None:
            if current.key == key:
                return current
            elif key > current.key:
                current = current.right
            else:
                current = current.left
        return None

    def delete(self, key):
        node = self.search(key)

        if node is None:
            return False

        # no children
        if node.left is None and node.right is None:
            if node == self.root:
                self.root = None
            elif node == node.parent.left:
                node.parent.left = None
            else:
                node.parent.right = None

            node_to_rebalance = node.parent

        # one children
        elif node.left is None or node.right is None:
            child = node.left if node.left else node.right
            if node == self.root:
                self.root = child
                child.parent = None
            else:
                if node == node.parent.left:
                    node.parent.left = child
                else:
                    node.parent.right = child
                child.parent = node.parent

            node_to_rebalance = node.parent

        # two children
        else:
            successor = self.min_key(node.right)

            # Move the successor's value to the node and delete the successor
            node.key,node.value = successor.key,successor.value


            if successor.right:
                if successor == successor.parent.left:
                    successor.parent.left = successor.right
                else:
                    successor.parent.right = successor.right
                successor.right.parent = successor.parent
            else:
                if successor == successor.parent.left:
                    successor.parent.left = None
                else:
                    successor.parent.right = None


            node_to_rebalance = successor.parent
        self.rebalance(node_to_rebalance)
        self.size -=1

        return True

    def min_key(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def max_key(self, node):
        current = node
        while current.right is not None:
            current = current.right
        return current

    # In-order traversal that returns tuples
    def inorder(self, node):
        if node is None:
            return []

        # Recursively visit left subtree, current node, and right subtree
        left_subtree = self.inorder(node.left)
        current_node = [node.key]
        right_subtree = self.inorder(node.right)

        return left_subtree + current_node + right_subtree


    def successor(self, key):
        node = self.search(key)

        if node is None:
            return None

        if node.right:
            return self.min_key(node.right)

        successor = None
        while node.parent:
            if node == node.parent.left:
                successor = node.parent
                break
            node = node.parent

        return successor

    def successor2(self, root, key):
        successor = None
        current = root

        while current is not None:
            if current.key >= key:

                successor = current
                current = current.left
            else:

                current = current.right

        return successor
