class Heap:
    '''
    Class to implement a heap with a general comparison function
    '''

    def __init__(self, comparison_function, init_array=[]):
        '''
        Initializes a heap with a comparison function
        '''
        self.comparison_function = comparison_function
        self.heap = init_array[:]
        self.build_heap()  # Create a heap from the initial array

    def build_heap(self):
        '''
        Build a heap from the initial array
        Time Complexity: O(n)
        '''
        for i in range(len(self.heap) // 2, -1, -1):
            self.heapify_down(i)

    def heapify_down(self, idx):
        '''
        Moves the element at idx down to its correct position in the heap
        '''
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx

        if left < len(self.heap) and self.comparison_function(self.heap[left], self.heap[smallest]):
            smallest = left
        if right < len(self.heap) and self.comparison_function(self.heap[right], self.heap[smallest]):
            smallest = right

        if smallest != idx:
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]
            self.heapify_down(smallest)

    def heapify_up(self, idx):
        '''
        Moves the element at idx up to its correct position in the heap
        '''
        parent = (idx - 1) // 2
        if idx > 0 and self.comparison_function(self.heap[idx], self.heap[parent]):
            self.heap[parent], self.heap[idx] = self.heap[idx], self.heap[parent]
            self.heapify_up(parent)

    def insert(self, value):
        '''
        Inserts a value into the heap
        '''
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)

    def extract(self):
        '''
        Extracts the value from the top of the heap
        '''
        if not self.heap:
            return None
        top_value = self.heap[0]
        if len(self.heap) == 1:
            self.heap.pop()
            return top_value
        self.heap[0] = self.heap.pop()  # Move last element to top and remove last
        self.heapify_down(0)
        return top_value

    def top(self):
        '''
        Returns the top value without removing it
        '''
        return self.heap[0] if self.heap else None

    def in_place_heap_sort(self):
        '''
        Performs in-place heap sort on the heap array
        Time Complexity: O(n log n)
        '''
        # Step 1: Build the heap (this is already done in the constructor or explicitly by the user)


        # Step 2: Repeatedly extract the max/min and reheapify
        for i in range(len(self.heap) - 1, 0, -1):
            # Swap the root (heap[0]) with the last element
            self.heap[0], self.heap[i] = self.heap[i], self.heap[0]
            # Reduce the size of the heap to ignore the sorted elements
            self.heapify_down_range(0, i)

    def heapify_down_range(self, idx, max_size):
        '''
        Heapifies down the element at idx for a restricted size of the heap (for sorting)
        '''
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx

        if left < max_size and self.comparison_function(self.heap[left], self.heap[smallest]):
            smallest = left
        if right < max_size and self.comparison_function(self.heap[right], self.heap[smallest]):
            smallest = right

        if smallest != idx:
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]
            self.heapify_down_range(smallest, max_size)
