from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.objects_stored = AVLTree()  # AVLTREE of objects in the bin

    def add_object1(self, obj):
        if obj.size <= self.capacity:
            self.capacity -= obj.size
            self.objects_stored.insert(obj.object_id, obj)
            return
        raise NoBinFoundException

    def remove_object(self, obj):
        if self.objects_stored.search(obj.object_id) is not None:
            self.capacity += obj.size
            self.objects_stored.delete(obj.object_id)
            return
