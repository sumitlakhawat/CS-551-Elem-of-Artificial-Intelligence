#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        st= [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]
        #print(st)
        return st

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        #Find my location, i.e. '@' location
        dest=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
        possible_moves_dict={}
        path=[]
        fringe=[(pichu_loc,0)]

        while fringe:
                (curr_move, curr_dist)=fringe.pop(0)
                possible_moves=moves(house_map, *curr_move)
                possible_moves_dict[curr_move]=possible_moves
                for move in possible_moves:
                        if house_map[move[0]][move[1]]=="@":
                                return (curr_dist+1, find_path(find_key(dest,possible_moves_dict,path),dest))  # return the answer
                        else:   
                                if (move, curr_dist + 1) not in fringe:
                                        fringe.append((move, curr_dist + 1))
                if (curr_dist) >= len(house_map) * len(house_map[0]):
                       return -1

#finds path from destination to initial location of pichu. 
def find_key(dest,possible_moves_dict,path):
        try:
                for i in range (0,len(list(possible_moves_dict.values()))):
                        if dest in list(possible_moves_dict.values())[i]:
                                dest=list(possible_moves_dict.keys())[i]
                                path.append(dest)
                                possible_moves_dict.pop(dest)
                                find_key(dest,possible_moves_dict,path)
                        else:
                                pass
        except:
                return path
        return path

#finds path required in desired format
def find_path(path,dest):
        letter_path=''
        try:
                path.reverse()
                path.append(dest)
                for i in range(0, len(path)-1):
                        if path[i][0] > path[i+1][0]:
                                letter_path = letter_path + 'U'
                        elif path[i][0] < path[i+1][0]:
                                letter_path = letter_path + 'D'
                        if path[i][1] < path[i+1][1]:
                                letter_path = letter_path + 'R'
                        elif path[i][1] > path[i+1][1]:
                                letter_path = letter_path + 'L'
                return letter_path
        except Exception as e:
                raise e
        
                                            

                              

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])

        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(solution)

