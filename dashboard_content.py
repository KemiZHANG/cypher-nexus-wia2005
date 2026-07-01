"""Dashboard metadata for the Cypher Nexus Streamlit dashboard.

This file contains only dashboard copy and analysis metadata. Official
algorithms, dataset loading, and saved outputs remain in cypher_nexus_project.py.
"""

from cypher_nexus_project import DEFAULT_SHEETS, PART_FILE_NAMES, PART_INFO, TOTAL_PARTS


ALGORITHM_CHOICES = {
    1: {
        "options": ["BFS", "Standard Dijkstra", "Modified Risk-Aware Dijkstra"],
        "correct": "Modified Risk-Aware Dijkstra",
        "wrong_feedback": {
            "BFS": "BFS is rejected because it treats all routes as equal and cannot model distance, risk, or detection.",
            "Standard Dijkstra": "Standard Dijkstra is rejected because it optimizes a single cost instead of the mission's risk-aware modified cost.",
        },
    },
    2: {
        "options": ["Linear Search", "Hash Table only", "Two-Stage Hybrid Verification"],
        "correct": "Two-Stage Hybrid Verification",
        "wrong_feedback": {
            "Linear Search": "Linear Search is rejected because repeated pairwise checking is too slow for a growing registry.",
            "Hash Table only": "Hash Table only is rejected because exact matching misses near-duplicate aliases.",
        },
    },
    3: {
        "options": ["Greedy Selection", "Brute Force", "Dynamic Programming Knapsack"],
        "correct": "Dynamic Programming Knapsack",
        "wrong_feedback": {
            "Greedy Selection": "Greedy Selection is rejected because a locally efficient checkpoint can block a better final combination.",
            "Brute Force": "Brute Force is rejected because checking every subset grows exponentially.",
        },
    },
    4: {
        "options": ["Expected Value", "MCDA Weighted Scoring", "Risk-Adjusted Return"],
        "correct": "MCDA Weighted Scoring",
        "wrong_feedback": {
            "Expected Value": "Expected Value is rejected because it can hide travel time and one-time survival constraints.",
            "Risk-Adjusted Return": "Risk-Adjusted Return is rejected because a very safe but low-reward route may fail the mission objective.",
        },
    },
    5: {
        "options": ["Greedy", "Dynamic Programming", "Topological Sort"],
        "correct": "Dynamic Programming",
        "wrong_feedback": {
            "Greedy": "Greedy is rejected because it can skip delayed fragments that are still recoverable.",
            "Topological Sort": "Topological Sort is rejected because ordering alone does not decide which fragments should be included.",
        },
    },
    6: {
        "options": ["Insertion Sort", "Counting-Radix Sort", "Modified Stable Merge Sort"],
        "correct": "Modified Stable Merge Sort",
        "wrong_feedback": {
            "Insertion Sort": "Insertion Sort is rejected because the event stream is not guaranteed to be nearly sorted and can degrade to O(n^2).",
            "Counting-Radix Sort": "Counting/Radix Sort is rejected because the key mixes priority, timestamp, launch relevance, and original order.",
        },
    },
    7: {
        "options": ["Deterministic Best Route", "Pure Random", "Controlled Randomisation"],
        "correct": "Controlled Randomisation",
        "wrong_feedback": {
            "Deterministic Best Route": "Deterministic Best Route is rejected because repeated optimal moves become predictable.",
            "Pure Random": "Pure Random is rejected because it ignores surveillance risk and decoy value.",
        },
    },
    8: {
        "options": ["KMP only", "Regex/Search only", "Brute Force String Matching + Threat Ranking"],
        "correct": "Brute Force String Matching + Threat Ranking",
        "wrong_feedback": {
            "KMP only": "KMP only is rejected because the mission also needs transparent threat ranking after phrase detection.",
            "Regex/Search only": "Regex/Search only is rejected because it does not explain the selected PPT algorithm or ranking logic clearly.",
        },
    },
    9: {
        "options": ["Narrative-only Ending", "Greedy Highest-Threat Selection", "Integrated DP Final Strategy"],
        "correct": "Integrated DP Final Strategy",
        "wrong_feedback": {
            "Narrative-only Ending": "Narrative-only ending is rejected because Part 9 must connect clearly to earlier algorithm outputs.",
            "Greedy Highest-Threat Selection": "Greedy highest-threat selection is rejected because it ignores resource constraints and the DP target plan.",
        },
    },
}

