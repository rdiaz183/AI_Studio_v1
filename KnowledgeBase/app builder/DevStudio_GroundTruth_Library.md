# AI DEV STUDIO: GROUND-TRUTH ENGINEERING & PHYSICS SPECIFICATION
**Project**: Project Code510 (New York State Racing Sim)
**Engine**: Unreal Engine 5.4+ (Chaos Vehicles, Nanite, Lumen)

---

## 1. Chaos Vehicle Physics & Damper Standards
All generated suspension setups must adhere strictly to these physical units:
- **Spring Rate**: Measured in N/cm or N/mm. Standard street cruiser: 200–350 N/mm; Track/Pursuit: 380–500 N/mm.
- **Rebound Damping (Extension)**: Must always be 25%–35% higher than Compression Damping to prevent uncontrolled chassis oscillation.
- **Compression Damping**: 250–350 N/mm for damp/uneven asphalt; 400+ N/mm for smooth race circuits.
- **Anti-Roll Bar (Stiffness)**: Front ARB should exceed Rear ARB by 10%–15% on high-speed cruisers to induce predictable understeer rather than snap oversteer.

---

## 2. Pacejka Tire Friction Calibration Table (Magic Formula)
Tire friction multipliers in Project Code510:
- **Dry Clean Asphalt**: Peak Lateral = 1.15–1.25, Longitudinal = 1.10–1.20
- **Damp Asphalt (Mist / Light Rain)**: Peak Lateral = 0.85–0.92, Longitudinal = 0.75–0.82
- **Heavy Rain / Standing Water**: Peak Lateral = 0.60–0.70 (Aquaplaning threshold > 65 mph)
- **Autumn Wet Leaves (Adirondacks)**: Friction coefficient drops to 0.45–0.55
- **Black Ice / Winter Slush**: Friction coefficient = 0.15–0.25

---

## 3. New York State Track & Geometry Constraints
- **Adirondack Pass**: Max road grade: 12%; Switchback banking angle: 4°–8°; Road width: 2 lanes (7.4 meters total).
- **Taconic State Parkway**: Rolling hills with continuous elevation undulations; tight median grass strips; minimum sight distance 150m at 70 mph.
- **Manhattan Urban Grid**: 90° intersections; asphalt with embedded metal utility plates; friction variance 15% on painted crosswalks.

---

## 4. C++ & Blueprint Architecture Rules
- All vehicle classes inherit from `AWheeledVehiclePawn`.
- Physics calculations must be executed inside `PhysicsTick` or sub-stepped to avoid frame-rate-dependent handling bugs.
- All telemetry broadcasts must emit standard JSON-RPC frames over port 9876 or UDP port 20777.