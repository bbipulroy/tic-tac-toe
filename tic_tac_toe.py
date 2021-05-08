"""
ID:       21170300697
Name:     Bipul Roy
Section:  A
"""
import numpy as np
import sys
from copy import copy

rows = 3
cols = 3

board = np.zeros((rows, cols))
inf = 9999999999
neg_inf = -9999999999


def print_board():
    for i in range(0, rows):
        for j in range(0, cols):
            if board[i, j] == 0:
                sys.stdout.write(' _ ')
            elif board[i, j] == 1:
                sys.stdout.write(' X ')
            else:
                sys.stdout.write(' O ')
        print('')


# for tic Tac Toe the heuris function will be evaluating the board position for each of the winning positions
heuristicTable = np.zeros((rows + 1, cols + 1))
numberOfWinningPositions = rows + cols + 2

for index in range(0, rows + 1):
    heuristicTable[index, 0] = 10 ** index
    heuristicTable[0, index]=-10 ** index

winningArray = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]])
# print('the heuristicTable is ', heuristicTable)
# print('numberOfWinningPositions is ', numberOfWinningPositions)


def utility_of_state(state):
    stateCopy = copy(state.ravel())
    heuristic = 0

    for i in range(0, numberOfWinningPositions):
        maxp = 0
        minp = 0

        for j in range(0, rows):
            if stateCopy[winningArray[i, j]] == 2:
                maxp += 1
            elif stateCopy[winningArray[i, j]] == 1:
                minp += 1
        
        # each iteration of the inner loop evalutes the objective function for each of the winning positions
        heuristic += heuristicTable[maxp][minp]
    # print('heuristic for state ', state, ' is ', heuristic)
    return heuristic


def minimax(state, alpha, beta, maximizing, depth, maxp, minp):
    if depth == 0:
        return utility_of_state(state), state
    
    rowsLeft, columnsLeft = np.where(state == 0)
    returnState = copy(state)

    if rowsLeft.shape[0] == 0:
        return utility_of_state(state), returnState
        
    if maximizing == True:
        utility = neg_inf

        for i in range(0, rowsLeft.shape[0]):
            nextState = copy(state)
            nextState[rowsLeft[i], columnsLeft[i]] = maxp
            # print('in max currently the Nextstate is ', nextState, '\n\n')
            Nutility, Nstate = minimax(nextState, alpha, beta, False, depth - 1, maxp, minp)

            if Nutility > utility:
                utility = Nutility
                returnState = copy(nextState)
            if utility > alpha:
                alpha = utility
            if alpha >= beta :
                # print('pruned')
                break
        
        # print('for max the best move is with utility ', utility, ' n state ', returnState)
        return utility, returnState
    else:
        utility = inf
        for i in range(0, rowsLeft.shape[0]):
            nextState = copy(state)
            nextState[rowsLeft[i], columnsLeft[i]] = minp
            # print('in min currently the Nextstate is ', nextState, '\n\n')

            Nutility, Nstate = minimax(nextState, alpha, beta, True, depth - 1, maxp, minp)
            if Nutility < utility:
                utility = Nutility
                returnState = copy(nextState)
            if utility < beta:
                beta = utility
            if alpha >= beta :
                # print('pruned')
                break
        return utility, returnState


def check_game_over(state):
    stateCopy = copy(state)
    value = utility_of_state(stateCopy)

    if value >= 1000:
        return 1
    else:
        another_check = copy(stateCopy.ravel())
        for winList in winningArray:
            isWin1 = True
            isWin2 = True

            for i in winList:
                isWin1 = isWin1 and another_check[i] == 1.0
                isWin2 = isWin2 and another_check[i] == 2.0
            if isWin1 or isWin2:
                return 1
    return -1


def main():
    print_board()

    print('Please move by command: row<space>column')
    print('row column example: 2 2 (is middle point)')
    print('')
    print('player select example command is 1 or 2')
    print('')

    while True:
        num = input('enter player num (1st or 2nd): ')
        if num.isnumeric() and (num == '1' or num == '2'):
            num = int(num)
            break
        print("Wrong Input")
    value = 0
    global board

    for turn in range(0, rows * cols):
        if (turn + num) % 2 == 1: # make the player go first, and make the user player as 'X'
            input_list = (1, 2, 3)
            while True:
                input_value = input('Enter your move: ').strip().split(' ')
                if len(input_value) == 2 and input_value[0].isnumeric() and input_value[1].isnumeric():
                    r = int(input_value[0])
                    c = int(input_value[1])
                    if r in input_list and c in input_list:
                        break
                print("Wrong Input")
            
            board[r - 1, c - 1] = 1
            print_board()
            value = check_game_over(board)

            if value == 1:
                print('You win. Game Over')
                sys.exit()
            print('\n')
        else: # its the computer's turn make the PC always put a circle'
            # right now we know the state if the board was filled by the other player
            state = copy(board)
            value, nextState = minimax(state, neg_inf, inf, True, 2, 2, 1)
            board = copy(nextState)
            print_board()
            print('\n')
            value = check_game_over(board)

            if value == 1:
                print('PC wins. Game Over')
                sys.exit()
        
    print('Its a draw')


if __name__ == "__main__":
    main()