CANDIDATE_ALGORITHMS = {part_number: choices["options"] for part_number, choices in ALGORITHM_CHOICES.items()}

MISSION_OUTCOMES = {
    1: "Route secured through the harbour network.",
    2: "Suspicious identities isolated.",
    3: "Resource lockdown plan selected.",
    4: "Best uncertainty-balanced route chosen.",
    5: "Activation signal reconstructed.",
    6: "Urgent event order stabilized.",
    7: "Unpredictable sector selected.",
    8: "Critical trigger message ranked.",
    9: "Maximum disruption strategy synthesized.",
}

MISSION_FEEDBACK = {
    1: "Route computed: harbour path mapped.",
    2: "Registry checked: suspicious identity risk exposed.",
    3: "Checkpoint plan selected under resource limits.",
    4: "Route decision computed with weighted criteria.",
    5: "Signal sequence reconstructed.",
    6: "Urgent event order prioritized.",
    7: "Sector selected with controlled randomness.",
    8: "Trigger messages detected and ranked.",
    9: "Final strategy synthesized from previous outputs.",
}

MISSION_STORIES = {
    1: "The harbour route dataset must be solved without choosing a path that is short but too risky.",
    2: "The identity registry contains exact duplicates and near-alias overlaps that need a combined verification method.",
    3: "The checkpoint dataset has limited energy, time, and token budgets, so the selected subset must maximize impact under constraints.",
    4: "The route options contain uncertainty, so the decision must balance reward, time, and multiple risk sources.",
    5: "The activation sequence is split across fragments; useful delayed pieces must be recovered instead of discarded too early.",
    6: "The countdown stream is noisy. Events must be sorted by priority, timestamp, launch relevance, and stable arrival order.",
    7: "Repeated deterministic choices are predictable, so the sector selection uses controlled randomness while respecting risk.",
    8: "Intercepted messages may contain trigger phrases; the output must detect and rank the highest-risk messages.",
    9: "The final ending must connect earlier outputs into one coherent strategy: gain access, use access evidence, select high-impact targets, and prioritize the final disruption.",
}

MISSION_STORY_TRANSLATIONS = {
    "中文": {
        1: "港口路线数据集需要避免选择看似最短但风险暴露过高的路线。",
        2: "身份档案中同时存在精确重复和近似别名，需要组合验证方法。",
        3: "检查点数据受到能量、时间和令牌限制，必须在约束内选择影响最大的子集。",
        4: "多条路线都可行，但不确定性要求同时权衡奖励、时间和多种风险。",
        5: "激活信号被拆成多个片段，仍可恢复的延迟片段不能过早丢弃。",
        6: "倒计时事件流很混乱，必须按优先级、时间、发射相关性和稳定到达顺序排序。",
        7: "重复的确定性选择容易被预测，因此区域选择需要在风险约束下进行受控随机化。",
        8: "拦截消息可能包含触发短语，输出需要检测并排序最高风险的信息。",
        9: "最终结局需要把前面结果连成一个完整策略：进入核心、使用访问证据、选择高影响目标，并完成最终破坏方案。",
    },
    "Bahasa Melayu": {
        1: "Dataset laluan pelabuhan perlu mengelak laluan pendek yang terlalu berisiko.",
        2: "Daftar identiti mengandungi pendua tepat dan alias hampir sama, jadi kaedah pengesahan gabungan diperlukan.",
        3: "Dataset checkpoint mempunyai had tenaga, masa dan token, jadi subset berimpak tinggi perlu dipilih dalam kekangan.",
        4: "Beberapa laluan boleh digunakan, tetapi ketidakpastian menuntut imbangan ganjaran, masa dan risiko.",
        5: "Isyarat aktivasi terpisah kepada fragmen; fragmen tertunda yang masih berguna tidak boleh dibuang terlalu awal.",
        6: "Aliran kiraan detik bercampur; acara perlu diisih mengikut prioriti, masa, kaitan pelancaran dan susunan stabil.",
        7: "Pilihan deterministik berulang mudah diramal, jadi pemilihan sektor menggunakan rawakan terkawal dengan risiko masih dikira.",
        8: "Mesej pintasan mungkin mengandungi frasa pencetus; output perlu mengesan dan menyusun mesej berisiko tinggi.",
        9: "Pengakhiran akhir menggabungkan output awal: akses masuk, bukti akses, sasaran berimpak tinggi dan gangguan akhir.",
    },
}

