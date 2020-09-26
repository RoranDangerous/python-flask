import sys
import random

def main(width, height, field):
    width = int(width)
    height = int(height)
    head_position = -1
    for i in range(len(field)):
        if field[i] == 'H':
            head_position = i


    moves = {
        'UP': next_up(width, height, head_position, field),
        'DOWN': next_down(width, height, head_position, field),
        'LEFT': next_left(width, height, head_position, field),
        'RIGHT': next_right(width, height, head_position, field)
    }

    possible_moves = []
    for move in moves:
        if moves[move] == 'F':
            print(move)
            return

        if moves[move] == 'E':
            possible_moves.append(move)

    if not possible_moves:
        print('')
    else:
        print(possible_moves[random.randint(0, len(possible_moves) - 1)])

def next_up(width, height, head_position, field):
    next_i = head_position - width
    if next_i < 0:
        return ''

    return field[next_i]

def next_down(width, height, head_position, field):
    next_i = head_position + width
    if next_i >= len(field):
        return ''

    return field[next_i]

def next_left(width, height, head_position, field):
    next_i = head_position - 1
    if int(next_i / width) != int(head_position / width):
        return ''

    return field[next_i]

def next_right(width, height, head_position, field):
    next_i = head_position + 1
    if int(next_i / width) != int(head_position / width):
        return ''

    return field[next_i]


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:])