from utils import read_input


# Distance travelled and corridors traversed to get from corridor C to room R
paths = {  # (C, R): (distance, cells)
    (0, 0): (3, [1]),
    (0, 1): (5, [1, 2]),
    (0, 2): (7, [1, 2, 3]),
    (0, 3): (9, [1, 2, 3, 4]),
    (1, 0): (2, []),
    (1, 1): (4, [2]),
    (1, 2): (6, [2, 3]),
    (1, 3): (8, [2, 4]),
    (2, 0): (2, []),
    (2, 1): (2, []),
    (2, 2): (4, [3]),
    (2, 3): (6, [3, 4]),
    (3, 0): (4, [2]),
    (3, 1): (2, []),
    (3, 2): (2, []),
    (3, 3): (4, [4]),
    (4, 0): (6, [2, 3]),
    (4, 1): (4, [3]),
    (4, 2): (2, []),
    (4, 3): (2, []),
    (5, 0): (8, [2, 3, 4]),
    (5, 1): (6, [3, 4]),
    (5, 2): (4, [4]),
    (5, 3): (2, []),
    (6, 0): (9, [2, 3, 4, 5]),
    (6, 1): (7, [3, 4, 5]),
    (6, 2): (5, [4, 5]),
    (6, 3): (3, [5]),
}


class State:
    def __init__(self, rooms, corridors=None, score=0):
        self.rooms = tuple(tuple(room) for room in rooms)
        self.corridors = tuple(corridors or (0,) * 7)
        self.score = score or 0

    def __repr__(self):
        return repr((self.rooms, self.corridors, self.score))

    def move(self, corr_i, corr_val, room_i, room_pos, room_val, score):
        rooms = [list(room) for room in self.rooms]
        rooms[room_i][room_pos] = room_val
        corridors = list(self.corridors)
        corridors[corr_i] = corr_val
        return State(rooms, corridors, self.score + score)


def valid_moves(state):
    for corr_i, mover in enumerate(state.corridors):
        if mover:
            room_i = mover - 1
            if all(cell in (0, mover) for cell in state.rooms[room_i]):
                distance, cells = paths[(corr_i, room_i)]
                if not any(state.corridors[cell] for cell in cells):
                    room_pos = state.rooms[room_i].count(0) - 1
                    score = (distance + room_pos) * (10 ** (mover - 1))
                    yield state.move(corr_i, 0, room_i, room_pos, mover, score)

    for room_i in range(4):
        room = state.rooms[room_i]
        if all(cell in (room_i + 1, 0) for cell in room):
            continue
        room_pos = room.count(0)
        mover = room[room_pos]
        for corr_i, occupant in enumerate(state.corridors):
            if not occupant:
                distance, cells = paths[(corr_i, room_i)]
                if not any(state.corridors[cell] for cell in cells):
                    score = (distance + room_pos) * (10 ** (mover - 1))
                    yield state.move(corr_i, mover, room_i, room_pos, 0, score)


def done(state):
    for room_i, cells in enumerate(state.rooms):
        if not all(cell == room_i + 1 for cell in cells):
            return False
    return True


def prune_states(states):
    scores = {}
    for state in states:
        key = (state.rooms, state.corridors)
        if key in scores:
            existing = scores[key]
            if existing.score > state.score:
                existing.score = state.score
        else:
            scores[key] = state
    return scores.values()


def play_game(initial_state):
    done_states = []
    states = [initial_state]
    while states:
        new_states = []
        for state in states:
            for new_state in valid_moves(state):
                if done(new_state):
                    done_states.append(new_state)
                else:
                    new_states.append(new_state)
        states = prune_states(new_states)
    return min(state.score for state in done_states)


def main():
    input_file = read_input("2021/23/example.txt")
    letters = list(zip(input_file[2][3:10:2], input_file[3][3:10:2]))
    d = {"A": 1, "B": 2, "C": 3, "D": 4}
    rooms = [[d[x] for x in row] for row in letters]
    state = State(rooms)
    print(state.rooms)
    print("Part 1:", play_game(state))
    # additions = [(4, 4), (3, 2), (2, 1), (1, 3)]
    # state.rooms = tuple(
    #     (a,) + cells + (b,) for (a, b), cells in zip(state.rooms, additions)
    # )
    # print("Part 2:", play_game(state))


if __name__ == "__main__":
    main()
