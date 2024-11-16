import hash_table as ht

def binarySearch(arr, low, high, x):
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid][0] == x:
                return mid
            elif arr[mid][0] < x:
                low = mid + 1
            else:
                high = mid - 1

        return -1
    
def binarySearch2(arr, low, high, x):
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid] == x:
                return mid
            elif arr[mid] < x:
                low = mid + 1
            else:
                high = mid - 1
        return -1
    
    
    
def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right =merge_sort(arr[mid:])
        return merge(left, right)

def merge(left, right):
    sorted_list = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
        # Append remaining elements
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list


class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        self.books = []
        self.total_books = 0
    
    def distinct_words(self, book_title):
        ind = binarySearch(self.books,0,self.total_books - 1,book_title)
        return self.books[ind][1]

    def count_distinct_words(self, book_title):
        ind = binarySearch(self.books,0,self.total_books - 1,book_title)
        return self.books[ind][2]

    def search_keyword(self, keyword):
        ans = []
        for i in self.books:
            ind = binarySearch2(i[1],0,i[2]-1,keyword)
            if ind != -1:
                ans.append(i[0])
        return ans
    
    def print_books(self):
        for i in self.books:
            print(f"{i[0]}: {' | '.join(i[1])}")


class MuskLibrary(DigitalLibrary):
    def __init__(self, book_titles, texts):
        super().__init__()
        
        
        for title, text in zip(book_titles, texts):
            text1 = merge_sort(text)
            textf = [text1[0]]
            
            for i in range(1,len(text1)):
                if(text1[i] == text1[i-1]):
                    continue
                    
                else:
                    textf.append(text1[i])
                    
            self.books.append((title,textf,len(textf)))
        self.books = merge_sort(self.books)
        self.total_books = len(self.books)
            
    

    


class JGBLibrary(DigitalLibrary):
    def __init__(self, name, params):
        super().__init__()
        self.name = name
        self.params = params
      
     
        if self.name == "Jobs":
            self.hash_table = ht.HashMap("Chain", self.params)
        elif self.name == "Gates":
            self.hash_table = ht.HashMap("Linear", self.params)
        elif self.name == "Bezos":
            self.hash_table = ht.HashMap("Double", self.params)

    def add_book(self, book_title, text):
        if self.name == "Jobs":
            textf = ht.HashSet("Chain", self.params)
        elif self.name == "Gates":
            textf = ht.HashSet("Linear", self.params)
        elif self.name == "Bezos":
            textf= ht.HashSet("Double", self.params)

        for i in text:
            textf.insert(i)

        self.hash_table.insert((book_title,textf))
        self.books.append((book_title,textf))
      

    def distinct_words(self, book_title):
        
        ans = self.hash_table.find(book_title).table
        
        final_ans = []
        for i in ans:
            if i != None:
                if(self.name == "Jobs"):
                    final_ans.extend(i)
                else:
                    final_ans.append(i)
        return final_ans
            

    def count_distinct_words(self, book_title):
        return self.hash_table.find(book_title).num_elements
        

    def search_keyword(self, keyword):
        ans = []
        for i in self.books:
            found = i[1].find(keyword)
            if found:
                ans.append(i[0])
        return ans
                

    def print_books(self):
        for i in self.books:
            print(f"{i[0]}: {i[1]}")