KEY_TAKEAWAYS = {
    1: "A route is only defendable when distance, risk, detection, and blocked edges are evaluated together.",
    2: "Exact duplicate evidence and near-alias evidence must be combined to rank suspicious identities fairly.",
    3: "The best checkpoint plan is a constrained optimization result, not a greedy pick of attractive targets.",
    4: "Route choice under uncertainty needs visible trade-offs between risk, time, and reward.",
    5: "Signal reconstruction succeeds because valid and delayed fragments are evaluated before skipping damaged data.",
    6: "Stable multi-field sorting turns a noisy countdown feed into an actionable priority order.",
    7: "Controlled randomness reduces predictability while still respecting surveillance risk.",
    8: "Phrase detection becomes useful only after messages are ranked by threat severity.",
    9: "A strong creative ending is defendable when it is synthesized from actual outputs, not invented separately.",
}

WHY_IT_MATTERS = {
    1: "This protects the route decision from the common mistake of picking a short path that carries too much detection risk.",
    2: "This gives the group evidence for suspicious identities instead of only claiming that duplicates exist.",
    3: "This proves the lockdown plan respects real mission limits while maximizing operational impact.",
    4: "This makes the uncertain route decision defendable because every score is tied to visible criteria.",
    5: "This shows why the signal can still be recovered even when some fragments are delayed or unusable.",
    6: "This turns a noisy event feed into an ordered action list that can be defended field by field.",
    7: "This explains how the team stays less predictable without ignoring risk and decoy value.",
    8: "This connects phrase matching to final threat priority, so the output supports mission action instead of just text search.",
    9: "This turns Part 9 from a story-only ending into a logical final decision backed by Parts 1, 2, 3, and 8.",
}

ALGORITHM_DECISIONS = {
    1: "Modified Risk-Aware Dijkstra is selected because the route score must combine distance, risk, detection exposure, and blocked-route filtering.",
    2: "Two-stage hybrid verification is selected because exact hash evidence and near-alias distance evidence answer different parts of the identity-matching problem.",
    3: "Dynamic Programming Knapsack is selected because checkpoint value depends on combinations under three resource limits, not on a single greedy metric.",
    4: "MCDA Weighted Scoring is selected because the route decision must keep reward, time, and risk trade-offs visible.",
    5: "Dynamic Programming is selected because signal fragments can be delayed or skipped, so the best reconstruction depends on previous states.",
    6: "Modified Stable Merge Sort is selected because the event stream needs a stable multi-field order: priority, timestamp, launch relevance, then original index.",
    7: "Controlled Randomisation is selected because the output should be less predictable while still using risk and decoy evidence.",
    8: "Brute Force String Matching plus ranking is selected because phrase detection must stay transparent and then be converted into threat priority.",
    9: "Integrated DP Final Strategy is selected because it reuses the official route, access, target-optimization, and threat-ranking outputs to produce one final decision.",
}

