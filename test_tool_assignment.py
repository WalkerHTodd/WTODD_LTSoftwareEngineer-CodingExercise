import pytest
from tool_assignment import Tool, Sample, calc_fit, assign_samples

def test_calc_fit():
    tool = Tool("T1", {"S": 2, "A": 3, "C": 1})
    sample = Sample("M1", {"S": 4, "A": 2, "C": 5}, ["T1"])
    
    assert calc_fit(tool, sample) == (2*4 + 3*2 + 1*5)  # 8 + 6 + 5 = 19

def test_assign_samples():
    tools = {
        "T1": Tool("T1", {"S": 1, "A": 2, "C": 3}),
        "T2": Tool("T2", {"S": 3, "A": 2, "C": 1}),
    }

    samples = [
        Sample("M1", {"S": 1, "A": 1, "C": 1}, ["T2", "T1"]),
        Sample("M2", {"S": 2, "A": 2, "C": 2}, ["T1", "T2"]),
    ]

    assign_samples(tools, samples)

    # Check that each sample is assigned to a tool
    assigned_ids = [sid for tid in tools for sid, _ in tools[tid].assigned]
    assert set(assigned_ids) == {"M1", "M2"}
