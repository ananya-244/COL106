from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.params = params
        self.table_size = params[-1]
        self.table = [None] * self.table_size
        self.num_elements = 0

    def polynomial_hash(self, key, z, mod):
        hash_value = 0
        for char in key[::-1]:
            x = ord(char)-ord('a')
            if x < 0:
                x = ord(char) - ord("A") + 26
            hash_value = (hash_value * z + x) % mod
        return hash_value

    def get_slot(self, key):
        z= self.params[0]
        mod = self.table_size
        hash_value = self.polynomial_hash(key,z,mod)
        return hash_value

    def get_load(self):
        return self.num_elements / self.table_size
    
    def rehashset(self):
     
        new_size = get_next_size()
        
   
        newtable = [None] * new_size
        oldtable = self.table  
        self.table = newtable  
        self.table_size = new_size
        self.num_elements = 0  
        
       
        for item in oldtable:
            if item is not None:
                if self.collision_type == "Chain":
                    
                    for element in item:
                        self.insert(element)
                else:
                   
                    self.insert(item)
    
    def rehashmap(self):
        
        new_size = get_next_size()
        
       
        newtable = [None] * new_size
        oldtable = self.table 
        self.table = newtable  
        self.table_size = new_size
        self.num_elements = 0  
        
       
        for item in oldtable:
            if item is not None:
                if self.collision_type == "Chain":
                    
                    for key, value in item:
                        self.insert((key, value))
                else:
                    
                    self.insert(item)

  
class HashSet(HashTable):
    def __init__(self, collision_type, params):
         super().__init__(collision_type, params)
    
    
    def find_slot(self, j, key):
       
        firstAvail = None
        start_slot = j
        jumps = 0
        while True:
            # Check if the slot is available
            if self.table[j] is None:
                if firstAvail is None:
                    firstAvail = j
                # If the slot is empty, return the first available slot
                if self.table[j] is None:
                    return (False, firstAvail)
            elif key == self.table[j]:
                # If the key matches, return the slot
                return (True, j)
            # Move to the next slot (linear probing)
            if self.collision_type == "Linear":
                j = (j + 1) % self.table_size
            elif self.collision_type == "Double":
                z2, c2 = self.params[1], self.params[2]
                hash2 = c2 - (super().polynomial_hash(key, z2, c2) % c2)
                j = (j + hash2) % self.table_size
            jumps += 1

            # Stop if we've made `table_size` jumps or return False on encountering empty slot
            if jumps >= self.table_size or j == start_slot:
                return (False,self.table_size)
                
    

    def insert(self, key):
        # Get the initial slot for the key
        if super().get_load() == 1:
            raise Exception("Table is full")
        start_slot = super().get_slot(key)
        # Use find_slot to locate the correct position for insertion
        if self.collision_type == "Chain":
            if self.table[start_slot] is None:
                self.table[start_slot] = [key]
                self.num_elements += 1
            else:
                if key not in self.table[start_slot]: 
                    self.table[start_slot].append(key)
                    self.num_elements += 1
                    
        else:
            found, slot = self.find_slot(start_slot, key)
            if not found and slot != self.table_size:
                # Insert the key if it does not already exist
                self.table[slot] = key
                self.num_elements += 1

    def find(self, key):
        if self.collision_type == "Chain":
            start_slot = super().get_slot(key)
            if self.table[start_slot] == None:
                return False
            for j in self.table[start_slot]:
                if j == key:
                    return True
            return False
        else:
            start_slot = super().get_slot(key)
            found, slot = self.find_slot(start_slot, key)
            return found
    
    def __str__(self):
        str_repl = []
        for slot in self.table:
            if slot is None:
                str_repl.append("<EMPTY>")
            elif isinstance(slot, list):
                str_repl.append(" ; ".join(f"{key}" for key in slot))
            else:
                str_repl.append(str(slot))
        return " | ".join(str_repl)


class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def find_slot(self, j, key):
       
        firstAvail = None
        start_slot = j
        jumps = 0
        while True:
            # Check if the slot is available
            if self.table[j] is None:
                if firstAvail is None:
                    firstAvail = j
                # If the slot is empty, return the first available slot
                if self.table[j] is None:
                    return (False, firstAvail)
            elif key == self.table[j][0]:
                # If the key matches, return the slot
                return (True, j)
            # Move to the next slot (linear probing)
            if self.collision_type == "Linear":
                j = (j + 1) % self.table_size
            elif self.collision_type == "Double":
                z2, c2 = self.params[1], self.params[2]
                hash2 = c2 - (super().polynomial_hash(key, z2, c2) % c2)
                j = (j + hash2) % self.table_size
            jumps += 1

            # Stop if we've made `table_size` jumps or return False on encountering empty slot
            if jumps >= self.table_size or j == start_slot:
                return (False,self.table_size)
                
    

    def insert(self, key):
        # Get the initial slot for the key
        if super().get_load() == 1:
            raise Exception("Table is full")
        start_slot = super().get_slot(key[0])
        # Use find_slot to locate the correct position for insertion
        if self.collision_type == "Chain":
            if self.table[start_slot] is None:
                self.table[start_slot] = [(key[0],key[1])]
                self.num_elements += 1
            else:
                # for i in self.table[start_slot]:
                #     if i[0] == key[0]:
                #         i[1] = key[1]
                        
                        
                for i in range(len(self.table[start_slot])):
                    if self.table[start_slot][i][0] == key[0]:
                        self.table[start_slot][i] = (key[0],key[1])
                # if (key[0],key[1]) not in self.table[start_slot]: 
                self.table[start_slot].append((key[0],key[1]))
                self.num_elements += 1
                    
        else:
            found, slot = self.find_slot(start_slot, key[0])
            if not found and slot != self.table_size:
                # Insert the key if it does not already exist
                self.table[slot] = (key[0],key[1])
                self.num_elements += 1
            elif found:
                self.table[slot] = (key[0],key[1])
            

    def find(self, key):
        # Get the initial slot for the key
        start_slot = super().get_slot(key)
        # Use find_slot to check if the key exists in the table
        found, slot = self.find_slot(start_slot, key)
        if self.collision_type == "Chain":
            for j in self.table[start_slot]:
                if j[0] == key:
                    return j[1]
        if found:
            return self.table[slot][1]
        else:
            return 
    
    def __str__(self):
        str_repl = []
        for slot in self.table:
            if slot is None:
                str_repl.append("<EMPTY>")
            elif isinstance(slot, list):
                str_repl.append(";".join(f"{(key,value)}" for key,value in slot))
            else:
                str_repl.append(f"{(slot[0],slot[1])}")
        return " | ".join(str_repl)

