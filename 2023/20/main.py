from collections import defaultdict

import numpy as np

from utils import read_input


class ModuleSelector(object):
    @staticmethod
    def factory(string):
        if string[0] == "%":
            return FlipFlop(string)
        elif string[0] == "&":
            return Conjunction(string)
        else:
            return Broadcaster(string)


class AbstractModule:
    def __init__(self, string) -> None:
        m_type, send_to = [x.strip() for x in string.split("->")]
        self.id = m_type[1:]
        self.send_to = [x.strip() for x in send_to.split(",")]
        self.dict_status: defaultdict = defaultdict(lambda: False)


class FlipFlop(AbstractModule):
    type = 0
    status = 0


class Conjunction(AbstractModule):
    type = 1


class Broadcaster(AbstractModule):
    type = 2


class ModuleProcess:
    flag = False

    def __init__(self, modules) -> None:
        self.modules = modules
        self.high = 0
        self.low = 0
        self.i = 0
        self.seeds = self.find_conjunctions()
        self.seeds_dict: defaultdict[str, list] = defaultdict(list)
        self.initialise_conjunctions()

    def find_conjunctions(self):
        # Find latest conjunctions before 'lx'
        # 'lx' feeds directly to 'rx' -
        #  when 'lx' inputs are all high, low pulse goes to 'rx'
        #  (only relevant for part 2)
        seeds = []
        for module in self.modules.values():
            if "lx" in module.send_to:
                seeds.append(module.id)
        return seeds

    def initialise_conjunctions(self):
        # Initialise conjunctions
        map_nodes = {module.id: module.send_to for module in self.modules.values()}
        for module in self.modules.values():
            if module.type == 1:
                for key, value in map_nodes.items():
                    if module.id in value:
                        module.dict_status[key] = False

    def process_pulse(self, input_pulse):
        module_id, pulse, orig_id = input_pulse

        if pulse:
            self.high += 1
        else:
            self.low += 1

        if module_id in ["output", "rx"]:
            return

        module = self.modules[module_id]
        if module.type == 2:  # broadcaster
            pulse_output = pulse
        elif module.type == 1:  # conjunction
            module.dict_status[orig_id] = pulse
            if all(module.dict_status.values()):
                pulse_output = False
            else:
                pulse_output = True
            if module_id in self.seeds:
                # Check when module is high
                if pulse_output:
                    # Since self i is not updated until cycle is finished, add one
                    self.seeds_dict[module_id].append(self.i)

        else:  # flipflop
            if not pulse:
                if not module.status:
                    module.status = True
                    pulse_output = True
                else:
                    module.status = False
                    pulse_output = False
        try:
            return [(o_module, pulse_output, module.id) for o_module in module.send_to]
        except NameError:
            pass

    def process_cycle(self):
        outputs = self.process_pulse(("roadcaster", False, "button"))
        self.i += 1
        while outputs:
            new_outputs = []
            for output in outputs:
                try:
                    new_outputs += self.process_pulse(output)
                except TypeError:
                    pass
            outputs = new_outputs
        # Check if process flag can be activated
        if len(self.seeds_dict) == 4 and [
            all(lists for lists in self.seeds_dict.values())
        ]:
            self.flag = True
        pass


def main(filename: str):
    modules_list = [ModuleSelector.factory(row) for row in read_input(filename)]
    modules = {module.id: module for module in modules_list}
    process = ModuleProcess(modules)

    for _ in range(1000):
        process.process_cycle()

    print(f"Result of part 1: {process.low * process.high}")

    # Iterate until you find all seeds.
    # You only need the first occurrence - seeds sequences are fully periodic
    while not process.flag:
        process.process_cycle()

    res = np.lcm.reduce([el[0] for el in process.seeds_dict.values()])
    print(f"Result of part 2: {res}")


if __name__ == "__main__":
    main("2023/20/input.txt")
