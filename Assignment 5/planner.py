from flight import Flight


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
        self.heap[0] = self.heap.pop()  
        self.heapify_down(0)
        return top_value

    

    
class CircularQueue:
    def __init__(self,capacity):
        
        self.queue = [None] * capacity
        self.capacity = capacity
        self.front = 0  
        self.rear = -1  
        self.size = 0   

    def enqueue(self, item):

        if self.size == self.capacity:
            return

        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1

    def dequeue(self):

        if self.size == 0:
            return
        
        item = self.queue[self.front]
        self.queue[self.front] = None  
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

        


class Planner:
    def __init__(self, flights):
        
        """
        Initializes the Planner with flight data.

        Args:
            flights (List[Flight]): A list of Flight objects representing available flights.
        """
        
        self.flight_count = len(flights)
        self.cities = 0
        
        for i in flights:
            x = max(i.end_city,i.start_city)
            self.cities = max(self.cities,x)
            
            
        self.adj = [[] for _ in range(self.flight_count)]

        self.flights_by_city = [[] for _ in range(self.cities+1)]
        
        
        for flight in flights:
            
            if flight.start_city == flight.end_city:
                continue
            self.flights_by_city[flight.start_city].append(flight)
            

        for flight in flights:
            
            if flight.start_city == flight.end_city:
                continue
            connect_flights = self.flights_by_city[flight.end_city]
            
            for connect_flight in connect_flights:
                if connect_flight.departure_time >= flight.arrival_time + 20:
                    self.adj[flight.flight_no].append(connect_flight)


    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        starting_flights = self.flights_by_city[start_city]
        
        queue = CircularQueue(self.flight_count)
        
        visited = [False for _ in range(self.flight_count)]
        parent = [None for _ in range(self.flight_count)]
        
        for start_flight in starting_flights:
            if start_flight.departure_time >= t1 and start_flight.arrival_time <= t2:
                queue.enqueue((start_flight, start_flight.arrival_time, 1))  
                visited[start_flight.flight_no] = True
                
        
        route = None
        
        while queue.size != 0:
            curr_flight, current_time, no_of_flights = queue.dequeue()
            
            if curr_flight.end_city == end_city:
                if (route is None or (no_of_flights,current_time) < (len(route),route[-1].arrival_time)):
                    route = self.backtracking_path(parent,curr_flight)
        
                    
            for connect_flight in self.adj[curr_flight.flight_no]:
                if not visited[connect_flight.flight_no] and connect_flight.arrival_time <= t2:
                    queue.enqueue((connect_flight, connect_flight.arrival_time, no_of_flights + 1))
                    visited[connect_flight.flight_no] = True
                    parent[connect_flight.flight_no] = curr_flight  
        
        return route if route else []
    
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<= t2) with the minimum fare.
        """
        if start_city == end_city:
            return []
        
        min_heap = Heap(lambda a, b: a[0] < b[0], [])
        
        visited = [float('inf')] * (self.flight_count)  
        parent = [None for _ in range(self.flight_count)]

        for flight in self.flights_by_city[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                min_heap.insert((flight.fare, flight, flight.arrival_time))
                visited[flight.flight_no] = flight.fare


        while min_heap.heap:

            tot_fare, curr_flight, current_time = min_heap.extract()

            if curr_flight.end_city == end_city:
                route = self.backtracking_path(parent,curr_flight)
                return route  

            for connect_flight in self.adj[curr_flight.flight_no]:
                if connect_flight.arrival_time <= t2:
                    new_tot_fare = tot_fare + connect_flight.fare
                    if new_tot_fare < visited[connect_flight.flight_no]:
                        
                        min_heap.insert((new_tot_fare, connect_flight, connect_flight.arrival_time))
                        parent[connect_flight.flight_no] = curr_flight
                        visited[connect_flight.flight_no] = new_tot_fare

        return []
      
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Finds the route from start_city to end_city with the least number of flights.
        Among routes with the same number of flights, it returns the one with the minimum fare.

        Parameters:
            start_city (int): The starting city ID.
            end_city (int): The destination city ID.
            t1 (int): Earliest departure time.
            t2 (int): Latest arrival time.

        Returns:
            List[Flight]: A list of Flight objects representing the best route.
        """
        if start_city == end_city:
            return []

        min_heap = Heap(lambda a, b: (a[0], a[1]) < (b[0], b[1]), [])
       
        visited = [(self.flight_count+5, float('inf'))] * self.flight_count  
        parent = [None] * self.flight_count

        for flight in self.flights_by_city[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                min_heap.insert((1, flight.fare, flight))
                visited[flight.flight_no] = (1, flight.fare)
                parent[flight.flight_no] = None  

        route = []

        while min_heap.heap:
            
            no_of_flights, tot_fare, curr_flight = min_heap.extract()
            if curr_flight.end_city == end_city:
                if not route or (no_of_flights,tot_fare) < (visited[route[-1].flight_no]):
                    route = self.backtracking_path(parent,curr_flight)
                    continue

            for connect_flight in self.adj[curr_flight.flight_no]:
                if connect_flight.arrival_time <= t2:
                    new_no_of_flights = no_of_flights + 1
                    new_tot_fare = tot_fare + connect_flight.fare
        
                    if (new_no_of_flights,new_tot_fare) < visited[connect_flight.flight_no]:
                        min_heap.insert((new_no_of_flights, new_tot_fare, connect_flight))
                        visited[connect_flight.flight_no] = (new_no_of_flights, new_tot_fare)
                        parent[connect_flight.flight_no] = curr_flight

        return route

    def backtracking_path(self,parent,curr_flight):
        route = [curr_flight]
        par = parent[curr_flight.flight_no]            
        while par is not None:
            route.append(par)
            par = parent[par.flight_no]
            
        return route[::-1]




    