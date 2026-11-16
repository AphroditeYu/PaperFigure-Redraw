# PaperFigure-Redraw

[English](README.md) | [中文](README.zh-CN.md)

Recreate paper figures as editable, traceable research assets.

## Desktop and CLI installation

Clone this repository, then copy the full skill folder into the project opened in the desktop app or CLI. Start a new session after copying. For CLI, change to that project directory before starting the agent.

```bash
git clone https://github.com/AphroditeYu/PaperFigure-Redraw.git
# From your target project, replace SOURCE with the clone's absolute path
mkdir -p .agents/skills .claude/skills
cp -R SOURCE/skills/paperfigure-redraw .agents/skills/  # Codex desktop or CLI
cp -R SOURCE/skills/paperfigure-redraw .claude/skills/  # Claude Code
```

Windows PowerShell: `New-Item -ItemType Directory -Force .agents/skills; Copy-Item -Recurse 'C:\path\to\PaperFigure-Redraw\skills\paperfigure-redraw' '.agents/skills/'`. For Claude Code use `.claude/skills` instead. For user-wide installation use `~/.agents/skills/` or `~/.claude/skills/`. In Claude Desktop use a local Claude Code session that can access the project; availability depends on the client. Invoke `$paperfigure-redraw` in Codex or `/paperfigure-redraw` in Claude Code.

[Codex documentation](https://developers.openai.com/codex/skills/) · [Claude Code documentation](https://code.claude.com/docs/en/skills)


### What it does

Give an agent a PDF, screenshot, or figure. The skill routes quantitative charts to reproducible plots, code and data; diagrams to editable PowerPoint shapes; and tables to editable Excel cells. For an entire PDF it inventories every page and panel, processes items in batches, and reports complete, partial and blocked work. User-supplied appendices and supplements are included.

**Limits:** This is an agent skill, not a standalone guarantee of perfect one-click reproduction. Fidelity depends on source quality, data access, available tools and time. Values digitized from images are estimates; missing observations are not invented. Photographs, microscopy, and complex illustrations may require a labeled reference crop with editable overlays. A screenshot alone is not counted as a reconstruction.

### Install

Clone this repository:

```bash
git clone https://github.com/AphroditeYu/PaperFigure-Redraw.git
```

Copy the complete `skills/paperfigure-redraw` directory to `.agents/skills/` in your project for Codex, or `.claude/skills/` for Claude Code. For user-wide installation, use `~/.agents/skills/` or `~/.claude/skills/` respectively. See the commands above for macOS, Linux and PowerShell. Start a new session. Requirements depend on the requested output; the optional PDF helper requires `python -m pip install pymupdf`.

### Example

Attach a paper or image and ask:

```text
Use $paperfigure-redraw to recreate every figure and table in this PDF.
Include each panel, runnable code, data, editable PowerPoint/Excel where
appropriate, and a report of approximations and blocked items.
```

In Claude Code, invoke `/paperfigure-redraw` with the attachment. Inspect the inventory and report before using reconstructed results in research. The PDF helper renders pages and finds candidate captions; it is not an automatic complete figure detector.

### Responsible use

Respect authors' rights and access restrictions. Original data is preferable to digitized estimates. Reconstructed scientific images should not be represented as original experimental evidence. Review all results before publication.


## License

MIT. See [LICENSE](LICENSE).
