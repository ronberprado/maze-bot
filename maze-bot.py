import heapq
import turtle
import time
import msvcrt
import os

background = turtle.Screen()
background.bgcolor("black")
background.setup(1300, 700)


class AnimateMaze(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


class Emerald(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)


class Scarlet(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)


class Gold(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.speed(0)


class Node:
    exploredContainer = []
    pathFound = 1
    alreadyExplored = set(exploredContainer)

    def __init__(self, prev=None, pos=None):
        self.prev = prev
        self.pos = pos
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, extra):
        return self.pos == extra.pos

    def __lt__(self, extra):
        return self.f < extra.f

    def __gt__(self, extra):
        return self.f > extra.f


def readMaze(file):
    with open(file) as f:
        mazeList = []
        mazeLines = f.read().splitlines()
        for i, line in enumerate(mazeLines):
            if i == 0:
                continue
            mazeList.append(list(line))
    return mazeList


def printTheMaze(maze):
    for i in maze:
        print("".join(i))


def findS(maze):
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'S':
                return r, c


def findG(maze):
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'G':
                return r, c


def lookPath(contain):
    reversedPath = []
    container = contain
    while container is not None:
        reversedPath.append(container.pos)
        container = container.prev
    return reversedPath[::-1]


def search(maze):
    s = findS(maze)
    g = findG(maze)

    stNode = Node(None, s)
    stNode.g = stNode.h = stNode.f = 0
    glNode = Node(None, g)
    glNode.g = glNode.h = glNode.f = 0

    frontierList = []
    exploredList = []

    heapq.heapify(frontierList)
    heapq.heappush(frontierList, stNode)

    fourDirections = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while len(frontierList) > 0:

        cNode = heapq.heappop(frontierList)
        exploredList.append(cNode)

        if cNode.pos not in Node.alreadyExplored:
            Node.alreadyExplored.add(cNode.pos)
            Node.exploredContainer.append(cNode.pos)

        if cNode == glNode:
            solPath = lookPath(cNode)
            print(f"Final path taken by the bot: {solPath}\n")
            print(f"All locations explored in order: {Node.exploredContainer}\n")
            print(f"Total number of states explored: {len(Node.exploredContainer)}\n")
            return solPath

        neighbors = []

        for newPos in fourDirections:

            nodePos = (cNode.pos[0] + newPos[0], cNode.pos[1] + newPos[1])

            if nodePos[0] > (len(maze) - 1) or nodePos[0] < 0 or nodePos[1] > (
                    len(maze[len(maze) - 1]) - 1) or nodePos[1] < 0:
                continue

            if maze[nodePos[0]][nodePos[1]] == '#':
                continue

            nNode = Node(cNode, nodePos)

            if nNode in exploredList:
                continue

            neighbors.append(nNode)

        for nb in neighbors:

            nb.g = cNode.g + 1
            nb.h = abs(glNode.pos[0] - nb.pos[0]) + abs(
                glNode.pos[1] - nb.pos[1])
            nb.f = nb.g + nb.h

            for fNode in frontierList:
                if nb == fNode and nb.g > fNode.g:
                    continue

            heapq.heappush(frontierList, nb)

    Node.pathFound = 0

    print(f"All locations explored in order: {Node.exploredContainer}\n")
    print(f"Total number of states explored: {len(Node.exploredContainer)}\n")

    return None


def animateFinalPath(maze, path):
    global start_x, start_y, end_x, end_y
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            character = maze[x][y]
            screen_x = -588 + (y * 20)
            screen_y = 288 - (x * 20)

            if character == '#':
                animateMaze.goto(screen_x, screen_y)
                animateMaze.stamp()

            if character == 'G':
                emerald.goto(screen_x, screen_y)
                end_x, end_y = screen_x, screen_y
                emerald.stamp()
                emerald.color("green")

            if character == 'S':
                start_x, start_y = screen_x, screen_y
                scarlet.goto(screen_x, screen_y)
                gold.goto(screen_x, screen_y)

    char = 0
    print("Press any key to start the search.")
    while not char:
        char = msvcrt.getch()

    for m in Node.exploredContainer:
        a = -588 + (m[1] * 20)
        b = 288 - (m[0] * 20)
        gold.goto(a, b)
        gold.stamp()
        gold.color("yellow")
        if m != Node.exploredContainer[-1]:
            time.sleep(0.2)

    if Node.pathFound == 1:
        for k in path:
            x = -588 + (k[1] * 20)
            y = 288 - (k[0] * 20)
            scarlet.goto(x, y)
            scarlet.stamp()
            scarlet.color("red")
            time.sleep(0.2)

    if Node.pathFound == 0:
        print("\nA solution cannot be found.")

    turtle.exitonclick()


animateMaze = AnimateMaze()
scarlet = Scarlet()
emerald = Emerald()
gold = Gold()

mazeFile = readMaze(os.path.abspath("maze.txt"))
animateFinalPath(mazeFile, search(mazeFile))
