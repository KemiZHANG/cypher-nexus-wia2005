"""
Operation Cypher Nexus: The Final Protocol

Python implementation for WIA2005 group project demonstration.

Run:
    python cypher_nexus_project.py

The program loads the dataset ZIP automatically when possible, runs Parts 1-8
in order, and saves presentation-friendly text outputs into the outputs folder.
"""

import argparse
import heapq
import math
import os
import random
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_SHEETS = {
    1: "C",  # PPT Part 1 explicitly shows Sheet C.
    2: "A",
    3: "A",  # PPT Part 3 output example uses Sheet A constraints.
    4: "A",
    5: "A",
    6: "A",
    7: "A",
    8: "A",  # PPT Part 8 enhancement example uses Sheet A.
}

PART_FILE_NAMES = {
    1: "Part 1.xlsx",
    2: "Part 2.xlsx",
    3: "Part 3.xlsx",
    4: "Part 4.xlsx",
    5: "Part 5.xlsx",
    6: "Part 6.xlsx",
    7: "Part 7.xlsx",
    8: "Part 8.xlsx",
}

COLUMN_ALIASES = {
    "fromnode": "From_Node",
    "tonode": "To_Node",
    "distance": "Distance",
    "traveltime": "Travel_Time",
    "risklevel": "Risk_Level",
    "detectionprobability": "Detection_Probability",
    "routestatus": "Route_Status",
    "agentid": "Agent_ID",
    "alias": "Alias",
    "nationalitycode": "Nationality_Code",
    "lastknowncity": "Last_Known_City",
    "accesskey": "Access_Key",
    "status": "Status",
    "linkedsite": "Linked_Site",
    "checkpoint": "Checkpoint",
    "energycost": "Energy_Cost",
    "timecost": "Time_Cost",
    "tokencost": "Token_Cost",
    "operationalimpact": "Operational_Impact",
    "targettype": "Target_Type",
    "routeid": "Route_ID",
    "routename": "Route_Name",
    "patrolprobability": "Patrol_Probability",
    "sensorfailureprobability": "Sensor_Failure_Probability",
    "collapseprobability": "Collapse_Probability",
    "successreward": "Success_Reward",
    "fragmentid": "Fragment_ID",
    "segmentgroup": "Segment_Group",
    "sequenceno": "Sequence_No",
    "datablock": "Data_Block",
    "integritystatus": "Integrity_Status",
    "serversource": "Server_Source",
    "eventid": "Event_ID",
    "threatpriority": "Threat_Priority",
    "timestamp": "Timestamp",
    "zone": "Zone",
    "eventtype": "Event_Type",
    "codevalue": "Code_Value",
    "sector": "Sector",
    "patrolfrequency": "Patrol_Frequency",
    "thermalscanlevel": "Thermal_Scan_Level",
    "dronecoverage": "Drone_Coverage",
    "predictedbyenemy": "Predicted_By_Enemy",
    "decoyvalue": "Decoy_Value",
    "messageid": "Message_ID",
    "textstream": "Text_Stream",
    "routetag": "Route_Tag",
    "triggerphrase": "Trigger_Phrase",
    "phrase": "Trigger_Phrase",
    "threatscore": "Threat_Score",
    "threatlevel": "Threat_Level",
}

DEFAULT_TRIGGER_WEIGHTS = {
    "silent code": 1,
    "shadow key": 2,
    "final protocol": 3,
    "launch trigger": 3,
    "cypher nexus": 3,
    "activation sequence": 2,
    "override code": 2,
    "core protocol": 2,
}

PART_INFO = {
    1: {
        "title": "The Shadow Network",
        "mission_problem": "Find a feasible directed route through the harbour network while balancing distance, risk, and detection exposure.",
        "algorithm": "Modified Risk-Aware Dijkstra",
        "rejected": [
            "BFS is rejected because it treats all routes as equal and cannot model weighted distance, risk, or detection.",
            "Standard Dijkstra is rejected because it optimizes distance only, while this mission must balance safety and speed.",
        ],
        "complexity": "Time O((V+E)logV), space O(V+E).",
        "columns": ["From_Node", "To_Node", "Distance", "Risk_Level", "Detection_Probability", "Route_Status"],
        "output_base": "part1_shadow_network",
    },
    2: {
        "title": "The Double Agent Registry",
        "mission_problem": "Detect suspicious identities using exact duplicate evidence and near-duplicate alias evidence.",
        "algorithm": "Two-Stage Hybrid Verification System: Hash Table Filtering + Levenshtein Distance",
        "rejected": [
            "Linear search is rejected because repeated pairwise checking is too slow for large registries.",
            "Hash table only is rejected because it cannot detect near-duplicate aliases such as Falcon and Falcon_1.",
        ],
        "complexity": "Hash filtering O(n); near-alias verification O(a^2*m*n) for unique aliases and string lengths; space O(n).",
        "columns": ["Agent_ID", "Alias", "Access_Key", "Status", "Linked_Site"],
        "output_base": "part2_double_agent_registry",
    },
    3: {
        "title": "The Resource Lockdown",
        "mission_problem": "Select checkpoints that maximize operational impact while staying within energy, time, and token limits.",
        "algorithm": "Dynamic Programming Knapsack",
        "rejected": [
            "Greedy selection is rejected because the highest immediate efficiency can block a better final combination.",
            "Brute force is rejected because checking every subset grows as O(2^n).",
        ],
        "complexity": "Time O(n*E*T*K), space O(E*T*K) for energy, time, and token capacities.",
        "columns": ["Checkpoint", "Energy_Cost", "Time_Cost", "Token_Cost", "Operational_Impact"],
        "output_base": "part3_resource_lockdown",
    },
    4: {
        "title": "The Probability Trap",
        "mission_problem": "Choose the best route under uncertainty by balancing route risk, travel time, and success reward.",
        "algorithm": "MCDA Weighted Scoring",
        "rejected": [
            "Expected value is rejected because it can ignore travel time and one-time survival constraints.",
            "Risk-adjusted return is rejected because a very safe but low-reward route can defeat the mission objective.",
        ],
        "complexity": "Time O(n*c) for n routes and c criteria, space O(n).",
        "columns": ["Route_ID", "Route_Name", "Travel_Time", "Patrol_Probability", "Sensor_Failure_Probability", "Collapse_Probability", "Success_Reward"],
        "output_base": "part4_probability_trap",
    },
    5: {
        "title": "The Split Signal Protocol",
        "mission_problem": "Reconstruct grouped signal fragments in sequence while using valid and useful delayed fragments and skipping unrecoverable fragments.",
        "algorithm": "Dynamic Programming Signal Reconstruction",
        "rejected": [
            "Greedy is rejected because it can permanently skip delayed fragments that are still recoverable.",
            "Topological sort is rejected because ordering fragments does not decide which fragments should be included.",
        ],
        "complexity": "Time O(nlogn) for grouping and ordering plus O(n) DP, space O(n).",
        "columns": ["Fragment_ID", "Segment_Group", "Sequence_No", "Data_Block", "Integrity_Status"],
        "output_base": "part5_split_signal_protocol",
    },
    6: {
        "title": "The Countdown Sequence",
        "mission_problem": "Prioritize mixed operational events by threat, time, launch relevance, and stable arrival order.",
        "algorithm": "Modified Stable Merge Sort",
        "rejected": [
            "Insertion Sort is rejected because the stream is not guaranteed to be nearly sorted and may degrade to O(n^2).",
            "Counting/Radix Sort is rejected because the sorting key mixes numeric priority, timestamp, event type, and original order.",
        ],
        "complexity": "Time O(nlogn), space O(n).",
        "columns": ["Event_ID", "Threat_Priority", "Timestamp", "Zone", "Event_Type", "Code_Value"],
        "output_base": "part6_countdown_sequence",
    },
    7: {
        "title": "The Phantom Dice",
        "mission_problem": "Choose a movement sector that is safe enough while avoiding deterministic patterns the enemy can predict.",
        "algorithm": "Controlled Randomisation",
        "rejected": [
            "Deterministic best route is rejected because repeated optimal moves become predictable to enemy AI.",
            "Pure random movement is rejected because it ignores surveillance risk and decoy usefulness.",
        ],
        "complexity": "Time O(n) for scoring and weighted selection, space O(n).",
        "columns": ["Sector", "Patrol_Frequency", "Thermal_Scan_Level", "Drone_Coverage", "Predicted_By_Enemy", "Decoy_Value"],
        "output_base": "part7_phantom_dice",
    },
    8: {
        "title": "The Silent Code",
        "mission_problem": "Scan intercepted messages for trigger phrases and rank messages by threat severity.",
        "algorithm": "Brute Force String Matching + Threat Ranking",
        "rejected": [
            "KMP is rejected for this small demonstration because optimization is less important than transparent ranking logic.",
            "Hash set lookup is rejected because it cannot naturally scan full text for multi-word trigger phrases.",
        ],
        "complexity": "Time O(messages*phrases*text_length*phrase_length), space O(messages+phrases).",
        "columns": ["Message_ID", "Text_Stream", "Route_Tag"],
        "output_base": "part8_silent_code",
    },
}


