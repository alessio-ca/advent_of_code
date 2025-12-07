import operator
import types

from scipy.optimize import fsolve

from utils import read_input

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}  # etc.


def create_monkeys(input_file):
    monkeys = {}
    for line in input_file:
        key, job = tuple(line.split(": "))
        if job.isdigit():
            monkeys[key] = int(job)
        else:
            monkeys[key] = tuple(job.split(" "))
    return monkeys


def branch(key, monkeys):
    job = monkeys[key]
    if isinstance(job, int):
        return job
    elif isinstance(job, types.LambdaType):
        return job
    else:
        aa, opp, bb = job
        return apply_operator(monkeys, aa, opp, bb)


def apply_operator(monkeys, a, op, b):
    if isinstance(a, types.LambdaType):
        job_a = a
    else:
        job_a = branch(a, monkeys)

    if isinstance(a, types.LambdaType):
        job_b = b
    else:
        job_b = branch(b, monkeys)

    # Check which one is the function
    fun_a = isinstance(job_a, types.LambdaType)
    fun_b = isinstance(job_b, types.LambdaType)
    if op == "=":
        # Find candidate by solving the equation (f(x) - k = 0)
        if fun_a:
            k, fun = job_b, job_a
        else:
            k, fun = job_a, job_b

        return int(fsolve(lambda x: fun(x) - k, k))

    elif fun_a:
        return lambda x: ops[op](job_a(x), job_b)
    elif fun_b:
        return lambda x: ops[op](job_a, job_b(x))

    res = ops[op](job_a, job_b)
    return int(res) if isinstance(res, float) else res


def main(filename: str):
    input_file = read_input(filename, line_strip=True)
    monkeys = create_monkeys(input_file)
    print(f"Result of part 1: {apply_operator(monkeys, *monkeys['root'])}")

    root_a, _, root_b = monkeys["root"]
    monkeys["root"] = (root_a, "=", root_b)
    monkeys["humn"] = lambda x: x
    print(f"Result of part 2: {apply_operator(monkeys, *monkeys['root'])}")


if __name__ == "__main__":
    main("2022/21/input.txt")
