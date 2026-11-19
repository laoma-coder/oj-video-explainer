# 音频：中文配音 + 稀疏音床

## 配音

默认使用 edge-tts：

```bash
pip install edge-tts
```

`audio/lines.json`：

```json
[
  { "id": "l1", "text": "第一句旁白。", "start": 0.7, "rate": "+2%", "voice": "zh-CN-XiaoxiaoNeural" },
  { "id": "l2", "text": "第二句旁白。", "start": 6.3, "rate": "+2%", "voice": "zh-CN-XiaoxiaoNeural" }
]
```

```bash
python scripts/tts_lines.py ./work/statement --config ./work/statement/audio/lines.json
```

脚本会输出每句时长，并检查是否有重叠。

## 混音

`audio/mix.json`：

```json
{
  "duration": 60,
  "lines": [
    { "file": "audio/lines/l1.wav", "start": 0.7 },
    { "file": "audio/lines/l2.wav", "start": 6.3 }
  ],
  "bed": {
    "notes": [523.25, 659.25, 783.99],
    "starts": [0.15, 6.25, 13.2]
  }
}
```

```bash
python scripts/mix_audio.py ./work/statement --config ./work/statement/audio/mix.json
```

输出 `audio/mix.wav`，48 kHz 立体声，峰值归一化到 -1 dBFS。

## 为什么不要持续 pad

持续正弦音（哪怕 220 Hz）在小喇叭上会被听成“嗡嗡”。音床只用：

- 短拨弦（0.9–1.1s 自然衰减）
- 轻踩镲 / 拍手（噪声瞬态）
- 转场处一个音，不铺底

人声期间音床自动 duck 到 40%。

## 检查

```bash
ffmpeg -i out/statement.mp4 -af volumedetect -f null NUL
```

期望：

- `max_volume` ≤ -1.0 dB
- `mean_volume` 约 -18 到 -22 dB
- 120 Hz 以下能量占比 < 1%

需要更严格时，用 Python 对 `audio/mix.wav` 做 FFT，检查有没有持续窄带峰。

## 许可

edge-tts 调用微软在线服务；商用/公开发布前确认服务条款。仓库不要提交生成的人声文件。