ALGORITHM_FLOWS = {
    1: {
        "note": "This flow explains why the selected path is not simply the shortest path: every edge is scored by distance, risk, detection exposure, and route status.",
        "steps": [
            {"title": "Input graph data", "detail": "Read From_Node, To_Node, Distance, Risk_Level, Detection_Probability, and Route_Status."},
            {"title": "Build edge cost", "detail": "Ignore blocked edges and compute modified cost for every available directed edge."},
            {"title": "Run Dijkstra queue", "detail": "Use a priority queue to expand the lowest modified-cost route first."},
            {"title": "Recover route", "detail": "Trace the lowest-cost predecessor chain from destination back to start."},
            {"title": "Output path evidence", "detail": "Show selected route, total distance, total risk, total detection, and final modified cost."},
        ],
    },
    2: {
        "note": "This flow separates fast exact evidence from slower near-alias evidence, making the identity decision easier to defend.",
        "steps": [
            {"title": "Input registry", "detail": "Read Agent_ID, Alias, Access_Key, Status, and Linked_Site."},
            {"title": "Hash exact matches", "detail": "Group repeated aliases, access keys, and linked sites using hash tables."},
            {"title": "Check near aliases", "detail": "Use Levenshtein distance to detect names that are similar but not identical."},
            {"title": "Score suspicion", "detail": "Combine duplicate evidence, near-alias evidence, linked-site evidence, and risky status."},
            {"title": "Rank identities", "detail": "Output suspicious agents ordered by strongest evidence first."},
        ],
    },
    3: {
        "note": "This flow shows why dynamic programming is needed: the best target set depends on combinations under several resource limits.",
        "steps": [
            {"title": "Input checkpoints", "detail": "Read checkpoint impact plus energy, time, and token costs."},
            {"title": "Define DP state", "detail": "Track best impact for each energy-time-token capacity combination."},
            {"title": "Evaluate choices", "detail": "For each checkpoint, compare skipping it with selecting it if resources allow."},
            {"title": "Backtrack selection", "detail": "Recover the checkpoint set that produced the best final impact."},
            {"title": "Output resource plan", "detail": "Show selected checkpoints, total usage, remaining capacity, and total impact."},
        ],
    },
    4: {
        "note": "This flow turns uncertain route properties into one defendable score while keeping every criterion visible.",
        "steps": [
            {"title": "Input route options", "detail": "Read travel time, patrol probability, sensor failure, collapse probability, and reward."},
            {"title": "Compute joint risk", "detail": "Combine multiple probability risks without simply adding them."},
            {"title": "Normalize criteria", "detail": "Scale reward, time, and risk so they can be compared fairly."},
            {"title": "Apply weights", "detail": "Use MCDA weights to calculate the final score for each route."},
            {"title": "Choose route", "detail": "Select the highest final-score route and show the score table."},
        ],
    },
    5: {
        "note": "This flow explains how the reconstruction avoids greedy skipping and keeps useful delayed fragments.",
        "steps": [
            {"title": "Input fragments", "detail": "Read fragment group, sequence number, data block, and integrity status."},
            {"title": "Group sequence data", "detail": "Separate fragments by segment group and order them by sequence number."},
            {"title": "Evaluate recoverability", "detail": "Keep valid and useful delayed fragments while marking unusable damaged data."},
            {"title": "Reconstruct groups", "detail": "Build the best available sequence for each group using prior state decisions."},
            {"title": "Output signal", "detail": "Show reconstructed activation groups and skipped fragments."},
        ],
    },
    6: {
        "note": "This flow is the clearest graphical explanation for Part 6: input events become a priority order through a stable multi-field merge sort.",
        "steps": [
            {"title": "Input event stream", "detail": "Read Event_ID, Threat_Priority, Timestamp, Event_Type, Code_Value, and original index."},
            {"title": "Build sorting key", "detail": "Use (-Threat_Priority, Timestamp, Launch_Rank, Original_Index)."},
            {"title": "Split recursively", "detail": "Divide the event list into smaller halves for merge sort."},
            {"title": "Stable merge", "detail": "Compare keys and preserve original order when all priority fields tie."},
            {"title": "Output urgent order", "detail": "Show original order, sorted order, and Top 5 urgent events."},
        ],
    },
    7: {
        "note": "This flow shows that the random choice is controlled by risk evidence, not pure chance.",
        "steps": [
            {"title": "Input sector data", "detail": "Read patrol frequency, thermal scan level, drone coverage, prediction risk, and decoy value."},
            {"title": "Compute safety score", "detail": "Reward safer sectors and penalize surveillance and predicted movement."},
            {"title": "Convert to weights", "detail": "Turn sector scores into selection probabilities."},
            {"title": "Apply fixed seed", "detail": "Use reproducible controlled randomisation for demo and defense."},
            {"title": "Output sector", "detail": "Show chosen sector and probability chart."},
        ],
    },
    8: {
        "note": "This flow separates phrase detection from threat ranking, so text matching becomes an actionable priority list.",
        "steps": [
            {"title": "Input messages", "detail": "Read Message_ID, Text_Stream, Route_Tag, and trigger phrase evidence."},
            {"title": "Scan phrases", "detail": "Use brute force string matching to check trigger phrases inside each message."},
            {"title": "Add route context", "detail": "Use route tags and phrase weights to strengthen threat evidence."},
            {"title": "Rank threat score", "detail": "Sort messages by computed threat score and severity level."},
            {"title": "Output alerts", "detail": "Show ranked messages and threat score chart."},
        ],
    },
    9: {
        "note": "This flow makes Part 9 more than a story ending: it shows how earlier official algorithm outputs feed the final strategy.",
        "steps": [
            {"title": "Use Part 1 output", "detail": "Take the selected route as the access path into the target network."},
            {"title": "Use Part 2 output", "detail": "Use suspicious identity evidence as internal access support."},
            {"title": "Use Part 3 output", "detail": "Keep selected targets within energy, time, and token limits."},
            {"title": "Use Part 8 output", "detail": "Prioritize the highest-threat systems and route tags."},
            {"title": "Output final strategy", "detail": "Show selected disruption targets, resource usage, and final effects."},
        ],
    },
}

