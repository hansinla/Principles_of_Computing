# IDA* solving of 15-puzzle
import math
import random
import time

#globals
CELLS=16
SIDE=4

#for blank in lower right
#vindx = [0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4]
#hindx = [0,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3]
#goal1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
#vgoal = tuple([1,1,1,1,2,2,2,2,3,3,3,3,0,4,4,4])

#for blank in upper left
vindx = [0,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
hindx = [0,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
goal1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
vgoal = tuple([0,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4])

#4x4 puzzles
p9 = [6,7,8,14,10,0,1,5,9,12,2,13,15,3,11,4] #52 moves blank lower right
p9r = [12,5,13,1,3,14,4,7,11,15,0,6,2,8,9,10] #52 moves blank upper left
p80 = [0,12,9,13,15,11,10,14,3,7,2,5,4,8,6,1] #80 moves blank lower right
p80r = [15,11,8,12,14,10,9,13,2,6,1,4,3,7,5,0] #80 moves blank upper left

puzzle = p9r

###############################################

def vert_only(perm1):
    """
    return perm of vert numbers only for Walking Distance
    sorted by row
    0 is blank, 1 is first row
    """

    perma = [vindx[perm1[i]] for i in range(CELLS)]
    for j in range(4):
        perma[j*4:(j+1)*4] = sorted(perma[j*4:(j+1)*4])
    return tuple(perma)

def horiz_only(perm1):
    """
    return perm of horiz numbers only for Walking Distance
    transposed and sorted by row
    """
    transpose = [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]

    perma = [hindx[perm1[transpose[i]]] for i in range(CELLS)]
    for j in range(4):
        perma[j*4:(j+1)*4] = sorted(perma[j*4:(j+1)*4])
    return tuple(perma)

def solve_vert():
    """
    exhaustive BFS counting up and down movements for Walking Distance
    """
    global w_distance
    neighbor = [[4,5,6,7],[4,5,6,7],[4,5,6,7],[4,5,6,7],[0,1,2,3,8,9,10,11],[0,1,2,3,8,9,10,11],[0,1,2,3,8,9,10,11],[0,1,2,3,8,9,10,11], \
                [4,5,6,7,12,13,14,15],[4,5,6,7,12,13,14,15],[4,5,6,7,12,13,14,15],[4,5,6,7,12,13,14,15],[8,9,10,11],[8,9,10,11],[8,9,10,11],[8,9,10,11]]
    level = 0
    current = []
    current.append(vgoal)
    while len(current) > 0:
        level += 1
        #print level, len(current)
        next = []
        for perm1 in current:
            w_distance[perm1] = level - 1
            card1 = perm1.index(0)
            for card2 in neighbor[card1]:
                perm2 = list(perm1)
                perm2[card1] = perm2[card2]
                perm2[card2] = 0
                j1 = card1 // 4
                perm2[j1*4:(j1+1)*4] = sorted(perm2[j1*4:(j1+1)*4])
                j2 = card2 // 4
                if j1 != j2:
                    perm2[j2*4:(j2+1)*4] = sorted(perm2[j2*4:(j2+1)*4])
                perm3 = tuple(perm2)
                if perm3 not in w_distance and perm3 not in next: 
                    next.append(perm3)
        current = next
    return None
  
def is_solvable(perm, goal):
    """
    determine by parity if goal is reachable from perm
    """
    idx = [0] * len(perm)
    for i in goal:
        idx[goal[i]] = i
    count = 0
    #parity of initial vs goal state
    for i in range(CELLS):
        for j in range(i+1,CELLS):
            if idx[perm[i]] > idx[perm[j]]:
                count += 1
    #parity of blank positions
    b1 = perm.index(0)
    b2 = goal.index(0)
    count += (b1 // SIDE) - (b2 // SIDE)
    count += (b1 % SIDE) - (b2 % SIDE)
    return (count % 2 ==0)

def mdist(perm):
    """
    score manhattan distance from goal
    do not count distance of blank
    """
    targs = [(0,0) for i in range(len(goal1))]
    for i in range(len(goal1)):
        targs[goal1[i]] = (i % SIDE, i // SIDE)
    dist = 0
    for i in range(len(perm)):
        if perm[i] > 0:
            dist += abs(i % SIDE - targs[perm[i]][0])
            dist += abs(i // SIDE - targs[perm[i]][1])
    return dist

def hdist(perm):
    """
    finds heuristic value of perm 
    using Walking Distance
    """
    val = w_distance[vert_only(perm)]
    val += w_distance[horiz_only(perm)]
    return val

def search(perm1, g, bound, prev):
    """
    IDA search
    """
    global path
    dir = ["u","r","d","l"]
    neighbor = [[-1,1,4,-1],[-1,2,5,0], [-1,3,6,1], [-1,-1,7,2], [0,5,8,-1], [1,6,9,4], [2,7,10,5], [3,-1,11,6], [4,9,12,-1], [5,10,13,8], [6,11,14,9], [7,-1,15,10], [8,13,-1,-1], [9,14,-1,12], [10,15,-1,13], [11,-1,-1,14]]
    f = g + hdist(perm1)
    if f > bound:
        return f
    if perm1 == goal1:
        return 0   #FOUND
    min_t = 1000000000 #infinity
    card1 = perm1.index(0)
    for k in range(4):
        card2 = neighbor[card1][k]
        if card2 > -1:
            if perm1[card2] != prev:
                perm2 = list(perm1)
                perm2[card1] = perm2[card2]
                perm2[card2] = 0
                #path[g] = card2
                path[g] = dir[k]
                threshold = search(perm2, g + 1, bound, perm1[card2])
                if threshold == 0:
                    return 0
                if threshold < min_t:
                    min_t = threshold
    return min_t

def ida_star(perm):
    """
    IDA*
    """
    bound = hdist(perm)
    while True:
        threshold = search(perm, 0, bound, -1)
        print ("threshold", threshold)
        if threshold == 0:
            return 0
        if threshold == 1000000000:
            return None #not found
        bound = threshold

w_distance = dict()
path = ["x"] * 88 #max path
idx = [0] * CELLS
for i in goal1:
    idx[goal1[i]] = i
print ("building walking distance table")
solve_vert()
print ("is solvable ", is_solvable(puzzle,goal1))
print ("Manhattan Distance = ", mdist(puzzle))
print ("Walking Distance = ", hdist(puzzle))
time0 = time.clock()
ida_star(puzzle)
k = 0
out = ""
while (k<80 and path[k] != "x"):
    out += path[k]
    k += 1
print (out)
time1 = time.clock()
print ("time: ", time1 - time0)
