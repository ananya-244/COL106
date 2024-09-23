from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        self.bins_by_capacity = AVLTree()  # AVL Tree to manage bins by capacity
        self.bins_by_ID = AVLTree()
        self.objects = AVLTree()  # AVL Tree to manage objects by object_id

    def delete_bin(self, capacity):
        found_bin = self.bins_by_capacity.search(capacity)
        if found_bin.value.root is not None:
            return
        else:
            self.bins_by_capacity.delete(capacity)

    def add_bin(self, bin_id, capacity):

        newbin = Bin(bin_id, capacity)

        if (self.bins_by_capacity.search(capacity) == None):
            tree = AVLTree()
            tree.insert(bin_id, newbin)
            self.bins_by_capacity.insert(capacity, tree)

        else:
            curr_found_node = self.bins_by_capacity.search(capacity)
            curr_found_node.value.insert(bin_id, newbin)
        self.bins_by_ID.insert(bin_id, newbin)

    def add_bins_after_adding_object(self, selected_bin):
        if (self.bins_by_capacity.search(selected_bin.capacity) == None):
            tree = AVLTree()
            tree.insert(selected_bin.bin_id, selected_bin)
            self.bins_by_capacity.insert(selected_bin.capacity, tree)

        else:

            curr_found_node = self.bins_by_capacity.search(selected_bin.capacity)
            curr_found_node.value.insert(selected_bin.bin_id, selected_bin)

    def add_object(self, object_id, size, color):
        current_node = self.bins_by_capacity.root
        selected_node = None

        if current_node is None:
            raise NoBinFoundException

        # GREEN/RED
        if color == Color.GREEN or color == Color.RED:
            current_node = self.bins_by_capacity.max_key(current_node)
        # BLUE/YELLOW
        elif color == Color.BLUE or color == Color.YELLOW:
            current_node = self.bins_by_capacity.successor2(current_node, size)

        if current_node is None:
            raise NoBinFoundException

        if (color == Color.RED or color == Color.BLUE):
            selected_node = current_node.value.min_key(current_node.value.root)
        elif (color == Color.GREEN or color == Color.YELLOW):
            selected_node = current_node.value.max_key(current_node.value.root)

        if selected_node is None:
            raise NoBinFoundException

        selected_bin = selected_node.value

        new_object = Object(object_id, size, color)

        if selected_bin.capacity < new_object.size:
            raise NoBinFoundException

        current_node.value.delete(selected_bin.bin_id)
        self.bins_by_ID.delete(selected_bin.bin_id)
        self.delete_bin(selected_bin.capacity)
        selected_bin.add_object1(new_object)
        self.add_bins_after_adding_object(selected_bin)
        self.objects.insert(object_id, (new_object, selected_bin))
        self.bins_by_ID.insert(selected_bin.bin_id, selected_bin)

    def insert_bin_after_deleting_object(self, bin):
        if (self.bins_by_capacity.search(bin.capacity) == None):
            tree = AVLTree()
            tree.insert(bin.bin_id, bin)
            self.bins_by_capacity.insert(bin.capacity, tree)

        else:

            curr_found_node = self.bins_by_capacity.search(bin.capacity)
            curr_found_node.value.insert(bin.bin_id, bin)

    def delete_object(self, object_id):
        node = self.objects.search(object_id)
        if node is None:
            return None

        obj = node.value[0]
        bin = node.value[1]
        current_node = self.bins_by_capacity.search(bin.capacity)
        current_node.value.delete(bin.bin_id)
        self.delete_bin(bin.capacity)
        self.bins_by_ID.delete(bin.bin_id)
        bin.remove_object(obj)
        self.insert_bin_after_deleting_object(bin)

        self.bins_by_ID.insert(bin.bin_id, bin)
        self.objects.delete(object_id)

    def bin_info(self, bin_id):
        bin_node = self.bins_by_ID.search(bin_id)
        if bin_node is not None:
            bin = bin_node.value
            return ((bin.capacity, bin.objects_stored.inorder(bin.objects_stored.root)))
        else:
            return None

    def object_info(self, object_id):
        node = self.objects.search(object_id)
        if node is not None:
            obj, bin = node.value
            return bin.bin_id
        else:
            return None

