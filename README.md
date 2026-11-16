# PaperFigure-Redraw

**上传论文图表或 PDF，调用 Skill，输入「复现」，获得可编辑、可追溯的图表素材。**

面向 Codex 与 Claude Code 的论文图表重建工作流。先判断每个面板的类型，再选择数据提取、绘图或场景重建方法，交付图片、代码、数据，以及适合继续修改的 PowerPoint 和 Excel。

> 当前能力：已完成部分复杂论文图的重建和 Office 实际编辑验证；尚不能保证任意论文全部高保真复现。保留原图的区域、估读数据、未完成项目会单独标记。原始数据优先于像素估读，截图不能算作可编辑重建。

## 目录

- [一、安装前先选好方式](#一安装前先选好方式)
- [二、获取与安装 Skill](#二获取与安装-skill)
- [三、桌面版使用教程](#三桌面版使用教程)
- [四、CLI 使用教程](#四cli-使用教程)
- [五、准备独立运行环境](#五准备独立运行环境)
- [六、从首次调用到结果验收](#六从首次调用到结果验收)
- [七、更新、固定版本与排错](#七更新固定版本与排错)

## 一、安装前先选好方式

### 你会得到什么

| 输入 | 默认目标交付物 | 修改方式 |
|---|---|---|
| 柱状图、折线图、散点图等 | 图片、Python、数据、Excel；适配时提供原生图表 | 修改单元格或数据文件，再重算或重绘 |
| 流程图、模型架构、结构示意图 | PPT、场景描述和生成代码 | 修改文字、形状、箭头和布局 |
| 数据表格 | Excel 与识别说明 | 编辑单元格、标题和格式 |
| 混合图 | 按面板组合上述文件 | 查看每个面板的可编辑范围 |
| 整篇 PDF | 逐页图表清单与各项结果 | 根据清单查找完整、部分、待处理和受阻项目 |

实验影像、复杂插画或遮挡数据可能无法恢复为原始可编辑对象。Skill 应保留来源、说明差异，不生成虚构观测值。

### 推荐：先安装到当前项目

项目级安装适合固定论文任务，也便于团队追踪版本；用户级安装适合个人跨项目使用。二者选一个即可，避免同名副本混用。

| 客户端 | 当前项目目录 | 用户级目录 | 显式调用 |
|---|---|---|---|
| Codex 桌面版、本地 CLI | `.agents/skills/paperfigure-redraw/` | `~/.agents/skills/paperfigure-redraw/` | `$paperfigure-redraw` |
| Claude Code 桌面本地会话、CLI | `.claude/skills/paperfigure-redraw/` | `~/.claude/skills/paperfigure-redraw/` | `/paperfigure-redraw` |

目录规则见 [Codex 官方说明](https://developers.openai.com/codex/skills/) 和 [Claude Code 官方说明](https://code.claude.com/docs/en/skills)。`~` 是运行该客户端的用户主目录；Windows、WSL、SSH 主机和容器不是同一个环境。

安装前需要：已安装且能登录使用的目标客户端、Git，以及用于执行重建脚本的 Python。没有 Git 也可在本仓库页面选择 **Code → Download ZIP**，解压后按下面的目录规则复制。

## 二、获取与安装 Skill

以下示例在**你的论文工作目录**执行。首次安装时目标目录应不存在；已有版本请转到更新章节。

### Windows：PowerShell

```powershell
# 进入你自己的论文工作目录，例如 D:\Research\PaperRedraw
Set-Location 'D:\Research\PaperRedraw'

git clone https://github.com/AphroditeYu/PaperFigure-Redraw.git

# Codex：执行这两行
New-Item -ItemType Directory -Force '.agents/skills' | Out-Null
Copy-Item -Recurse './PaperFigure-Redraw/skills/paperfigure-redraw' '.agents/skills/'

# Claude Code：执行这两行；只使用 Codex 时可跳过
New-Item -ItemType Directory -Force '.claude/skills' | Out-Null
Copy-Item -Recurse './PaperFigure-Redraw/skills/paperfigure-redraw' '.claude/skills/'
```

将示例路径替换为实际存在的工作目录。不要只复制 `SKILL.md`，脚本和参考文档必须一起复制。

### macOS / Linux：终端

```bash
# 进入你自己的论文工作目录
cd /path/to/your/paper-project

git clone https://github.com/AphroditeYu/PaperFigure-Redraw.git

# Codex
mkdir -p .agents/skills
cp -R ./PaperFigure-Redraw/skills/paperfigure-redraw .agents/skills/

# Claude Code；不使用时可跳过
mkdir -p .claude/skills
cp -R ./PaperFigure-Redraw/skills/paperfigure-redraw .claude/skills/
```

### 进阶：用户级安装

沿用已下载的仓库，只改变复制目的地。

```powershell
# Windows：Codex；Claude Code 将 .agents 换为 .claude
$skillParent = Join-Path $HOME '.agents/skills'
New-Item -ItemType Directory -Force $skillParent | Out-Null
Copy-Item -Recurse './PaperFigure-Redraw/skills/paperfigure-redraw' $skillParent
```

```bash
# macOS / Linux：Codex；Claude Code 将 .agents 换为 .claude
mkdir -p "$HOME/.agents/skills"
cp -R ./PaperFigure-Redraw/skills/paperfigure-redraw "$HOME/.agents/skills/"
```

### 安装结构检查

正确结构如下，Claude Code 对应 `.claude`：

```text
论文工作目录/
  .agents/skills/paperfigure-redraw/
    SKILL.md
    references/
    scripts/
    tests/
  inputs/                 # 放论文 PDF、图像、作者数据
  outputs/                # 接收复现结果
  PaperFigure-Redraw/      # 下载的仓库，用于更新
```

Windows 检查：

```powershell
Test-Path '.agents/skills/paperfigure-redraw/SKILL.md'
Test-Path '.agents/skills/paperfigure-redraw/scripts/render_scene.py'
```

macOS / Linux 检查：

```bash
test -f .agents/skills/paperfigure-redraw/SKILL.md && echo '入口文件已找到'
test -f .agents/skills/paperfigure-redraw/scripts/render_scene.py && echo '渲染脚本已找到'
```

使用 Claude Code 时把检查路径中的 `.agents` 改为 `.claude`。

## 三、桌面版使用教程

### Codex 桌面版

1. 按第二节完成项目级或用户级安装。
2. 在桌面版打开安装对应的**本地论文工作目录**，新建会话。若任务使用独立工作树，确认该工作树也能访问 Skill 与输入文件。
3. 在输入框输入 `$paperfigure-redraw`，在客户端提供的技能候选中选择它；也可直接在消息中显式指定名称。若没有候选，先用下方自检提示验证路径。
4. 附上图像/PDF，或把文件放进 `inputs/` 并提供路径，然后发送 `复现`。
5. 查看 `outputs/` 的交付物和报告。缺少执行依赖时，让智能体按第五节使用项目虚拟环境。

### Claude Code 桌面版

1. 按第二节把 Skill 安装到 `.claude/skills/` 或 `~/.claude/skills/`。
2. 打开支持 Claude Code 的桌面客户端，进入 **Code 的本地会话**，选择论文工作目录。
3. 新建会话，在输入框输入 `/`，选择 `paperfigure-redraw`，再输入 `复现` 并附上文件或路径。
4. 本地会话读取本机 Skill；SSH 会话读取远程主机目录，云端会话不会直接读取本机用户目录。具体行为见 [桌面版官方说明](https://code.claude.com/docs/en/desktop)。

本教程针对可访问本地文件并执行代码的会话。普通聊天窗口、Cowork、云端会话的安装机制不能直接套用上述本地路径。

### 桌面自检提示

```text
请检查当前会话是否能发现并读取 paperfigure-redraw Skill。
报告实际加载的 SKILL.md 路径，确认 references 和 scripts 可以访问，
并检查可用的 Python 解释器。先不要开始复现。
```

确认实际加载路径后再正式使用；“找到了文件”与“完成高质量复现”是两项不同的检查。

## 四、CLI 使用教程

CLI 指终端中的 `codex` 或 `claude`。本教程安装的是 Skill；如果这些命令不存在，先按各客户端官方安装说明安装客户端。

### Codex CLI

```bash
cd /path/to/your/paper-project
codex
```

进入交互会话后输入（这不是操作系统终端命令）：

```text
$paperfigure-redraw 复现 inputs/figure.png，结果保存到 outputs/figure-test。
```

处理论文：

```text
$paperfigure-redraw 复现 inputs/paper.pdf 中的全部图表，逐页清点，保留每个子图。
```

### Claude Code CLI

```bash
cd /path/to/your/paper-project
claude
```

进入交互会话后输入：

```text
/paperfigure-redraw 复现 inputs/figure.png，结果保存到 outputs/figure-test。
```

Windows PowerShell 同样先用 `Set-Location '你的项目路径'`，再执行 `codex` 或 `claude`。通过交互输入 Skill 名称，可以避免终端把 Codex 的 `$paperfigure-redraw` 当成环境变量展开。

## 五、准备独立运行环境

Skill 被发现不代表绘图依赖已经安装。建议每个论文项目使用独立虚拟环境；若客户端自带可用环境，可让智能体先检查并复用。

Windows：

```powershell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install pymupdf pillow numpy matplotlib openpyxl python-pptx
```

macOS / Linux：

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install pymupdf pillow numpy matplotlib openpyxl python-pptx
```

这里直接使用解释器路径，不依赖激活脚本。Windows 如果 `python` 不可用，可用已安装解释器的绝对路径，或在安装了 Python 启动器时使用 `py` 创建环境。

可向智能体补充：

```text
请使用本项目 .venv 中的 Python 执行重建，并把实际依赖版本和重跑命令写进报告。
```

PowerPoint、Excel 或其他兼容 Office 的软件用于实际打开、编辑与渲染验收。Python 库能生成文件，但不保证所有软件显示完全一致；没有 Office 时也可交付文件，报告应明确哪些检查没有执行。

## 六、从首次调用到结果验收

### 最短调用

选中 Skill 并附上文件后，只输入：

```text
复现
```

这是工作流约定，不保证客户端每次都会自动选中 Skill。首次使用建议显式调用 `$paperfigure-redraw` 或 `/paperfigure-redraw`。

### 进阶提示模板

```text
复现我上传的论文图表。
先按面板判断类型；优先查找并核对作者源数据。
数据图输出 Excel、图片、Python 和数据；流程图输出原生对象组成的 PPT。
保留布局、标签与箭头，不要简化成摘要框。
对图片保留区域、估读值和无法恢复内容单独列出，禁止编造缺失数据。
实际打开或渲染交付物，检查可编辑性。输出完整的面板清单、差异和重跑方法。
```

整篇 PDF 可追加：`覆盖正文及已提供的附录；分批处理但保持同一份总清单，不遗漏待处理项。`

### 建议的第一次验收

| 检查项 | 合格表现 |
|---|---|
| 分类 | 一张混合图中的流程、数据和影像分开处理 |
| PPT | 文字、形状和连接线可以独立修改；原图区域明确标记 |
| Excel | 修改输入后关联公式和图表能更新；误差棒有依据 |
| 溯源 | 区分作者数据、截图估读、缺失内容 |
| 完整性 | 每个面板都有结果或具体状态，待处理不冒充无法复现 |
| 可重跑 | 提供代码、必要数据、依赖和命令 |

目录示例：

```text
outputs/
  manifest.json
  report.md
  figure-01/
    redraw.py
    data.xlsx
    figure.png
  figure-02/
    scene.json
    diagram.pptx
    preview.png
```

当前脚本包括 PDF 页面渲染与候选图注清点、有限条件下的柱高提取、人工核对场景的 PPT 渲染。它们不是自动完成所有图表识别的独立应用；具体适用条件见 [Skill 入口](skills/paperfigure-redraw/SKILL.md)。

## 七、更新、固定版本与排错

### 更新

在论文工作目录执行：

```bash
git -C PaperFigure-Redraw pull --ff-only
git -C PaperFigure-Redraw rev-parse HEAD
```

随后将已安装的 `paperfigure-redraw` 文件夹移至 **skills 目录之外**备份，再复制仓库中的新版本。不要把整个仓库嵌套复制到 Skill 文件夹内，也不要只更新 `SKILL.md`。新建会话，再用自检提示确认加载路径。`git pull` 只更新下载的仓库，不会自动同步之前复制的安装副本。

### 固定版本与团队复用

在测试通过后记录 `git rev-parse HEAD` 输出的提交号。需要复用时，在下载的仓库中执行 `git checkout 你的提交号`，再安装该版本。团队项目可将项目级 Skill 纳入版本管理；论文输入、第三方图片和结果是否提交应另行决定。

### 常见问题

| 现象 | 优先检查 |
|---|---|
| 名称没有出现在候选中 | 是否复制到当前会话读取的目录；文件夹是否多嵌套了一层；是否新建会话 |
| 更新后行为没变 | 安装副本是否同步；用户级与项目级是否有同名版本 |
| 本地能用，WSL/SSH 不能用 | Skill、Python、输入文件是否在实际执行的环境中 |
| 能读 Skill，但脚本报缺库 | 使用的 Python 是否为安装依赖的同一个解释器 |
| Excel 图表空白或坐标轴不见 | 重新计算公式；检查图表范围与坐标轴设置；实际导出后目视核对 |
| PPT 看起来像原图但不能编辑内部 | 是否只是嵌入图片；查看报告中的原生对象与原图区域说明 |
| 源数据重绘与论文不同 | 核对筛选规则、重复次数、统计口径与配色，不能随意删点来匹配 |
| PDF 只处理了一部分 | 要求核对逐页清单，继续待处理项，并列出缺失补充材料 |

### 卸载

移走或删除对应安装位置的 `paperfigure-redraw` 文件夹，然后新建会话。保留论文输入、输出和下载的仓库即可；无需删除其他 Skill。

## 许可与使用边界

本仓库代码与说明使用 [MIT 许可](LICENSE)。论文图片、作者数据及第三方插画遵循各自来源许可。复现结果应核对后再用于研究或发表，估读值不能冒充原始实验观测。
