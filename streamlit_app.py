"""Mission-style Streamlit dashboard for Operation Cypher Nexus.

This is only a local visualization layer. The source of truth for algorithms
and official outputs remains cypher_nexus_project.py.
"""

import math

import pandas as pd
import streamlit as st

from cypher_nexus_project import (
    PART_INFO,
    RUNNERS_BY_PART,
    TOTAL_PARTS,
    choose_start_and_destination,
    controlled_randomisation,
    event_sort_key,
    joint_risk_from_row,
    modified_risk_aware_dijkstra,
    normalize_values,
    prepare_part_dataframe,
    run_all_parts,
    timestamp_to_seconds,
)


from dashboard_content import (
    ALGORITHM_CHOICES,
    ALGORITHM_DECISIONS,
    ALGORITHM_FLOWS,
    CANDIDATE_ALGORITHMS,
    DEFENSE_MATRIX_COLUMNS,
    DEFENSE_NOTES,
    HELPFUL_CHART_PARTS,
    KEY_TAKEAWAYS,
    MISSION_FEEDBACK,
    MISSION_FORWARD,
    MISSION_OUTCOMES,
    RESULT_KEYS,
    RESULT_PAGE_SECTIONS,
    WHY_IT_MATTERS,
    build_defense_matrix_rows,
    key_output_for_part,
)
from dashboard_i18n import LANGUAGE_OPTIONS, localized_part_info, mission_story, part_label, t


def dataframe_from_rows(rows):
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def extract_key_result(part_number, result):
    return key_output_for_part(part_number, result)


@st.cache_data(show_spinner=False)
def get_part_dataframe_cached(part_number, sheet_override):
    return prepare_part_dataframe(part_number, sheet_override)


@st.cache_data(show_spinner=False)
def run_official_part_cached(part_number, sheet_override):
    return RUNNERS_BY_PART[part_number](sheet=sheet_override, output_dir="outputs")


@st.cache_data(show_spinner=False)
def run_all_official_parts_cached():
    return run_all_parts(output_dir="outputs")


def build_challenge_state(completed_missions=None, coins=0, current_mission=1, mode="landing"):
    completed = set(completed_missions or set())
    badges = [f"Part {part_number} Evidence Mark" for part_number in sorted(completed)]
    return {
        "results": {},
        "mission_log": [],
        "completed_missions": completed,
        "coins": coins,
        "badges": badges,
        "current_mission": current_mission,
        "mode": mode,
        "last_choice_feedback": {},
    }


def mission_status(part_number, completed_missions):
    completed = set(completed_missions or set())
    if part_number in completed:
        return "COMPLETED"
    if part_number == 1 or (part_number - 1) in completed:
        return "READY"
    return "PENDING"


def apply_algorithm_choice(part_number, selected_algorithm, state):
    choices = ALGORITHM_CHOICES[part_number]
    correct = selected_algorithm == choices["correct"]
    if not correct:
        feedback = choices["wrong_feedback"].get(
            selected_algorithm,
            f"{selected_algorithm} is rejected for this mission.",
        )
        return {
            "correct": False,
            "feedback": feedback,
            "expected": choices["correct"],
        }

    completed = state.setdefault("completed_missions", set())
    if not isinstance(completed, set):
        completed = set(completed)
        state["completed_missions"] = completed

    if part_number not in completed:
        completed.add(part_number)
        state["coins"] = int(state.get("coins", 0)) + 1
        badges = state.setdefault("badges", [])
        badge_name = f"Part {part_number} Evidence Mark"
        if badge_name not in badges:
            badges.append(badge_name)

    next_mission = min(TOTAL_PARTS, part_number + 1)
    state["current_mission"] = max(int(state.get("current_mission", 1)), next_mission)
    return {
        "correct": True,
        "feedback": MISSION_FEEDBACK[part_number],
        "expected": choices["correct"],
    }


def sync_session_challenge_state():
    defaults = build_challenge_state()
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
    st.session_state.setdefault("results", {})
    st.session_state.setdefault("direct_results_visible", False)


def reset_challenge_progress():
    defaults = build_challenge_state()
    for key, value in defaults.items():
        st.session_state[key] = value
    st.session_state["results"] = {}
    st.session_state["direct_results_visible"] = False
    st.session_state["nav_index"] = 0


def dataset_metadata_for_part(part_number, result=None, sheet_override=None):
    if result and result.get("meta"):
        return result["meta"]
    if part_number == 9:
        return {
            "member": "Derived from Parts 1, 2, 3, and 8",
            "source": "Previous official outputs",
            "sheet": "N/A",
            "row_count": "-",
            "columns_used": PART_INFO[part_number]["columns"],
        }
    try:
        _, metadata = get_part_dataframe_cached(part_number, sheet_override)
        return metadata
    except Exception as error:  # Streamlit should explain dataset issues instead of crashing the card.
        return {
            "member": f"Dataset preview unavailable: {error}",
            "sheet": sheet_override or "-",
            "row_count": "-",
            "columns_used": PART_INFO[part_number]["columns"],
        }


def build_mission_cards(results, language, completed_missions=None):
    cards = []
    for part_number in range(1, TOTAL_PARTS + 1):
        result = results.get(f"part{part_number}")
        info = localized_part_info(part_number, language)
        status = (
            mission_status(part_number, completed_missions)
            if completed_missions is not None
            else ("COMPLETED" if result else "READY")
        )
        cards.append(
            {
                "part_number": part_number,
                "mission_name": info["title"],
                "chosen_algorithm": PART_INFO[part_number]["algorithm"],
                "status": status,
                "key_result": extract_key_result(part_number, result),
            }
        )
    return cards


