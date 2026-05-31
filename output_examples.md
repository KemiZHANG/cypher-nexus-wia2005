# Output Examples

Generated with:

```bash
python cypher_nexus_project.py --all
```

## Standard Output Format

Every Part now prints:

- Mission Problem
- Algorithm Used
- Rejected Algorithms
- Dataset
- Key Result
- Result Explanation
- Time and Space Complexity
- Detailed Output

## Dataset Evidence

Example from Part 6:

```text
dataset file: Part 6.xlsx
dataset source: D:\Datasets (2).zip
sheet name: A
row count: 10
columns used: Event_ID, Threat_Priority, Timestamp, Zone, Event_Type, Code_Value
```

## Part 1

```text
Selected route:
Port Authority Hub -> Warehouse A -> Safe House 1 -> Financial Vault Access

Total distance: 15
Total risk: 9
Total detection: 0.31
Total modified cost: 36.1
```

## Part 2

Top suspicious identities include:

```text
A2876 Falcon_1 score 12
A3102 Raven score 12
A5127 Cipher score 12
A8044 Cipher score 12
A9012 Viper score 12
```

## Part 3

```text
Selected checkpoints:
- Disable Camera Grid
- Jam Patrol Drone Relay
- Disrupt Escape Route Beacon
- Upload False Navigation Beacon

Total energy used: 15 / 15
Total time used: 33 / 35
Total tokens used: 4 / 4
Total operational impact: 46
```

## Part 4

```text
Chosen route: R3 - Cable-Car Line
Final score: 0.600
```

## Part 5

```text
Final activation sequence:
CNX-44 M13-76 X7P-91 TR5-11 KR9-31 LP4-62 ZZ1-20 AX2-55
```

## Part 6

Top 5 urgent events:

```text
E091 Threat 5 04:20:10 Thermal Alarm
E104 Threat 5 04:21:15 Biometric Alert
E087 Threat 4 04:19:58 Drone Entry
E103 Threat 4 04:21:11 Patrol Shift
E095 Threat 3 04:20:25 Override Attempt
```

Part 6 also confirms:

```text
The project implements merge sort manually through stable_merge_sort_events();
it does not rely on Python sorted() as the sorting algorithm for Part 6.
```

## Part 7

```text
Highest probability sectors:
S6 probability 0.273
S2 probability 0.199
S4 probability 0.136

Chosen sector with seed 2005: S4
```

## Part 8

```text
M04 Critical score 7
Detected phrases: silent code, shadow key, final protocol
Route tag: GRID-HUB-B2
```

## Generated Files

Important TXT files:

```text
outputs/part1_shadow_network.txt
outputs/part2_double_agent_registry.txt
outputs/part3_resource_lockdown.txt
outputs/part4_probability_trap.txt
outputs/part5_split_signal_protocol.txt
outputs/part6_countdown_sequence.txt
outputs/part7_phantom_dice.txt
outputs/part8_silent_code.txt
outputs/data_mapping_report.txt
```

Important CSV files include:

```text
outputs/part2_double_agent_registry_suspicious_identities.csv
outputs/part3_resource_lockdown_selected_checkpoints.csv
outputs/part4_probability_trap_route_scores.csv
outputs/part6_countdown_sequence_top_five.csv
outputs/part7_phantom_dice_sector_scores.csv
outputs/part8_silent_code_ranked_messages.csv
```

## Dashboard View

Run:

```bash
streamlit run streamlit_app.py
```

The landing page shows:

```text
Operation Cypher Nexus: The Final Protocol
Algorithmic Mission Control Dashboard
Sequential review progress, reward tokens, and evidence marks
8 part cards with PENDING / READY / COMPLETED status
Defense Matrix covering Parts 1-8
```

Sequential Review Mode shows three algorithm choices per Part. An alternative choice shows the rejection reason and does not unlock or overwrite official outputs. A correct choice marks the Part completed, awards one reward token/evidence mark, runs the official Part runner, and makes the result available.

Direct Demo Mode provides:

```text
Run All / Show All Results
All Parts 1-8 results without algorithm-selection steps
```

Helpful dashboard charts:

```text
Part 2: suspicion score chart
Part 3: resource usage chart/progress bars
Part 4: route final score chart
Part 6: urgent-event priority chart plus original/sorted/top-5 tables
Part 7: sector probability chart
Part 8: threat score chart
```

Each Part page follows:

```text
Key Takeaway
Why it matters
Mission Brief
Dataset Used
Algorithm Decision
Candidate Algorithms
Rejected Algorithms
Chosen Algorithm
Key Result
Visualization
Time and Space Complexity
Defense Notes
How this moves the mission forward
```

Defense Matrix columns:

```text
Part
Dataset
Problem Type
Candidate Algorithms
Rejected Algorithms
Chosen Algorithm
Key Output
Complexity
```
