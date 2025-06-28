import streamlit as st

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from z3 import *
from models.street_light import street_light_logic
from models.traffic_control import traffic_light_logic
from models.emergency_response import emergency_logic
from models.pedestrian_system import pedestrian_button_logic
from models.temporal_traffic import temporal_traffic_model

st.set_page_config(page_title="Smart City Formal Verification", layout="centered")
st.title("🚦 Smart City Formal Verification Dashboard")

st.markdown("""
Select a logic module, choose input values, and verify the system properties with formal Z3 SMT solving.  
Each module returns either **SAT** (logic holds) or **UNSAT** (violation detected).
""")

# --- Helper to display Z3 results ---
def show_z3_result(title, solver):
    result = solver.check()
    st.subheader(f"{title} Result: {result}")
    if result == sat:
        model = solver.model()
        st.code("\n".join([f"{d} = {model[d]}" for d in model.decls()]), language="python")
    elif result == unsat:
        st.error("No valid model exists (UNSAT).")
    else:
        st.warning("Could not determine satisfiability.")

# --- Tabs for each module ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Street Light", "Traffic Light", "Emergency", "Pedestrian", "Temporal Traffic"
])

with tab1:
    st.header("Street Light Logic")
    is_dark = st.checkbox("Is it dark?", value=True)
    motion = st.checkbox("Motion detected?", value=True)
    light_on = st.checkbox("Light should be ON?", value=True)
    if st.button("Verify Street Light Logic"):
        s, (dark, mot, light) = street_light_logic()
        s.add(dark == is_dark, mot == motion, light == light_on)
        show_z3_result("Street Light Logic", s)

with tab2:
    st.header("Traffic Light Logic")
    laneA = st.checkbox("Lane A green?", value=True)
    laneB = st.checkbox("Lane B green?", value=True)
    if st.button("Verify Traffic Light Logic"):
        s, (a, b) = traffic_light_logic()
        s.add(a == laneA, b == laneB)
        show_z3_result("Traffic Light Logic", s)

with tab3:
    st.header("Emergency Response Logic")
    is_em = st.checkbox("Is emergency?", value=True)
    siren_on = st.checkbox("Siren ON?", value=False)
    if st.button("Verify Emergency Logic"):
        s, (em, siren) = emergency_logic()
        s.add(em == is_em, siren == siren_on)
        show_z3_result("Emergency Logic", s)

with tab4:
    st.header("Pedestrian Button Logic")
    btn_pressed = st.checkbox("Button Pressed?", value=True)
    ped_green = st.checkbox("Pedestrian Green Light?", value=True)
    if st.button("Verify Pedestrian Logic"):
        s, (btn, green) = pedestrian_button_logic()
        s.add(btn == btn_pressed, green == ped_green)
        show_z3_result("Pedestrian Button Logic", s)

with tab5:
    st.header("Temporal Traffic Model")
    ticks = st.slider("Number of ticks (steps)", min_value=3, max_value=8, value=4)
    user_set = st.checkbox("Manually set green/red for each tick")
    s, green = temporal_traffic_model(ticks)
    user_bools = []
    if user_set:
        st.write("Set green/red state for each tick:")
        for i in range(ticks):
            state = st.checkbox(f"Tick {i}: Green?", key=f"green_{i}")
            user_bools.append(state)
        if st.button("Verify Temporal Traffic Logic"):
            for i in range(ticks):
                s.add(green[i] == user_bools[i])
            show_z3_result("Temporal Traffic Logic", s)
    else:
        if st.button("Check Existential Solution (Model)"):
            show_z3_result("Temporal Traffic Logic", s)

st.markdown("---")
st.info("Built with Z3, Streamlit, and Python • Formal Verification for Smart Cities 🚦")

