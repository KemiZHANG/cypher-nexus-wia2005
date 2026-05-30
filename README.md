# Operation Cypher Nexus: The Final Protocol

## 中文说明

这是 WIA2005 小组项目的 Python 实现与本地 Streamlit 可视化看板。核心算法、正式输出和 CLI 命令都以 `cypher_nexus_project.py` 为准；`streamlit_app.py` 只是本地浏览器展示层，用来更清楚地展示数据集、算法选择、被拒算法、结果、复杂度和答辩要点。

本项目保留 PPT 中选定的算法，不改变官方算法逻辑或输出。

## 主要文件

- `cypher_nexus_project.py`：核心程序，包含 8 个 Part 的算法、数据读取、CLI 和输出保存。
- `streamlit_app.py`：本地 Streamlit dashboard，复用核心程序函数，不复制算法逻辑。
- `dashboard_content.py`：任务说明、候选算法、拒绝理由、关键结论、防守矩阵等展示内容。
- `dashboard_components.py`：Streamlit UI 组件，例如卡片、徽章、金币奖励、数据集面板、任务日志。
- `dashboard_i18n.py`：英文 / 中文 / Bahasa Melayu 三语界面文本。
- `run_dashboard_chrome.ps1`：Windows Chrome 启动脚本，避免默认联想浏览器乱码。
- `colab_runner.py`：Google Colab 运行入口。
- `test_cypher_nexus_project.py`：单元测试。
- `outputs/`：运行后生成的 TXT、CSV、summary 和 data mapping 文件。

## 算法总览

| Part | 任务 | 选定算法 |
|---|---|---|
| 1 | The Shadow Network | Modified Risk-Aware Dijkstra |
| 2 | The Double Agent Registry | Hash Table + Levenshtein Distance |
| 3 | The Resource Lockdown | Dynamic Programming Knapsack |
| 4 | The Probability Trap | MCDA Weighted Scoring |
| 5 | The Split Signal Protocol | Dynamic Programming Signal Reconstruction |
| 6 | The Countdown Sequence | Modified Stable Merge Sort |
| 7 | The Phantom Dice | Controlled Randomisation |
| 8 | The Silent Code | Brute Force String Matching + Threat Ranking |

## 数据集

程序会自动查找 `Datasets (2).zip`，优先位置包括：

- 当前项目文件夹
- 上级文件夹
- `D:/Datasets (2).zip`
- `/content/Datasets (2).zip`，用于 Colab

默认 sheet：

| Part | 默认 Sheet |
|---|---|
| 1 | C |
| 2-8 | A |

每个 Part 都会输出：

- 数据文件
- sheet 名称
- 行数
- 使用列

生成的 `outputs/data_mapping_report.txt` 会列出原始数据列如何映射到算法字段。

## 安装

```bash
pip install -r requirements.txt
```

## CLI 运行方式

运行全部 Part：

```bash
python cypher_nexus_project.py
python cypher_nexus_project.py --all
```

运行单个 Part：

```bash
python cypher_nexus_project.py --part 6
```

查看数据集文件、sheet、行数和列：

```bash
python cypher_nexus_project.py --list-data
```

指定 sheet：

```bash
python cypher_nexus_project.py --part 6 --sheet B
```

## 输出文件

每个 Part 都会生成标准 TXT 报告，包含：

- Mission Problem
- Algorithm Used
- Rejected Algorithms
- Dataset
- Key Result
- Result Explanation
- Time and Space Complexity
- Detailed Output

重要表格会尽量另存为 CSV。

## Streamlit 本地看板

启动看板：

```bash
streamlit run streamlit_app.py
```

如果默认联想浏览器显示乱码，使用 Chrome 启动脚本：

```powershell
powershell -ExecutionPolicy Bypass -File .\run_dashboard_chrome.ps1
```

看板功能：

- 英文 / 中文 / Bahasa Melayu 三语切换
- 8 个 Part 的任务卡
- Mission Challenge Mode：选择正确算法后解锁结果
- Direct Demo Mode：快速显示官方输出
- 数据集面板：文件、sheet、行数、使用列
- Algorithm Decision：候选算法、被拒算法、选定算法
- Key Takeaway / Why it matters
- 结果卡片、图表、复杂度徽章、答辩要点
- 答对后金币奖励和徽章反馈
- Mission Log 和 Next Mission 导航
- Direct Demo 默认只渲染一个详细 Part，使页面切换更快
- 数据预览和 dashboard 结果调用使用 Streamlit 缓存，重复点击更快

注意：dashboard 是本地展示层。核心算法和正式 TXT/CSV 输出仍然来自 `cypher_nexus_project.py`。

## Part 6 说明

Part 6 使用 Modified Stable Merge Sort，排序键为：

```text
(-Threat_Priority, Timestamp, Launch_Rank, Original_Index)
```

含义：

- 威胁优先级高的事件先处理
- 优先级相同时，时间更早的事件先处理
- 再按 launch-related 事件优先
- 如果所有字段都相同，保留原始到达顺序

代码中手动实现了 merge sort，Part 6 的主算法不是 Python `sorted()`。

