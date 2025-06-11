from typing import Dict, List, Tuple

class Tool:
    def __init__(self, id: str, metrics: Dict[str, int]):
        self.id = id
        self.metrics = metrics
        self.assigned: List[Tuple[str, int]] = []

class Sample:
    def __init__(self, id: str, needs: Dict[str, int], preferences: List[str]):
        self.id = id
        self.needs = needs
        self.preferences = preferences

def parse_input(filepath: str) -> Tuple[Dict[str, Tool], List[Sample]]:
    tools = {}
    samples = []

    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'T':
                tool_id = parts[1]
                metrics = {kv.split(':')[0]: int(kv.split(':')[1]) for kv in parts[2:]}
                tools[tool_id] = Tool(tool_id, metrics)

            elif parts[0] == 'M':
                sample_id = parts[1]
                needs = {}
                idx = 2
                while ':' in parts[idx]:
                    k, v = parts[idx].split(':')
                    needs[k] = int(v)
                    idx += 1
                preferences = parts[idx].split('>')
                samples.append(Sample(sample_id, needs, preferences))

    return tools, samples

def calc_fit(tool: Tool, sample: Sample) -> int:
    return sum(tool.metrics[k] * sample.needs[k] for k in ['S', 'A', 'C'])

def assign_samples(tools: Dict[str, Tool], samples: List[Sample]):
    max_per_tool = len(samples) // len(tools)
    assigned = {tid: [] for tid in tools}
    assigned_samples = set()

    while len(assigned_samples) < len(samples):
        candidates = []

        for sample in samples:
            if sample.id in assigned_samples:
                continue

            for pref_rank, tool_id in enumerate(sample.preferences):
                if len(assigned[tool_id]) >= max_per_tool:
                    continue

                score = calc_fit(tools[tool_id], sample)
                # Lower preference rank is better — we sort by (-score, pref_rank)
                candidates.append((score, -pref_rank, sample, tool_id))
                break  # only consider top-most preferred tool with room

        # Pick best candidate
        if not candidates:
            break

        candidates.sort(reverse=True, key=lambda x: (x[0], x[1]))  # max score, then best pref
        best_score, _, sample, tool_id = candidates[0]
        assigned[tool_id].append((sample.id, best_score))
        assigned_samples.add(sample.id)
        print(f"✅ Assigned {sample.id} (score {best_score}) to {tool_id}")

    for tid in tools:
        tools[tid].assigned = sorted(assigned[tid], key=lambda x: -x[1])




def write_output(tools: Dict[str, Tool], filepath: str):
    with open(filepath, "w") as f:
        for tool_id in sorted(tools.keys()):
            line = f"{tool_id}: " + " ".join(f"{sid}({score})" for sid, score in tools[tool_id].assigned)
            f.write(line + "\n")

if __name__ == '__main__':
    tools, samples = parse_input('sample_input.txt')
    assign_samples(tools, samples)
    write_output(tools, 'tool_assignment_output.txt')
    print("✅ Output written to tool_assignment_output.txt")
