# architecture-paper-deep-reader

面向博士研究生的计算机体系结构与系统论文深度精读 Codex Skill（V2）。输入本地 PDF，输出可保存的中文 Markdown 笔记。

## 功能

- 首页作者与机构逐一对应，完整中文摘要翻译。
- 概念基础、科学问题、技术挑战与创新映射。
- 逐创新解释公式、算法、架构、数据流、控制流、存储访问、代价和边界。
- 实验采用总览、配置、逐项解析、创新证据映射四部分，稳定使用 E01 等编号。
- 区分原文证据与推导、真实硬件与仿真，关键图表要求视觉检查。

## 安装与使用

将仓库克隆到个人 Codex skills 目录下的 architecture-paper-deep-reader 文件夹；SKILL.md 应位于该文件夹根目录。

```powershell
git clone https://github.com/sleeppoo/architecture-paper-deep-reader.git "$env:USERPROFILE/.codex/skills/architecture-paper-deep-reader"
```

如果配置了 CODEX_HOME，请改用其 skills 子目录。然后在 Codex 中请求：

> 使用 architecture-paper-deep-reader 精读这篇论文：D:/papers/paper.pdf

默认输出论文简称_Deep_Reading.md。用户可指定输出位置与关注重点。

## PDF 辅助工具

```text
python -m pip install pymupdf
python scripts/prepare_pdf.py input.pdf --out work --pages 3,5-7
```

生成逐页文本、块坐标 JSON 和指定页面 PNG；不指定 pages 时渲染全部页面。脚本负责准备资料，技术分析由 Codex 根据 Skill 完成。

## 文件结构

- SKILL.md：触发场景、证据规则和流程。
- references/analysis.md：技术深析规范。
- references/template.md：十二章输出模板。
- references/experiments.md：实验组织与编号规则。
- references/quality.md：交付检查。
- scripts/prepare_pdf.py：PDF提取和渲染。

## 验证与限制

已通过 Skill 结构检查及合成 PDF 提取/渲染测试，并使用 InstAttention（HPCA 2025）进行笔记迭代。没有复现论文实验。双栏阅读顺序需要视觉复核；扫描件需额外 OCR；脚本不自动判断科学结论是否正确。缺失证据必须披露，不补造内容。

仓库不包含论文 PDF、私人阅读材料或生成笔记。许可证尚未指定。