from dashboard_components import (
    add_mission_log,
    badge,
    badge_list_html,
    card_html,
    coin_reward_panel_html,
    feedback_card_html,
    flowchart_html,
    inject_css,
    render_dataset_card,
    render_mission_log as render_log_component,
    render_table_note,
    reward_chip,
    section_header,
    trace_step_card_html,
)


def mission_log_add(message):
    add_mission_log(st.session_state, message)


def run_part_and_store(part_number, sheet_override, language):
    result = run_official_part_cached(part_number, sheet_override)
    st.session_state.results[f"part{part_number}"] = result
    mission_log_add(
        f"Part {part_number}: {MISSION_FEEDBACK[part_number]} Official output saved; key result: {extract_key_result(part_number, result)}."
    )
    st.session_state.last_completed = part_number
    st.session_state.celebrate_part = part_number
    st.toast(t("mission_completed", language))
    return result


def render_coin_reward_for_part(part_number, language, feedback=None):
    message = feedback.get("feedback") if feedback else MISSION_FEEDBACK[part_number]
    badge_label = f"Part {part_number} Evidence Mark"
    st.markdown(
        coin_reward_panel_html(
            title=t("coin_reward", language),
            message=f"{message} {t('result_unlocked', language)}.",
            coins=st.session_state.get("coins", 0),
            badge_label=badge_label,
            result_label=t("result_unlocked", language),
            wallet_label=t("wallet_balance", language),
            badge_prefix=t("badge_unlocked", language),
        ),
        unsafe_allow_html=True,
    )


