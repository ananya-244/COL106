from maze import *
from exception import *
from stack import *
class PacMan:
    def __init__(self, grid : Maze) -> None:
        ## DO NOT MODIFY THIS FUNCTION
        self.navigator_maze = grid.grid_representation
    def rows(self):
        return len(self.navigator_maze)
    
    def cols(self):
        return len(self.navigator_maze[0])
    def find_path(self, start, end):
        # IMPLEMENT FUNCTION HERE
        rows = self.rows()
        cols = self.cols()
        visited = [[False for i in range(cols)] for j in range(rows)]
        visited[start[0]][start[1]] = True
        paths = Stack()
        paths.push(start)
        if self.navigator_maze[start[0]][start[1]] == 1:
            raise PathNotFoundException
            

        

        while not paths.is_empty():
            curr = paths.top()
            x, y = curr[0], curr[1]
            if curr == end:
                return paths.show()
            moved = False

            for i in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                x_ = x + i[0]
                y_ = y + i[1]
                newpos = (x_, y_)
    
                if 0 <= x_ < rows and 0 <= y_ < cols and not visited[x_][y_] and self.navigator_maze[x_][y_] != 1:
                    paths.push(newpos)
                    visited[x_][y_] = True
                    moved = True
                    break
            if not moved:
                paths.pop()

        raise PathNotFoundException
