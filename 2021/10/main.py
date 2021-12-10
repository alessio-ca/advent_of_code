from utils import read_input


def main():
    input_file = read_input("2021/10/input.txt")
    dict_open_close = {"(": ")", "[": "]", "{": "}", "<": ">"}
    points_dict_wrong = {")": 3, "]": 57, "}": 1197, ">": 25137}
    points_dict_incomplete = {")": 1, "]": 2, "}": 3, ">": 4}

    wrong_scores = []
    incomplete_scores = []
    for line in input_file:
        #  Instantiate empty list of opened brackets
        opened = []
        #  Iterate over the line
        for char in line:
            # If char is an opening character, add to list
            if char in dict_open_close.keys():
                opened.append(char)
            else:
                last_open = opened.pop()
                #  If char matches the closing of the last element, continue
                if char == dict_open_close[last_open]:
                    continue
                # Else, line is corrupted. Add score to list & reset the opened list
                else:
                    wrong_scores.append(points_dict_wrong[char])
                    opened = []
                    break
        # If the opened list is not empty, it is an incomplete line
        if len(opened):
            # Obtain closing sequence
            closing_sequence = [dict_open_close[char] for char in opened]
            # Obtain score
            score = 0
            while len(closing_sequence):
                score = (5 * score) + points_dict_incomplete[closing_sequence.pop()]
            incomplete_scores.append(score)

    print(f"Result of part 1: {sum(wrong_scores)}")
    print(
        f"Result of part 2:"
        f" {sorted(incomplete_scores)[int(len(incomplete_scores) / 2)]}"
    )


if __name__ == "__main__":
    main()