def normalized_name(value):
    """Normalize column names so Threat Priority, threat_priority, etc. match."""
    return "".join(ch.lower() for ch in str(value).strip() if ch.isalnum())


def to_text(value, default=""):
    if value is None or pd.isna(value):
        return default
    return str(value).strip()


def to_float(value, default=0.0):
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def to_int(value, default=0):
    return int(round(to_float(value, default)))


def first_existing_column(df, possible_names):
    lookup = {normalized_name(column): column for column in df.columns}
    for name in possible_names:
        key = normalized_name(name)
        if key in lookup:
            return lookup[key]
    return None


def standardize_columns(df, return_mapping=False):
    rename_map = {}
    for column in df.columns:
        key = normalized_name(column)
        if key in COLUMN_ALIASES:
            rename_map[column] = COLUMN_ALIASES[key]
    standardized = df.rename(columns=rename_map)
    if not return_mapping:
        return standardized
    mapping = {str(column): str(rename_map.get(column, column)) for column in df.columns}
    return standardized, mapping


def clean_dataframe(df, return_mapping=False):
    df = df.dropna(axis=1, how="all").dropna(how="all")
    usable_columns = []
    for column in df.columns:
        label = str(column).strip()
        if not label or label.lower().startswith("unnamed") or label.lower() == "nan":
            usable_columns.append(False)
        else:
            usable_columns.append(True)
    if usable_columns:
        df = df.loc[:, usable_columns]
    if return_mapping:
        standardized, mapping = standardize_columns(df, return_mapping=True)
        return standardized.reset_index(drop=True), mapping
    return standardize_columns(df).reset_index(drop=True)


def detect_header_row(raw_df):
    best_score = -1
    best_index = 0
    max_rows = min(10, len(raw_df))
    for index in range(max_rows):
        score = 0
        for value in raw_df.iloc[index].tolist():
            key = normalized_name(value)
            if key in COLUMN_ALIASES:
                score += 3
            elif any(token in key for token in ("node", "route", "event", "message", "sector")):
                score += 1
        if score > best_score:
            best_score = score
            best_index = index
    return best_index


def find_dataset_zip(dataset_zip_path=None):
    candidates = []
    if dataset_zip_path:
        requested = Path(dataset_zip_path)
        if not requested.exists():
            raise FileNotFoundError(
                f"Dataset ZIP not found: {requested}\n"
                "Place Datasets (2).zip in the project folder, pass the correct path, "
                "or set CYPHER_DATASET_ZIP."
            )
        candidates.append(requested)
    env_path = os.environ.get("CYPHER_DATASET_ZIP")
    if env_path:
        candidates.append(Path(env_path))

    cwd = Path.cwd()
    candidates.extend(
        [
            cwd / "Datasets (2).zip",
            cwd / "Datasets.zip",
            cwd.parent / "Datasets (2).zip",
            cwd.parent / "Datasets.zip",
            Path("D:/Datasets (2).zip"),
            Path("D:/Datasets.zip"),
            Path("/content/Datasets (2).zip"),
            Path("/content/Datasets.zip"),
        ]
    )
    for path in cwd.glob("*.zip"):
        if "dataset" in path.name.lower():
            candidates.append(path)

    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists():
            return candidate
    return None


def find_part_member(zip_file, part_number):
    expected = PART_FILE_NAMES[part_number].lower()
    for name in zip_file.namelist():
        simple = Path(name).name.lower()
        if name.startswith("__MACOSX"):
            continue
        if simple == expected:
            return name
    for name in zip_file.namelist():
        simple = Path(name).name.lower()
        if name.startswith("__MACOSX"):
            continue
        if simple.endswith((".xlsx", ".xls", ".csv")) and f"part {part_number}" in simple:
            return name
    return None


def load_part_dataframe(part_number, sheet=None, dataset_zip_path=None):
    sheet = sheet or DEFAULT_SHEETS.get(part_number, "A")
    dataset_zip = find_dataset_zip(dataset_zip_path)
    if dataset_zip:
        with zipfile.ZipFile(dataset_zip) as zf:
            member = find_part_member(zf, part_number)
            if not member:
                available = [name for name in zf.namelist() if not name.startswith("__MACOSX")]
                raise ValueError(
                    f"Dataset file for Part {part_number} was not found in {dataset_zip}.\n"
                    f"Expected something like {PART_FILE_NAMES.get(part_number)}.\n"
                    f"Available files: {available}"
                )

            if member.lower().endswith(".csv"):
                with zf.open(member) as handle:
                    df = pd.read_csv(handle)
                clean_df, mapping = clean_dataframe(df, return_mapping=True)
                meta = {
                    "source": str(dataset_zip),
                    "member": member,
                    "sheet": "CSV",
                    "requested_sheet": sheet,
                    "fallback_used": False,
                    "row_count": len(clean_df),
                    "available_columns": list(clean_df.columns),
                    "column_mapping": mapping,
                }
                return clean_df, meta

            with zf.open(member) as handle:
                excel_file = pd.ExcelFile(handle)
                if sheet not in excel_file.sheet_names:
                    raise ValueError(
                        f"Sheet '{sheet}' was not found for Part {part_number} in {member}.\n"
                        f"Available sheets: {excel_file.sheet_names}\n"
                        "Use a valid sheet name such as A, B, or C."
                    )
                raw = excel_file.parse(sheet, header=None)
                header_row = detect_header_row(raw)
                df = excel_file.parse(sheet, header=header_row)
            clean_df, mapping = clean_dataframe(df, return_mapping=True)
            meta = {
                "source": str(dataset_zip),
                "member": member,
                "sheet": sheet,
                "requested_sheet": sheet,
                "fallback_used": False,
                "row_count": len(clean_df),
                "available_columns": list(clean_df.columns),
                "column_mapping": mapping,
            }
            return clean_df, meta

    df = fallback_dataframe(part_number)
    clean_df, mapping = clean_dataframe(df, return_mapping=True)
    meta = {
        "source": "fallback demo data",
        "member": PART_FILE_NAMES.get(part_number, "unknown"),
        "sheet": sheet,
        "requested_sheet": sheet,
        "fallback_used": True,
        "row_count": len(clean_df),
        "available_columns": list(clean_df.columns),
        "column_mapping": mapping,
    }
    return clean_df, meta