DEFENSE_NOTES = {
    1: [
        "Directed graph matters because reverse travel is not assumed.",
        "Modified cost explains why shortest is not always safest.",
    ],
    2: [
        "Hash tables provide fast exact evidence.",
        "Levenshtein distance handles alias variations missed by exact lookup.",
    ],
    3: [
        "The state stores resource usage, not just a single cost.",
        "DP is defendable because combinations matter.",
    ],
    4: [
        "MCDA keeps conflicting criteria visible.",
        "Joint risk is more realistic than adding probabilities directly.",
    ],
    5: [
        "Delayed fragments are recoverable, so greedy skipping is unsafe.",
        "DP supports partial reconstruction instead of total failure.",
    ],
    6: [
        "Manual merge sort implementation confirmed; Python sorted() is not used as the main algorithm.",
        "Stable sorting matters because equal-priority events keep original stream order.",
        "The key exactly follows the PPT: higher priority, earlier timestamp, launch-related first, then original order.",
    ],
    7: [
        "Controlled randomness reduces predictability without ignoring risk.",
        "Fixed seed makes the randomized selection reproducible.",
    ],
    8: [
        "Brute force is transparent and easy to defend for multi-word phrase scanning.",
        "Ranking links detection results to threat priority.",
    ],
    9: [
        "Part 9 has no separate dataset; it is derived from previous official outputs.",
        "The selected targets still come from the Part 3 DP result, so resource constraints remain visible.",
        "The final ending connects Part 1 route access, Part 2 access evidence, Part 3 target optimization, and Part 8 threat ranking.",
    ],
}

MISSION_FORWARD = {
    1: "The project gains a route result that balances safety and speed.",
    2: "The registry evidence supports the next identity-risk decision.",
    3: "The selected checkpoints show how resource limits shape the optimal subset.",
    4: "The chosen route makes the uncertainty trade-off visible and defendable.",
    5: "The reconstructed sequence provides a clear ordered output for the next step.",
    6: "The sorted event feed shows which alerts should be handled first under countdown pressure.",
    7: "Controlled randomness reduces predictability while keeping risk in the scoring model.",
    8: "Threat ranking identifies the most important message evidence.",
    9: "The final strategy closes the project by showing how earlier algorithm outputs combine into a coherent ending.",
}

RESULT_KEYS = {
    1: "route_summary",
    2: "suspicious_identities",
    3: "selected_checkpoints",
    4: "routes",
    5: "groups",
    6: "top_five",
    7: "sector_scores",
    8: "ranked_messages",
    9: "selected_targets",
}

