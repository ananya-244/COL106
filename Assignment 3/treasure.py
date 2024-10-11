
class Treasure:
    '''
    Class to represent a piece of treasure
    '''

    def __init__(self, id, size, arrival_time):
        '''
        Initializes a treasure
        Arguments:
            id : int : The unique ID of the treasure
            size : int : The size (time required to process) of the treasure
            arrival_time : int : The time at which the treasure becomes available
        '''
        self.id = id
        self.size = size
        self.arrival_time = arrival_time
        self.completion_time = None  # This will be set when treasure is fully processed
