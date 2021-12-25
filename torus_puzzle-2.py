''' author: Zonglin Yang
    source: cs540 P2 2020 Spring
    email: zyang439@wisc.edu
    credit help to: Kunlun Wang
                    Piazza
                    a anonymous classmate in 1304 in Monday
                    Github
    Got too many helps, a tough one for me. Should work harder in this course.
'''

import copy
import priorityQueue

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
pq = priorityQueue.PriorityQueue()


# generates the successors of state and returns them in a list of states
def generate_succ(state):
    """stateArray = [chessBoard[0][0], chessBoard[0][1], chessBoard[0][2],
                chessBoard[1][0], chessBoard[1][1], chessBoard[1][2],
                chessBoard[2][0], chessBoard[2][1], chessBoard[2][2]]"""

    """def move_left(state):

        new_state = state[:]
        index = new_state.index(0)
        if index not in [0, 3, 6]:
            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp
        else:
            temp = new_state[index + 2]
            new_state[index + 2] = new_state[index]
            new_state[index] = temp

    def move_right(state):

        new_state = state[:]
        index = new_state.index(0)
        if index not in [2, 5, 8]:
            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp
        else:
            temp = new_state[index - 2]
            new_state[index - 2] = new_state[index]
            new_state[index] = temp
            
    def move_up(state):
        new_state = state[:]
        index = new_state.index(0)
        if index not in [0, 1, 2]:
            temp = new_state[index - 3]
            new_state[index - 3] = new_state[index]
            new_state[index] = temp
        else:
            temp = new_state[index + 6 ]
            new_state[index + 6] = new_state[index]
            new_state[index] = temp
            
    def move_down(state):

        new_state = state[:]
        index = new_state.index(0)
        if index not in [6, 7, 8]:
            temp = new_state[index + 3]
            new_state[index + 3] = new_state[index]
            new_state[index] = temp
        else:
            temp = new_state[index - 6]
            new_state[index - 6] = new_state[index]
            new_state[index] = temp"""

    zero_posi = None  # the position of index 0, which we want to switch

    # finds what index in state that 0 is stored in
    for i in range(len(state)):
        if state[i] == 0:
            zero_posi = i
    states = []

    # move up
    up = zero_posi - 3
    if up < 0:  # if the 0 is at the top line of the chessboard
        up = len(state) + up
    states.append(swap(zero_posi, up, state))

    # move down
    down = zero_posi + 3
    if down >= len(state):  # if the 0 is at the bottom line of the chessboard
        down = down - len(state)
    states.append(swap(zero_posi, down, state))

    # move left
    left = (zero_posi % 3) - 1
    if left >= 0:
        left = zero_posi - 1
    else:
        left = zero_posi + 2
    states.append(swap(zero_posi, left, state))

    # move right
    right = (zero_posi % 3) + 1
    if right <= 2:
        right = zero_posi + 1
    else:
        right = zero_posi - 2
    states.append(swap(zero_posi, right, state))

    # return a list of 4 states
    return states


# swap the values of index1 and index2 and return it as new_state
def swap(index1, index2, state):
    new_state = copy.deepcopy(state)
    new_state[index1] = state[index2]
    new_state[index2] = state[index1]
    return new_state


def print_succ(state):
    states = generate_succ(state)
    states = sorted(states)
    for i in states:
        print(str(i) + " h = " + str(calculate_heu(i)))


# calculates the heuristic for the given state
def calculate_heu(state):
    h = 0
    for i in range(len(state) - 1):
        if i != state[i] - 1:
            h += 1

    return h


''' Original author: Xuyun Yang
    Source: https://github.com/newbieyxy/eight-puzzle/tree/f69eb7c3cc9fcbbbc6522431ba32d82274fbb5d5
    the part of "close" list and solve was inspired by here.
'''

# adds dict_state to closed
def add_to_closed(closed, dic_state):
    new_state = dic_state['state']  # gets the state from state_dict
    added = False

    # compares the state to all items in queue to find a match
    for dic in closed:
        if dic['state'] == new_state:
            # replaces dict in closed if the cost is lower
            if dic_state['f'] >= dic['f']:
                closed.remove(dic)
                closed.append(dic_state)
            added = True

    # if not already in closed list, then add it
    if not added:
        closed.append(dic_state)


''' Original author: JeremyFang11
    Source: https://github.com/JeremyFang11/8-puzzle (Links to an external site.)
    The following function was inspired from the original Java project in github.
'''
def solve(state):
    # solves the 8-torus problem in the least amount of move possible
    # run A* search algorithm

    closed = []  # stores all 'closed' nodes
    global_dic = None  # will store the dictionary of the desired goal state

    # stores the given state as a dictionary and stores it in our priority queue
    state_dict = {'state': state, 'h': calculate_heu(state), 'parent': None, 'g': 0,
                  'f': calculate_heu(state)}
    pq.enqueue(state_dict)


    # finds the goal state through the A* algorithm
    while not pq.is_empty():
        # pops the min-cost element from the queue, adds it to closed, and stores the state
        curr_dict = pq.pop()
        curr_state = curr_dict['state']
        add_to_closed(closed, curr_dict)

        # checks if goal_state is reached
        if curr_state == goal_state:
            global_dic = curr_dict  # stores the goal dictionary
            break

        # generates and enqueues the successor states as dictionaries
        succ_states = generate_succ(curr_state)

        for succ in succ_states:
            enqueue = True
            succ_dict = {'state': succ, 'h': calculate_heu(succ), 'parent': curr_dict['state'],
                         'g': curr_dict['g'] + 1, 'f': calculate_heu(succ) + curr_dict['g'] + 1}
            for closed_dict in closed:
                # compare success and false state
                if closed_dict['state'] == succ_dict['state']:
                    if closed_dict['f'] < succ_dict['f']:
                        enqueue = False
            if enqueue:
                pq.enqueue(succ_dict)

    prev = global_dic
    move = [prev]  # stores the list of move requires to solve the puzzle

    # required to reach the goal state
    num_moves = int(global_dic['f'])
    for i in range(num_moves):
        for curr in closed:
            if curr['state'] == prev['parent']:
                prev = curr  # sets the previous state to the current state
                move.append(curr)  # adds the current to the move list
                break

    # reverses the list of move into the correct order
    move = reversed(move)

    # prints out the desired results
    for j in move:
        print(str(j['state']) + " h= " + str(j['h']) + " move: " + str(j['g']))
    print("Max queue length: " + str(pq.max_len))


def find_dic(state, list):
    # finds and returns the dictionary with the given state

    global dic
    for s in list:
        print(s['state'])
        if state == s['state']:
            dic = s  # sets dict to s if the state is found

    return dic


# solve([4,3,8,5,1,6,7,2,0])
# solve([1,2,3,4,5,6,7,0,8])
# solve([6,3,2,4,0,1,8,5,7])
# solve([8,7,6,5,4,3,2,1,0])
