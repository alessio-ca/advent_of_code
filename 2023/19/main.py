import math
import re

from utils import read_input_batch


def create_flow_dict(worflows):
    flow_dict = dict()
    for flow in worflows:
        f_id, rules = flow[:-1].split("{")
        rules_dict = dict([rule.split(":") for rule in rules.split(",")[:-1]])
        end_rule = rules.split(",")[-1]
        flow_dict[f_id] = {"rules": rules_dict, "end": end_rule}
    return flow_dict


def format_flow_dict(flow_dict):
    for outer_key, inner_dict in flow_dict.items():
        rules = inner_dict["rules"]
        formatted_rules = []
        for key, value in rules.items():
            new_key, thr = re.split("<|>", key)
            thr = int(thr)
            if "<" in key:
                formatted_rules.append((new_key, value, 1, thr))
            elif ">" in key:
                formatted_rules.append((new_key, value, thr + 1, 4000 + 1))
        flow_dict[outer_key]["rules"] = formatted_rules
    return flow_dict


def process_part(part, workflows):
    x, m, a, s = part
    flow_id = "in"
    while flow_id != "A" and flow_id != "R":
        for rule, new_id in workflows[flow_id]["rules"].items():
            if eval(rule):
                flow_id = new_id
                break
        else:
            flow_id = workflows[flow_id]["end"]

    return x + m + a + s if flow_id == "A" else 0


def process_range(flow_dict):
    # Each ranges dict is of the form {tag: range}
    # Tags can be xmas, range is a tuple (bottom inclusive, top exclusive)
    ranges_dict = {k: (1, 4001) for k in ["x", "m", "a", "s"]}
    flow_id = "in"
    accepted = []
    queue = [(flow_id, ranges_dict)]
    while queue:
        flow_id, ranges_dict = queue.pop()

        if flow_id == "A":
            accepted.append(ranges_dict)
            continue
        elif flow_id == "R":
            continue

        # Loop over rules of current `flow_id`
        for tag, id_dest, map_root, map_end in flow_dict[flow_id]["rules"]:
            unmapped = []
            input_root, input_end = ranges_dict[tag]

            if (lower_end := min(input_end, map_root)) > input_root:
                unmapped.append((tag, (input_root, lower_end)))

            # Check if a mapped cut exists
            middle_cut = (max(input_root, map_root), min(map_end, input_end))
            if middle_cut[1] > middle_cut[0]:
                queue.append(
                    (id_dest, generate_new_segment(tag, middle_cut, ranges_dict))
                )

            if input_end > (upper_end := max(map_end, input_root)):
                unmapped.append((tag, (upper_end, input_end)))

            # Update ranges dict with the unmapped cuts
            for key, cut in unmapped:
                ranges_dict[key] = cut

        # The surviving dict get propagated to the last condition
        queue.append((flow_dict[flow_id]["end"], ranges_dict))
    return accepted


def generate_new_segment(tag, cut, orig_dict):
    new_ranges_dict = orig_dict.copy()
    new_ranges_dict[tag] = cut
    return new_ranges_dict


def calculate_combinations(intervals_dict):
    n = 0
    for result_dict in intervals_dict:
        n += math.prod([y - x for x, y in result_dict.values()])
    return n


def main(filename: str):
    workflows, parts = [row for row in read_input_batch(filename)]
    parsed_parts = [tuple(map(int, re.findall(r"\d+", part))) for part in parts]
    flow_dict = create_flow_dict(workflows)
    total_n = 0
    for part in parsed_parts:
        total_n += process_part(part, flow_dict)
    print(f"Result of part 1: {total_n}")
    range_flow_dict = format_flow_dict(flow_dict)
    print(f"Result of part 2: {calculate_combinations(process_range(range_flow_dict))}")


if __name__ == "__main__":
    main("2023/19/input.txt")
