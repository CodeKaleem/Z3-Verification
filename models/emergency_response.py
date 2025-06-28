from z3 import *

def emergency_logic():
    """
    Formal contract:
    - Precondition: None (inputs are unconstrained)
    - Postcondition: (is_emergency ↔ siren_on)
    """
    is_emergency = Bool('is_emergency')
    siren_on = Bool('siren_on')

    s = Solver()
    # All logical properties added as Z3 constraints
    s.add(siren_on == is_emergency)
    # Optionally, add Implies for explicitness
    s.add(Implies(is_emergency, siren_on))
    s.add(Implies(Not(is_emergency), Not(siren_on)))
    return s, (is_emergency, siren_on)

def test_emergency_logic():
    s, (is_emergency, siren_on) = emergency_logic()

    # Test: Emergency & siren on (should be SAT)
    s.push()
    s.add(is_emergency == True, siren_on == True)
    assert s.check() == sat, "Emergency and siren should be SAT"
    s.pop()

    # Test: No emergency & siren off (should be SAT)
    s.push()
    s.add(is_emergency == False, siren_on == False)
    assert s.check() == sat, "No emergency and siren off should be SAT"
    s.pop()

    # Test: Emergency but siren off (should be UNSAT)
    s.push()
    s.add(is_emergency == True, siren_on == False)
    assert s.check() == unsat, "Emergency but siren off should be UNSAT"
    s.pop()

    # Test: No emergency but siren on (should be UNSAT)
    s.push()
    s.add(is_emergency == False, siren_on == True)
    assert s.check() == unsat, "No emergency but siren on should be UNSAT"
    s.pop()

if __name__ == "__main__":
    test_emergency_logic()
    print("All emergency logic tests passed.")
