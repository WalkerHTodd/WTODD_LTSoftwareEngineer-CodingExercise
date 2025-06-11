from typing import Dict, List, Tuple
from collections import defaultdict

# Tool class: holds an ID and a dictionary of its metrics (speed, accuracy, cost)
class Tool:
    def __init__(self, id: str, metrics: Dict[str, int]):
        self.id = id
        self.metrics = metrics
        self.assigned: List[Tuple[str, int]] = []  # list of (sample_id, fit_score)

# Sample class: holds an ID, its testing needs, and tool preferences
class Sample:
    def __init__(self, id: str, needs: Dict[str, int], preferences: List[str]):
        self.id = id
        self.needs = needs
        self.preferences = preferences

# Parse input file and build tools and samples from the data
def parse_input(filepath: str) -> Tuple[Dict[str, Tool], List[Sample]]:
    tools = {}      # holds all tools indexed by ID
    samples = []    # list of Sample objects

    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()

            # Tool line: starts with T, then tool ID, then metrics
            if parts[0] == 'T':
                tool_id = parts[1]
                metrics = {
                    kv.split(':')[0]: int(kv.split(':')[1]) for kv in parts[2:]
                }  # turn S:5 A:6 C:7 into a dict
                tools[tool_id] = Tool(tool_id, metrics)

            # Sample line: starts with M, then sample ID, then needs + preferences
            elif parts[0] == 'M':
                sample_id = parts[1]
                needs = {}
                idx = 2
                # keep pulling metric:value until we hit preferences (which don't have ':')
                while ':' in parts[idx]:
                    key, val = parts[idx].split(':')
                    needs[key] = int(val)
                    idx += 1
                # Preferences are listed like T2>T1>T3 — split them into a list
                preferences = parts[idx].split('>')
                samples.append(Sample(sample_id, needs, preferences))

    return tools, samples

# A sample’s fit for a tool is calculated by the dot product of the tool’s metrics and the
# sample’s need for those metrics.
def calc_fit(tool: Tool, sample: Sample) -> int:
    return sum(tool.metrics[k] * sample.needs[k] for k in ['S', 'A', 'C'])

# Assign each sample to the first preferred tool that has space
def assign_samples(tools: Dict[str, Tool], samples: List[Sample]):
    tool_list = list(tools.keys())
    max_samples = len(samples) // len(tool_list)
    assigned = defaultdict(list)

    for s in samples:
        for preferred_tool in s.preferences:
            if len(assigned[preferred_tool]) < max_samples:
                score = calc_fit(tools[preferred_tool], s)
                assigned[preferred_tool].append((s.id, score))
                break  # only assign once

    # Save assignments to each Tool object
    for tid in tool_list:
        tools[tid].assigned = assigned[tid]

# Write out the tool assignments to a file
def write_output(tools: Dict[str, Tool], filepath: str):
    with open(filepath, 'w') as f:
        for tid in sorted(tools.keys()):
            line = f"{tid}: " + ' '.join(f"{sid}({fit})" for sid, fit in tools[tid].assigned)
            f.write(line + '\n')

# Run everything
if __name__ == '__main__':
    input_path = 'sample_input.txt'
    output_path = 'tool_assignment_output.txt'

    tools, samples = parse_input(input_path)
    assign_samples(tools, samples)
    write_output(tools, output_path)
    print(f"Output written to {output_path}")
