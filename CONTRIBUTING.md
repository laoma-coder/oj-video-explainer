# Contributing

感谢你愿意补充题目或改进工作流。

## 可以贡献什么

- 新的题目示例（最好覆盖不同题型：数组、字符串、DP、图、贪心）
- 更清楚的状态可视化（数组、栈、队列、DP 表、图）
- 门禁规则（防剧透、溢出、样例一致性）
- 文档修正、英文翻译

## 不要提交

- 完整题面原文（版权归原平台/作者）
- 生成的 MP4、字体、人声文件
- 含真实姓名/学校/机构信息的截图
- 无法复现的渲染工程

## 新增一个题目示例

1. 复制模板：

```bash
python scripts/init_project.py statement ./examples/<pid>/statement
python scripts/init_project.py solution  ./examples/<pid>/solution
```

2. 按 `templates/README.md` 替换文案、代码、时间轴。
3. 跑门禁：

```bash
python scripts/check_gates.py ./examples/<pid>/statement --statement
python scripts/check_gates.py ./examples/<pid>/solution
```

4. 至少提交：

- 两张封面 `statement.jpg` / `solution.jpg`
- `README.md`（题目摘要、样例、生成参数）
- 可选：15 秒演示片段

5. PR 描述里写清：

- 题目来源与题号
- 题意片是否含做法词
- 答案片的状态可视化是什么
- 实际时长与分辨率

## PR 检查清单

- [ ] `python -m py_compile scripts/*.py` 通过
- [ ] `check_gates.py --statement` 通过
- [ ] `npx hyperframes check` 通过（如果你改了模板）
- [ ] 没有提交生成物
- [ ] 没有版权风险内容

## 代码风格

- Python 3.10+，只依赖标准库 + `edge-tts` / `numpy`
- 页面只允许确定性逻辑
- 不引入新的付费 API
- 不破坏 16:9 默认画幅
