# HyperFrames 页面契约

## 最小页面

```html
<!doctype html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
  </head>
  <body>
    <div id="root"
         data-composition-id="main"
         data-start="0"
         data-duration="60"
         data-width="1920"
         data-height="1080">
      ...
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      window.DUR = 60;
      window.TEXTS = () => [];   // 有文字时返回文本框
      window.render = (t) => tl.seek(t);
      window.READY = true;
    </script>
  </body>
</html>
```

真实模板里由 HyperFrames 运行时接管 `render`；页面只需要：

- `window.READY = true`
- 一个暂停的 GSAP 时间轴注册在 `window.__timelines["main"]`
- 根节点写 `data-duration`

## 规则

1. 所有动画只用确定性逻辑；禁止 `Math.random()` / `Date.now()` / 网络请求。
2. 时间轴注册后先 `tl.seek(0)`。
3. 元素显隐优先用 `opacity`，不要用 `display` 切换（seek 时容易错）。
4. 需要“文字逐条出现”时，预建多个 DOM 节点切换透明度；不要用 `tl.call` 改 `textContent`，逐帧截图/分段渲染时回调时机不可靠。
5. 音轨用一个 `<audio>`，`data-start="0"`、`data-duration` 与总时长一致。
6. 画幅由 `data-width/height` 和根元素尺寸共同决定；渲染前确认 `index.html` 的 `body` 宽高一致。

## 命令

```bash
npx hyperframes check
npx hyperframes snapshot "--at=2,8,16,24"
npx hyperframes render -o out/video.mp4
npx hyperframes doctor
```

默认视口 1920×1080；竖版在页面里写 1080×1920。

## 常见错误

| 现象 | 原因 | 处理 |
|---|---|---|
| 页面全黑 | WebGL/字体/脚本报错 | 看 `check` 输出；先 `snapshot` 单帧 |
| 文字重叠 | 用了 `tl.call` 改文本，或未预建节点 | 改成多节点切透明度 |
| 导出缺字 | 字体子集没覆盖全部汉字 | 重新跑 `subset_fonts.py` |
| 时长不对 | `data-duration` 与音频/时间轴不一致 | 三处统一 |
| 渲染很慢 | 每帧重绘网点/粒子 | 静态层预渲染到离屏 canvas |
| 内存吃满 | 并发 workers 太多 | 1080p 用 `--workers 2`，一次只跑一个 |

## 生成视频的完整命令

```bash
npx hyperframes check
npx hyperframes render -o out/statement.mp4
```

HyperFrames 输出 H.264 / yuv420p；需要无音轨素材时，去掉 `<audio>` 再渲染。
