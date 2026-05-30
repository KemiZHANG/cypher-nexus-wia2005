"""Presentation metadata for the Cypher Nexus Streamlit dashboard.

This file contains only dashboard copy and analysis metadata. Official
algorithms, dataset loading, and saved outputs remain in cypher_nexus_project.py.
"""

from cypher_nexus_project import DEFAULT_SHEETS, PART_FILE_NAMES, PART_INFO


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
}

MISSION_FEEDBACK = {
    1: "Layer disabled: harbour route mapped.",
    2: "Registry filtered: double-agent risk exposed.",
    3: "Protocol weakened: checkpoint plan locked.",
    4: "Probability trap cleared: route decision defended.",
    5: "Signal secured: fragment chain restored.",
    6: "Countdown stabilized: urgent events prioritized.",
    7: "Prediction loop disrupted: sector choice randomized.",
    8: "Silent code traced: dangerous messages ranked.",
}

MISSION_STORIES = {
    1: "The team enters the harbour network and must cross without choosing a route that looks short but exposes the mission.",
    2: "The registry contains hidden identity overlaps; the mission needs proof that suspicious agents are not just exact duplicates.",
    3: "Resources are limited, so the lockdown must pick the checkpoints that give the strongest impact under strict caps.",
    4: "Several routes look possible, but uncertainty means the decision must balance reward, time, and multiple risk sources.",
    5: "The activation signal is split across fragments; useful delayed pieces must be recovered instead of discarded too early.",
    6: "The countdown stream is noisy. The team must sort urgent alerts by priority, timestamp, launch relevance, and stable arrival order.",
    7: "The enemy predicts repeated optimal moves, so the escape sector must be selected with controlled randomness.",
    8: "Final intercepted messages may contain trigger phrases; the mission must expose and rank the most dangerous message.",
}

MISSION_STORY_TRANSLATIONS = {
    "中文": {
        1: "小组进入港口网络，必须避开看似最短但暴露风险过高的路线。",
        2: "档案中隐藏着身份重叠，任务需要证明可疑代理不只是完全重复项。",
        3: "资源有限，封锁方案必须在严格限制内选择影响最大的检查点。",
        4: "多条路线都可行，但不确定性要求同时权衡奖励、时间和多种风险。",
        5: "激活信号被拆成多个片段，仍可恢复的延迟片段不能过早丢弃。",
        6: "倒计时事件流很混乱，必须按优先级、时间、发射相关性和稳定到达顺序排序。",
        7: "敌方会预测重复的最优行动，因此逃离区域需要受控随机化。",
        8: "最终拦截消息可能包含触发短语，任务必须找出并排序最危险的信息。",
    },
    "Bahasa Melayu": {
        1: "Pasukan memasuki rangkaian pelabuhan dan perlu mengelak laluan pendek yang terlalu terdedah.",
        2: "Daftar menyembunyikan pertindihan identiti; misi memerlukan bukti selain pendua tepat.",
        3: "Sumber terhad, jadi pelan sekatan mesti memilih checkpoint berimpak tinggi dalam had ketat.",
        4: "Beberapa laluan boleh digunakan, tetapi ketidakpastian menuntut imbangan ganjaran, masa dan risiko.",
        5: "Isyarat aktivasi terpisah kepada fragmen; fragmen tertunda yang masih berguna tidak boleh dibuang terlalu awal.",
        6: "Aliran kiraan detik bercampur; acara perlu diisih mengikut prioriti, masa, kaitan pelancaran dan susunan stabil.",
        7: "Musuh meramal gerakan optimum berulang, jadi sektor keluar dipilih dengan rawakan terkawal.",
        8: "Mesej pintasan akhir mungkin mengandungi frasa pencetus; misi mesti mendedahkan mesej paling berbahaya.",
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
        "Fixed seed makes the demo repeatable for presentation.",
    ],
    8: [
        "Brute force is transparent and easy to defend for multi-word phrase scanning.",
        "Ranking links detection results to mission urgency.",
    ],
}

MISSION_FORWARD = {
    1: "The team reaches the next intelligence layer with a route that balances safety and speed.",
    2: "The suspicious registry points toward the operational support chain.",
    3: "The selected checkpoints weaken the enemy system before the route decision.",
    4: "The chosen route moves the team through uncertainty with a defensible trade-off.",
    5: "The reconstructed signal reveals the next active control layer.",
    6: "The sorted event feed tells the team which alerts to handle first under countdown pressure.",
    7: "Controlled randomness breaks the enemy's prediction pattern.",
    8: "Threat ranking reveals the most dangerous message and final trigger evidence.",
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
}

RESULT_PAGE_SECTIONS = [
    "Key Takeaway",
    "Why it matters",
    "Mission Brief",
    "Dataset Used",
    "Candidate Algorithms",
    "Rejected Algorithms",
    "Chosen Algorithm",
    "Key Result",
    "Visualization",
    "Time and Space Complexity",
    "Defense Notes",
    "How this result moves the mission forward",
]

HELPFUL_CHART_PARTS = {2, 3, 4, 6, 7, 8}

PROBLEM_TYPES = {
    1: "Weighted graph route planning",
    2: "Identity verification and ranking",
    3: "Multi-resource optimization",
    4: "Multi-criteria route decision",
    5: "Sequential signal reconstruction",
    6: "Stable multi-field sorting",
    7: "Risk-aware randomized selection",
    8: "String matching and threat ranking",
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
    return MISSION_OUTCOMES[part_number]


def build_defense_matrix_rows(results=None):
    results = results or {}
    rows = []
    for part_number in range(1, 9):
        result = results.get(f"part{part_number}")
        meta = result.get("meta", {}) if result else {}
        dataset = meta.get("member") or f"{PART_FILE_NAMES[part_number]} / Sheet {DEFAULT_SHEETS.get(part_number, 'A')}"
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
            }
        )
    return rows