## Google Colab

上传：

- `cypher_nexus_project.py`
- `colab_runner.py`
- `requirements.txt`
- `Datasets (2).zip`

然后运行：

```python
!pip install -r requirements.txt
!python colab_runner.py
```

## 测试

```bash
python -m unittest test_cypher_nexus_project.py
```

---

## English README

This is the Python implementation and local Streamlit dashboard for the WIA2005 group project. `cypher_nexus_project.py` remains the source of truth for official algorithms, CLI commands, dataset loading, and saved outputs. `streamlit_app.py` is only a local browser visualization layer that reuses the core project functions.

The selected algorithms still follow the group PPT. The dashboard improves presentation clarity without changing official algorithm logic or output.

## Main Files

- `cypher_nexus_project.py`: core program for all 8 Parts, dataset loading, CLI, and saved outputs.
- `streamlit_app.py`: local Streamlit dashboard that imports and reuses `cypher_nexus_project.py`.
- `dashboard_content.py`: mission metadata, candidate algorithms, rejection reasons, key takeaways, and Defense Matrix content.
- `dashboard_components.py`: reusable Streamlit UI components such as cards, badges, coin rewards, dataset panels, and mission logs.
- `dashboard_i18n.py`: English / 中文 / Bahasa Melayu UI text.
- `run_dashboard_chrome.ps1`: Windows helper that opens the dashboard in Google Chrome.
- `colab_runner.py`: simple Google Colab runner.
- `test_cypher_nexus_project.py`: lightweight verification tests.
- `outputs/`: generated TXT, CSV, summary, and data mapping files.

## Algorithms

| Part | Mission Section | Selected Algorithm |
|---|---|---|
| 1 | The Shadow Network | Modified Risk-Aware Dijkstra |
| 2 | The Double Agent Registry | Hash Table + Levenshtein Distance |
| 3 | The Resource Lockdown | Dynamic Programming Knapsack |
| 4 | The Probability Trap | MCDA Weighted Scoring |
| 5 | The Split Signal Protocol | Dynamic Programming Signal Reconstruction |
| 6 | The Countdown Sequence | Modified Stable Merge Sort |
| 7 | The Phantom Dice | Controlled Randomisation |
| 8 | The Silent Code | Brute Force String Matching + Threat Ranking |

## Dataset

The program automatically looks for `Datasets (2).zip` in:

- the project folder
- the parent folder
- `D:/Datasets (2).zip`
- `/content/Datasets (2).zip` for Colab

Default sheets:

| Part | Sheet |
|---|---|
| 1 | C |
| 2-8 | A |

Every Part prints the dataset file, sheet name, row count, and columns used. The generated `outputs/data_mapping_report.txt` shows how original dataset columns map to algorithm fields.

## Install

```bash
pip install -r requirements.txt
```

## CLI Usage

Run all Parts:

```bash
python cypher_nexus_project.py
python cypher_nexus_project.py --all
```

Run one Part:

```bash
python cypher_nexus_project.py --part 6
```

List dataset files, sheets, row counts, and columns:

```bash
python cypher_nexus_project.py --list-data
```

Optional sheet override:

```bash
python cypher_nexus_project.py --part 6 --sheet B
```

## Outputs

Each Part saves a standardized TXT report with:

- Mission Problem
- Algorithm Used
- Rejected Algorithms
- Dataset
- Key Result
- Result Explanation
- Time and Space Complexity
- Detailed Output

Important tables are also saved as CSV files when possible.

## Streamlit Dashboard

Run:

```bash
streamlit run streamlit_app.py
```

On Windows, use the Chrome helper if the default Lenovo browser displays garbled text:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_dashboard_chrome.ps1
```

Dashboard features:

- English / 中文 / Bahasa Melayu language selector
- 8 mission cards
- Mission Challenge Mode: choose the correct algorithm before the result unlocks
- Direct Demo Mode: quickly show official outputs
- dataset file, sheet, row count, and columns used
- candidate algorithms, rejected algorithms, and chosen algorithm
- Key Takeaway / Why it matters
- result cards, charts, complexity badges, and defense notes
- coin and badge feedback after correct answers
- Mission Log and Next Mission navigation
- faster page switching through Streamlit caching and one-Part-at-a-time detailed rendering

The dashboard is a local visualization layer only. Official algorithms and saved TXT/CSV outputs still come from `cypher_nexus_project.py`.

## Part 6 Note

Part 6 uses Modified Stable Merge Sort with this sorting key:

```text
(-Threat_Priority, Timestamp, Launch_Rank, Original_Index)
```

It means higher priority first, earlier timestamp first, launch-related first, and original order preserved when all fields tie. Merge sort is manually implemented; Python `sorted()` is not the main Part 6 algorithm.

## Google Colab

Upload:

- `cypher_nexus_project.py`
- `colab_runner.py`
- `requirements.txt`
- `Datasets (2).zip`

Then run:

```python
!pip install -r requirements.txt
!python colab_runner.py
```

## Tests

```bash
python -m unittest test_cypher_nexus_project.py
```