RESULT_PAGE_SECTIONS = [
    "Key Takeaway",
    "Why it matters",
    "Mission Brief",
    "Dataset Used",
    "Candidate Algorithms",
    "Rejected Algorithms",
    "Chosen Algorithm",
    "Graphical Algorithm Explanation",
    "Detailed Algorithm Trace",
    "Key Result",
    "Visualization",
    "Time and Space Complexity",
    "Defense Notes",
    "How this result moves the mission forward",
]

HELPFUL_CHART_PARTS = {2, 3, 4, 6, 7, 8, 9}

PROBLEM_TYPES = {
    1: "Weighted graph route planning",
    2: "Identity verification and ranking",
    3: "Multi-resource optimization",
    4: "Multi-criteria route decision",
    5: "Sequential signal reconstruction",
    6: "Stable multi-field sorting",
    7: "Risk-aware randomized selection",
    8: "String matching and threat ranking",
    9: "Final result synthesis",
}

DEFENSE_MATRIX_COLUMNS = [
    "Part",
    "Dataset",
    "Problem Type",
    "Candidate Algorithms",
    "Rejected Algorithms",
    "Chosen Algorithm",
    "Key Output",
    "Complexity",
    "Defense Notes",
]


def key_output_for_part(part_number, result=None):
    if not result:
        return MISSION_OUTCOMES[part_number]
    if part_number == 1:
        return " -> ".join(result.get("route", [])) or MISSION_OUTCOMES[part_number]
    if part_number == 2:
        rows = result.get("suspicious_identities", [])
        return f"{rows[0]['Agent_ID']} score {rows[0]['Suspicion_Score']}" if rows else MISSION_OUTCOMES[part_number]
    if part_number == 3:
        return f"Impact {result.get('total_impact', 0)} using {len(result.get('selected_checkpoints', []))} checkpoints"
    if part_number == 4:
        chosen = result.get("chosen_route", {})
        return f"{chosen.get('Route_ID', '')} - {chosen.get('Route_Name', '')}".strip(" -")
    if part_number == 5:
        return result.get("final_activation_sequence", MISSION_OUTCOMES[part_number])
    if part_number == 6:
        top = result.get("top_five", [])
        return f"Top event {top[0]['Event_ID']}" if top else MISSION_OUTCOMES[part_number]
    if part_number == 7:
        return f"Sector {result.get('chosen_sector', {}).get('Sector', '')}"
    if part_number == 8:
        rows = result.get("ranked_messages", [])
        return f"{rows[0]['Message_ID']} score {rows[0]['Threat_Score']}" if rows else MISSION_OUTCOMES[part_number]
    if part_number == 9:
        return (
            f"{result.get('final_result', MISSION_OUTCOMES[part_number])}: "
            f"impact {result.get('total_operational_impact', 0)}"
        )
    return MISSION_OUTCOMES[part_number]


def build_defense_matrix_rows(results=None):
    results = results or {}
    rows = []
    for part_number in range(1, TOTAL_PARTS + 1):
        result = results.get(f"part{part_number}")
        meta = result.get("meta", {}) if result else {}
        dataset = meta.get("member")
        if not dataset:
            dataset = (
                f"{PART_FILE_NAMES[part_number]} / Sheet {DEFAULT_SHEETS.get(part_number, 'A')}"
                if part_number in PART_FILE_NAMES
                else "Derived from Parts 1, 2, 3, and 8"
            )
        rows.append(
            {
                "Part": f"Part {part_number}",
                "Dataset": dataset,
                "Problem Type": PROBLEM_TYPES[part_number],
                "Candidate Algorithms": " / ".join(CANDIDATE_ALGORITHMS[part_number]),
                "Rejected Algorithms": "; ".join(PART_INFO[part_number]["rejected"]),
                "Chosen Algorithm": PART_INFO[part_number]["algorithm"],
                "Key Output": key_output_for_part(part_number, result),
                "Complexity": PART_INFO[part_number]["complexity"],
                "Defense Notes": " / ".join(DEFENSE_NOTES[part_number]),
            }
        )
    return rows
