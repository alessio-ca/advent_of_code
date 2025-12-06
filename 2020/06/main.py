from utils import read_input_batch


def main():
    input_file = read_input_batch("2020/06/input.txt")
    # Convert each group of questions into a set and calculate length
    group_questions_size = [
        len(set(list("".join(questions)))) for questions in input_file
    ]
    print(f"Result of part 1: {sum(group_questions_size)}")

    # Convert each questions into a set, calculate intersection
    #  and calculate length
    shared_question_size = [
        len(set.intersection(*map(set, questions))) for questions in input_file
    ]
    print(f"Result of part 2: {sum(shared_question_size)}")


if __name__ == "__main__":
    main()
