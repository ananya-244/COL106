from treasure import *
from heap import *

class CrewMate:
    '''
    Class to implement a crewmate
    '''

    def __init__(self):
        '''
        Initializes the crewmate
        '''
        self.assigned_treasures = []  # List to store treasures assigned to this crewmate
        self.total_completion_time = 0  # Keep track of the total load (sum of sizes of assigned treasures)
        self.last_arrival_time = 0


    def assign_treasure(self, treasure):
        '''
        Assigns a treasure to the crewmate
        Arguments:
            treasure : Treasure : The treasure to be assigned
        '''


        self.total_completion_time = max(self.total_completion_time, treasure.arrival_time) + treasure.size
        self.assigned_treasures.append(treasure)
        self.last_arrival_time = treasure.arrival_time

    def process_treasures(self):
        treasure_list = []
        if not self.assigned_treasures:
            return treasure_list

        t = self.assigned_treasures[0].arrival_time
        curr_treasure = Treasure(self.assigned_treasures[0].id, self.assigned_treasures[0].size, self.assigned_treasures[0].arrival_time)
        heap = Heap(lambda a, b: (a.size + a.arrival_time, a.id) < (b.size + b.arrival_time, b.id), [curr_treasure])

        for i in range(1, len(self.assigned_treasures)):
            curr_treasure = heap.top()
            new_time = self.assigned_treasures[i].arrival_time
            available_time = new_time - t

            while curr_treasure and available_time >= curr_treasure.size:
                in_processing = heap.extract()
                treasure_list.append(in_processing)
                t += in_processing.size  # Update the current time before setting completion
                in_processing.size = 0
                available_time = new_time - t
                in_processing.completion_time = t  # Correct time
                curr_treasure = heap.top()


            if curr_treasure:
                curr_treasure.size -= available_time  # Reduce remaining size by available time
                heap.heapify_down(0)  # Restore heap order
            t = new_time

            to_be_added = Treasure(self.assigned_treasures[i].id, self.assigned_treasures[i].size, self.assigned_treasures[i].arrival_time)
            heap.insert(to_be_added)





        heap.in_place_heap_sort()
        t = self.last_arrival_time


        for i in range(len(heap.heap)-1,-1,-1):
            curr = heap.heap[i]
            # Set the completion time as the current time plus the remaining size of the treasure
            # print(curr.id,curr.arrival_time,curr.size)

            if t< curr.arrival_time:
                t = curr.arrival_time
            t += curr.size
            curr.completion_time = t

            treasure_list.append(curr)

        heap.build_heap()


        return treasure_list

