# Templates

这两个目录是**已经能渲染的完整工程**，不是空壳。

- `statement/index.html` — 60 秒题意讲解（P14357 示例）
- `solution/index.html` — 90 秒答案讲解（P14357 示例）

复制到工作目录：

```bash
python scripts/init_project.py statement ./work/statement
python scripts/init_project.py solution  ./work/solution
```

## 替换什么

1. **文案**：所有标题、字幕、卡片文字
2. **题目数据**：字符串、样例、约束
3. **代码面板**：答案片里的 15 行参考代码
4. **时间轴**：`data-start` / `data-duration`、GSAP 的绝对时间
5. **音频配置**：`audio/lines.json`、`audio/mix.json`

## 不要直接提交生成物

以下文件被 `.gitignore` 忽略，换机器后重新生成：

- `fonts/*.woff2` → `subset_fonts.py`
- `audio/lines/*.mp3|wav` → `tts_lines.py`
- `audio/mix.wav` → `mix_audio.py`
- `out/*.mp4` → `hyperframes render`

## 页面契约

- 根节点必须有 `data-composition-id`、`data-duration`、`data-width`、`data-height`
- GSAP 时间轴暂停，注册到 `window.__timelines["main"]`
- 禁止 `Math.random()` / `Date.now()` / 网络请求
- 文字变化用多节点切换透明度，不要用 `tl.call` 改 `textContent`

详见 `references/hyperframes-contract.md`。