def render_progress_strip(language):
    completed = set(st.session_state.get("completed_missions", set()))
    completed_count = len(completed)
    coins = st.session_state.get("coins", 0)
    badges = st.session_state.get("badges", [])
    st.markdown(
        f"""
        <div class="mission-strip">
            <div class="strip-cell"><div class="card-small">{t('progress', language)}</div><div class="strip-number">{completed_count}/{TOTAL_PARTS}</div></div>
            <div class="strip-cell"><div class="card-small">{t('coins', language)}</div><div class="strip-number">{coins}</div></div>
            <div class="strip-cell"><div class="card-small">{t('badges', language)}</div><div class="strip-number">{len(badges)}</div></div>
            <div class="strip-cell"><div class="card-small">{t('mission_challenge_mode', language)}</div><div class="strip-number">{mission_status(st.session_state.get('current_mission', 1), completed)}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(completed_count / TOTAL_PARTS, text=f"{completed_count} / {TOTAL_PARTS}")


def render_landing(language):
    completed = set(st.session_state.get("completed_missions", set()))
    completed_count = len(completed)
    coins = st.session_state.get("coins", 0)
    badges = st.session_state.get("badges", [])
    st.markdown(
        f"""
        <div class="mission-hero">
            <div class="mission-subtitle">{t('subtitle', language)}</div>
            <h1>{t('title', language)}</h1>
            <p>{t('story', language)}</p>
            {badge(f"{completed_count} / {TOTAL_PARTS} {t('completed_missions', language)}", 'complete' if completed_count == TOTAL_PARTS else 'ready')}
            {badge(f"{t('coins', language)}: {coins}", 'ready')}
            {badge(f"{t('badges', language)}: {len(badges)}", 'muted')}
            {badge(t('optional_note', language), 'muted')}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"**{t('progress', language)}**")
    st.progress(completed_count / TOTAL_PARTS, text=f"{completed_count} / {TOTAL_PARTS}")

    first, second, third = st.columns(3)
    with first:
        if st.button(t("start_challenge", language), type="primary", width="stretch"):
            st.session_state.mode = "challenge"
            st.session_state.nav_index = st.session_state.get("current_mission", 1)
            st.rerun()
    with second:
        if st.button(t("direct_demo_mode", language), width="stretch"):
            st.session_state.mode = "direct"
            st.rerun()
    with third:
        if st.button(t("reset_progress", language), width="stretch"):
            reset_challenge_progress()
            st.rerun()

    cards = build_mission_cards(st.session_state.get("results", {}), language, completed_missions=completed)
    rows = [st.columns(3) for _ in range(math.ceil(len(cards) / 3))]
    for index, mission_card in enumerate(cards):
        with rows[index // 3][index % 3]:
            st.markdown(
                card_html(
                    f"{t('part_word', language)} {mission_card['part_number']}: {mission_card['mission_name']}",
                    mission_card["chosen_algorithm"],
                    status=mission_card["status"],
                    key_result=mission_card["key_result"],
                ),
                unsafe_allow_html=True,
            )
    render_defense_matrix(st.session_state.get("results", {}), language)
    render_mission_log(language)


def render_dataset_panel(part_number, result, language, sheet_override=None):
    meta = dataset_metadata_for_part(part_number, result, sheet_override)
    render_dataset_card(
        meta,
        {
            "dataset_loaded": t("dataset_loaded", language),
            "dataset_file": t("dataset_file", language),
            "sheet_used": t("sheet_used", language),
            "rows_used": t("rows_used", language),
            "columns_used": t("columns_used", language),
        },
    )


def render_candidate_algorithms(part_number):
    rows = []
    chosen = ALGORITHM_CHOICES[part_number]["correct"]
    for name in CANDIDATE_ALGORITHMS[part_number]:
        rows.append({"Algorithm": name, "Decision": "Chosen" if name == chosen else "Rejected / baseline"})
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def render_rejected_algorithms(part_number):
    info = PART_INFO[part_number]
    st.markdown('<div class="reject-box">', unsafe_allow_html=True)
    for reason in info["rejected"]:
        st.write(f"- {reason}")
    st.markdown("</div>", unsafe_allow_html=True)


def render_complexity(part_number, language):
    complexity = PART_INFO[part_number]["complexity"]
    pieces = [piece.strip() for piece in complexity.split(",")]
    rendered = []
    for piece in pieces:
        kind = "complete" if piece.lower().startswith("time") else "muted"
        rendered.append(badge(piece, kind))
    st.markdown(" ".join(rendered), unsafe_allow_html=True)


def render_algorithm_flow(part_number, language):
    flow = ALGORITHM_FLOWS.get(part_number)
    if not flow:
        st.info("Algorithm flow explanation is not available for this Part.")
        return
    st.markdown(flowchart_html(flow, title=t("algorithm_flow_note", language)), unsafe_allow_html=True)


def existing_columns(df, columns):
    return [column for column in columns if column in df.columns]


def limited_df(df, columns=None, rows=8):
    if df is None or df.empty:
        return pd.DataFrame()
    selected = df[existing_columns(df, columns)] if columns else df
    return selected.head(rows).reset_index(drop=True)


def render_trace_table(title, note, data, columns=None, rows=8):
    st.markdown(trace_step_card_html(title.split(" ", 1)[0], title, note), unsafe_allow_html=True)
    df = dataframe_from_rows(data) if isinstance(data, list) else data
    table = limited_df(df, columns, rows)
    if table.empty:
        st.caption("No trace data available for this step.")
        return
    st.dataframe(table, width="stretch", hide_index=True)


def dataset_trace_dataframe(part_number, sheet_override):
    if part_number == 9:
        return pd.DataFrame()
    try:
        df, _ = get_part_dataframe_cached(part_number, sheet_override)
        return df
    except Exception as error:
        st.warning(f"Dataset trace unavailable: {error}")
        return pd.DataFrame()


def render_algorithm_trace(part_number, result, language, sheet_override):
    st.markdown(
        trace_step_card_html(
            "TRACE",
            "Dataset to output trace",
            "This section uses real dataset rows, intermediate calculation tables, and the official result to show how the algorithm transforms input into output.",
        ),
        unsafe_allow_html=True,
    )

    df = dataset_trace_dataframe(part_number, sheet_override)

    if part_number != 9:
        render_trace_table(
            "01 Real dataset input",
            "Sample rows from the actual dataset columns used by this Part.",
            df,
            PART_INFO[part_number]["columns"],
            rows=8,
        )

    if not result:
        st.info("Run this Part or use Direct Demo Mode to unlock the intermediate calculation and final output trace.")
        return

    if part_number == 1:
        edge_df = df.copy()
        for column in ["Distance", "Risk_Level", "Detection_Probability"]:
            edge_df[column] = pd.to_numeric(edge_df[column], errors="coerce").fillna(0)
        edge_df["Modified_Cost"] = edge_df["Distance"] + edge_df["Risk_Level"] * 2 + edge_df["Detection_Probability"] * 10
        render_trace_table(
            "02 Edge cost calculation",
            "Each directed edge is converted into the modified Dijkstra cost: Distance + Risk_Level * 2 + Detection_Probability * 10.",
            edge_df,
            ["From_Node", "To_Node", "Distance", "Risk_Level", "Detection_Probability", "Route_Status", "Modified_Cost"],
            rows=10,
        )
        route = result.get("route", [])
        route_pairs = list(zip(route, route[1:]))
        selected_edges = []
        for source, target in route_pairs:
            match = edge_df[(edge_df["From_Node"].astype(str) == str(source)) & (edge_df["To_Node"].astype(str) == str(target))]
            if not match.empty:
                selected_edges.append(match.iloc[0].to_dict())
        render_trace_table(
            "03 Selected path evidence",
            "The final route is reconstructed from the lowest modified-cost predecessor chain.",
            selected_edges,
            ["From_Node", "To_Node", "Distance", "Risk_Level", "Detection_Probability", "Modified_Cost"],
            rows=10,
        )

    elif part_number == 2:
        duplicate_rows = []
        for column in ["Alias", "Access_Key", "Linked_Site"]:
            if column not in df.columns:
                continue
            counts = df[column].dropna().astype(str).value_counts()
            for value, count in counts[counts > 1].items():
                duplicate_rows.append({"Evidence_Field": column, "Repeated_Value": value, "Count": int(count)})
        render_trace_table(
            "02 Hash-table evidence",
            "Repeated aliases, access keys, and linked sites are grouped before suspicion scoring.",
            duplicate_rows,
            ["Evidence_Field", "Repeated_Value", "Count"],
            rows=12,
        )
        render_trace_table(
            "03 Suspicion score output",
            "The final table combines exact duplicates, near-alias checks, linked-site evidence, and status risk.",
            result.get("suspicious_identities", []),
            ["Agent_ID", "Alias", "Access_Key", "Status", "Linked_Site", "Suspicion_Score", "Reasons"],
            rows=10,
        )

    elif part_number == 3:
        selected = dataframe_from_rows(result.get("selected_checkpoints", []))
        if not selected.empty:
            selected["Cumulative_Energy"] = selected["Energy"].cumsum()
            selected["Cumulative_Time"] = selected["Time"].cumsum()
            selected["Cumulative_Token"] = selected["Token"].cumsum()
            selected["Cumulative_Impact"] = selected["Impact"].cumsum()
        render_trace_table(
            "02 DP resource decision",
            "The selected checkpoints show how the DP result accumulates resources while staying inside capacity limits.",
            selected,
            ["Checkpoint", "Energy", "Time", "Token", "Impact", "Cumulative_Energy", "Cumulative_Time", "Cumulative_Token", "Cumulative_Impact"],
            rows=10,
        )
        caps = result.get("capacities", (0, 0, 0))
        usage = pd.DataFrame(
            [
                {"Resource": "Energy", "Used": result.get("total_energy", 0), "Capacity": caps[0]},
                {"Resource": "Time", "Used": result.get("total_time", 0), "Capacity": caps[1]},
                {"Resource": "Token", "Used": result.get("total_tokens", 0), "Capacity": caps[2]},
            ]
        )
        usage["Remaining"] = usage["Capacity"] - usage["Used"]
        render_trace_table("03 Final resource usage", "The official output is checked against all resource constraints.", usage)

    elif part_number == 4:
        render_trace_table(
            "02 MCDA normalized scoring",
            "Raw route uncertainty is transformed into normalized risk, time, reward, and final weighted score.",
            result.get("routes", []),
            ["Route_ID", "Route_Name", "Joint_Risk", "N_Risk", "N_Time", "N_Reward", "Final_Score"],
            rows=10,
        )
        render_trace_table(
            "03 Chosen route evidence",
            "The first row after sorting by Final_Score is the official route decision.",
            [result.get("chosen_route", {})],
            ["Route_ID", "Route_Name", "Joint_Risk", "N_Risk", "N_Time", "N_Reward", "Final_Score"],
        )

    elif part_number == 5:
        render_trace_table(
            "02 Fragment reconstruction",
            "Each segment group records which fragments were kept and the reconstructed sequence after DP-style evaluation.",
            result.get("groups", []),
            ["Group", "Score", "Used_Fragments", "Sequence"],
            rows=10,
        )
        render_trace_table(
            "03 Skipped fragment evidence",
            "Fragments that are corrupted, missing, or lower-value are explicitly recorded instead of silently ignored.",
            result.get("skipped_fragments", []),
            ["Group", "Fragment_ID", "Status", "Reason"],
            rows=10,
        )

    elif part_number == 6:
        key_rows = []
        for index, row in df.reset_index(drop=True).iterrows():
            record = row.to_dict()
            record["Original_Index"] = index
            key = event_sort_key(record)
            key_rows.append(
                {
                    "Event_ID": record.get("Event_ID"),
                    "Threat_Priority": record.get("Threat_Priority"),
                    "Timestamp": record.get("Timestamp"),
                    "Event_Type": record.get("Event_Type"),
                    "Original_Index": index,
                    "Negative_Priority": key[0],
                    "Timestamp_Seconds": timestamp_to_seconds(record.get("Timestamp")),
                    "Launch_Rank": key[2],
                    "Full_Sort_Key": str(key),
                }
            )
        render_trace_table(
            "02 Sorting key table",
            "Every event receives the exact key used by Modified Stable Merge Sort: (-Threat_Priority, Timestamp, Launch_Rank, Original_Index).",
            key_rows,
            ["Event_ID", "Threat_Priority", "Timestamp", "Event_Type", "Original_Index", "Negative_Priority", "Timestamp_Seconds", "Launch_Rank", "Full_Sort_Key"],
            rows=12,
        )
        render_trace_table(
            "03 Stable sorted output",
            "The final sorted order is produced by comparing the sort keys while preserving original order for full ties.",
            result.get("sorted_order", []),
            ["Event_ID", "Threat_Priority", "Timestamp", "Zone", "Event_Type", "Code_Value"],
            rows=12,
        )
        render_trace_table(
            "04 Top urgent events",
            "The first five rows after sorting are the urgent action list used in the official output.",
            result.get("top_five", []),
            ["Event_ID", "Threat_Priority", "Timestamp", "Zone", "Event_Type", "Code_Value"],
            rows=5,
        )

    elif part_number == 7:
        render_trace_table(
            "02 Risk-to-probability table",
            "Sector risk and decoy value are converted into selection score and probability.",
            result.get("sector_scores", []),
            ["Sector", "Risk", "Decoy_Value", "Selection_Score", "Probability"],
            rows=10,
        )
        render_trace_table(
            "03 Controlled random draw",
            "A fixed random seed makes the demonstration reproducible while still avoiding deterministic movement.",
            [
                {
                    "Random_Draw": result.get("random_draw"),
                    "Chosen_Sector": result.get("chosen_sector", {}).get("Sector"),
                    "Chosen_Probability": result.get("chosen_sector", {}).get("Probability"),
                }
            ],
        )

    elif part_number == 8:
        weights = [{"Trigger_Phrase": phrase, "Weight": weight} for phrase, weight in result.get("trigger_weights", {}).items()]
        render_trace_table(
            "02 Trigger phrase weights",
            "Each phrase contributes threat points when brute-force matching finds it inside a message.",
            weights,
            ["Trigger_Phrase", "Weight"],
            rows=12,
        )
        render_trace_table(
            "03 Ranked message output",
            "Detected phrases and route-tag evidence become the final threat score and threat level.",
            result.get("ranked_messages", []),
            ["Message_ID", "Detected_Phrases", "Route_Tag", "Threat_Score", "Threat_Level"],
            rows=10,
        )

    elif part_number == 9:
        render_trace_table(
            "01 Previous output inputs",
            "Part 9 has no separate dataset; it synthesizes official outputs from Parts 1, 2, 3, and 8.",
            result.get("strategy_steps", []),
            ["Phase", "Source", "Decision", "Evidence"],
            rows=8,
        )
        render_trace_table(
            "02 Threat and target evidence",
            "The final strategy combines high-ranked messages with DP-selected high-impact targets.",
            result.get("top_threats", []) + result.get("selected_targets", []),
            rows=10,
        )
        render_trace_table(
            "03 Final effects",
            "The final output is a constrained disruption plan with explicit resource usage and expected mission effects.",
            [{"Effect": effect} for effect in result.get("final_effects", [])],
        )


def render_key_result(part_number, result, language):
    key = extract_key_result(part_number, result)
    st.markdown(
        f"""
        <div class="result-card">
            {badge(t('mission_completed', language), 'complete') if result else badge(t('ready', language), 'ready')}
            <div class="card-title">{key}</div>
            <div class="card-small">{MISSION_FEEDBACK[part_number] if result else MISSION_OUTCOMES[part_number]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if result:
        st.markdown(
            '<div class="reward-row">'
            + reward_chip(t("dataset_loaded", language))
            + reward_chip(t("algorithm_executed", language))
            + reward_chip(t("output_saved", language))
            + "</div>",
            unsafe_allow_html=True,
        )


def render_visualization(part_number, result, language):
    if not result:
        st.caption("Run this mission to unlock the output table and chart.")
        return

    if part_number == 1:
        route = " -> ".join(result.get("route", []))
        st.success(f"{t('selected_route', language)}: {route}")
        render_table_note("Route evidence summary: distance, accumulated risk, detection exposure, and final modified cost.")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Total Distance": result.get("total_distance"),
                        "Total Risk": result.get("total_risk"),
                        "Total Detection": result.get("total_detection"),
                        "Total Modified Cost": result.get("total_modified_cost"),
                    }
                ]
            ),
            width="stretch",
            hide_index=True,
        )
    elif part_number == 2:
        df = dataframe_from_rows(result.get("suspicious_identities", []))
        render_table_note("Suspicion table ranked by exact duplicate evidence, near-alias evidence, linked site evidence, and status risk.")
        st.dataframe(df, width="stretch", hide_index=True)
        if not df.empty:
            st.caption("Suspicion score chart")
            st.bar_chart(df.set_index("Agent_ID")["Suspicion_Score"])
    elif part_number == 3:
        df = dataframe_from_rows(result.get("selected_checkpoints", []))
        render_table_note("Selected checkpoints are the DP-backed lockdown plan under energy, time, and token limits.")
        st.dataframe(df, width="stretch", hide_index=True)
        caps = result.get("capacities", (1, 1, 1))
        usage = [
            ("Energy", result.get("total_energy", 0), caps[0]),
            ("Time", result.get("total_time", 0), caps[1]),
            ("Token", result.get("total_tokens", 0), caps[2]),
        ]
        usage_rows = []
        for label, used, cap in usage:
            usage_rows.append({"Resource": label, "Used": used, "Capacity": cap, "Remaining": max(cap - used, 0)})
            st.write(f"{label}: {used} / {cap}")
            st.progress(min(float(used) / float(cap), 1.0) if cap else 0)
        st.caption("Resource usage chart")
        st.bar_chart(pd.DataFrame(usage_rows).set_index("Resource")[["Used", "Remaining"]])
        st.metric("Total Operational Impact", result.get("total_impact", 0))
    elif part_number == 4:
        df = dataframe_from_rows(result.get("routes", []))
        render_table_note("Route score table shows the normalized MCDA criteria and final score used for the official route decision.")
        st.dataframe(df, width="stretch", hide_index=True)
        if not df.empty:
            st.caption("Final route score chart")
            st.bar_chart(df.set_index("Route_ID")["Final_Score"])
    elif part_number == 5:
        render_table_note("Signal reconstruction evidence is split between fragments used and fragments skipped.")
        st.write("Reconstructed groups")
        st.dataframe(dataframe_from_rows(result.get("groups", [])), width="stretch", hide_index=True)
        st.write("Skipped fragments")
        st.dataframe(dataframe_from_rows(result.get("skipped_fragments", [])), width="stretch", hide_index=True)
    elif part_number == 6:
        render_part6_tables(result, language)
    elif part_number == 7:
        df = dataframe_from_rows(result.get("sector_scores", []))
        render_table_note("Sector probabilities show controlled randomness: safer high-decoy sectors become more likely without becoming deterministic.")
        st.dataframe(df, width="stretch", hide_index=True)
        if not df.empty:
            st.caption("Sector probability chart")
            st.bar_chart(df.set_index("Sector")["Probability"])
    elif part_number == 8:
        df = dataframe_from_rows(result.get("ranked_messages", []))
        render_table_note("Threat ranking connects phrase detections and route tags to a defendable final priority order.")
        st.dataframe(df, width="stretch", hide_index=True)
        if not df.empty:
            st.caption("Threat score chart")
            st.bar_chart(df.set_index("Message_ID")["Threat_Score"])
    elif part_number == 9:
        render_table_note("Part 9 synthesizes previous official outputs into one final strategy instead of loading a new dataset.")
        st.write("Mission synthesis")
        st.dataframe(dataframe_from_rows(result.get("strategy_steps", [])), width="stretch", hide_index=True)
        threats = dataframe_from_rows(result.get("top_threats", []))
        if not threats.empty:
            st.write("Top threats from Part 8")
            st.dataframe(threats, width="stretch", hide_index=True)
        targets = dataframe_from_rows(result.get("selected_targets", []))
        if not targets.empty:
            st.write("Selected disruption targets")
            st.dataframe(targets, width="stretch", hide_index=True)
            st.caption("Target impact chart")
            st.bar_chart(targets.set_index("Target")["Impact"])
        caps = result.get("capacities", (1, 1, 1))
        usage = [
            ("Energy", result.get("total_energy", 0), caps[0]),
            ("Time", result.get("total_time", 0), caps[1]),
            ("Token", result.get("total_tokens", 0), caps[2]),
        ]
        for label, used, cap in usage:
            st.write(f"{label}: {used} / {cap}")
            st.progress(min(float(used) / float(cap), 1.0) if cap else 0)
        effects = result.get("final_effects", [])
        if effects:
            st.write("Final effects")
            for effect in effects:
                st.write(f"- {effect}")


def render_part6_tables(result, language):
    st.markdown(f"**{t('sorting_key', language)}:** `(-Threat_Priority, Timestamp, Launch_Rank, Original_Index)`")
    st.write("Higher priority first; earlier timestamp first; launch-related first; preserve original order.")
    st.markdown(badge(t("manual_merge", language), "complete"), unsafe_allow_html=True)
    st.markdown(f"**{t('stable_sorting', language)}**")
    st.write(t("stable_sorting_note", language))
    left, right = st.columns(2)
    with left:
        st.write(t("original_order", language))
        render_table_note("Original dataset arrival order before the manual stable merge sort.")
        st.dataframe(dataframe_from_rows(result.get("original_order", [])), width="stretch", hide_index=True)
    with right:
        st.write(t("sorted_order", language))
        render_table_note("Sorted order after applying priority, timestamp, launch rank, and original index.")
        st.dataframe(dataframe_from_rows(result.get("sorted_order", [])), width="stretch", hide_index=True)
    top = dataframe_from_rows(result.get("top_five", []))
    st.write(t("top_five", language))
    if not top.empty:
        render_table_note("Top urgent events are highlighted to support explanation of the sorting result.")
        st.dataframe(top.style.highlight_max(subset=["Threat_Priority"], color="#fff2a8"), width="stretch")
        st.caption("Top urgent events threat-priority chart")
        st.bar_chart(top.set_index("Event_ID")["Threat_Priority"])


def render_demo_controls(part_number, result, sheet_override, language):
    if part_number not in {1, 4, 7}:
        return
    with st.expander(f"{t('demo_mode', language)}"):
        st.caption(t("demo_controls_hint", language))
        if not st.checkbox(t("enable_demo_controls", language), key=f"enable_demo_controls_{part_number}"):
            return
        if part_number == 1:
            df, _ = get_part_dataframe_cached(1, sheet_override)
            nodes = sorted(set(df["From_Node"].dropna().astype(str)) | set(df["To_Node"].dropna().astype(str)))
            default_start, default_end = choose_start_and_destination(df)
            start = st.selectbox(t("start_node", language), nodes, index=nodes.index(default_start) if default_start in nodes else 0)
            end = st.selectbox(t("end_node", language), nodes, index=nodes.index(default_end) if default_end in nodes else len(nodes) - 1)
            demo = modified_risk_aware_dijkstra(df.to_dict("records"), start, end)
            st.write(f"{t('selected_route', language)}: {' -> '.join(demo.get('route', [])) or 'No route'}")
        elif part_number == 4 and result:
            risk_weight = st.slider(t("risk_weight", language), 0.0, 1.0, 0.40, 0.05)
            time_weight = st.slider(t("time_weight", language), 0.0, 1.0, 0.20, 0.05)
            reward_weight = st.slider(t("reward_weight", language), 0.0, 1.0, 0.40, 0.05)
            total = risk_weight + time_weight + reward_weight or 1.0
            rows = []
            for row in result.get("routes", []):
                score = (
                    row["N_Risk"] * risk_weight
                    + row["N_Time"] * time_weight
                    + row["N_Reward"] * reward_weight
                ) / total
                rows.append({"Route_ID": row["Route_ID"], "Route_Name": row["Route_Name"], "Demo_Score": score})
            rows.sort(key=lambda item: item["Demo_Score"], reverse=True)
            st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        elif part_number == 7:
            seed = st.slider(t("random_seed", language), 1, 9999, 2005)
            df, _ = get_part_dataframe_cached(7, sheet_override)
            scores, chosen, _ = controlled_randomisation(df.to_dict("records"), seed=seed)
            st.write(f"{t('chosen_sector', language)}: {chosen.get('Sector', '')}")
            st.dataframe(pd.DataFrame(scores), width="stretch", hide_index=True)


def render_defense_notes(part_number):
    for note in DEFENSE_NOTES[part_number]:
        st.write(f"- {note}")


def render_key_takeaway(part_number, language):
    section_header(t("key_takeaway", language), 1)
    st.markdown(
        f"""
        <div class="result-card">
            {badge(t('key_takeaway', language), 'complete')}
            <div class="card-title">{KEY_TAKEAWAYS[part_number]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_why_it_matters(part_number, language):
    section_header(t("why_it_matters", language), 2)
    st.markdown(
        f"""
        <div class="section-card why-card">
            {badge(t('why_it_matters', language), 'complete')}
            <div class="card-title">{WHY_IT_MATTERS[part_number]}</div>
            <div class="card-small">{MISSION_FORWARD[part_number]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_defense_matrix(results, language):
    section_header(t("defense_matrix", language))
    st.caption(f"Group-wide evidence that all {TOTAL_PARTS} Parts include dataset usage or synthesis evidence, algorithm comparison, output, and complexity.")
    rows = build_defense_matrix_rows(results)
    st.dataframe(pd.DataFrame(rows, columns=DEFENSE_MATRIX_COLUMNS), width="stretch", hide_index=True)


def render_algorithm_choice(part_number, language, sheet_override):
    choices = ALGORITHM_CHOICES[part_number]
    section_header(t("choose_algorithm", language))
    st.caption("Alternative selections are used only for algorithm comparison. Official outputs stay unchanged until the selected runner executes.")
    columns = st.columns(3)
    for index, option in enumerate(choices["options"]):
        with columns[index]:
            st.markdown(
                f"""
                <div class="choice-card">
                    {badge('OPTION ' + str(index + 1), 'muted')}
                    <strong>{option}</strong>
                    <span class="card-small">Select to compare the reasoning.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(option, key=f"choice_{part_number}_{index}", width="stretch"):
                feedback = apply_algorithm_choice(part_number, option, st.session_state)
                st.session_state.last_choice_feedback[part_number] = feedback
                if feedback["correct"]:
                    result_key = f"part{part_number}"
                    if result_key not in st.session_state.results:
                        with st.spinner(t("running_selected", language)):
                            run_part_and_store(part_number, sheet_override, language)
                else:
                    mission_log_add(f"Part {part_number}: {option} rejected. {feedback['feedback']}")
                st.rerun()

    feedback = st.session_state.get("last_choice_feedback", {}).get(part_number)
    if not feedback:
        return False
    if feedback["correct"]:
        return True
    st.error(f"{t('wrong_algorithm', language)}: {feedback['feedback']}")
    st.markdown(
        feedback_card_html(
            t("wrong_algorithm", language),
            f"<b>{t('why_rejected', language)}:</b> {feedback['feedback']}<br><b>{t('try_again', language)}:</b> {t('retry_choice', language)}",
            kind="danger",
        ),
        unsafe_allow_html=True,
    )
    st.warning(t("retry_choice", language))
    return False


def render_mission_intro(part_number, result, language, sheet_override, status=None):
    info = localized_part_info(part_number, language)

    render_key_takeaway(part_number, language)
    render_why_it_matters(part_number, language)

    section_header(t("mission_brief", language), 3)
    st.markdown(
        card_html(
            part_label(part_number, language),
            f"{mission_story(part_number, language)}<br><br><b>{t('computational_problem', language)}:</b> {info['mission_problem']}",
            status=status,
            key_result=MISSION_OUTCOMES[part_number],
        ),
        unsafe_allow_html=True,
    )

    section_header(t("dataset_used", language), 4)
    render_dataset_panel(part_number, result, language, sheet_override)
    return info


def render_algorithm_analysis_sections(part_number, result, language, sheet_override, show_run_button=True):
    section_header(t("algorithm_decision", language), 5)
    st.markdown(
        f"""
        <div class="section-card">
            {badge(t('chosen_algorithm', language), 'complete')}
            <div class="card-title">{PART_INFO[part_number]["algorithm"]}</div>
            <div class="card-small">{ALGORITHM_DECISIONS[part_number]}</div>
            <div class="card-small">{t('official_layer_note', language)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_header(t("candidate_algorithms", language), 6)
    render_candidate_algorithms(part_number)

    section_header(t("rejected_algorithms", language), 7)
    render_rejected_algorithms(part_number)

    section_header(t("chosen_algorithm", language), 8)
    st.markdown(f'<div class="chosen-box"><b>{PART_INFO[part_number]["algorithm"]}</b></div>', unsafe_allow_html=True)

    section_header(t("algorithm_flow", language), 9)
    render_algorithm_flow(part_number, language)

    section_header(t("algorithm_trace", language), 10)
    render_algorithm_trace(part_number, result, language, sheet_override)

    if show_run_button:
        section_header(t("run_algorithm", language), 11)
        if st.button(t("run_selected", language), type="primary", key=f"run_part_{part_number}"):
            with st.spinner(t("running_selected", language)):
                result = run_part_and_store(part_number, sheet_override, language)
            st.success(f"{t('mission_completed', language)}: {MISSION_FEEDBACK[part_number]}")
        elif result:
            st.success(f"{t('mission_completed', language)}: {MISSION_FEEDBACK[part_number]}")

    section_header(t("key_result", language), 12)
    render_key_result(part_number, result, language)

    section_header(t("visualization", language), 13)
    render_visualization(part_number, result, language)
    render_demo_controls(part_number, result, sheet_override, language)

    section_header(t("time_space_complexity", language), 14)
    render_complexity(part_number, language)

    section_header(t("defense_notes", language), 15)
    render_defense_notes(part_number)

    section_header(t("mission_forward", language), 16)
    st.write(MISSION_FORWARD[part_number])

    if result:
        with st.expander(t("full_output", language)):
            st.text(result.get("output_text", ""))

    return result


def render_result_sections(part_number, result, language, sheet_override, show_run_button=True):
    render_mission_intro(part_number, result, language, sheet_override)
    return render_algorithm_analysis_sections(part_number, result, language, sheet_override, show_run_button)


def render_final_completion(language):
    completed = set(st.session_state.get("completed_missions", set()))
    if len(completed) < TOTAL_PARTS:
        return
    completed_names = ", ".join(part_label(part_number, language) for part_number in sorted(completed))
    badges = st.session_state.get("badges", [])
    st.markdown(
        f"""
        <div class="result-card">
            {badge(t('final_complete', language), 'complete')}
            <div class="card-title">{t('final_complete', language)} - {TOTAL_PARTS} / {TOTAL_PARTS} {t('completed_missions', language)}</div>
            <div class="card-small"><b>{t('final_mission_summary', language)}:</b> {t('final_summary', language)}</div>
            <div class="card-small"><b>{t('total_rewards', language)}:</b> {t('coins', language)}: {st.session_state.get('coins', 0)} | {t('badges', language)}: {len(badges)}</div>
            <div class="card-small"><b>{t('completed_missions', language)}:</b> {completed_names}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"**{t('badge_list', language)}**", unsafe_allow_html=True)
    st.markdown(badge_list_html(badges, t("no_badges", language)), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("view_all_outputs", language), width="stretch"):
            st.session_state.mode = "direct"
            st.session_state.direct_results_visible = True
            st.rerun()
    with col2:
        if st.button(t("restart_challenge", language), width="stretch"):
            reset_challenge_progress()
            st.session_state.mode = "challenge"
            st.rerun()


def render_mission_log(language):
    render_log_component(st.session_state.get("mission_log", []), t("mission_log", language))


def next_part_button(part_number, language):
    next_part = 1 if part_number == TOTAL_PARTS else part_number + 1
    if st.button(f"{t('next_mission', language)}: {part_label(next_part, language)}"):
        st.session_state.nav_index = next_part
        st.session_state.current_mission = next_part
        st.rerun()


def render_part_page(part_number, language, sheet_override):
    result = st.session_state.get("results", {}).get(f"part{part_number}")
    result = render_result_sections(part_number, result, language, sheet_override, show_run_button=True)

    if result:
        next_part_button(part_number, language)

    render_mission_log(language)


def render_challenge_part_page(part_number, language, sheet_override):
    completed = set(st.session_state.get("completed_missions", set()))
    status = mission_status(part_number, completed)
    st.session_state.nav_index = part_number
    render_progress_strip(language)

    if status == "PENDING":
        previous = part_number - 1
        st.markdown(
            card_html(
                part_label(part_number, language),
                f"This part is pending. Complete Part {previous} first.",
                status="PENDING",
                key_result=MISSION_OUTCOMES[part_number],
            ),
            unsafe_allow_html=True,
        )
        render_mission_log(language)
        return

    result = st.session_state.get("results", {}).get(f"part{part_number}")
    render_mission_intro(part_number, result, language, sheet_override, status=status)

    unlocked = status == "COMPLETED"
    if not unlocked:
        unlocked = render_algorithm_choice(part_number, language, sheet_override)
        result = st.session_state.get("results", {}).get(f"part{part_number}")

    if not unlocked:
        render_mission_log(language)
        return

    result = st.session_state.get("results", {}).get(f"part{part_number}")
    if not result:
        with st.spinner(t("running_selected", language)):
            result = run_part_and_store(part_number, sheet_override, language)

    recent_feedback = st.session_state.get("last_choice_feedback", {}).get(part_number)
    if (
        recent_feedback
        and recent_feedback.get("correct")
        and st.session_state.pop("celebrate_part", None) == part_number
    ):
        render_coin_reward_for_part(part_number, language, recent_feedback)

    render_algorithm_analysis_sections(part_number, result, language, sheet_override, show_run_button=False)

    if part_number < TOTAL_PARTS:
        next_part_button(part_number, language)
    else:
        render_final_completion(language)

    render_mission_log(language)


def render_direct_demo(language, sheet_override):
    st.markdown(
        f"""
        <div class="mission-hero">
            <div class="mission-subtitle">{t('direct_demo_mode', language)}</div>
            <h1>{t('title', language)}</h1>
            <p>{t('optional_note', language)}</p>
            {badge(t('implemented', language), 'complete')}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t("run_all_show_results", language), type="primary", key="direct_run_all"):
        with st.spinner(t("running_all", language)):
            st.session_state.results = run_all_official_parts_cached()
        st.session_state.direct_results_visible = True
        mission_log_add(f"Direct Demo Mode: all {TOTAL_PARTS} official mission outputs executed.")
        st.success(t("all_finished", language))

    results = st.session_state.get("results", {})
    render_defense_matrix(results, language)
    if not st.session_state.get("direct_results_visible") and not all(f"part{i}" in results for i in range(1, TOTAL_PARTS + 1)):
        cards = build_mission_cards(results, language)
        rows = [st.columns(3) for _ in range(math.ceil(len(cards) / 3))]
        for index, mission_card in enumerate(cards):
            with rows[index // 3][index % 3]:
                st.markdown(
                    card_html(
                        f"{t('part_word', language)} {mission_card['part_number']}: {mission_card['mission_name']}",
                        mission_card["chosen_algorithm"],
                        status=mission_card["status"],
                        key_result=mission_card["key_result"],
                    ),
                    unsafe_allow_html=True,
                )
        render_mission_log(language)
        return

    st.caption(t("fast_mode_note", language))
    if st.checkbox(t("render_all_details", language), value=False):
        for part_number in range(1, TOTAL_PARTS + 1):
            result = results.get(f"part{part_number}")
            with st.expander(part_label(part_number, language), expanded=part_number == 1):
                render_result_sections(part_number, result, language, sheet_override, show_run_button=not result)
    else:
        selected_part = st.selectbox(
            t("select_result_detail", language),
            list(range(1, TOTAL_PARTS + 1)),
            format_func=lambda part_number: part_label(part_number, language),
            key="direct_detail_part",
        )
        result = results.get(f"part{selected_part}")
        render_result_sections(selected_part, result, language, sheet_override, show_run_button=not result)

    render_mission_log(language)


def sidebar(language):
    view_options = [t("overview", language)] + [part_label(i, language) for i in range(1, TOTAL_PARTS + 1)]
    default_index = min(st.session_state.get("nav_index", 0), len(view_options) - 1)
    selected_label = st.sidebar.selectbox(t("select_part", language), view_options, index=default_index)
    st.session_state.nav_index = view_options.index(selected_label)
    sheet = st.sidebar.selectbox(t("sheet", language), [t("default", language), "A", "B", "C"])
    sheet_override = None if sheet == t("default", language) else sheet

    st.sidebar.markdown("---")
    st.sidebar.caption(t("direct_demo_mode", language) if st.session_state.get("mode") == "direct" else t("mission_challenge_mode", language))
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button(t("mission_challenge_mode", language), width="stretch", key="sidebar_challenge"):
            st.session_state.mode = "challenge"
            st.rerun()
    with col2:
        if st.button(t("direct_demo_mode", language), width="stretch", key="sidebar_direct"):
            st.session_state.mode = "direct"
            st.rerun()
    if st.sidebar.button(t("reset_progress", language), width="stretch", key="sidebar_reset"):
        reset_challenge_progress()
        st.rerun()
    return selected_label, sheet_override


def main():
    st.set_page_config(page_title="Cypher Nexus Mission Control", layout="wide")
    inject_css()
    sync_session_challenge_state()

    language = st.sidebar.selectbox(t("language", "English"), LANGUAGE_OPTIONS)
    selected_label, sheet_override = sidebar(language)

    if selected_label == t("overview", language):
        if st.session_state.get("mode") == "direct":
            render_direct_demo(language, sheet_override)
            return
        render_landing(language)
        return

    part_number = st.session_state.nav_index
    if st.session_state.get("mode") == "challenge":
        render_challenge_part_page(part_number, language, sheet_override)
    else:
        render_part_page(part_number, language, sheet_override)


if __name__ == "__main__":
    main()

