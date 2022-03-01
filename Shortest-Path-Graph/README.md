## Part 1: Navigation - 

# Code when the solution exists-

In route_pichu.py, we read the input file and convert the file into list of characters. Now we find the location(coordinates) of pichu given in the map and we put the location and the distance travelled from this location in a fringe. The fringe here used is a Queue where each element in that is combination of current state and distance travelled from pichu to this state. Now pop the first element of the fringe and check all the possible states from that element. Possible directions we can go are up, down, right and left only if that direction has a '.' or '@' in it. All the possible states we append in the fringe if it is not present already. We keep doing this till the fringe is not empty or if we stumble upon '@' in our fringe. We return the path and distance travelled when we encounter '@'.

Now to find the correct path out of all the traversed path, we first find the location of out destination, which is coordinates of '@'. What I have done now is created a dictionary where key is the location(coordinates) and values is the all possible moves from there. To find the coordinates path, we first call the find_key function which will return the correct path but in coordinates form. Then we pass the output of this function to find_path() function which will then output the path in desired form like 'UURRDL..'

In find_key function, I'm checking the location of '@', which is stored in 'dest' variable, in all the values of the dictionary, once I find it in any values part of the dictionary, I append the key of that in the path list variable and call this function again with this key as the new destination('dest' variable). I'm also popping out the coordinate from the dictionary once it is appended in the path list variable to avoid extra iterations. This function calls itself recursively untill it reaches the location of pichu. Now we have the coordinated path.

Now, we call the find_path, which takes input path list variable returned from find_key function. This function will give us the path in desired format. Since the path list we got was in reverse order, we call the reverse() function on it and then traverse it to convert it to letter format. For that, we check the x and y coordinated of elements next to each other in the list. If the x coordinate of ith element is less than x coordinate of (i+1)th element, that means we have travelled in the right direction, so we append 'R' to the letter_path variable and letter 'L' for vice versa. Similarly, if y coordinate of ith element is greater than (i+1)th coordinate, then we have travelled upwards, so we append 'U' and for vice versa, we append letter 'D'. We return this letter_path.


# For the inputs when there is no solution-

When there is no solution, it goes into infinte loop as the fringe keeps appending and the path distance keep increasing. To avoid that, I have written a condition that if the path distance from 'p' to '@' goes beyond the maximun distance that is possible then return -1 and break the loop. In any given matrix of (NXM), the maximum distance that we can travel will be NXM. The maximum distance in any matrix will be when you traverse all the points in the matrix. That will be equal to N*M. So no distance between two points in any matrix can be more than that. So if the traversed distance variable in our code, which is curr_dist, goes beyond NXM, we break the loop as there were no solution possible.


---------------------------------------------------------------------------------------------------------------


## Part 2: Hide-and-seek -

# Code when the solution exists

In arrange_pichus.py, we take 2 inputs, map file and number of pichus and we convert the map file into list of characters. Here we take a fringe which is a list of states where each state is the next successor state. 

The state space is all the possible states where pichu can be placed. 
Initial state here is the current map file given where we have 1 pichu and number of 'X'. 
Goal state is the state where all the k pichus are places in such a way that none of them are in the same row, column or diagonal unless there is a 'X' or '@' between them.
Successor function determines the next state we are going to consider. Here the successor function checks if the new 'p' that is being inserted in the map is in the correct location or not, i.e satisfies the required condition to place a pichu.

Now, we start with the initial state and call the successors() function on that. This function calls add_pichu(). We pass the parameters(r,c) to this function which are the exact location where we want to add the 'p'. Now this r and c are determined in successors() function before calling add_pichu(). To find out the correct coordinate where adding a 'p' will still satisfy the successor function, we take this coordinate and call three functions on it- check_row(), check_column() and check_diagonal(). If all of them return True and the current r and c position is '.' then we call the add_pichu() function which adds a 'p' on location(r,c).
We do this till we add number of 'p' equal to the number of pichus that we were given in the program input and once that is done, we return the map. 

Now, in check_row() funciton, I am taking (r,c) position and traversing through the columns for a particular r value and checking on both sides of c. That is, traversing left of c till start of the row and traversing right of c till end of row to check if the the row satisfies the required condition that there is no other 'p' in that row or if there is, then there is a 'X' or '@' between the them. If yes, then I return True, meaning that 'p' can be inserted in that position if we were to just check that particular Row and nothing else.

Similarly, I do the same with check_column() function. We traverse through the rows and check for a particular column. On the coordinate(r,c), we check top of r till beginning of the column and down of r till end of the column. If the particular column satisfies the required condition, we return True, meaning that 'p' can be inserted in that position if we were to just check that particular Column and nothing else.

check_diagonal() also works in similar way, only here I check in 4 possible direcions from point (r,c). To travel diagonally, I used zip() function which takes 2 arguments and matches both the arguments simultaneously which allowed me to write both the arguments in such a way that row and column both get incremented/decremented together so it would move diagonally and only one for loop is used. In check_diagonal(), from a point, I am checking in four directions, i.e, top_left, top_right, bottom_left and bottom_right. The code checks in all directions and returns True if it is allowed to insert a 'p' in the location, meaning that 'p' can be inserted in that position if we were to just check diagonally on that point and nothing else.

Now, if all these 3 functions return True, that means the point satisfies all the conditions and 'p' can be inserted in that point. Now we call add_pichu() with this location(r,c). It adds the 'p' and then we append this new state to our fringe.

And once, we reach the required number of 'p', we return the Map.


# When we try to insert n number of 'p' but only (n-1) are possible

In this case, no solution exists. So to find that, we realize that once the while loop iterates for (n-1) number of 'p', there are no more positions left in the map where it can insert more 'p'. So there are no more addition to the fringe and the while loop runs till we pop all the elements in the fringe. So once the fringe is empty, we know that there is no solution possible, so we return False.
