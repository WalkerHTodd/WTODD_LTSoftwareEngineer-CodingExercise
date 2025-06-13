from typing import Dict, List, Tuple

# Your task is to write code to assign material samples to tools such that, once they have
# been scheduled on a tool, no sample could be moved to a different tool that a customer
# would prefer more and be a better fit for it than any sample already scheduled on it.
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
        # Explore the file line by line
        for line in file:
            line = line.strip()

            parts = line.split()

            if parts[0] == 'T':
                # print("Parsing Tool:", parts)
                tool_id = parts[1]
                metrics = {}
                for part in parts[2:]:
                    key, value = part.split(':')
                    # print (f"Metric Key: {key}, Value: {value}")
                    metrics[key] = int(value)
                tools[tool_id] = Tool(tool_id, metrics)

            elif parts[0] == 'M':
                # print("Parsing Sample:", parts)
                sample_id = parts[1]
                needs = {}
                idx = 2
                while ':' in parts[idx]:
                    key, value = parts[idx].split(':')
                    # print(f"Need Key: {key}, Value: {value}")
                    needs[key] = int(value)
                    idx += 1
                preferences = parts[idx].split('>')
                # print(f"Sample ID: {sample_id}, Needs: {needs}, Preferences: {preferences}")
                samples.append(Sample(sample_id, needs, preferences))

    return tools, samples


# Dot Product Calculation (In directions)
def calc_fit(tool: Tool, sample: Sample) -> int:
    s_score = tool.metrics['S'] * sample.needs['S']
    a_score = tool.metrics['A'] * sample.needs['A']
    c_score = tool.metrics['C'] * sample.needs['C']
    
    total_score = s_score + a_score + c_score
    return total_score

# Original Version – Rank-Based Passes
# Per Tool, Per Rank, One Sample per Loop
# Each tool would pick one sample per preference rank pass.

# Final Version – Global Loop, Preference-Aware
# Key Fix:
# No more rank-based passes.
# Loop until all samples are assigned.
# Each iteration picks the globally best (fit score + preference-aware) assignment.
def assign_samples(tools: Dict[str, Tool], samples: List[Sample]):
    max_per_tool = len(samples) // len(tools)
    assigned = {}

    # dictionary that tracks which samples are assigned to each tool.
    for tool_id in tools:
        assigned[tool_id] = []

    assigned_samples = set()

    # Keep looping until all samples have been assigned.
    while len(assigned_samples) < len(samples):
        candidates = []
        
        # Find all possible candidates for this round:
        for sample in samples:
            if sample.id in assigned_samples:
                continue
            # For each unassigned sample:
            # We go through their tool preference list in order, and only consider the top-most tool that still has space.
            for pref_rank, tool_id in enumerate(sample.preferences):
                if len(assigned[tool_id]) >= max_per_tool:
                    continue

                score = calc_fit(tools[tool_id], sample)
                # negate pref_rank so that lower preference values sort higher (0 is best).
                candidates.append((score, -pref_rank, sample, tool_id))
                break  # only consider top-most preferred tool with room

        # Pick best candidate
        if not candidates:
            break
        
        # Got Help with using ai to write the lambda function
        # Sort candidates by score (descending) and preference rank (ascending)
        # We want the highest score and the lowest preference rank (best preference)
        candidates.sort(reverse=True, key=lambda x: (x[0], x[1]))  # max score, then best pref
        # take the top result
        best_score, _, sample, tool_id = candidates[0]
        # assign it to the
        assigned[tool_id].append((sample.id, best_score))
        assigned_samples.add(sample.id)
        print(f"Assigned {sample.id} (score {best_score}) to {tool_id}")

    for tid in tools:
        tools[tid].assigned = sorted(assigned[tid], key=lambda x: -x[1])


def write_output(tools: Dict[str, Tool], filepath: str):
    with open(filepath, "w") as file:
        for tool_id in sorted(tools):
            file.write(tool_id + ": ")
            for sample_id, score in tools[tool_id].assigned:
                file.write(f"{sample_id}({score}) ")
            file.write("\n")


if __name__ == '__main__':
    tools, samples = parse_input('sample_input.txt')
    assign_samples(tools, samples)
    write_output(tools, 'tool_assignment_output.txt')
    print("Output written to tool_assignment_output.txt")
