from z3 import *

def temporal_traffic_model(ticks=4):
    """
    Formal contract:
    - Precondition: ticks >= 2
    - Postcondition:
        1. green[0] == False  (Initially red)
        2. Or(green[1], ..., green[ticks-1])  (Eventually green at some tick)
        3. Not(green[i] and green[i+1]) for all i (no consecutive green)
    """
    assert ticks >= 2, "At least two ticks needed."

    green = [Bool(f"green_{i}") for i in range(ticks)]
    s = Solver()
    # Initially red
    s.add(green[0] == False)
    # Eventually green (at least once, after tick 0)
    s.add(Or([green[i] for i in range(1, ticks)]))
    # No two consecutive greens
    for i in range(ticks - 1):
        s.add(Not(And(green[i], green[i + 1])))

    return s, green

# --- UNIT TESTS ---
def test_temporal_traffic_model():
    ticks = 4
    s, green = temporal_traffic_model(ticks)

    # Test: Initially green[0] is False (required by contract)
    s.push()
    s.add(green[0] == True)
    assert s.check() == unsat, "Tick 0 cannot be green."
    s.pop()

    # Test: At least one later tick is green (SAT if e.g. tick 2 green)
    s.push()
    s.add(green[2] == True)
    assert s.check() == sat, "Tick 2 can be green."
    s.pop()

    # Test: No two consecutive greens (e.g. tick 2 and 3 green is UNSAT)
    s.push()
    s.add(green[2] == True, green[3] == True)
    assert s.check() == unsat, "No two consecutive greens allowed."
    s.pop()

    # Test: All ticks after 0 are not green (UNSAT, violates 'eventually green')
    s.push()
    for i in range(1, ticks):
        s.add(green[i] == False)
    assert s.check() == unsat, "Must be green at least once after tick 0."
    s.pop()

    # Test: Only one tick is green (should be SAT)
    s.push()
    s.add(green[1] == True)
    for i in range(2, ticks):
        s.add(green[i] == False)
    assert s.check() == sat, "Single green at tick 1 should be SAT."
    s.pop()

if __name__ == "__main__":
    test_temporal_traffic_model()
    print("All temporal traffic model tests passed.")