def fallback_dataframe(part_number):
    if part_number == 1:
        return pd.DataFrame(
            [
                ["Port Authority Hub", "Warehouse A", 3, 5, 4, 0.14, "Open"],
                ["Warehouse A", "Safe House 1", 6, 8, 2, 0.07, "Open"],
                ["Safe House 1", "Financial Vault Access", 6, 7, 3, 0.10, "Open"],
                ["Port Authority Hub", "Patrol Relay East", 4, 4, 7, 0.31, "Monitored"],
                ["Patrol Relay East", "Signal Loft", 3, 3, 6, 0.24, "Monitored"],
                ["Signal Loft", "Financial Vault Access", 5, 5, 5, 0.19, "Open"],
            ],
            columns=[
                "From_Node",
                "To_Node",
                "Distance",
                "Travel_Time",
                "Risk_Level",
                "Detection_Probability",
                "Route_Status",
            ],
        )
    if part_number == 2:
        return pd.DataFrame(
            [
                ["A1023", "Raven", "MY", "Blackridge", "K9X4", "Active", "East Daran Depot"],
                ["A3102", "Raven", "MY", "Blackridge", "K9X4", "Suspicious", "Greyfen Reach"],
                ["A1194", "Falcon", "TH", "Norvale", "T7Q1", "Missing", "North Cargo Pier"],
                ["A2876", "Falcon_1", "TH", "Norvale", "T7Q1", "Suspicious", "Greyfen Reach"],
            ],
            columns=[
                "Agent_ID",
                "Alias",
                "Nationality_Code",
                "Last_Known_City",
                "Access_Key",
                "Status",
                "Linked_Site",
            ],
        )
    if part_number == 3:
        return pd.DataFrame(
            [
                ["Disable Camera Grid", 3, 8, 1, 11, "Surveillance"],
                ["Compromise Security Gate Control", 4, 7, 1, 10, "Access Control"],
                ["Extract Access Logs", 2, 5, 0, 7, "Intelligence"],
                ["Jam Patrol Drone Relay", 5, 11, 1, 14, "Aerial Defence"],
                ["Disrupt Escape Route Beacon", 4, 8, 1, 12, "Mobility"],
            ],
            columns=[
                "Checkpoint",
                "Energy_Cost",
                "Time_Cost",
                "Token_Cost",
                "Operational_Impact",
                "Target_Type",
            ],
        )
    if part_number == 4:
        return pd.DataFrame(
            [
                ["R1", "Ridge Tunnel", 12, 0.20, 0.10, 0.15, 25],
                ["R2", "Forest Service Road", 18, 0.10, 0.05, 0.05, 18],
                ["R3", "Cable-Car Line", 9, 0.35, 0.08, 0.20, 30],
            ],
            columns=[
                "Route_ID",
                "Route_Name",
                "Travel_Time",
                "Patrol_Probability",
                "Sensor_Failure_Probability",
                "Collapse_Probability",
                "Success_Reward",
            ],
        )
    if part_number == 5:
        return pd.DataFrame(
            [
                ["F01", "Alpha", 1, "CNX-44", "Valid", "S-West-1"],
                ["F02", "Alpha", 2, "M13-76", "Valid", "S-West-2"],
                ["F03", "Alpha", 3, "X7P-91", "Valid", "S-East-2"],
                ["F04", "Alpha", 4, "QL2-88", "Corrupted", "S-North-3"],
                ["F05", "Beta", 1, "TR5-11", "Valid", "S-Central"],
                ["F07", "Beta", 3, "LP4-62", "Delayed", "S-North-1"],
            ],
            columns=[
                "Fragment_ID",
                "Segment_Group",
                "Sequence_No",
                "Data_Block",
                "Integrity_Status",
                "Server_Source",
            ],
        )
    if part_number == 6:
        return pd.DataFrame(
            [
                ["E104", 5, "04:21:15", "Z3", "Biometric Alert", 881],
                ["E098", 2, "04:20:40", "Z1", "Door Access", 204],
                ["E121", 1, "04:21:30", "Z5", "Launch Trigger", 997],
                ["E087", 4, "04:19:58", "Z2", "Drone Entry", 650],
            ],
            columns=["Event_ID", "Threat_Priority", "Timestamp", "Zone", "Event_Type", "Code_Value"],
        )
    if part_number == 7:
        return pd.DataFrame(
            [
                ["S1", 3, 2, 3, "Yes", 5],
                ["S2", 4, 3, 4, "No", 8],
                ["S6", 4, 2, 3, "No", 9],
            ],
            columns=[
                "Sector",
                "Patrol_Frequency",
                "Thermal_Scan_Level",
                "Drone_Coverage",
                "Predicted_By_Enemy",
                "Decoy_Value",
            ],
        )
    if part_number == 8:
        return pd.DataFrame(
            [
                ["M04", "final protocol begins when shadow key and silent code appear together", "GRID-HUB-B2"],
                ["M07", "prepare shadow key for launch trigger at first light", np.nan],
            ],
            columns=["Message_ID", "Text_Stream", "Route_Tag"],
        )
    return pd.DataFrame()


def format_number(value, digits=3):
    if isinstance(value, int):
        return str(value)
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.{digits}f}".rstrip("0").rstrip(".")


