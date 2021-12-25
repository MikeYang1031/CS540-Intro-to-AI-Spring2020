"""
    File name: nqueens.py
    Author: Zonglin Yang
    Project: P3
    course: cs540 Spring2020
    credit: Suyan Qu, Piazza, GeeksforGeeks
"""
import copy
import random


# given a state of the board, return a list of all valid successor states
def succ(state, boulderX, boulderY):
    successors = []

    for i in range(0, len(state)):
        for j in range(0, len(state)):

            if i == boulderX and j == boulderY:
                continue
            elif j is not state[i]:
                # stores a copy of the current state
                successor = copy.deepcopy(state)
                successor[i] = j
                successors.append(successor)

    # print(successors)
    return successors


# got the idea of this method from GeeksforGeeks and github
# https://www.geeksforgeeks.org/python-program-for-n-queen-problem-backtracking-3/ given a state of the board,
# return an integer score such that the goal state scores 0
def f(state, boulderX, boulderY):
    if state is None:
        return 0

    n = len(state)
    attack_queens = [0] * n
    attack = 0

    for i in range(n):
        boulder = False
        for j in range(i + 1, n):
            if state[i] is state[j]:
                if j > boulderX > i and state[j] == boulderY == state[i]:
                    continue
                else:
                    attack_queens[i] = 1
                    attack_queens[j] = 1
            if j == boulderX and (state[i] + j - i == boulderY or
                                  state[i] - j + i == boulderY):
                boulder = True
            if (state[j] == state[i] + j - i or state[j] == state[i] - j + i) != boulder:
                attack_queens[i] = 1
                attack_queens[j] = 1
    for i in range(n):
        if attack_queens[i] == 1:
            attack = attack + 1

    # print(attack)
    return attack


# def choose_next(curr, boulderX, boulderY): # use to check the correctness of my method
#     succ_states = succ(curr, boulderX, boulderY)
#     min_f = f(curr, boulderX, boulderY)
#
#     next_list = [state_dict]
#     lowest_f_states = [curr]
#
#     lowest_f_states = sorted(lowest_fstates)
#     if lowest_fstates[0] == curr:
#         return None
#     print(lowest_fstates[0])
#     return lowest_fstates[0]


# given the current state, use succ() to generate the successors and return the selected next state
def choose_next(curr, boulderX, boulderY):
    successors = succ(curr, boulderX, boulderY)
    successors.append(curr)
    successors = sorted(successors)
    uni_suc = None
    uni_suc_val = len(curr) + 1
    node = False

    for suc in successors:
        suc_f = f(suc, boulderX, boulderY)

        # checks for new unique_successor
        if suc_f < uni_suc_val:
            uni_suc_val = suc_f
            uni_suc = suc
            node = False

        elif suc_f == uni_suc_val:
            node = True

    # if no more unique successor, returns the state with lowest f value
    if not node:
        if uni_suc == curr:
            return None
        return uni_suc

    length = len(successors)
    x = 0
    for i in range(length):
        # removes any state with f value greater than uni_suc_val
        if uni_suc_val < f(successors[x], boulderX, boulderY):
            successors.remove(successors[x])
            x = x - 1
            length = length - 1

        x = x + 1
        if x >= length:
            break

    # if selected next is the given state, returns none
    if successors[0] == curr:
        return None

    return successors[0]


# run the hill-climbing algorithm from a given initial state, return the convergence state
def nqueens(initial_state, boulderX, boulderY):
    curr_state = initial_state
    state_f = f(curr_state, boulderX, boulderY)
    print(curr_state, "- f =", state_f)

    # continue loop
    while True:
        next_state = choose_next(curr_state, boulderX, boulderY)
        state_f = f(next_state, boulderX, boulderY)

        if state_f == 0:
            print("=> ", curr_state)
            return curr_state

        curr_state = next_state
        print(curr_state, "- f =", state_f)


# run the hill-climbing algorithm on an n*n board with random restarts
def nqueens_restart(n, k, boulderX, boulderY):
    initial_state = [0] * n
    print(initial_state)
    best_solu = [] * k
    f_state = 0

    # n = random.randint(1, 8)

    while True:
        for i in range(n):
            initial_state[i] = random.randint(0, n - 1)

        if initial_state[boulderX] is not boulderY:
            state = nqueens(initial_state, boulderX, boulderY)
            f_state = f(state, boulderX, boulderY)

            if f_state == 0:
                print(state)
                return 0
            best_solu.append(state)
            k = k - 1

        if k == 0:
            break

    best_solu = sorted(best_solu)
    m = len(best_solu)
    for i in range(m):
        print(best_solu[i])
    return f_state


# def random_test():
#     n = random.randint(1, 8)
#
#     # k = random.randint(10 * n, 20 * n)
#
#     boulderX = random.randint(0, n - 1)
#     boulderY = random.randint(0, n - 1)
#
#     print(nqueens_restart(n, k, boulderX, boulderY))

# choose_next([1, 1, 2], 0, 0)
# nqueens_restart(8, 5, 1, 1)
# nqueens([0, 2, 2, 3, 4, 5, 6, 7], 1, 1)
# nqueens([0,1,2,3,5,5,6,7], 4, 4)
# succ([1, 1, 2], 0, 0)
