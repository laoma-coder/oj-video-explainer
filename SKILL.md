---
name: oj-video-explainer
description: 把一道编程题（LeetCode / 洛谷 / CSP-J / NOI / 学校 OJ）做成两条视频：只讲题面的题意讲解，和逐行执行的参考答案讲解。Use when asked to explain an OJ problem as video, produce 题意讲解 / 答案讲解, or build a coding-problem video pipeline.
version: 0.1.0
author: OJ Video Explainer contributors
license: MIT
language: zh-CN
entrypoint: SKILL.md
mode: workflow
tags:
  - competitive-programming
  - education
  - hyperframes
  - video
  - agent-skill
outputs:
  - mp4
  - jpg
  - md
---

# OJ Video Explainer

把一道编程题拆成两条互相独立的视频：

1. **题意讲解**（45–75 秒）：只讲题面、输入输出、约束、样例；**绝不出现做法**。
2. **答案讲解**（90–150 秒）：逐行执行参考代码，讲清变量/数组怎么变、为什么这么写、边界在哪。

两条视频都用 [HyperFrames](https://github.com/heygen-com/hyperframes) 渲染：HTML + GSAP → 浏览器逐帧截图 → MP4。

## 什么时候用

- 用户给出一道题（题面、题号、截图或链接），想要讲解视频
- 用户只要“题意讲解”，不要答案
- 用户有参考答案，想要“答案讲解 / 代码走读”
- 需要批量做 OJ 题目的教学素材

## 什么时候不用

- 只是要文字题解 → 直接写 Markdown
- 要真人出镜口播 → 这是 motion graphics 工作流，不替代拍摄
- 题目涉及版权素材且用户没有授权 → 先确认题面使用权限

## 输入

必填（至少一种）：

- 题目原文（文本 / 截图 / HTML）
- 或题号 + 平台（洛谷 P14357、CSP-J 2025 T1 等）

可选：

- 参考答案代码（没有的话，答案讲解阶段先生成并人工确认）
- 目标平台与画幅（默认 16:9 横版 1920×1080）
- 时长（默认题意 60 秒，答案 90 秒）
- 配音音色（默认 `zh-CN-XiaoxiaoNeural`）

## 绝对约束

1. **题意视频不能剧透**：不能出现做法名（排序、贪心、统计、前缀和、DP、二分、哈希、桶）、不能出现完整代码、不能出现“所以答案是”。
2. **样例必须与题面一致**：输入、输出、标点逐字核对。
3. **不编造约束**：题面没写的复杂度、数据范围、特殊性质，不能自己加。
4. **答案必须能过**：参考答案先人工确认；答案片可以讲“为什么”，但不能把错误代码当正确代码。
5. **大数用 string**：只要答案可能超过 18 位，参考代码和讲解都必须用字符串，禁止 `int` / `long long` 存答案。
6. **统一规格**：1920×1080（或 1080×1920）、30fps、H.264、yuv420p、无第三方版权素材。
7. **可复现**：页面只允许确定性逻辑，禁止 `Math.random()`、`Date.now()`、网络请求。
8. **音频无持续低频**：不要持续 pad / 噪声床；只留短音、拨弦、轻节奏，避免“嗡嗡”。

## 工作流

### Step 0：拆题

把题目整理成 `problem.md`：

- 平台 / 题号 / 题目名 / 难度
- 一句话任务
- 输入格式
- 输出格式
- 数据范围（逐条抄，不改写）
- 样例（输入 / 输出 / 解释）
- 特殊性质（如果有）
- 易错点（仅记录，题意片不展开）

参考：`references/problem-parsing.md`

### Step 1：写题意脚本

结构建议（60 秒）：

1. 0–5s 标题：题号、题目名、来源
2. 5–15s 给了什么：输入对象、取值范围、关键限制
3. 15–25s 能做什么：允许的操作、禁止的操作
4. 25–40s 例子：用题面样例走一遍“是什么”，不推导做法
5. 40–50s 输入输出格式
6. 50–60s 收尾：提醒“先想清楚，再看答案”

写完后跑 `scripts/check_gates.py --statement`，确认没有做法词和代码。

参考：`references/statement-video.md`

### Step 2：写答案脚本

结构建议（90 秒）：

1. 0–8s 开场：这份代码分几步
2. 8–30s 第一步：数据结构 / 统计 / 初始化，配合数组或变量动画
3. 30–45s 为什么这么写：正确性直觉、边界
4. 45–70s 主循环 / 核心操作：逐行高亮，展示状态变化
5. 70–85s 边界与坑：溢出、空输入、前导零、复杂度
6. 85–90s 总结：三步口诀

答案片必须包含：

- 代码面板 + 当前行高亮
- 至少一个“状态可视化”（数组桶、字符串、栈、队列、DP 表、图）
- 一次“错误写法 vs 正确写法”对比（如果题目有典型坑）
- 复杂度

参考：`references/solution-video.md`、`references/visual-grammar.md`

### Step 3：搭工程

```bash
python scripts/init_project.py statement ./work/statement
python scripts/init_project.py solution  ./work/solution
```

模板在 `templates/statement/` 与 `templates/solution/`，是已经能渲染的 P14357 示例；把文案、代码、时间轴替换成当前题目。

HyperFrames 契约见 `references/hyperframes-contract.md`。

### Step 4：生成音频与字体

```bash
python scripts/tts_lines.py ./work/statement --config ./work/statement/audio/lines.json
python scripts/subset_fonts.py ./work/statement/index.html ./work/statement/fonts
python scripts/mix_audio.py ./work/statement --config ./work/statement/audio/mix.json
```

三条命令分别做：配音、中文子集字体、配音 + 稀疏音床混音。

参考：`references/audio.md`

### Step 5：检查

```bash
python scripts/check_gates.py ./work/statement --statement
python scripts/check_gates.py ./work/solution
cd ./work/statement && npx hyperframes check
cd ../solution && npx hyperframes check
```

### Step 6：抽帧审片

```bash
npx hyperframes snapshot "--at=2,8,16,24,33,48,62,83"
```

必须亲眼确认：

- 字幕没有被底部 UI 遮住
- 代码高亮对得上当前行
- 数组/变量变化看得懂
- 没有黑帧、文字溢出、素材缺失

### Step 7：渲染与交付

```bash
npx hyperframes render -o out/statement.mp4
npx hyperframes render -o out/solution.mp4
```

交付清单：

- `statement.mp4` / `solution.mp4`
- `poster.jpg` ×2
- `shotlist.md`（两片时间轴）
- `params.md`（分辨率、帧率、配音、音乐、字体、时长）

## 目录

```text
oj-video-explainer/
├── SKILL.md
├── references/
│   ├── problem-parsing.md
│   ├── statement-video.md
│   ├── solution-video.md
│   ├── visual-grammar.md
│   ├── hyperframes-contract.md
│   ├── audio.md
│   └── qa-gates.md
├── scripts/
│   ├── init_project.py
│   ├── tts_lines.py
│   ├── subset_fonts.py
│   ├── mix_audio.py
│   └── check_gates.py
├── templates/
│   ├── statement/index.html
│   └── solution/index.html
└── examples/p14357/
```

## 质量门禁

- [ ] 题意片 0 个做法词、0 段完整代码
- [ ] 两片样例与题面逐字一致
- [ ] 答案片至少一个状态可视化
- [ ] 代码高亮与口播同步
- [ ] 大数用 string，且有溢出对比
- [ ] `hyperframes check` 通过
- [ ] 无黑帧、无文字溢出、无遮挡
- [ ] 音频峰值 ≤ -1 dBFS，无持续低频嗡鸣

完整清单：`references/qa-gates.md`

## 示例

`examples/p14357/` 是 CSP-J 2025 T1「拼数」的双片示例：

- 题意 60 秒
- 答案 90 秒
- 数组桶计数 + 数字飞入 + `res` 逐位拼接

## 许可

代码 MIT。题目原文版权归原平台/作者所有；示例只使用自己改写的题意摘要。字体 Noto Sans SC / Inter / JetBrains Mono 均为 OFL。edge-tts 为微软在线服务，商用前请确认条款。
