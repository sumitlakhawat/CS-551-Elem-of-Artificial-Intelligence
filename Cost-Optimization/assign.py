#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Rajdeep Singh Chauhan rajchauh, Shruti Padole spadole, Sumit Lakhawat slakhawa
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import copy

#check if the goal is reached
def is_goal(total_students, assigned_list, cost, lowest_cost):

    student_list = [item for sublist in [assigned_list[i].split('-') for i in range(0,len(assigned_list))] for item in sublist]

    return total_students == len(student_list) and (lowest_cost > cost or lowest_cost < 0)

#state space, all the possible combinations of all students
def all_successors(students):
    successors={}
    student_names=[]

    student_names = [i['name'] for i in students]

    for i in range(0, len(student_names)):
        successors[student_names[i]] = calculate_cost(student_names[i], students)
        for j in range(i+1, len(student_names)):
            successors[student_names[i]+'-'+student_names[j]] = calculate_cost(student_names[i]+'-'+student_names[j], students)
            for k in range(j+1, len(student_names)):
                successors[student_names[i]+'-'+student_names[j]+'-'+student_names[k]] = calculate_cost(student_names[i]+'-'+student_names[j]+'-'+student_names[k], students)

    return successors

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

    students = []
    with open(input_file, 'r') as file:
        for line in file:
            [name, assign, not_assign] = line.split(' ')
            students.append({"name": name, "assign": assign.split('-')[1:], "not_assign": not_assign[:-1].split(',')})

    # Dictionary with all the possible permutations and their cost
    all_nodes = all_successors(copy.deepcopy(students))
    sorted_all_nodes = []
    for key, value in all_nodes.items():
        sorted_all_nodes.append((value, [key], value / len(key.split('-'))))
    sorted_all_nodes.sort(key=lambda x: x[2], reverse=True)
    sorted_all_nodes = [(sorted_value, sorted_key) for sorted_value, sorted_key, sorting_factor in sorted_all_nodes]

    starting_depth = (len(students) // 3) + (len(students) % 3)
    lowest_cost = -1

    while starting_depth <= len(students):
        fringe = []
        fringe += sorted_all_nodes # fringe.append((value, [key]))
        while fringe:
            cost, assignment_list = fringe.pop()
            if is_goal(len(students), assignment_list, cost, lowest_cost):
                lowest_cost = cost
                yield({"assigned-groups": assignment_list, "total-cost": cost})
            if(len(assignment_list) < starting_depth):
                for (succ, cost) in next_successors(copy.deepcopy(assignment_list), cost, copy.deepcopy(sorted_all_nodes)):
                    fringe.append((cost, succ))
        starting_depth += 1

def next_successors(assignment_list, cost, all_nodes):
    succ = []
    list = []
    for assignment in assignment_list:
        for student in assignment.split("-"):
            list.append(student)
    for value, key in all_nodes:
        student_exists = False
        for student in key[0].split("-"):
            
            if student in list:
                student_exists = True
                break
        if not student_exists:
            succ.append((copy.deepcopy(assignment_list) + key, value + cost))
    return succ

def calculate_cost(group, students):
    people = group.split("-")
    trim_students = {}
    for each in students:
        if each["name"] in people:
            trim_students[each["name"]] = each
    cost = 5
    for student, student_pref in trim_students.items():
        #import pdb; pdb.set_trace()
        members = [one for one in list(trim_students.keys()) if one!=student]
        if len(members) != len(student_pref["assign"]):
            cost += 2
        for each in [one for one in student_pref["assign"] if one not in ['zzz','xxx']]:
            if each not in members:
                cost += 0.05 * 60
        for each in student_pref["not_assign"]:
            if each in members:
                cost += 10
    return cost


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
