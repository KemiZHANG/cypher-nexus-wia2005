# Demo Script

## Opening

Good day everyone. We are Group 8, and our project is Operation Cypher Nexus: The Final Protocol. The mission is divided into eight dataset-driven algorithmic stages plus a final Part 9 creative synthesis. Our Python program reads the real dataset, runs each selected algorithm, and prints a standard explanation for each Part.

During the demo, run the CLI first:

```bash
python cypher_nexus_project.py --all
python cypher_nexus_project.py --part 6
python cypher_nexus_project.py --part 9
python cypher_nexus_project.py --list-data
```

Then open the optional Cyber Mission Control dashboard:

```bash
streamlit run streamlit_app.py
```

If the default Lenovo browser shows garbled text, open the dashboard through Chrome:

```powershell
.\run_dashboard_chrome.ps1
```

The dashboard is only a visualization layer. The real algorithms are implemented in `cypher_nexus_project.py`. Start from the landing page, show the Sequential Review progress, reward tokens/evidence marks, and PENDING / READY / COMPLETED part cards. Explain that alternative algorithm choices are comparison feedback only and do not change official outputs.

Suggested dashboard flow:

1. Run CLI `--all` to generate official TXT/CSV outputs.
2. Show `--list-data` evidence for dataset files, sheets, rows, and columns.
3. Open the dashboard and show the mission overview.
4. Show the Defense Matrix to prove all 9 Parts have dataset or synthesis evidence, candidate algorithms, rejected algorithms, chosen algorithms, outputs, and complexity.
5. Use `Sequential Review Mode` and intentionally choose one alternative algorithm to show the rejection reason.
6. Choose the correct PPT algorithm to show the reward-vault animation, award one reward token/evidence mark, run the official output, and make the result available.
7. Use `Direct Demo Mode` when the teacher wants to skip the sequential review and press `Run All / Show All Results`.
8. Explain one assigned Part in detail while still reminding the teacher that every Part follows the same group-wide evidence structure.
9. End with Part 9 to show how the route, access evidence, optimized targets, and threat ranking combine into the final creative ending.

After each mission, point to the same defense order: Key Takeaway, Why it matters, Mission Brief, Dataset Used, Algorithm Decision, Candidate Algorithms, Rejected Algorithms, Chosen Algorithm, Graphical Algorithm Explanation, Key Result, Visualization, Complexity, Defense Notes, and mission-forward explanation.

## Part 1: The Shadow Network

Mission problem: choose a directed harbour route while balancing distance, risk, and detection. We reject BFS because it ignores weights. We reject standard Dijkstra because it only minimizes distance. Our chosen algorithm is Modified Risk-Aware Dijkstra with this cost formula:

```text
Distance + Risk_Level * 2 + Detection_Probability * 10
```

## Part 2: The Double Agent Registry

Mission problem: detect suspicious identities. We use hash tables for repeated aliases, access keys, and linked sites, then Levenshtein distance for near-duplicate aliases. The output is a ranked suspicion score table.

## Part 3: The Resource Lockdown

Mission problem: select the best checkpoint combination under energy, time, and token constraints. Greedy can miss the best combination, and brute force is too expensive. Dynamic Programming Knapsack gives the best total impact within the limits.

## Part 4: The Probability Trap

Mission problem: choose a route under uncertain risk. We use MCDA Weighted Scoring with Risk 0.40, Time 0.20, and Reward 0.40. Risks are combined using joint risk, then all criteria are normalized before scoring.

## Part 5: The Split Signal Protocol

Mission problem: reconstruct fragmented activation signals. Dynamic programming lets us include valid and useful delayed fragments while skipping corrupted or missing fragments.

## Part 6: The Countdown Sequence - ZHANG YIMING

My assigned part is Part 6. In this stage, the team receives many event records at once inside the control room. The records contain Threat Priority, Timestamp, Zone, Event Type, and Code Value. The challenge is not just sorting one number. It is a multi-field priority sorting problem.

Our sorting rule is:

```text
1. Higher Threat_Priority first
2. Earlier Timestamp first
3. Launch-related Event_Type first
4. Preserve Original_Index if everything else is equal
```

The exact key is:

```text
(-Threat_Priority, Timestamp, Launch_Rank, Original_Index)
```

We use negative Threat Priority because sorting normally places smaller values first, but the mission needs higher threat priority first. Timestamp makes earlier alerts come first when priorities tie. Launch Rank gives launch-related events priority when earlier fields tie. Original Index makes the sort stable.

We chose Modified Stable Merge Sort because it supports multi-field comparison, preserves the original order of equal records, and keeps reliable O(nlogn) performance even when event records are scrambled.

We reject Insertion Sort because the event stream is not guaranteed to be nearly sorted. If many records are scrambled, insertion sort can become O(n^2).

We reject Counting Sort and Radix Sort because our key is mixed. It is not just one integer; it combines priority, timestamp, event type, and original order.

The code manually implements merge sort in `stable_merge_sort_events()`. It does not use Python `sorted()` as the main Part 6 sorting algorithm. The output prints the original event order, sorted event order, and top 5 urgent events.

Demo command:

```bash
python cypher_nexus_project.py --part 6
```

Dashboard flow for Part 6:

1. In Sequential Review Mode, complete Parts 1-5 or switch to Direct Demo Mode for a fast teacher demo.
2. Show Mission Brief: this is a multi-field priority sorting problem.
3. Show Dataset Used: file, sheet, rows, and columns.
4. In the algorithm challenge, show why Insertion Sort and Counting-Radix Sort are rejected.
5. Select `Modified Stable Merge Sort` as the correct PPT algorithm.
6. Show Graphical Algorithm Explanation: input event stream, sorting key, recursive split, stable merge, and urgent output.
7. Show the completion status, evidence marks, and the official Part 6 result.
8. Compare original event order and sorted event order.
9. Show top 5 urgent events and explain the sorting key.
10. Use the urgent-event chart as a quick visual summary, then return to the tables for evidence.
11. Use the Defense Notes to explain why stable sorting matters and why Python `sorted()` is not the main algorithm.

When explaining the whole group project, do not jump only to Part 6. First use the Defense Matrix or Direct Demo Mode to show Parts 1-9 are complete, then zoom into Part 6 as ZHANG YIMING's assigned section.

## Part 7: The Phantom Dice

Mission problem: avoid predictable movement. Controlled randomisation calculates sector risk and decoy-adjusted probability, then chooses a sector with a fixed random seed for repeatable demonstration.

## Part 8: The Silent Code

Mission problem: scan intercepted messages for trigger phrases and rank danger. We use manual brute force string matching because it is simple, explainable, and supports multi-word phrases.

## Part 9: Maximum Disruption Strategy

Part 9 is the final creative ending. It does not need a new Excel dataset. It reuses the official results from Part 1, Part 2, Part 3, and Part 8. The final strategy shows route access, suspicious access evidence, selected high-impact targets, top threat messages, resource usage, and the final maximum disruption result.

## Closing

The final program is presentation-ready because every Part prints the mission problem, selected algorithm, rejected algorithms, dataset or synthesis evidence, result, explanation, and complexity.
