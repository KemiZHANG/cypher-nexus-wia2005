import inspect
import unittest

from cypher_nexus_project import (
    PART_INFO,
    RUNNERS_BY_PART,
    TOTAL_PARTS,
    build_maximum_disruption_strategy,
    build_standard_report,
    brute_force_phrase_match,
    format_data_mapping_report,
    levenshtein_distance,
    modified_risk_aware_dijkstra,
    parse_args,
    require_columns,
    stable_merge_sort_events,
)
from dashboard_components import badge, card_html, coin_reward_panel_html, flowchart_html, trace_step_card_html
from dashboard_content import (
    ALGORITHM_DECISIONS,
    DEFENSE_MATRIX_COLUMNS,
    DEFENSE_NOTES,
    KEY_TAKEAWAYS,
    build_defense_matrix_rows,
)
from streamlit_app import (
    ALGORITHM_CHOICES,
    ALGORITHM_FLOWS,
    CANDIDATE_ALGORITHMS,
    HELPFUL_CHART_PARTS,
    LANGUAGE_OPTIONS,
    MISSION_OUTCOMES,
    RESULT_PAGE_SECTIONS,
    apply_algorithm_choice,
    build_challenge_state,
    build_mission_cards,
    dataset_metadata_for_part,
    get_part_dataframe_cached,
    localized_part_info,
    mission_status,
    mission_story,
    part_label,
    render_landing,
    render_direct_demo,
    run_all_official_parts_cached,
    run_official_part_cached,
    run_part_and_store,
    t,
)


