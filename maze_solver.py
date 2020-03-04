from PIL import Image, ImageDraw, ImageOps
import sys

#Maze generator used for mazes:
# http://hereandabove.com/maze/mazeorig.form.html

#open our png and get it ready to draw on, also set our recursive limit higher than the default (1000)
crop = ImageOps.crop(Image.open('maze.png').convert("RGB"), (1,1,1,1))  
draw = ImageDraw.Draw(crop)
sys.setrecursionlimit(10000)


#recursive method
def solveRecursiveMaze(arr,x,y):
    successful = False
    if (x,y) == getExitPoint():
        successful = True
    elif isValid(arr,x,y):
        arr[x][y] = "V" #set to V to show it's a visited path
        successful = solveRecursiveMaze(arr, x-1, y)    
        if not successful:
            successful = solveRecursiveMaze(arr, x, y+1)
        if not successful:
            successful = solveRecursiveMaze(arr, x+1, y)
        if not successful:
            successful = solveRecursiveMaze(arr, x, y-1)
    if successful:
        arr[x][y] = "P" #Mark as P to show it's a valid pa
    return successful

#are the values in the array, and is it a valid path
def isValid(arr,x,y):
    if x < len(arr) and y < len(arr) and x >= 0 and y >= 0:
        if arr[x][y] == "W":
            return True
    return False

#find the entryPoint of the maze     
def getEntryPoint():
    x = 0
    for y in range(0, crop.size[1] - 1):
        if(crop.getpixel((x,y)) == (255,255,255)):
            return x,y
        if(crop.getpixel((y,x)) == (255,255,255)):
            return y,x

#find the exitPoint of the maze
def getExitPoint():
    x = crop.size[0] - 1
    for y in range(0, crop.size[1] - 1):
        if(crop.getpixel((x,y)) == (255,255,255)):
            return x,y

#Loop through the array and draw the solution
def drawSolution(arr):
    for i in range(1, crop.size[0] - 1):
        for j in range(1, crop.size[1] - 1):
            if arr[i][j] == "P":
                if arr[i+1][j] == "P":
                    draw.line([(i,j),(i+1,j)],fill=128,width=1)
                elif arr[i-1][j] == "P":
                    draw.line([(i,j),(i-1,j)],fill=128,width=1)
                elif arr[i][j+1] == "P":
                    draw.line([(i,j),(i,j+1)],fill=128,width=1)
                elif arr[i][j-1] == "P":
                    draw.line([(i,j),(i,j-1)],fill=128,width=1)

#2D array of each pixel, "W" representing a white pixel. "B" is representing a black pixel        
maze = []
width,height = crop.size
for x in range(0, width):
    mazeX = []
    for y in range(0, height):
        if(crop.getpixel((x,y)) == (0,0,0)):
            mazeX.append("B")
        elif(crop.getpixel((x,y)) == (255,255,255)):
            mazeX.append("W")
    maze.append(mazeX)

#get X,Y pixels of both entry and exit points
entryX,entryY = getEntryPoint()
exitX,exitY = getExitPoint()
#if it is solved, draw the solution, if not just draw the entry/exit points
if solveRecursiveMaze(maze,entryX,entryY):
    print("Solved")
    draw.line([(exitX,exitY),(exitX-1,exitY)],fill=128,width=1)
    draw.line([(entryX,entryY),(entryX-1,entryY)],fill=128,width=1)
    drawSolution(maze)
else:
    print("Not Solved")
    draw.line([(exitX,exitY),(exitX-1,exitY)],fill=128,width=1)
    draw.line([(entryX,entryY),(entryX-1,entryY)],fill=128,width=1)

#show the completed picture
crop.show()