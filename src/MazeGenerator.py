import pygame
from random import *
pygame.init()

width = 30
height = 20
cellwidth = 15

disWidth = 2 * width * cellwidth + cellwidth
disHeight = 2 * height * cellwidth + cellwidth

window = pygame.display.set_mode((disWidth, disHeight))

pygame.display.set_caption("Maze Generator using Prim's Algoritm")

class cell:
    def __init__(self):
        self.leftNeighbor = False
        self.rightNeighbor = False
        self.upNeighbor = False
        self.downNeighbor = False
        self.neighbor = False
        self.inMaze = False
    
    def up(self):
        self.upNeighbor = True
    def left(self):
        self.leftNeighbor = True
    def right(self):
        self.rightNeighbor = True
    def down(self):
        self.downNeighbor = True
        
    def becomeNeighbor(self):
        self.neighbor = True
    def maze(self):
        self.neighbor = False
        self.inMaze = True
        
    def getMaze(self):
        return self.inMaze
    def isNeighbor(self):
        return self.neighbor
        
    def getConnections(self):
        connections = [self.upNeighbor, self.downNeighbor, self.leftNeighbor, self.rightNeighbor]
        return connections

maze = [[]]
neighbors = []

for i in range(width):
    for j in range(height):
        maze[i].append(cell())
    maze.append([])


def joinMaze(x, y):
    maze[x][y].maze()
    if x < width - 1:
        if not maze[x+1][y].getMaze() and not maze[x+1][y].isNeighbor():
            maze[x+1][y].becomeNeighbor()
            neighbors.append((x+1, y))
    if y < height - 1:
        if not maze[x][y+1].getMaze() and not maze[x][y+1].isNeighbor():
            maze[x][y+1].becomeNeighbor()
            neighbors.append((x, y+1))
    if x > 0:
        if not maze[x-1][y].getMaze() and not maze[x-1][y].isNeighbor():
            maze[x-1][y].becomeNeighbor()
            neighbors.append((x-1, y))
    if y > 0:
        if not maze[x][y-1].getMaze() and not maze[x][y-1].isNeighbor():
            maze[x][y-1].becomeNeighbor()
            neighbors.append((x, y-1))
    return
    
joinMaze(int(width / 2), int(height / 2))


#print(neighbors[1].getCoords())
#print(isNeighbor(maze[0], maze[1]))

#Add a cell to the maze
#First picks a random neighbor cell
#Finds and picks a random cell in the maze to connect to
#Establish said connection
#Add the neighbor cell to the maze
#Add new neighboring cells to neighbors
def nextMaze():
    randNeighbor = randint(0, len(neighbors) - 1)
    
    neighborX = neighbors[randNeighbor][0]
    neighborY = neighbors[randNeighbor][1]
    
    connections = []
    if neighborX > 0:
        if maze[neighborX - 1][neighborY].getMaze():
            connections.append(1)
    if neighborX < width - 1:
        if maze[neighborX + 1][neighborY].getMaze():
            connections.append(2)
    if neighborY > 0:
        if maze[neighborX][neighborY - 1].getMaze():
            connections.append(3)
    if neighborY < height - 1:
        if maze[neighborX][neighborY + 1].getMaze():
            connections.append(4)

    randConnection = randint(0, len(connections) - 1)
    #print(connections)
    #print(randConnection)
    if connections[randConnection] == 1:
        maze[neighborX][neighborY].left()
    if connections[randConnection] == 2:
        maze[neighborX][neighborY].right()
    if connections[randConnection] == 3:
        maze[neighborX][neighborY].down()
    if connections[randConnection] == 4:
        maze[neighborX][neighborY].up()
    
    joinMaze(neighborX, neighborY)
    del neighbors[randNeighbor]
    
    return
    
run = True
useKey = False
showNeighbors = False

wallColor = (0,0,0)
pathColor = (255,255,255)
neighborColor = (175,0,0)

while run:
    pygame.time.delay(25) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if len(neighbors) > 0:
        if useKey:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                nextMaze()
                print(neighbors)
        else:
            nextMaze()
        
    
    #White = Path
    #Red  = Neighbor
    #Black = Wall
    
    window.fill(wallColor)
    for i in range (0, width):
        for j in range (0, height):
            if maze[i][j].isNeighbor() and showNeighbors:
                pygame.draw.rect(window, neighborColor, (2 * i * cellwidth + cellwidth, 2 * j * cellwidth + cellwidth, cellwidth, cellwidth))
            elif maze[i][j].getMaze():
                pygame.draw.rect(window, pathColor, (2 * i * cellwidth + cellwidth, 2 * j * cellwidth + cellwidth, cellwidth, cellwidth))
                cellConnections = maze[i][j].getConnections()
                #print(cellConnections)
                if cellConnections[0]: #Up
                    pygame.draw.rect(window, pathColor, (2 * i * cellwidth + cellwidth, 2 * j * cellwidth + cellwidth + cellwidth, cellwidth, cellwidth))
                if cellConnections[1]: #Down
                    pygame.draw.rect(window, pathColor, (2 * i * cellwidth + cellwidth, 2 * j * cellwidth - cellwidth + cellwidth, cellwidth, cellwidth))
                if cellConnections[2]: #Left
                    pygame.draw.rect(window, pathColor, (2 * i * cellwidth - cellwidth + cellwidth, 2 * j * cellwidth + cellwidth, cellwidth, cellwidth))
                if cellConnections[3]: #Right
                    pygame.draw.rect(window, pathColor, (2 * i * cellwidth + cellwidth + cellwidth, 2 * j * cellwidth + cellwidth, cellwidth, cellwidth))
                
                    
            #else:
                #pygame.draw.rect(window, (255,255,255), (2 * i * cellwidth, 2 * j * cellwidth, cellwidth, cellwidth))
    pygame.display.update()
    
pygame.quit()