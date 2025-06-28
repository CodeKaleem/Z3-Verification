from z3 import *

def traffic_light_logic():
    """
    Formal contract:
    - Precondition: None (inputs unconstrained)
    - Postcondition: NOT (laneA_green ∧ laneB_green)
        - Both lanes cannot be green together.
    """
    laneA_green = Bool('laneA_green')
    laneB_green = Bool('laneB_green')

    s = Solver()
    # Main constraint: Mutual exclusion
    s.add(Not(And(laneA_green, laneB_green)))
    # Redundant explicit: If one green, other not necessarily off; both red allowed.
    return s, (laneA_green, laneB_green)

# --- UNIT TESTS ---
def test_traffic_light_logic():
    s, (laneA_green, laneB_green) = traffic_light_logic()

    # Test: Both green (UNSAT)
    s.push()
    s.add(laneA_green == True, laneB_green == True)
    assert s.check() == unsat
    s.pop()

    # Test: Lane A green, Lane B not (SAT)
    s.push()
    s.add(laneA_green == True, laneB_green == False)
    assert s.check() == sat
    s.pop()

    # Test: Lane A not green, Lane B green (SAT)
    s.push()
    s.add(laneA_green == False, laneB_green == True)
    assert s.check() == sat
    s.pop()

    # Test: Both red (SAT)
    s.push()
    s.add(laneA_green == False, laneB_green == False)
    assert s.check() == sat
    s.pop()

if __name__ == "__main__":
    test_traffic_light_logic()
    print("All traffic light logic tests passed.")
