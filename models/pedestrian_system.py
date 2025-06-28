from z3 import *

def pedestrian_button_logic():
    """
    Formal contract:
    - Precondition: None (inputs unconstrained)
    - Postcondition: (button_pressed ↔ pedestrian_green)
        - If button is pressed, pedestrian green must be on.
        - If button not pressed, pedestrian green must be off.
    """
    button_pressed = Bool('button_pressed')
    pedestrian_green = Bool('pedestrian_green')

    s = Solver()
    # Main constraint: pedestrian_green iff button_pressed
    s.add(pedestrian_green == button_pressed)
    # Explicitly: both implications (redundant, but clear)
    s.add(Implies(button_pressed, pedestrian_green))
    s.add(Implies(Not(button_pressed), Not(pedestrian_green)))

    return s, (button_pressed, pedestrian_green)

# --- UNIT TESTS ---
def test_pedestrian_button_logic():
    s, (button_pressed, pedestrian_green) = pedestrian_button_logic()

    # Test: Button pressed, pedestrian green (SAT)
    s.push()
    s.add(button_pressed == True, pedestrian_green == True)
    assert s.check() == sat, "Button pressed & green should be SAT"
    s.pop()

    # Test: Button NOT pressed, pedestrian NOT green (SAT)
    s.push()
    s.add(button_pressed == False, pedestrian_green == False)
    assert s.check() == sat, "Button not pressed & green off should be SAT"
    s.pop()

    # Test: Button pressed, pedestrian NOT green (UNSAT)
    s.push()
    s.add(button_pressed == True, pedestrian_green == False)
    assert s.check() == unsat, "Button pressed but green off should be UNSAT"
    s.pop()

    # Test: Button NOT pressed, pedestrian green (UNSAT)
    s.push()
    s.add(button_pressed == False, pedestrian_green == True)
    assert s.check() == unsat, "Button not pressed but green on should be UNSAT"
    s.pop()

if __name__ == "__main__":
    test_pedestrian_button_logic()
    print("All pedestrian button logic tests passed.")
