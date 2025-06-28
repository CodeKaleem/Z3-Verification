from z3 import *

def street_light_logic():
    """
    Formal contract:
    - Precondition: None (inputs unconstrained)
    - Postcondition: (light_on ↔ (is_dark ∧ motion))
        - Light is ON if and only if it is dark AND motion is detected.
    """
    is_dark = Bool('is_dark')
    motion = Bool('motion')
    light_on = Bool('light_on')

    s = Solver()
    # Constraint: light_on iff (is_dark and motion)
    s.add(light_on == And(is_dark, motion))
    # Explicit implications for clarity
    s.add(Implies(And(is_dark, motion), light_on))
    s.add(Implies(Not(And(is_dark, motion)), Not(light_on)))

    return s, (is_dark, motion, light_on)

# --- UNIT TESTS ---
def test_street_light_logic():
    s, (is_dark, motion, light_on) = street_light_logic()

    # Dark + motion → light ON (SAT)
    s.push()
    s.add(is_dark == True, motion == True, light_on == True)
    assert s.check() == sat
    s.pop()

    # Not dark or no motion → light OFF (SAT)
    for dark, mot in [(False, True), (True, False), (False, False)]:
        s.push()
        s.add(is_dark == dark, motion == mot, light_on == False)
        assert s.check() == sat
        s.pop()

    # Light ON without both dark and motion (UNSAT)
    for dark, mot in [(False, True), (True, False), (False, False)]:
        s.push()
        s.add(is_dark == dark, motion == mot, light_on == True)
        assert s.check() == unsat
        s.pop()

    # Light OFF when both dark and motion present (UNSAT)
    s.push()
    s.add(is_dark == True, motion == True, light_on == False)
    assert s.check() == unsat
    s.pop()

if __name__ == "__main__":
    test_street_light_logic()
    print("All street light logic tests passed.")