def format_table(rows, columns, max_rows=None):
    rows = rows[:max_rows] if max_rows else rows
    text_rows = []
    for row in rows:
        text_rows.append([format_number(row.get(column, "")) for column in columns])
    widths = [len(column) for column in columns]
    for row in text_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    header = " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns))
    divider = "-+-".join("-" * width for width in widths)
    body = [" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) for row in text_rows]
    return "\n".join([header, divider] + body)


def ensure_output_dir(output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def write_output(output_dir, filename, text):
    if output_dir is None:
        return None
    output_path = ensure_output_dir(output_dir) / filename
    output_path.write_text(text, encoding="utf-8")
    return str(output_path)


def write_csv_output(output_dir, filename, rows):
    if output_dir is None or not rows:
        return None
    output_path = ensure_output_dir(output_dir) / filename
    pd.DataFrame(rows).to_csv(output_path, index=False, encoding="utf-8-sig")
    return str(output_path)


def require_columns(part_number, required_columns, available_columns):
    missing = [column for column in required_columns if column not in available_columns]
    if missing:
        raise ValueError(
            f"Part {part_number}: Missing required columns: {missing}. "
            f"Available columns: {list(available_columns)}.\n"
            "Guidance: check the Excel sheet, header row, and column names. "
            "The loader accepts variants like Threat Priority, Threat_Priority, and threat_priority."
        )


def prepare_part_dataframe(part_number, sheet=None, dataset_zip_path=None):
    df, meta = load_part_dataframe(part_number, sheet, dataset_zip_path)
    required_columns = PART_INFO[part_number]["columns"]
    require_columns(part_number, required_columns, list(df.columns))
    meta = dict(meta)
    meta["row_count"] = len(df)
    meta["columns_used"] = [column for column in required_columns if column in df.columns]
    meta["available_columns"] = list(df.columns)
    return df, meta


def dataset_summary_lines(metadata):
    return [
        f"dataset file: {metadata.get('member', 'unknown')}",
        f"dataset source: {metadata.get('source', 'unknown')}",
        f"sheet name: {metadata.get('sheet', 'unknown')}",
        f"row count: {metadata.get('row_count', 0)}",
        f"columns used: {', '.join(metadata.get('columns_used', []))}",
    ]


def build_standard_report(part_number, metadata, key_result, result_explanation, detail_lines=None):
    info = PART_INFO[part_number]
    lines = [
        f"Part {part_number} - {info['title']}",
        "",
        "Mission Problem",
        info["mission_problem"],
        "",
        "Algorithm Used",
        info["algorithm"],
        "",
        "Rejected Algorithms",
    ]
    lines.extend(f"- {reason}" for reason in info["rejected"])
    lines.extend(
        [
            "",
            "Dataset",
            *dataset_summary_lines(metadata),
            "",
            "Key Result",
            key_result,
            "",
            "Result Explanation",
            result_explanation,
            "",
            "Time and Space Complexity",
            info["complexity"],
        ]
    )
    if detail_lines:
        lines.extend(["", "Detailed Output", *detail_lines])
    return "\n".join(lines)


def attach_outputs(result, part_number, output_dir, text, csv_tables=None):
    base = PART_INFO[part_number]["output_base"]
    result["output_file"] = write_output(output_dir, f"{base}.txt", text)
    result["output_text"] = text
    result["csv_files"] = []
    for suffix, rows in (csv_tables or {}).items():
        csv_file = write_csv_output(output_dir, f"{base}_{suffix}.csv", rows)
        if csv_file:
            result["csv_files"].append(csv_file)
    return result


def format_data_mapping_report(metadata_by_part):
    lines = ["Cypher Nexus Data Mapping Report", ""]
    for part_number in sorted(metadata_by_part):
        meta = metadata_by_part[part_number]
        lines.extend(
            [
                f"Part {part_number} - {PART_INFO[part_number]['title']}",
                f"Dataset file: {meta.get('member', 'unknown')}",
                f"Sheet name: {meta.get('sheet', 'unknown')}",
                f"Row count: {meta.get('row_count', 0)}",
                "Columns used by algorithm: " + ", ".join(meta.get("columns_used", [])),
                "Original column -> algorithm field:",
            ]
        )
        mapping = meta.get("column_mapping", {})
        used = set(meta.get("columns_used", []))
        used_pairs = [(original, mapped) for original, mapped in mapping.items() if mapped in used]
        if not used_pairs:
            used_pairs = list(mapping.items())
        for original, mapped in used_pairs:
            lines.append(f"- {original} -> {mapped}")
        lines.append("")
    return "\n".join(lines)


def list_dataset_contents(dataset_zip_path=None):
    dataset_zip = find_dataset_zip(dataset_zip_path)
    if not dataset_zip:
        return "Dataset ZIP was not found. Fallback demo data would be used."
    lines = [f"Dataset ZIP: {dataset_zip}", ""]
    with zipfile.ZipFile(dataset_zip) as zf:
        for part_number in sorted(PART_FILE_NAMES):
            member = find_part_member(zf, part_number)
            if not member:
                lines.append(f"Part {part_number}: missing expected file {PART_FILE_NAMES[part_number]}")
                continue
            if member.lower().endswith(".csv"):
                lines.append(f"Part {part_number}: {member} (CSV)")
                continue
            with zf.open(member) as handle:
                excel_file = pd.ExcelFile(handle)
                lines.append(f"Part {part_number}: {member}")
                lines.append(f"  sheets: {', '.join(excel_file.sheet_names)}")
                for sheet_name in excel_file.sheet_names:
                    raw = excel_file.parse(sheet_name, header=None)
                    header_row = detect_header_row(raw)
                    df = excel_file.parse(sheet_name, header=header_row)
                    clean_df, _ = clean_dataframe(df, return_mapping=True)
                    lines.append(
                        f"  {sheet_name}: rows={len(clean_df)}, columns={', '.join(map(str, clean_df.columns))}"
                    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Part 1: Modified Risk-Aware Dijkstra


def route_edge_cost(edge):
    return (
        to_float(edge.get("Distance"))
        + to_float(edge.get("Risk_Level")) * 2
        + to_float(edge.get("Detection_Probability")) * 10
    )


def modified_risk_aware_dijkstra(edges, start_node, destination_node):
    graph = defaultdict(list)
    for edge in edges:
        from_node = to_text(edge.get("From_Node"))
        to_node = to_text(edge.get("To_Node"))
        if not from_node or not to_node:
            continue
        status = to_text(edge.get("Route_Status")).lower()
        if status in {"closed", "blocked", "unavailable"}:
            continue
        graph[from_node].append(
            {
                "to": to_node,
                "distance": to_float(edge.get("Distance")),
                "risk": to_float(edge.get("Risk_Level")),
                "detection": to_float(edge.get("Detection_Probability")),
                "modified_cost": route_edge_cost(edge),
                "status": to_text(edge.get("Route_Status"), "Open"),
            }
        )

    heap = [(0.0, start_node, 0.0, 0.0, 0.0, [start_node])]
    best_cost = {start_node: 0.0}

    while heap:
        current_cost, node, distance, risk, detection, path = heapq.heappop(heap)
        if current_cost > best_cost.get(node, math.inf):
            continue
        if node == destination_node:
            return {
                "route": path,
                "total_distance": distance,
                "total_risk": risk,
                "total_detection": detection,
                "total_modified_cost": current_cost,
            }
        for edge in graph.get(node, []):
            next_node = edge["to"]
            next_cost = current_cost + edge["modified_cost"]
            if next_cost < best_cost.get(next_node, math.inf):
                best_cost[next_node] = next_cost
                heapq.heappush(
                    heap,
                    (
                        next_cost,
                        next_node,
                        distance + edge["distance"],
                        risk + edge["risk"],
                        detection + edge["detection"],
                        path + [next_node],
                    ),
                )

    return {
        "route": [],
        "total_distance": 0,
        "total_risk": 0,
        "total_detection": 0,
        "total_modified_cost": math.inf,
    }


def choose_start_and_destination(df):
    from_col = first_existing_column(df, ["From_Node"])
    to_col = first_existing_column(df, ["To_Node"])
    if from_col is None or to_col is None or df.empty:
        return "", ""
    start = to_text(df[from_col].dropna().iloc[0])
    all_to_nodes = [to_text(value) for value in df[to_col].dropna().tolist()]
    all_from_nodes = {to_text(value) for value in df[from_col].dropna().tolist()}
    for node in all_to_nodes:
        if node.lower() == "financial vault access":
            return start, node
    sink_nodes = [node for node in all_to_nodes if node and node not in all_from_nodes]
    destination = sink_nodes[-1] if sink_nodes else all_to_nodes[-1]
    return start, destination


def run_part1_shadow_network(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(1, sheet, dataset_zip_path)
    df = df.dropna(subset=["From_Node", "To_Node"])
    meta["row_count"] = len(df)
    start, destination = choose_start_and_destination(df)
    result = modified_risk_aware_dijkstra(df.to_dict("records"), start, destination)
    result.update({"start": start, "destination": destination, "meta": meta})

    route_text = " -> ".join(result["route"]) if result["route"] else "No feasible route"
    detail_lines = [
        f"Start: {start}",
        f"Destination: {destination}",
        f"Route: {route_text}",
        f"Total distance: {format_number(result['total_distance'])}",
        f"Total risk: {format_number(result['total_risk'])}",
        f"Total detection: {format_number(result['total_detection'])}",
        f"Total modified cost: {format_number(result['total_modified_cost'])}",
        "Cost formula: Distance + Risk_Level * 2 + Detection_Probability * 10",
    ]
    text = build_standard_report(
        1,
        meta,
        key_result=f"Selected route: {route_text}",
        result_explanation="The selected path has the lowest modified cost after combining distance, risk, and detection probability.",
        detail_lines=detail_lines,
    )
    result = attach_outputs(
        result,
        1,
        output_dir,
        text,
        {"route_summary": [
            {
                "Route": route_text,
                "Total_Distance": result["total_distance"],
                "Total_Risk": result["total_risk"],
                "Total_Detection": result["total_detection"],
                "Total_Modified_Cost": result["total_modified_cost"],
            }
        ]},
    )
    return result


# ---------------------------------------------------------------------------
# Part 2: Hash table filtering + Levenshtein verification


def levenshtein_distance(left, right):
    left = to_text(left).lower()
    right = to_text(right).lower()
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current = [i]
        for j, right_char in enumerate(right, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            replace_cost = previous[j - 1] + (0 if left_char == right_char else 1)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]


def aliases_are_near_duplicates(alias_a, alias_b, max_distance=2):
    left = to_text(alias_a).lower()
    right = to_text(alias_b).lower()
    if not left or not right or left == right:
        return False
    distance = levenshtein_distance(left, right)
    if distance > max_distance:
        return False

    compact_left = normalized_name(left)
    compact_right = normalized_name(right)
    same_start = compact_left[:1] == compact_right[:1]
    contains_base = compact_left in compact_right or compact_right in compact_left
    return same_start or contains_base


def run_part2_double_agent_registry(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(2, sheet, dataset_zip_path)
    df = df.dropna(subset=["Agent_ID", "Alias"]).reset_index(drop=True)
    meta["row_count"] = len(df)

    alias_map = defaultdict(list)
    key_map = defaultdict(list)
    site_map = defaultdict(list)
    for idx, row in df.iterrows():
        alias_map[to_text(row.get("Alias")).lower()].append(idx)
        key_map[to_text(row.get("Access_Key")).lower()].append(idx)
        site_map[to_text(row.get("Linked_Site")).lower()].append(idx)

    near_aliases = defaultdict(list)
    alias_values = [to_text(value) for value in df["Alias"].dropna().unique()]
    for i, alias_a in enumerate(alias_values):
        for alias_b in alias_values[i + 1 :]:
            if aliases_are_near_duplicates(alias_a, alias_b):
                distance = levenshtein_distance(alias_a, alias_b)
                near_aliases[alias_a.lower()].append((alias_b, distance))
                near_aliases[alias_b.lower()].append((alias_a, distance))

    suspicious_records = []
    for idx, row in df.iterrows():
        score = 0
        reasons = []
        alias = to_text(row.get("Alias"))
        access_key = to_text(row.get("Access_Key"))
        linked_site = to_text(row.get("Linked_Site"))
        status = to_text(row.get("Status")).lower()

        if len(alias_map[alias.lower()]) > 1:
            score += 3
            reasons.append("same alias +3")
        if access_key and len(key_map[access_key.lower()]) > 1:
            score += 5
            reasons.append("same access key +5")
        if near_aliases[alias.lower()]:
            score += 3
            matches = ", ".join(f"{name} (d={distance})" for name, distance in near_aliases[alias.lower()])
            reasons.append(f"near-duplicate alias +3: {matches}")
        if linked_site and len(site_map[linked_site.lower()]) > 1:
            score += 2
            reasons.append("repeated linked site +2")
        if status in {"suspicious", "missing", "inactive", "unknown", ""}:
            score += 2
            reasons.append("suspicious/missing status +2")

        if score > 0:
            suspicious_records.append(
                {
                    "Agent_ID": to_text(row.get("Agent_ID")),
                    "Alias": alias,
                    "Access_Key": access_key,
                    "Status": to_text(row.get("Status")),
                    "Linked_Site": linked_site,
                    "Suspicion_Score": score,
                    "Reasons": "; ".join(reasons),
                }
            )

    suspicious_records.sort(key=lambda item: (-item["Suspicion_Score"], item["Agent_ID"]))
    detail_lines = [
        "Stage 1: Hash tables filter repeated aliases, access keys, and linked sites.",
        "Stage 2: Levenshtein distance checks near-duplicate aliases.",
        "",
        format_table(
            suspicious_records,
            ["Agent_ID", "Alias", "Access_Key", "Status", "Linked_Site", "Suspicion_Score", "Reasons"],
            max_rows=20,
        ),
    ]
    top_identity = suspicious_records[0] if suspicious_records else {}
    text = build_standard_report(
        2,
        meta,
        key_result=(
            f"Highest suspicious identity: {top_identity.get('Agent_ID', 'None')} "
            f"with score {top_identity.get('Suspicion_Score', 0)}."
        ),
        result_explanation="Hash tables quickly identify exact repeated evidence, then Levenshtein distance adds near-alias evidence before ranking identities by suspicion score.",
        detail_lines=detail_lines,
    )
    result = {"suspicious_identities": suspicious_records, "meta": meta}
    result = attach_outputs(result, 2, output_dir, text, {"suspicious_identities": suspicious_records})
    return result


# ---------------------------------------------------------------------------
# Part 3: Multi-resource dynamic programming knapsack


def dynamic_programming_knapsack(records, capacities=(15, 35, 4)):
    max_energy, max_time, max_tokens = capacities
    states = {(0, 0, 0): (0.0, tuple())}

    for index, record in enumerate(records):
        energy = to_int(record.get("Energy_Cost"))
        time_cost = to_int(record.get("Time_Cost"))
        token = to_int(record.get("Token_Cost"))
        impact = to_float(record.get("Operational_Impact"))
        next_states = dict(states)

        for (used_energy, used_time, used_tokens), (score, chosen) in states.items():
            new_state = (used_energy + energy, used_time + time_cost, used_tokens + token)
            if (
                new_state[0] <= max_energy
                and new_state[1] <= max_time
                and new_state[2] <= max_tokens
            ):
                new_score = score + impact
                old_score, old_chosen = next_states.get(new_state, (-1.0, tuple()))
                if new_score > old_score or (
                    new_score == old_score and len(chosen) + 1 < len(old_chosen)
                ):
                    next_states[new_state] = (new_score, chosen + (index,))
        states = next_states

    best_state = max(
        states,
        key=lambda state: (
            states[state][0],
            -state[0] - state[1] - state[2],
        ),
    )
    best_score, chosen_indexes = states[best_state]
    return {
        "selected_indexes": list(chosen_indexes),
        "total_energy": best_state[0],
        "total_time": best_state[1],
        "total_tokens": best_state[2],
        "total_impact": best_score,
        "capacities": capacities,
    }


def run_part3_resource_lockdown(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(3, sheet, dataset_zip_path)
    df = df.dropna(subset=["Checkpoint"]).reset_index(drop=True)
    meta["row_count"] = len(df)
    records = df.to_dict("records")
    result = dynamic_programming_knapsack(records)
    selected = [records[index] for index in result["selected_indexes"]]
    selected_rows = []
    for row in selected:
        selected_rows.append(
            {
                "Checkpoint": to_text(row.get("Checkpoint")),
                "Energy": to_int(row.get("Energy_Cost")),
                "Time": to_int(row.get("Time_Cost")),
                "Token": to_int(row.get("Token_Cost")),
                "Impact": to_float(row.get("Operational_Impact")),
            }
        )

    result.update({"selected_checkpoints": selected_rows, "meta": meta})
    caps = result["capacities"]
    detail_lines = [
        f"Capacities: Energy {caps[0]}, Time {caps[1]}, Token {caps[2]}",
        "",
        format_table(selected_rows, ["Checkpoint", "Energy", "Time", "Token", "Impact"]),
        "",
        f"Total energy used: {result['total_energy']} / {caps[0]}",
        f"Total time used: {result['total_time']} / {caps[1]}",
        f"Total tokens used: {result['total_tokens']} / {caps[2]}",
        f"Total operational impact: {format_number(result['total_impact'])}",
    ]
    text = build_standard_report(
        3,
        meta,
        key_result=f"Selected {len(selected_rows)} checkpoints with total impact {format_number(result['total_impact'])}.",
        result_explanation="The DP table compares taking or skipping each checkpoint and keeps only combinations within energy, time, and token limits.",
        detail_lines=detail_lines,
    )
    result = attach_outputs(result, 3, output_dir, text, {"selected_checkpoints": selected_rows})
    return result


# ---------------------------------------------------------------------------
# Part 4: MCDA weighted scoring


def joint_risk_from_row(row):
    risk_columns = [
        key
        for key in row.keys()
        if normalized_name(key).endswith("probability") and normalized_name(key) != "detectionprobability"
    ]
    survival = 1.0
    for column in risk_columns:
        probability = min(max(to_float(row.get(column)), 0.0), 1.0)
        survival *= 1.0 - probability
    if risk_columns:
        return 1.0 - survival
    return to_float(row.get("Risk"), 0.0)


def normalize_values(values, benefit=True):
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return [1.0 for _ in values]
    if benefit:
        return [(value - minimum) / (maximum - minimum) for value in values]
    return [(maximum - value) / (maximum - minimum) for value in values]


def run_part4_probability_trap(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(4, sheet, dataset_zip_path)
    df = df.dropna(subset=["Route_ID"]).reset_index(drop=True)
    meta["row_count"] = len(df)
    rows = df.to_dict("records")

    risks = [joint_risk_from_row(row) for row in rows]
    times = [to_float(row.get("Travel_Time")) for row in rows]
    rewards = [to_float(row.get("Success_Reward")) for row in rows]
    normalized_risks = normalize_values(risks, benefit=False)
    normalized_times = normalize_values(times, benefit=False)
    normalized_rewards = normalize_values(rewards, benefit=True)

    scored_rows = []
    for index, row in enumerate(rows):
        final_score = (
            normalized_risks[index] * 0.40
            + normalized_times[index] * 0.20
            + normalized_rewards[index] * 0.40
        )
        scored_rows.append(
            {
                "Route_ID": to_text(row.get("Route_ID")),
                "Route_Name": to_text(row.get("Route_Name")),
                "Joint_Risk": risks[index],
                "N_Risk": normalized_risks[index],
                "N_Time": normalized_times[index],
                "N_Reward": normalized_rewards[index],
                "Final_Score": final_score,
            }
        )

    scored_rows.sort(key=lambda item: item["Final_Score"], reverse=True)
    chosen = scored_rows[0] if scored_rows else {}
    detail_lines = [
        "Weights: Risk 0.40, Time 0.20, Reward 0.40",
        "Multiple risks are combined using joint risk: 1 - product(1 - p_i).",
        "",
        format_table(
            scored_rows,
            ["Route_ID", "Route_Name", "Joint_Risk", "N_Risk", "N_Time", "N_Reward", "Final_Score"],
        ),
        "",
        f"Chosen route: {chosen.get('Route_ID', '')} - {chosen.get('Route_Name', '')}",
    ]
    text = build_standard_report(
        4,
        meta,
        key_result=f"Chosen route: {chosen.get('Route_ID', '')} - {chosen.get('Route_Name', '')}.",
        result_explanation="The chosen route has the strongest weighted balance after normalizing risk, time, and reward.",
        detail_lines=detail_lines,
    )
    result = {"routes": scored_rows, "chosen_route": chosen, "meta": meta}
    result = attach_outputs(result, 4, output_dir, text, {"route_scores": scored_rows})
    return result


# ---------------------------------------------------------------------------
# Part 5: Dynamic programming signal reconstruction


def fragment_value(status):
    status = to_text(status).lower()
    if status == "valid":
        return 2
    if status == "delayed":
        return 1
    return -1


def reconstruct_fragment_group(records):
    ordered = sorted(records, key=lambda row: (to_int(row.get("Sequence_No")), to_text(row.get("Fragment_ID"))))
    dp = [(0, tuple())]
    for record in ordered:
        previous_score, previous_chain = dp[-1]
        value = fragment_value(record.get("Integrity_Status"))
        skip_option = (previous_score, previous_chain)
        if value >= 0:
            take_option = (previous_score + value, previous_chain + (record,))
            dp.append(take_option if take_option[0] >= skip_option[0] else skip_option)
        else:
            dp.append(skip_option)
    used = list(dp[-1][1])
    used_ids = {to_text(row.get("Fragment_ID")) for row in used}
    skipped = [row for row in ordered if to_text(row.get("Fragment_ID")) not in used_ids]
    return used, skipped, dp[-1][0]


def run_part5_split_signal_protocol(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(5, sheet, dataset_zip_path)
    df = df.dropna(subset=["Fragment_ID", "Segment_Group"]).reset_index(drop=True)
    meta["row_count"] = len(df)

    groups = defaultdict(list)
    group_order = []
    for row in df.to_dict("records"):
        group = to_text(row.get("Segment_Group"))
        if group not in groups:
            group_order.append(group)
        groups[group].append(row)

    group_results = []
    activation_parts = []
    skipped_rows = []
    for group in group_order:
        used, skipped, score = reconstruct_fragment_group(groups[group])
        used_blocks = [to_text(row.get("Data_Block")) for row in used]
        activation_parts.extend(used_blocks)
        group_results.append(
            {
                "Group": group,
                "Score": score,
                "Used_Fragments": ", ".join(to_text(row.get("Fragment_ID")) for row in used),
                "Sequence": " ".join(used_blocks),
            }
        )
        for row in skipped:
            skipped_rows.append(
                {
                    "Group": group,
                    "Fragment_ID": to_text(row.get("Fragment_ID")),
                    "Status": to_text(row.get("Integrity_Status")),
                    "Reason": "unrecoverable or lower-value fragment",
                }
            )

    final_sequence = " ".join(activation_parts)
    detail_lines = [
        "Reconstructed groups:",
        format_table(group_results, ["Group", "Score", "Used_Fragments", "Sequence"]),
        "",
        "Skipped fragments:",
        format_table(skipped_rows, ["Group", "Fragment_ID", "Status", "Reason"])
        if skipped_rows
        else "No skipped fragments.",
        "",
        f"Final activation sequence: {final_sequence}",
    ]
    text = build_standard_report(
        5,
        meta,
        key_result=f"Final activation sequence: {final_sequence}",
        result_explanation="Fragments are reconstructed group by group; valid and delayed fragments are used, while corrupted or missing fragments are skipped.",
        detail_lines=detail_lines,
    )
    result = {
        "groups": group_results,
        "skipped_fragments": skipped_rows,
        "final_activation_sequence": final_sequence,
        "meta": meta,
    }
    result = attach_outputs(
        result,
        5,
        output_dir,
        text,
        {"reconstructed_groups": group_results, "skipped_fragments": skipped_rows},
    )
    return result


# ---------------------------------------------------------------------------
# Part 6: Modified stable merge sort


def timestamp_to_seconds(value):
    text = to_text(value)
    try:
        parsed = datetime.strptime(text, "%H:%M:%S")
        return parsed.hour * 3600 + parsed.minute * 60 + parsed.second
    except ValueError:
        try:
            parsed = pd.to_datetime(text)
            return parsed.hour * 3600 + parsed.minute * 60 + parsed.second
        except (ValueError, TypeError, AttributeError):
            return 0


def event_sort_key(event):
    event_type = to_text(event.get("Event_Type")).lower()
    launch_rank = 0 if "launch" in event_type else 1
    return (
        -to_int(event.get("Threat_Priority")),
        timestamp_to_seconds(event.get("Timestamp")),
        launch_rank,
        to_int(event.get("Original_Index")),
    )


def stable_merge_sort_events(events):
    prepared = []
    for index, event in enumerate(events):
        copied = dict(event)
        copied.setdefault("Original_Index", index)
        prepared.append(copied)

    def merge_sort(items):
        if len(items) <= 1:
            return items
        middle = len(items) // 2
        left = merge_sort(items[:middle])
        right = merge_sort(items[middle:])
        return merge(left, right)

    def merge(left, right):
        merged = []
        left_index = 0
        right_index = 0
        while left_index < len(left) and right_index < len(right):
            if event_sort_key(left[left_index]) <= event_sort_key(right[right_index]):
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1
        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        return merged

    return merge_sort(prepared)


def run_part6_countdown_sequence(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(6, sheet, dataset_zip_path)
    df = df.dropna(subset=["Event_ID"]).reset_index(drop=True)
    meta["row_count"] = len(df)
    records = []
    for index, row in df.iterrows():
        record = row.to_dict()
        record["Original_Index"] = index
        records.append(record)

    sorted_events = stable_merge_sort_events(records)
    original_order = [
        {
            "Event_ID": to_text(row.get("Event_ID")),
            "Threat_Priority": to_int(row.get("Threat_Priority")),
            "Timestamp": to_text(row.get("Timestamp")),
            "Zone": to_text(row.get("Zone")),
            "Event_Type": to_text(row.get("Event_Type")),
            "Code_Value": to_int(row.get("Code_Value")),
        }
        for row in records
    ]
    sorted_order = [
        {
            "Event_ID": to_text(row.get("Event_ID")),
            "Threat_Priority": to_int(row.get("Threat_Priority")),
            "Timestamp": to_text(row.get("Timestamp")),
            "Zone": to_text(row.get("Zone")),
            "Event_Type": to_text(row.get("Event_Type")),
            "Code_Value": to_int(row.get("Code_Value")),
        }
        for row in sorted_events
    ]
    top_five = sorted_order[:5]

    columns = ["Event_ID", "Threat_Priority", "Timestamp", "Zone", "Event_Type", "Code_Value"]
    detail_lines = [
        "Sorting key explanation:",
        "(-Threat_Priority, Timestamp, Launch_Rank, Original_Index)",
        "- Negative Threat_Priority makes higher threat values appear first.",
        "- Timestamp puts earlier events first when priority ties.",
        "- Launch_Rank prioritizes launch-related event types when earlier fields tie.",
        "- Original_Index preserves stable arrival order when all priority fields are equal.",
        "",
        "Manual implementation confirmation:",
        "The project implements merge sort manually through stable_merge_sort_events(); it does not rely on Python sorted() as the sorting algorithm for Part 6.",
        "",
        "Why Modified Stable Merge Sort is chosen:",
        "It supports multi-field comparison, preserves equal-record order, and keeps reliable O(nlogn) time even when the stream is scrambled.",
        "",
        "Original event order:",
        format_table(original_order, columns),
        "",
        "Sorted event order:",
        format_table(sorted_order, columns),
        "",
        "Top 5 urgent events:",
        format_table(top_five, columns),
    ]
    text = build_standard_report(
        6,
        meta,
        key_result=f"Top urgent event after sorting: {top_five[0]['Event_ID'] if top_five else 'None'}.",
        result_explanation="Events are ordered by the PPT key: higher threat first, earlier timestamp next, launch relevance next, and original order last for stability.",
        detail_lines=detail_lines,
    )
    result = {
        "original_order": original_order,
        "sorted_order": sorted_order,
        "top_five": top_five,
        "meta": meta,
    }
    result = attach_outputs(
        result,
        6,
        output_dir,
        text,
        {
            "original_order": original_order,
            "sorted_order": sorted_order,
            "top_five": top_five,
        },
    )
    return result


# ---------------------------------------------------------------------------
# Part 7: Controlled randomisation


def controlled_randomisation(sector_records, seed=2005, prediction_penalty=5):
    scored = []
    for row in sector_records:
        risk = (
            to_float(row.get("Patrol_Frequency"))
            + to_float(row.get("Thermal_Scan_Level"))
            + to_float(row.get("Drone_Coverage"))
        )
        if to_text(row.get("Predicted_By_Enemy")).lower() == "yes":
            risk += prediction_penalty
        decoy = to_float(row.get("Decoy_Value"), 1.0)
        selection_score = decoy / max(risk, 0.000001)
        scored.append(
            {
                "Sector": to_text(row.get("Sector")),
                "Risk": risk,
                "Decoy_Value": decoy,
                "Selection_Score": selection_score,
            }
        )

    total_score = sum(row["Selection_Score"] for row in scored)
    for row in scored:
        row["Probability"] = row["Selection_Score"] / total_score if total_score else 0

    random_value = random.Random(seed).random()
    cumulative = 0.0
    chosen = scored[-1] if scored else {}
    for row in scored:
        cumulative += row["Probability"]
        if random_value <= cumulative:
            chosen = row
            break
    return scored, chosen, random_value


def run_part7_phantom_dice(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(7, sheet, dataset_zip_path)
    df = df.dropna(subset=["Sector"]).reset_index(drop=True)
    meta["row_count"] = len(df)
    scored, chosen, random_value = controlled_randomisation(df.to_dict("records"))
    sorted_scores = sorted(scored, key=lambda row: row["Probability"], reverse=True)

    detail_lines = [
        "Risk = Patrol + Thermal + Drone + PredictionPenalty(5 if predicted).",
        "Selection score = Decoy_Value / Risk.",
        "Random seed: 2005",
        f"Random draw: {format_number(random_value)}",
        "",
        format_table(sorted_scores, ["Sector", "Risk", "Decoy_Value", "Selection_Score", "Probability"]),
        "",
        f"Chosen sector: {chosen.get('Sector', '')}",
    ]
    text = build_standard_report(
        7,
        meta,
        key_result=f"Chosen sector: {chosen.get('Sector', '')}.",
        result_explanation="The selected sector comes from weighted randomness, so safer high-decoy sectors are more likely without becoming fully predictable.",
        detail_lines=detail_lines,
    )
    result = {"sector_scores": sorted_scores, "chosen_sector": chosen, "random_draw": random_value, "meta": meta}
    result = attach_outputs(result, 7, output_dir, text, {"sector_scores": sorted_scores})
    return result


# ---------------------------------------------------------------------------
# Part 8: Brute force string matching + threat ranking


def brute_force_find_all(phrase, text):
    phrase = to_text(phrase).lower()
    text = to_text(text).lower()
    if not phrase or len(phrase) > len(text):
        return []
    positions = []
    for start in range(0, len(text) - len(phrase) + 1):
        matched = True
        for offset, phrase_char in enumerate(phrase):
            if text[start + offset] != phrase_char:
                matched = False
                break
        if matched:
            positions.append(start)
    return positions


def brute_force_phrase_match(phrase, text):
    return bool(brute_force_find_all(phrase, text))


def threat_level_from_score(score):
    if score >= 6:
        return "Critical"
    if score >= 3:
        return "High"
    if score >= 1:
        return "Medium"
    return "Low"


def run_part8_silent_code(sheet=None, dataset_zip_path=None, output_dir="outputs"):
    df, meta = prepare_part_dataframe(8, sheet, dataset_zip_path)
    df = df.dropna(subset=["Message_ID", "Text_Stream"]).reset_index(drop=True)
    meta["row_count"] = len(df)

    trigger_weights = dict(DEFAULT_TRIGGER_WEIGHTS)
    if "Trigger_Phrase" in df.columns:
        trigger_weights = {}
        for _, row in df.dropna(subset=["Trigger_Phrase"]).iterrows():
            phrase = to_text(row.get("Trigger_Phrase"))
            trigger_weights[phrase] = to_int(row.get("Threat_Score"), 1)

    ranked_messages = []
    for _, row in df.iterrows():
        text_stream = to_text(row.get("Text_Stream"))
        detected = []
        score = 0
        for phrase, weight in trigger_weights.items():
            if brute_force_phrase_match(phrase, text_stream):
                detected.append(phrase)
                score += weight
        route_tag = to_text(row.get("Route_Tag"))
        if route_tag:
            score += 1
        ranked_messages.append(
            {
                "Message_ID": to_text(row.get("Message_ID")),
                "Detected_Phrases": ", ".join(detected) if detected else "None",
                "Route_Tag": route_tag if route_tag else "None",
                "Threat_Score": score,
                "Threat_Level": threat_level_from_score(score),
            }
        )

    ranked_messages.sort(key=lambda item: (-item["Threat_Score"], item["Message_ID"]))
    top_message = ranked_messages[0] if ranked_messages else {}
    detail_lines = [
        "Fallback trigger phrases are used unless a trigger phrase dataset is present.",
        "",
        format_table(
            ranked_messages,
            ["Message_ID", "Detected_Phrases", "Route_Tag", "Threat_Score", "Threat_Level"],
        ),
    ]
    text = build_standard_report(
        8,
        meta,
        key_result=(
            f"Highest-ranked message: {top_message.get('Message_ID', 'None')} "
            f"with threat score {top_message.get('Threat_Score', 0)}."
        ),
        result_explanation="Each message is scanned with manual brute force phrase matching, then ranked by phrase weights and route-tag evidence.",
        detail_lines=detail_lines,
    )
    result = {"ranked_messages": ranked_messages, "trigger_weights": trigger_weights, "meta": meta}
    result = attach_outputs(result, 8, output_dir, text, {"ranked_messages": ranked_messages})
    return result


def run_all_parts(sheet_overrides=None, dataset_zip_path=None, output_dir="outputs"):
    sheet_overrides = sheet_overrides or {}
    runners = [
        ("part1", run_part1_shadow_network),
        ("part2", run_part2_double_agent_registry),
        ("part3", run_part3_resource_lockdown),
        ("part4", run_part4_probability_trap),
        ("part5", run_part5_split_signal_protocol),
        ("part6", run_part6_countdown_sequence),
        ("part7", run_part7_phantom_dice),
        ("part8", run_part8_silent_code),
    ]
    results = {}
    summary_lines = ["Operation Cypher Nexus - Run Summary", ""]
    metadata_by_part = {}
    for index, (name, runner) in enumerate(runners, start=1):
        result = runner(
            sheet=sheet_overrides.get(index),
            dataset_zip_path=dataset_zip_path,
            output_dir=output_dir,
        )
        results[name] = result
        metadata_by_part[index] = result.get("meta", {})
        csv_files = result.get("csv_files", [])
        summary_lines.extend(
            [
                f"Part {index}: {PART_INFO[index]['title']}",
                f"Dataset file: {result.get('meta', {}).get('member', '')}",
                f"Sheet name: {result.get('meta', {}).get('sheet', '')}",
                f"Row count: {result.get('meta', {}).get('row_count', 0)}",
                f"Columns used: {', '.join(result.get('meta', {}).get('columns_used', []))}",
                f"TXT output: {result.get('output_file')}",
                f"CSV outputs: {', '.join(csv_files) if csv_files else 'None'}",
                "",
            ]
        )

    summary_text = "\n".join(summary_lines)
    write_output(output_dir, "run_summary.txt", summary_text)
    mapping_text = format_data_mapping_report(metadata_by_part)
    mapping_file = write_output(output_dir, "data_mapping_report.txt", mapping_text)
    results["summary"] = {"output_text": summary_text, "output_file": str(Path(output_dir) / "run_summary.txt")}
    results["data_mapping_report"] = {"output_text": mapping_text, "output_file": mapping_file}
    return results


RUNNERS_BY_PART = {
    1: run_part1_shadow_network,
    2: run_part2_double_agent_registry,
    3: run_part3_resource_lockdown,
    4: run_part4_probability_trap,
    5: run_part5_split_signal_protocol,
    6: run_part6_countdown_sequence,
    7: run_part7_phantom_dice,
    8: run_part8_silent_code,
}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run Operation Cypher Nexus algorithms.")
    parser.add_argument("--all", action="store_true", help="Run all parts and save outputs.")
    parser.add_argument("--part", type=int, choices=range(1, 9), help="Run one part only, for example --part 6.")
    parser.add_argument("--sheet", choices=["A", "B", "C"], help="Optional sheet override for the selected part.")
    parser.add_argument("--dataset", help="Optional path to Datasets (2).zip.")
    parser.add_argument("--list-data", action="store_true", help="List dataset files, sheets, row counts, and columns.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        if args.list_data:
            print(list_dataset_contents(args.dataset))
            return

        if args.part:
            result = RUNNERS_BY_PART[args.part](
                sheet=args.sheet,
                dataset_zip_path=args.dataset,
                output_dir="outputs",
            )
            print(result["output_text"])
            print(f"\nTXT output saved to: {result.get('output_file')}")
            if result.get("csv_files"):
                print("CSV outputs saved to:")
                for csv_file in result["csv_files"]:
                    print(f"- {csv_file}")
            return

        results = run_all_parts(dataset_zip_path=args.dataset, output_dir="outputs")
        for index in range(1, 9):
            print(results[f"part{index}"]["output_text"])
            print("\n" + "=" * 80 + "\n")
        print(results["summary"]["output_text"])
        print(f"Data mapping report: {results['data_mapping_report']['output_file']}")
        print("All detailed outputs were saved in the outputs folder.")
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
