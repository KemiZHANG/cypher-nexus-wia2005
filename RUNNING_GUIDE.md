# Cypher Nexus 运行说明

这份文档是给本地 `2005` 文件夹和小组成员使用的运行指南。核心程序是 `cypher_nexus_project.py`，网页端是 `streamlit_app.py`。

## 1. 本地 Windows 电脑运行

进入项目文件夹：

```powershell
cd C:\Users\张祎鸣\Desktop\WIA2005\2005
```

安装依赖：

```powershell
pip install -r requirements.txt
```

运行网页端：

```powershell
streamlit run streamlit_app.py
```

如果默认联想浏览器打开后乱码，使用 Chrome 脚本：

```powershell
powershell -ExecutionPolicy Bypass -File .\run_dashboard_chrome.ps1
```

## 2. 数据集怎么放

项目需要 `Datasets (2).zip` 才能完整运行算法和 dashboard。

程序会自动查找这些位置：

```text
当前项目文件夹
上一级文件夹
D:/Datasets (2).zip
/content/Datasets (2).zip
```

最简单的方法：把 `Datasets (2).zip` 放到项目文件夹里，也就是和 `streamlit_app.py` 同一层。

## 3. CLI 命令

运行全部 Part：

```powershell
python cypher_nexus_project.py --all
```

运行 Part 6：

```powershell
python cypher_nexus_project.py --part 6
```

查看数据集是否被识别：

```powershell
python cypher_nexus_project.py --list-data
```

运行测试：

```powershell
python -m unittest test_cypher_nexus_project.py
```

## 4. 给 Mac 同学从 GitHub 拉下来运行网页端

如果 Mac 已经有 Git 和 Python，请复制运行：

```bash
git clone https://github.com/KemiZHANG/cypher-nexus-wia2005.git
cd cypher-nexus-wia2005
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m streamlit run streamlit_app.py
```

然后浏览器会打开一个本地地址，通常是：

```text
http://localhost:8501
```

## 5. 如果 Mac 没有 Git

先安装 Apple Command Line Tools：

```bash
xcode-select --install
```

安装完成后重新打开 Terminal，再运行：

```bash
git --version
```

如果能看到版本号，再运行 GitHub 拉取命令：

```bash
git clone https://github.com/KemiZHANG/cypher-nexus-wia2005.git
cd cypher-nexus-wia2005
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m streamlit run streamlit_app.py
```

## 6. 如果 Mac 不想安装 Git

可以不用 Git：

1. 打开 GitHub 仓库：
   `https://github.com/KemiZHANG/cypher-nexus-wia2005`
2. 点击 `Code`
3. 点击 `Download ZIP`
4. 解压 ZIP
5. 把 `Datasets (2).zip` 放进解压后的项目文件夹
6. 在 Terminal 里进入该文件夹，例如：

```bash
cd ~/Downloads/cypher-nexus-wia2005-main
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m streamlit run streamlit_app.py
```

## 7. 如果 Mac 没有 Python

先检查：

```bash
python3 --version
```

如果没有 Python，可以去 Python 官网下载安装：

```text
https://www.python.org/downloads/
```

安装后重新打开 Terminal，再运行上面的命令。

## 8. 常见问题

如果提示找不到 dataset：

```text
确认 Datasets (2).zip 是否放在项目文件夹里。
```

如果提示 streamlit 命令找不到：

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run streamlit_app.py
```

如果页面打开很慢：

```text
第一次运行需要读取数据和安装缓存，后面切换会更快。
Direct Demo Mode 默认只渲染一个详细 Part，可以减少卡顿。
```
