## Choosing Teams

### Problem Statement
- Iteratively generate a list of groups of students that has a lower cost than the previously yielded grouping based on the student preferences and cost rules:
- **Goal State** : Sum of students in all groups should be equal to number of entries in the test file.
- **Student Preferences** : Every student provides the following info -
    - The ideal group size they would like to work in. 
    - A hyphen separated string of students they wish to work with (If group size is 2 or more). If they have no preference, then they fill in 'xxx', 'zzz'. We are assuming that only *'xxx' or 'zzz'* will be used to indicate no preference
    - A comma separated string of students they wish NOT to work with. 
- **Cost Rules** :
    - Each group assignment takes 5 mintues to correct.
    - If a person is assigned a group size that they did not originally want, cost gets incremented by 2 mintues.
    - If a person is not grouped with the person they asked for, cost gets incremented by 3 minutes(product of 5% probabality and the the 60-minute time window taken to resolve Academic integrity issues).
    - If a person is assigned a group member they specifically asked NOT to be grouped with, the cost incremented by 10 minutes.

### Design Decisions
- Created all combinations of 1 student, 2 student and 3 student groups possible for students.
- Calculated cost for each of the combination using the cost information provided.
- Sorted this permutation list according to the dimension -> (cost_of_assignment/number_of_person_in_group)
- Applied DFS on the dataset such that, the fringe will always try to pop least cost(calculated above in sorted list) possible node from the sorted list.
- Since DFS can go till the depth of number of students, we limited depth to - ceiling of total_number_of_students / 3. Thus applied IDA.

- Currently, it is not using Local Search since test cases are getting threshold values. So we can implement local search using below approach:-
    - We can stop the DFS process after certain time limit, check the last popped assignment_list, get the 0th index assignment.
    - remove all assignments in the sorted list after the index of this 0th index assigment in sorted list.
    - This will reduce the size of our sorted_list and again start the DFS process with this sorted list.

### Solution Review

- Final Solution
    - __Abstraction Used__ :- IDA
    - __Set of Valid States__, list of student assignments with no student repeating in any assignment
    - __Successor Function__, Each successor will have each combination of all combination with constraint that no similar student present in list is inserted.
    - __Goal State__ Sum of assignment_costs less than previously yielded total cost and assignment list should contain all students.
