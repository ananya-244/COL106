from heap import *
from crewmate import *

class StrawHatTreasury:
    '''
    Class to manage the Straw Hat pirates' treasure
    '''

    def __init__(self, m):
        '''
        Initializes the StrawHatTreasury
        Arguments:
            m : int : The number of crewmates
        '''
        self.crewmates_no = m
        self.crewmates = [CrewMate() for _ in range(m)]  # Initialize crewmates
        self.treasures = []  # List to store all treasures
        self.heap = Heap(lambda a, b: a.total_completion_time < b.total_completion_time, self.crewmates)
        self.treasure_count = 0
        
# Min-heap based on completion time

    def add_treasure(self, treasure):
        '''
        Adds a treasure to the system and assigns it to the crewmate with the least load
        Arguments:
            treasure : Treasure : The treasure to be added
        '''
        # Assign to the crewmate with the least load
        self.treasure_count += 1
        least_loaded_crewmate = self.heap.extract()  # Extract crewmate with least load
        least_loaded_crewmate.assign_treasure(treasure)
        self.heap.insert(least_loaded_crewmate)  # Reinsert after modifying the load
        self.treasures.append(treasure)

    def get_completion_time(self):
        '''
        Returns the list of treasures with updated completion times
        '''
        listoftreasures = []
        if (self.treasure_count > self.crewmates_no):

            # while any(crewmate.assigned_treasures for crewmate in self.crewmates):
            for crewmate in self.crewmates:
                listoftreasures += crewmate.process_treasures()
                

        else:
            for i in self.treasures:
                i.completion_time = i.size + i.arrival_time
                listoftreasures.append(i)

         # Sort treasures by their ID
        sorted_treasures = sorted(listoftreasures, key=lambda t: t.id)
        # sorted_treasures = [(i.id,i.completion_time) for i in sorted_treasures]
        return sorted_treasures