class CypherNexusAlgorithmTests(unittest.TestCase):
    def test_modified_dijkstra_prefers_lower_risk_modified_cost(self):
        edges = [
            {
                "From_Node": "A",
                "To_Node": "B",
                "Distance": 3,
                "Risk_Level": 5,
                "Detection_Probability": 0.0,
                "Route_Status": "Open",
            },
            {
                "From_Node": "B",
                "To_Node": "D",
                "Distance": 2,
                "Risk_Level": 5,
                "Detection_Probability": 0.0,
                "Route_Status": "Open",
            },
            {
                "From_Node": "A",
                "To_Node": "C",
                "Distance": 5,
                "Risk_Level": 1,
                "Detection_Probability": 0.0,
                "Route_Status": "Open",
            },
            {
                "From_Node": "C",
                "To_Node": "D",
                "Distance": 1,
                "Risk_Level": 1,
                "Detection_Probability": 0.0,
                "Route_Status": "Open",
            },
        ]

        result = modified_risk_aware_dijkstra(edges, "A", "D")

        self.assertEqual(result["route"], ["A", "C", "D"])
        self.assertEqual(result["total_distance"], 6)
        self.assertEqual(result["total_risk"], 2)
        self.assertEqual(result["total_modified_cost"], 10)

    def test_levenshtein_distance_counts_insertions_and_substitutions(self):
        self.assertEqual(levenshtein_distance("Falcon", "Falcon_1"), 2)
        self.assertEqual(levenshtein_distance("Raven", "Ravin"), 1)

    def test_stable_merge_sort_uses_priority_time_launch_and_original_order(self):
        events = [
            {"Event_ID": "E1", "Threat_Priority": 3, "Timestamp": "04:01:00", "Event_Type": "Door Access"},
            {"Event_ID": "E2", "Threat_Priority": 5, "Timestamp": "04:03:00", "Event_Type": "Door Access"},
            {"Event_ID": "E3", "Threat_Priority": 5, "Timestamp": "04:02:00", "Event_Type": "Launch Trigger"},
            {"Event_ID": "E4", "Threat_Priority": 5, "Timestamp": "04:02:00", "Event_Type": "Door Access"},
            {"Event_ID": "E5", "Threat_Priority": 5, "Timestamp": "04:02:00", "Event_Type": "Door Access"},
        ]

        sorted_events = stable_merge_sort_events(events)

        self.assertEqual([event["Event_ID"] for event in sorted_events], ["E3", "E4", "E5", "E2", "E1"])

    def test_brute_force_phrase_match_detects_multi_word_phrase(self):
        self.assertTrue(brute_force_phrase_match("final protocol", "activate the final protocol now"))
        self.assertFalse(brute_force_phrase_match("shadow key", "shadow gateway only"))

    def test_part9_synthesizes_previous_outputs_into_final_strategy(self):
        result = build_maximum_disruption_strategy(
            part1_result={"route": ["Port Authority Hub", "Warehouse A", "Core Chamber"]},
            part2_result={
                "suspicious_identities": [
                    {"Agent_ID": "A2876", "Access_Key": "T7Q1", "Suspicion_Score": 12}
                ]
            },
            part3_result={
                "selected_checkpoints": [
                    {"Checkpoint": "Disable Camera Grid", "Energy": 3, "Time": 8, "Token": 1, "Impact": 11},
                    {"Checkpoint": "Jam Patrol Drone Relay", "Energy": 5, "Time": 11, "Token": 1, "Impact": 14},
                ],
                "total_energy": 8,
                "total_time": 19,
                "total_tokens": 2,
                "total_impact": 25,
                "capacities": (15, 35, 4),
            },
            part8_result={
                "ranked_messages": [
                    {"Message_ID": "M04", "Threat_Score": 7, "Threat_Level": "Critical", "Route_Tag": "CORE-LINK-7"},
                    {"Message_ID": "M08", "Threat_Score": 4, "Threat_Level": "High", "Route_Tag": "GRID-HUB-B2"},
                ]
            },
        )

        self.assertEqual(result["final_result"], "Maximum Disruption Achieved")
        self.assertEqual(result["total_operational_impact"], 25)
        self.assertEqual(result["resource_usage"]["Energy"], "8 / 15")
        self.assertEqual([target["Target"] for target in result["selected_targets"]], ["Disable Camera Grid", "Jam Patrol Drone Relay"])
        self.assertEqual(result["top_threats"][0]["Message_ID"], "M04")
        self.assertIn("Part 1", result["strategy_steps"][0]["Source"])

    def test_standard_report_contains_required_presentation_sections(self):
        report = build_standard_report(
            6,
            metadata={"member": "Part 6.xlsx", "sheet": "A", "row_count": 10, "columns_used": ["Event_ID"]},
            key_result="Top urgent event: E091",
            result_explanation="Events are sorted by threat priority and timestamp.",
        )

        for heading in [
            "Mission Problem",
            "Algorithm Used",
            "Rejected Algorithms",
            "Dataset",
            "Key Result",
            "Result Explanation",
            "Time and Space Complexity",
        ]:
            self.assertIn(heading, report)
        self.assertIn("Part 6.xlsx", report)
        self.assertIn("row count: 10", report)

    def test_require_columns_raises_helpful_error(self):
        with self.assertRaisesRegex(ValueError, "Part 6.*Missing required columns.*Available columns"):
            require_columns(6, ["Event_ID", "Threat_Priority"], ["Event_ID", "Timestamp"])

    def test_data_mapping_report_lists_original_to_algorithm_fields(self):
        report = format_data_mapping_report(
            {
                6: {
                    "member": "Part 6.xlsx",
                    "sheet": "A",
                    "row_count": 10,
                    "column_mapping": {"Threat Priority": "Threat_Priority"},
                    "columns_used": ["Threat_Priority"],
                }
            }
        )

        self.assertIn("Part 6", report)
        self.assertIn("Threat Priority -> Threat_Priority", report)

    def test_streamlit_language_copy_supports_three_languages(self):
        self.assertEqual(set(LANGUAGE_OPTIONS), {"English", "中文", "Bahasa Melayu"})
        self.assertEqual(t("run_selected", "中文"), "运行选中部分")
        self.assertEqual(t("run_all", "Bahasa Melayu"), "Jalankan semua bahagian")
        self.assertIn("倒计时事件排序", part_label(6, "中文"))
        self.assertIn("Susunan Acara Kiraan Detik", part_label(6, "Bahasa Melayu"))

        part_info = localized_part_info(6, "中文")
        self.assertIn("多字段", part_info["mission_problem"])
        self.assertIn("Modified Stable Merge Sort", part_info["algorithm"])
        self.assertIn("倒计时事件流", mission_story(6, "中文"))
        self.assertIn("Aliran kiraan detik", mission_story(6, "Bahasa Melayu"))

    def test_streamlit_mission_control_metadata_is_complete(self):
        self.assertEqual(TOTAL_PARTS, 9)
        self.assertEqual(len(MISSION_OUTCOMES), 9)
        self.assertEqual(len(CANDIDATE_ALGORITHMS), 9)
        self.assertIn("Modified Stable Merge Sort", CANDIDATE_ALGORITHMS[6])
        self.assertIn("Integrated DP Final Strategy", CANDIDATE_ALGORITHMS[9])
        self.assertEqual(
            RESULT_PAGE_SECTIONS,
            [
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
            ],
        )
        self.assertEqual(HELPFUL_CHART_PARTS, {2, 3, 4, 6, 7, 8, 9})
        self.assertEqual(len(ALGORITHM_FLOWS), 9)
        self.assertTrue(all(len(flow["steps"]) == 5 for flow in ALGORITHM_FLOWS.values()))
        self.assertEqual(len(KEY_TAKEAWAYS), 9)
        cards = build_mission_cards({}, "English", completed_missions=set())
        self.assertEqual(len(cards), 9)
        self.assertEqual(cards[0]["status"], "READY")
        self.assertEqual(cards[1]["status"], "PENDING")
        self.assertIn("chosen_algorithm", cards[0])
        self.assertEqual(len(ALGORITHM_DECISIONS), 9)

    def test_dashboard_content_balances_all_parts_and_demo_flow(self):
        for part_number in range(1, TOTAL_PARTS + 1):
            with self.subTest(part=part_number):
                self.assertEqual(len(CANDIDATE_ALGORITHMS[part_number]), 3)
                self.assertGreaterEqual(len(PART_INFO[part_number]["rejected"]), 2)
                self.assertGreaterEqual(len(DEFENSE_NOTES[part_number]), 2)

        landing_source = inspect.getsource(render_landing)
        self.assertNotIn("Presentation Guide", landing_source)
        self.assertNotIn("presentation_guide", landing_source)

    def test_dashboard_helper_modules_support_group_wide_defense_matrix(self):
        self.assertIn("badge-complete", badge("Mission Completed", "complete"))
        self.assertIn("mission-card", card_html("Part 1", "Route mission", status="READY"))

        self.assertEqual(
            DEFENSE_MATRIX_COLUMNS,
            [
                "Part",
                "Dataset",
                "Problem Type",
                "Candidate Algorithms",
                "Rejected Algorithms",
                "Chosen Algorithm",
                "Key Output",
                "Complexity",
                "Defense Notes",
            ],
        )
        rows = build_defense_matrix_rows()
        self.assertEqual(len(rows), 9)
        self.assertEqual({row["Part"] for row in rows}, {f"Part {part}" for part in range(1, TOTAL_PARTS + 1)})
        for row in rows:
            self.assertTrue(row["Dataset"])
            self.assertTrue(row["Candidate Algorithms"])
            self.assertTrue(row["Rejected Algorithms"])
            self.assertTrue(row["Chosen Algorithm"])
            self.assertTrue(row["Key Output"])
            self.assertTrue(row["Complexity"])
            self.assertTrue(row["Defense Notes"])

    def test_challenge_mode_algorithm_choices_match_ppt_decisions(self):
        expected_correct = {
            1: "Modified Risk-Aware Dijkstra",
            2: "Two-Stage Hybrid Verification",
            3: "Dynamic Programming Knapsack",
            4: "MCDA Weighted Scoring",
            5: "Dynamic Programming",
            6: "Modified Stable Merge Sort",
            7: "Controlled Randomisation",
            8: "Brute Force String Matching + Threat Ranking",
            9: "Integrated DP Final Strategy",
        }

        self.assertEqual(set(ALGORITHM_CHOICES), set(range(1, TOTAL_PARTS + 1)))
        for part_number, correct in expected_correct.items():
            self.assertEqual(ALGORITHM_CHOICES[part_number]["correct"], correct)
            self.assertEqual(len(ALGORITHM_CHOICES[part_number]["options"]), 3)
            self.assertIn(correct, ALGORITHM_CHOICES[part_number]["options"])

    def test_challenge_progress_locks_ready_and_completed_missions(self):
        state = build_challenge_state()

        self.assertEqual(state["coins"], 0)
        self.assertEqual(state["completed_missions"], set())
        self.assertEqual(state["current_mission"], 1)
        self.assertEqual(mission_status(1, state["completed_missions"]), "READY")
        self.assertEqual(mission_status(2, state["completed_missions"]), "PENDING")

        completed_state = build_challenge_state(completed_missions={1}, coins=1, current_mission=2)
        self.assertEqual(mission_status(1, completed_state["completed_missions"]), "COMPLETED")
        self.assertEqual(mission_status(2, completed_state["completed_missions"]), "READY")
        self.assertEqual(mission_status(3, completed_state["completed_missions"]), "PENDING")

    def test_challenge_choice_feedback_does_not_change_official_outputs(self):
        state = build_challenge_state()

        wrong = apply_algorithm_choice(1, "BFS", state)
        self.assertFalse(wrong["correct"])
        self.assertEqual(state["coins"], 0)
        self.assertEqual(state["completed_missions"], set())
        self.assertEqual(state["results"], {})
        self.assertIn("rejected", wrong["feedback"].lower())

        correct = apply_algorithm_choice(1, "Modified Risk-Aware Dijkstra", state)
        self.assertTrue(correct["correct"])
        self.assertEqual(state["coins"], 1)
        self.assertEqual(state["completed_missions"], {1})
        self.assertEqual(state["current_mission"], 2)

        repeat = apply_algorithm_choice(1, "Modified Risk-Aware Dijkstra", state)
        self.assertTrue(repeat["correct"])
        self.assertEqual(state["coins"], 1)
        self.assertEqual(state["completed_missions"], {1})

    def test_direct_demo_mode_uses_official_run_all_parts(self):
        self.assertIn("run_all_parts(output_dir=\"outputs\")", inspect.getsource(run_all_official_parts_cached))
        self.assertIn("run_all_official_parts_cached()", inspect.getsource(render_direct_demo))

    def test_streamlit_uses_cached_data_paths_for_faster_clicks(self):
        self.assertIn("@st.cache_data", inspect.getsource(get_part_dataframe_cached))
        self.assertIn("@st.cache_data", inspect.getsource(run_official_part_cached))
        self.assertIn("get_part_dataframe_cached", inspect.getsource(dataset_metadata_for_part))
        self.assertIn("run_official_part_cached", inspect.getsource(run_part_and_store))

    def test_coin_reward_panel_has_animation_hooks(self):
        html = coin_reward_panel_html(
            title="Part Completed",
            message="Route computed.",
            coins=3,
            badge_label="Part 1 Evidence Mark",
            result_label="Result available",
        )
        self.assertIn("coin-reward-panel", html)
        self.assertIn("coin-flight", html)
        self.assertIn("reward-vault", html)
        self.assertIn("+1", html)
        self.assertIn("Part 1 Evidence Mark", html)

    def test_flowchart_html_renders_as_markup_not_markdown_code(self):
        html = flowchart_html(ALGORITHM_FLOWS[6], title="Flow explanation")
        self.assertTrue(html.startswith('<div class="flow-card">'))
        self.assertIn('<div class="flow-node">', html)
        self.assertIn("Build sorting key", html)
        self.assertIn("Stable merge", html)
        self.assertNotIn("\n    <div", html)

    def test_trace_step_card_supports_dataset_to_output_explanation(self):
        html = trace_step_card_html("TRACE", "Dataset to output trace", "Real rows become intermediate calculations.")
        self.assertIn("TRACE", html)
        self.assertIn("Dataset to output trace", html)
        self.assertIn("Real rows become intermediate calculations.", html)

    def test_cli_contract_for_required_commands_is_still_available(self):
        self.assertEqual(set(RUNNERS_BY_PART), set(range(1, TOTAL_PARTS + 1)))

        all_args = parse_args(["--all"])
        self.assertTrue(all_args.all)

        part_args = parse_args(["--part", "6", "--sheet", "B"])
        self.assertEqual(part_args.part, 6)
        self.assertEqual(part_args.sheet, "B")

        part9_args = parse_args(["--part", "9"])
        self.assertEqual(part9_args.part, 9)

        list_args = parse_args(["--list-data"])
        self.assertTrue(list_args.list_data)


if __name__ == "__main__":
    unittest.main()
