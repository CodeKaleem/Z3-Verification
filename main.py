import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "models")))

from models.street_light import test_street_light_logic
from models.traffic_control import test_traffic_light_logic
from models.emergency_response import test_emergency_logic
from models.pedestrian_system import test_pedestrian_button_logic
from models.temporal_traffic import test_temporal_traffic_model

def run_all_unit_tests():
    print("\n[UNIT TESTS] Street Light Logic")
    test_street_light_logic()
    print("\n[UNIT TESTS] Traffic Light Logic")
    test_traffic_light_logic()
    print("\n[UNIT TESTS] Emergency Response Logic")
    test_emergency_logic()
    print("\n[UNIT TESTS] Pedestrian Button Logic")
    test_pedestrian_button_logic()
    print("\n[UNIT TESTS] Temporal Traffic Model")
    test_temporal_traffic_model()

def run_gui():
    os.system("streamlit run gui/streamlit_app.py")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Smart City Z3 Project Main Runner")
    parser.add_argument('--tests', action='store_true', help="Run all unit tests")
    parser.add_argument('--gui', action='store_true', help="Launch Streamlit GUI")
    args = parser.parse_args()

    if args.tests:
        run_all_unit_tests()
    elif args.gui:
        run_gui()
    else:
        print("Usage: python main.py --tests   # Run all unit tests")
        print("       python main.py --gui     # Launch Streamlit GUI")
