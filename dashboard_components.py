"""Reusable Streamlit UI components for the Cypher Nexus dashboard."""

import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                linear-gradient(90deg, rgba(126, 231, 219, .045) 1px, transparent 1px),
                linear-gradient(180deg, rgba(126, 231, 219, .035) 1px, transparent 1px),
                radial-gradient(circle at top left, rgba(32, 178, 170, .16), transparent 30%),
                linear-gradient(180deg, #07111f 0%, #0b1726 48%, #101820 100%);
            background-size: 48px 48px, 48px 48px, auto, auto;
            color: #e9f4f2;
        }
        .block-container {
            padding-top: 2rem;
            max-width: 1280px;
        }
        [data-testid="stSidebar"] {
            background: #0b131f;
            border-right: 1px solid rgba(126, 231, 219, .18);
        }
        .mission-hero {
            border: 1px solid rgba(126, 231, 219, .28);
            background:
                linear-gradient(135deg, rgba(8, 20, 34, .98), rgba(16, 39, 56, .90)),
                linear-gradient(90deg, rgba(126, 231, 219, .16), transparent 38%),
                linear-gradient(180deg, rgba(255, 207, 92, .08), transparent 55%);
            padding: 28px;
            border-radius: 8px;
            margin-bottom: 18px;
            box-shadow: 0 18px 45px rgba(0, 0, 0, .30);
            position: relative;
            overflow: hidden;
        }
        .mission-hero:before {
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 3px;
            background: linear-gradient(90deg, #7ee7db, #64f58d, #ffcf5c);
            opacity: .95;
        }
        .mission-hero h1 {
            font-size: 2.4rem;
            margin: 0 0 6px;
            letter-spacing: 0;
            position: relative;
        }
        .mission-subtitle {
            color: #7ee7db;
            font-size: 1.05rem;
            font-weight: 700;
            text-transform: uppercase;
            position: relative;
        }
        .mission-card, .result-card, .section-card {
            border: 1px solid rgba(126, 231, 219, .22);
            background: rgba(12, 24, 36, .86);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, .18);
            animation: panelFadeIn .22s ease-out both;
        }
        .mission-card:hover {
            border-color: rgba(126, 231, 219, .45);
            transform: translateY(-1px);
        }
        .result-card {
            border-color: rgba(255, 207, 92, .45);
            background: linear-gradient(135deg, rgba(42, 34, 18, .72), rgba(22, 38, 44, .78));
        }
        .why-card {
            border-color: rgba(126, 231, 219, .42);
            background: linear-gradient(135deg, rgba(12, 43, 55, .78), rgba(12, 24, 36, .88));
        }
        .feedback-card {
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
            box-shadow: 0 12px 30px rgba(0, 0, 0, .20);
            animation: panelFadeIn .22s ease-out both;
        }
        .feedback-success {
            border-color: rgba(100, 245, 141, .42);
            background: linear-gradient(135deg, rgba(13, 58, 40, .78), rgba(11, 30, 38, .90));
        }
        .feedback-danger {
            border-color: rgba(255, 98, 98, .48);
            background: linear-gradient(135deg, rgba(74, 22, 30, .78), rgba(22, 25, 34, .92));
        }
        .feedback-warn {
            border-color: rgba(255, 207, 92, .45);
            background: linear-gradient(135deg, rgba(61, 43, 16, .74), rgba(22, 25, 34, .90));
        }
        .card-title {
            color: #ffffff;
            font-weight: 800;
            font-size: 1.02rem;
            margin-bottom: 6px;
        }
        .card-small {
            color: #b8c7c9;
            font-size: .9rem;
        }
        .badge {
            display: inline-block;
            padding: 4px 9px;
            border-radius: 999px;
            margin: 2px 4px 2px 0;
            font-size: .78rem;
            font-weight: 800;
            border: 1px solid rgba(255,255,255,.16);
        }
        .badge-ready { background: rgba(255, 207, 92, .18); color: #ffdf85; }
        .badge-complete { background: rgba(100, 245, 141, .18); color: #a4ffbe; }
        .badge-muted { background: rgba(160, 170, 180, .13); color: #d5dcdf; }
        .badge-locked { background: rgba(115, 126, 138, .14); color: #98a4ad; }
        .badge-warn { background: rgba(255, 153, 102, .14); color: #ffc3a3; }
        .badge-danger { background: rgba(255, 98, 98, .20); color: #ffaaa5; }
        .section-kicker {
            color: #7ee7db;
            font-size: .76rem;
            font-weight: 900;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-top: 18px;
        }
        .section-title {
            color: #ffffff;
            font-size: 1.24rem;
            font-weight: 900;
            margin: 0 0 10px;
        }
        .chosen-box {
            border-left: 4px solid #7ee7db;
            background: rgba(126, 231, 219, .1);
            padding: 12px 14px;
            border-radius: 6px;
        }
        .reject-box {
            border-left: 4px solid #ff6868;
            background: rgba(255, 98, 98, .09);
            padding: 12px 14px;
            border-radius: 6px;
        }
        .choice-card {
            border: 1px solid rgba(126, 231, 219, .20);
            background: rgba(9, 19, 29, .70);
            border-radius: 8px;
            padding: 14px;
            min-height: 108px;
            margin-bottom: 10px;
        }
        .choice-card strong {
            color: #ffffff;
            display: block;
            margin-bottom: 8px;
        }
        .choice-card:hover {
            border-color: rgba(126, 231, 219, .52);
            background: rgba(15, 32, 47, .88);
        }
        .mission-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin: 12px 0 18px;
        }
        .strip-cell {
            border: 1px solid rgba(255,255,255,.12);
            background: rgba(255,255,255,.04);
            padding: 12px;
            border-radius: 8px;
        }
        .strip-number {
            font-size: 1.35rem;
            font-weight: 900;
            color: #ffffff;
        }
        .reward-row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 10px 0 4px;
        }
        .reward-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(255, 207, 92, .36);
            background: rgba(255, 207, 92, .10);
            border-radius: 999px;
            padding: 6px 11px;
            color: #ffe09a;
            font-weight: 800;
            font-size: .86rem;
        }
        .reward-dot {
            width: 14px;
            height: 14px;
            border-radius: 999px;
            background: radial-gradient(circle at 35% 35%, #fff6bf, #ffcf5c 58%, #8a5c12 100%);
            box-shadow: 0 0 14px rgba(255, 207, 92, .42);
        }
        .coin-reward-panel {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 207, 92, .46);
            background:
                radial-gradient(circle at 15% 25%, rgba(255, 207, 92, .20), transparent 28%),
                linear-gradient(135deg, rgba(43, 34, 12, .86), rgba(9, 32, 39, .92));
            border-radius: 8px;
            padding: 18px 18px 16px;
            margin: 12px 0;
            box-shadow: 0 16px 38px rgba(0, 0, 0, .28), 0 0 28px rgba(255, 207, 92, .10);
            animation: rewardPop .34s cubic-bezier(.2, .9, .25, 1.15) both;
        }
        .coin-reward-panel:after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(105deg, transparent 20%, rgba(255,255,255,.12) 45%, transparent 68%);
            transform: translateX(-100%);
            animation: panelSweep 1.25s ease-out both;
            pointer-events: none;
        }
        .coin-reward-topline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            position: relative;
            z-index: 1;
        }
        .coin-stack {
            position: relative;
            width: 68px;
            height: 68px;
            flex: 0 0 68px;
        }
        .coin-main, .coin-orbit {
            position: absolute;
            border-radius: 999px;
            background: radial-gradient(circle at 34% 28%, #fff7c7 0%, #ffcf5c 45%, #b97919 100%);
            border: 1px solid rgba(255, 246, 191, .75);
            box-shadow: 0 0 18px rgba(255, 207, 92, .38);
        }
        .coin-main {
            inset: 12px;
            display: grid;
            place-items: center;
            color: #2e1d04;
            font-weight: 1000;
            animation: coinPulse .8s ease-out both;
        }
        .coin-orbit {
            width: 18px;
            height: 18px;
            opacity: .95;
            animation: coinOrbit .95s ease-out both;
        }
        .coin-orbit:nth-child(2) { left: 4px; top: 8px; animation-delay: .02s; }
        .coin-orbit:nth-child(3) { right: 2px; top: 4px; animation-delay: .08s; }
        .coin-orbit:nth-child(4) { right: 7px; bottom: 6px; animation-delay: .14s; }
        .coin-reward-title {
            color: #fff7d1;
            font-size: 1.16rem;
            font-weight: 950;
            margin-bottom: 4px;
        }
        .coin-reward-message {
            color: #d9e7e7;
            font-size: .92rem;
        }
        .coin-meter {
            color: #ffdf85;
            font-size: .9rem;
            font-weight: 900;
            margin-top: 8px;
            position: relative;
            z-index: 1;
        }
        .badge-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .badge-token {
            border: 1px solid rgba(255, 207, 92, .34);
            background: rgba(255, 207, 92, .10);
            color: #ffe09a;
            border-radius: 999px;
            padding: 6px 10px;
            font-weight: 800;
            font-size: .84rem;
        }
        .table-note {
            color: #b8c7c9;
            font-size: .86rem;
            margin: 0 0 8px;
        }
        .log-line {
            border-left: 3px solid #7ee7db;
            padding-left: 10px;
            margin: 6px 0;
            color: #dbe9ea;
        }
        @keyframes panelFadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes rewardPop {
            from { opacity: 0; transform: translateY(8px) scale(.985); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes panelSweep {
            0% { transform: translateX(-110%); }
            70%, 100% { transform: translateX(110%); }
        }
        @keyframes coinPulse {
            0% { transform: scale(.7) rotate(-12deg); }
            70% { transform: scale(1.08) rotate(4deg); }
            100% { transform: scale(1) rotate(0); }
        }
        @keyframes coinOrbit {
            from { opacity: 0; transform: translateY(8px) scale(.5); }
            to { opacity: .95; transform: translateY(0) scale(1); }
        }
        @media (max-width: 760px) {
            .mission-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .mission-hero h1 { font-size: 1.85rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def badge(text, kind="muted"):
    return f'<span class="badge badge-{kind}">{text}</span>'


def status_badge_kind(status):
    if status == "COMPLETED":
        return "complete"
    if status == "LOCKED":
        return "locked"
    return "ready"


def card_html(title, body, status=None, key_result=None):
    status_html = badge(status, status_badge_kind(status)) if status else ""
    result_html = f'<div class="card-small"><b>Key:</b> {key_result}</div>' if key_result else ""
    return f"""
    <div class="mission-card">
        {status_html}
        <div class="card-title">{title}</div>
        <div class="card-small">{body}</div>
        {result_html}
    </div>
    """


def feedback_card_html(title, body, kind="success", chips=None):
    chip_html = ""
    if chips:
        chip_html = '<div class="reward-row">' + "".join(reward_chip(chip) for chip in chips) + "</div>"
    badge_kind = "complete" if kind == "success" else "danger" if kind == "danger" else "ready"
    return f"""
    <div class="feedback-card feedback-{kind}">
        {badge(title, badge_kind)}
        <div class="card-title">{title}</div>
        <div class="card-small">{body}</div>
        {chip_html}
    </div>
    """


def coin_reward_panel_html(
    title,
    message,
    coins,
    badge_label,
    result_label,
    wallet_label="Wallet",
    badge_prefix="Badge",
):
    return f"""
    <div class="coin-reward-panel">
        <div class="coin-reward-topline">
            <div>
                {badge("+1", "ready")}
                <div class="coin-reward-title">{title}</div>
                <div class="coin-reward-message">{message}</div>
                <div class="coin-meter">{result_label} | {wallet_label}: {coins} | {badge_prefix}: {badge_label}</div>
            </div>
            <div class="coin-stack" aria-hidden="true">
                <span class="coin-main">+1</span>
                <span class="coin-orbit"></span>
                <span class="coin-orbit"></span>
                <span class="coin-orbit"></span>
            </div>
        </div>
    </div>
    """


def badge_list_html(badges, empty_text):
    tokens = badges or [empty_text]
    return '<div class="badge-list">' + "".join(f'<span class="badge-token">{label}</span>' for label in tokens) + "</div>"


def section_header(label, index=None):
    prefix = f"SECTION {index:02d}" if index is not None else "MISSION CONTROL"
    st.markdown(
        f"""
        <div class="section-kicker">{prefix}</div>
        <div class="section-title">{label}</div>
        """,
        unsafe_allow_html=True,
    )


def render_table_note(text):
    st.markdown(f'<div class="table-note">{text}</div>', unsafe_allow_html=True)


def reward_chip(label):
    return f'<span class="reward-chip"><span class="reward-dot"></span>{label}</span>'


def render_dataset_card(meta, labels):
    st.markdown(
        f"""
        <div class="section-card">
            {badge(labels['dataset_loaded'], 'complete')}
            <div class="card-small"><b>{labels['dataset_file']}:</b> {meta.get('member', '-')}</div>
            <div class="card-small"><b>{labels['sheet_used']}:</b> {meta.get('sheet', '-')}</div>
            <div class="card-small"><b>{labels['rows_used']}:</b> {meta.get('row_count', '-')}</div>
            <div class="card-small"><b>{labels['columns_used']}:</b> {', '.join(meta.get('columns_used', [])) or '-'}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_mission_log(session_state, message, limit=8):
    session_state.setdefault("mission_log", [])
    session_state.mission_log.insert(0, message)
    session_state.mission_log = session_state.mission_log[:limit]


def render_mission_log(logs, title, empty_text="No mission actions yet."):
    section_header(title)
    if not logs:
        st.caption(empty_text)
        return
    for line in logs:
        st.markdown(f'<div class="log-line">{line}</div>', unsafe_allow_html=True)
