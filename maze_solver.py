from PIL import Image, ImageDraw, ImageOps
import sys

#Maze generator used for mazes:
# http://hereandabove.com/maze/mazeorig.form.html

#recursive method
def solveRecursiveMaze(arr, width, height, exitX, exitY, x,y):
    successful = False
    if (x,y) == (exitX,exitY):
        successful = True
    elif isValid(arr,width,height,x,y):
        arr[x][y] = "V" #set to V to show it's a visited path
        successful = solveRecursiveMaze(arr, width, height, exitX, exitY, x-1, y)  
        if not successful:
            successful = solveRecursiveMaze(arr, width, height, exitX, exitY, x, y+1)
        if not successful:
            successful = solveRecursiveMaze(arr, width, height, exitX, exitY, x+1, y)
        if not successful:
            successful = solveRecursiveMaze(arr, width, height, exitX, exitY, x, y-1)  
    if successful:
        arr[x][y] = "P" #Mark as P to show it's a valid path
    return successful

#are the values in the array, and is it a valid path
def isValid(arr,width,height,x,y):
    if x < width and y < height and x >= 0 and y >= 0:
        if arr[x][y] == "W":
            return True
    return False

#find the entryPoint of the maze     
def getEntryPoint(arr, width, height):
    #traverse along top
    for x in range(1, width - 1):
        if(arr[x][1] == 'W'):
            return x,1

    #traverse left side
    for y in range(1, height - 1):
        if(arr[1][y] == 'W'):
            return 1,y
    raise Exception("Entry point was not found!")

#find the exitPoint of the maze
def getExitPoint(arr, width, height):
    #Traverse bottom
    for x in range(1, width - 1):
        if arr[x][height - 2] == 'W':
            return x, height - 2

    #Traverse right side
    for y in range(1, height - 1):
        if arr[width - 2][y] == 'W':
            return width - 2,y
    raise Exception("Exit point was not found!")

#Loop through the array and draw the solution
def drawSolution(arr,width,height):
    newImg = Image.new('RGB',(width,height),(0,0,0))
    for x in range(width):
        for y in range(height):
            charToRGB = {
                'W' : (255,255,255),
                'B' : (0,0,0),
                'P' : (0,255,0),
                'V' : (255,0,128)
            }
            newImg.putpixel((x, y),charToRGB[arr[x][y]])
    newImg.save("solution.png","png")
    newImg.show()


#2D array of each pixel, "W" representing a white pixel. "B" is representing a black pixel
def convertImageToArray(imageName):
    crop = Image.open(imageName).convert("RGB")
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
    return maze, width, height

def main():
    solved = False
    maze,width,height = convertImageToArray("maze.png")
    x,y = getEntryPoint(maze,width,height)
    w,z = getExitPoint(maze,width,height)
    print("Entering maze at x = %d, y = %d"%(x,y))   
    #if it is solved, draw the solution, if not just draw the entry/exit points
    solved = solveRecursiveMaze(maze,width,height,w,z,x,y)
    if not solved:
        print("Cannot find solution")
    else:
        print("Solution found!")
        drawSolution(maze,width,height)
    return 0 if solved else 1

if __name__ == "__main__":
    sys.setrecursionlimit(15000)
    sys.exit(main())