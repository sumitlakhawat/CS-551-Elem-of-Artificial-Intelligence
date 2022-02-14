#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if (house_map[r][c] == '.' and check_row(house_map, r, c) and check_column(house_map, r, c) and check_diagonal(house_map, r, c))]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

#check on left and right of the current position(R,C)
def check_row(house_map, R, C):
    
    left=right=True
    for c in range(C, -1, -1):
        if house_map[R][c] == 'p':
            left= False
            break
        elif house_map[R][c] == 'X' or house_map[R][c] == '@':
            left= True
            break
        elif house_map[R][c] == '.':
            continue

    for c in range(C, len(house_map[R])):
        if house_map[R][c] == 'p':
            right= False
            break
        elif house_map[R][c] == 'X' or house_map[R][c] == '@':
            right= True
            break
        elif house_map[R][c] == '.':
            continue
    return left and right

#check up and down on the current position(R,C)
def check_column(house_map, R, C):
    
    up=down=True
    for r in range(R, -1, -1):
        if house_map[r][C] == 'p':
            up= False
            break
        elif house_map[r][C] == 'X' or house_map[r][C] == '@':
            up= True
            break
        elif house_map[r][C] == '.':
            continue

    for r in range(R, len(house_map)):
        if house_map[r][C] == 'p':
            down= False
            break
        elif house_map[r][C] == 'X' or house_map[r][C] == '@':
            down= True
            break
        elif house_map[r][C] == '.':
            continue
    return up and down

#check diagonally in all four directions of current position(R,C)
def check_diagonal(house_map, R, C):
    
    bott_left=bott_right=top_left=top_right=True

    #check in bottom left direction of the point
    for r, c in zip(range(R, len(house_map)), range(C, -1, -1)):
            if house_map[r][c] == 'p':
                bott_left= False
                break
            elif house_map[r][c] == 'X' or house_map[r][c] == '@':
                bott_left= True
                break
            elif house_map[r][c] == '.':
                continue

    #check in top right direction of the point
    for r, c in zip(range(R, -1, -1), range(C, len(house_map[R]))):

            if house_map[r][c] == 'p':
                top_right= False
                break
            elif house_map[r][c] == 'X' or house_map[r][c] == '@':
                top_right= True
                break
            elif house_map[r][c] == '.':
                continue

    #check in bottom right direction of the point
    for r, c in zip(range(R, len(house_map)), range(C, len(house_map[R]))):

            if house_map[r][c] == 'p':
                bott_right= False
                break
            elif house_map[r][c] == 'X' or house_map[r][c] == '@':
                bott_right= True
                break
            elif house_map[r][c] == '.':
                continue

    #check in top left direction of the point
    for r, c in zip(range(R, -1, -1), range(C, -1, -1)):

            if house_map[r][c] == 'p':
                top_left= False
                break
            elif house_map[r][c] == 'X' or house_map[r][c] == '@':
                top_left= True
                break
            elif house_map[r][c] == '.':
                continue

    return top_left and top_right and bott_left and bott_right

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    if(k==1):
        return(initial_house_map,True)
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            fringe.append(new_house_map)
    return (None,False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else False)
    
