def test_output_matches_expected():
    with open("tool_assignment_output.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    expected = [
        "T0: M5(161) M11(154) M2(128) M4(122)",
        "T1: M9(23) M8(21) M7(20) M1(18)",
        "T2: M6(128) M3(120) M10(86) M0(83)"
    ]
    assert lines == expected
