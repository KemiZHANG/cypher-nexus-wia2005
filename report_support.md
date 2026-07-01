# Report Support Notes

## Presentation-Ready Structure

The optimized program prints a consistent explanation for every Part: Mission Problem, Algorithm Used, Rejected Algorithms, Dataset, Key Result, Result Explanation, and Time and Space Complexity. This makes the implementation easier to defend because the code output directly matches the report and presentation criteria.

## Dataset Handling

The loader reads the real dataset ZIP when available. It detects Excel header rows, standardizes column names, and records the mapping from original dataset columns to algorithm fields. The generated `outputs/data_mapping_report.txt` shows this mapping for every Part.

If a dataset file, sheet, or required column is missing, the program raises a helpful error that lists the missing item and available columns or sheets. This avoids unclear raw `KeyError` messages.

## Part 1: Modified Risk-Aware Dijkstra

The harbour network is modelled as a directed weighted graph. Each route uses the cost formula `Distance + Risk_Level * 2 + Detection_Probability * 10`. This keeps the selected algorithm aligned with the PPT because it balances safety and speed instead of optimizing distance only. Time complexity is O((V+E)logV), and space complexity is O(V+E).

## Part 2: Two-Stage Hybrid Verification

The registry is processed using hash tables for exact repeated evidence and Levenshtein distance for near-duplicate aliases. Suspicion scoring ranks identities by repeated alias, repeated access key, near-duplicate alias, repeated linked site, and suspicious or missing status. The result is saved as TXT and CSV.

## Part 3: Dynamic Programming Knapsack

The checkpoint problem is solved as a multi-resource knapsack. The DP state tracks energy, time, and token usage, and stores the best impact for each feasible state. This rejects greedy selection because a local best checkpoint can block a better combination later.

## Part 4: MCDA Weighted Scoring

The route decision uses MCDA with Risk 0.40, Time 0.20, and Reward 0.40. Multiple risk probabilities are combined using joint risk. Risk and time are normalized as cost criteria, while reward is normalized as a benefit criterion.

## Part 5: Dynamic Programming Signal Reconstruction

Fragments are grouped, ordered by sequence number, and evaluated using dynamic programming. Valid fragments are worth more, delayed fragments can still contribute, and corrupted or missing fragments are skipped. This explains why greedy and topological sort are weaker for this dataset.

## Part 6: Modified Stable Merge Sort

The event feed is sorted using the key `(-Threat_Priority, Timestamp, Launch_Rank, Original_Index)`. Higher threat priority comes first, earlier timestamp breaks ties, launch events are prioritized next, and original index preserves stability.

The implementation manually performs merge sort in `stable_merge_sort_events()`. It does not use Python `sorted()` as the Part 6 sorting algorithm. The output prints original order, sorted order, and top 5 urgent events so the sorting logic can be explained directly from the result.

## Part 7: Controlled Randomisation

The program calculates risk from patrol frequency, thermal scan level, drone coverage, and prediction penalty. It then converts decoy-adjusted scores into probabilities and uses a fixed seed for repeatable demonstration. This balances safety and unpredictability.

## Part 8: Brute Force String Matching

The scanner manually checks each trigger phrase against every possible position in each message. Detected phrases add weighted threat points, and route tags add an intelligence bonus. Messages are ranked by final threat score and saved as TXT and CSV.

## Part 9: Maximum Disruption Strategy

Part 9 is the creative ending required by the project brief. It does not introduce a new dataset file. Instead, it synthesizes previous official outputs: Part 1 route access, Part 2 suspicious access evidence, Part 3 dynamic-programming target selection, and Part 8 threat ranking.

The chosen method is Integrated DP Final Strategy. Narrative-only ending is rejected because it is not tied to evidence. Greedy highest-threat selection is rejected because it ignores the resource constraints already handled by Part 3. The output shows the final phase plan, top threats, selected targets, resource usage, final effects, and saved TXT/CSV evidence.

## Streamlit Mission-Control Dashboard

`streamlit_app.py` is an optional visualization layer. It imports and reuses `cypher_nexus_project.py`, displays the same algorithm explanations, and shows tables and simple charts for review. It does not replace the CLI or duplicate the core algorithm logic. Dashboard copy and group-wide metadata are kept in `dashboard_content.py`, reusable UI pieces are kept in `dashboard_components.py`, and language text is kept in `dashboard_i18n.py`.

The dashboard uses a professional Cyber Mission Control style: landing page, part cards, progress, completion badges, execution log, and next-part navigation. These elements support the project context but do not change the algorithms or turn the project into a real game.

Sequential Review Mode adds algorithm-choice prompts, PENDING / READY / COMPLETED progression, reward tokens, evidence marks, and final completion feedback. These are stored in Streamlit `session_state` and do not move, duplicate, or change algorithm logic. Alternative choices explain why the selected algorithm was rejected. Correct choices call the existing official runner for that Part, award one reward token/evidence mark, and make the result available.

Direct Demo Mode provides `Run All / Show All Results` when the group wants to skip the sequential review flow and display Parts 1-9 immediately.

The polished dashboard keeps a consistent defense order for all Parts: Key Takeaway, Why it matters, Mission Brief, Dataset Used, Algorithm Decision, Candidate Algorithms, Rejected Algorithms, Chosen Algorithm, Graphical Algorithm Explanation, Key Result, Visualization, Time and Space Complexity, Defense Notes, and How this result moves the mission forward. The graphical explanation uses flowchart-style nodes to show input, processing, algorithm steps, and output for every Part. Charts are added only where they clarify the algorithm result: suspicion scores, resource usage, route scores, urgent event priority, sector probabilities, threat scores, and Part 9 target impact.

The final completion page confirms all 9 Parts completed, total reward tokens/evidence marks, final project summary, View All Outputs, and Restart Review.

The Defense Matrix summarizes Part, Dataset or synthesis source, Problem Type, Candidate Algorithms, Rejected Algorithms, Chosen Algorithm, Key Output, Complexity, and Defense Notes for Parts 1-9. This is the main group-project evidence page, so the dashboard does not appear to focus only on Part 6.

Every Part page follows the same defense-friendly structure. Part 6 remains clear with original order, sorted order, top 5 urgent events, sorting key explanation, manual merge sort confirmation, and stable sorting notes, and Part 9 clearly shows how the final ending is derived from earlier outputs.
