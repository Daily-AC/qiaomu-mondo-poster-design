# OpenClaw 部署指南（Seedream 5.0 版）

这份文档是给 OpenClaw / Claude Code 用户看的最小部署说明，目标是：**尽量少配、装完就能用**。

## 这份 skill 现在的行为

安装这个 skill 后：
- Claude 命中 `qiaomu-mondo-poster-design` skill 时
- 会调用本地脚本生成提示词
- 底层**直接走 Seedream 5.0** 出图

当前不是多模型轮询，也不是多个 provider 自动 fallback。

默认模型：
- `doubao-seedream-5-0-260128`

鉴权方式：
- 环境变量 `ARK_API_KEY`

当前限制：
- 文生图：支持
- 图生图：支持
- **图生图首版仅支持远程图片 URL**，暂不支持本地图片文件直传

---

## 一键安装（推荐）

如果要安装维护好的 fork 版本：

```bash
npx skills add Daily-AC/qiaomu-mondo-poster-design
```

安装完成后，skill 会出现在本地 Claude skills 目录中。

---

## 依赖安装

这个 skill 的脚本依赖 Python 运行环境。

### 1. 确认 Python 3

```bash
python3 --version
```

### 2. 安装依赖

```bash
python3 -m pip install -r ~/.claude/skills/qiaomu-mondo-poster-design/requirements.txt
```

依赖包括：
- `requests`
- `Pillow`

---

## 配置 Seedream 5.0 API Key

### 临时方式（当前 shell 生效）

```bash
export ARK_API_KEY="你的 Seedream / Ark API Key"
```

### 持久方式（macOS / zsh）

把下面这行加入 `~/.zshrc`：

```bash
export ARK_API_KEY="你的 Seedream / Ark API Key"
```

然后执行：

```bash
source ~/.zshrc
```

---

## 验证是否安装成功

### 1. 验证 prompt 生成功能

```bash
python3 ~/.claude/skills/qiaomu-mondo-poster-design/scripts/generate_mondo.py "Akira cyberpunk anime" movie --no-generate
```

如果成功，会打印一段 Mondo 风格提示词。

### 2. 验证增强版 prompt 生成功能

```bash
python3 ~/.claude/skills/qiaomu-mondo-poster-design/scripts/generate_mondo_enhanced.py "Blade Runner" movie --no-generate
```

### 3. 验证真实文生图

```bash
python3 ~/.claude/skills/qiaomu-mondo-poster-design/scripts/generate_mondo.py "Jazz Festival poster, Mondo style" event --output ~/.claude/skills/qiaomu-mondo-poster-design/outputs/test-seedream.png
```

如果成功，会在 `outputs/` 目录下生成 PNG。

---

## OpenClaw / Claude 中怎么触发

这个 skill 的触发方式主要看用户输入是否命中下面这些意图：

- `Mondo风格`
- `书籍封面设计`
- `专辑封面`
- `海报设计`
- `读书笔记配图`
- `公众号封面`
- `小红书配图`
- `文章配图`

示例：

```text
用 Mondo 风格为《三体》生成一张书籍封面
为周杰伦《七里香》设计专辑封面
为我的公众号文章《人类简史》设计一张封面
```

命中 skill 后，底层出图就会直接调用 Seedream 5.0。

---

## 可选：命令行直接使用

### 基础版

```bash
python3 ~/.claude/skills/qiaomu-mondo-poster-design/scripts/generate_mondo.py "Dune sci-fi epic" movie
```

### 增强版

```bash
python3 ~/.claude/skills/qiaomu-mondo-poster-design/scripts/generate_mondo_enhanced.py "Blade Runner" movie --ai-enhance
```

### 图生图（仅远程 URL）

```bash
python3 ~/.claude/skills/qiaomu-mondo-poster-design/scripts/generate_mondo_enhanced.py "cyberpunk noir" movie --input https://example.com/poster.png --style saul-bass
```

---

## 常见问题

### 1. 报错 `ARK_API_KEY environment variable is required`

说明没有配置 API Key。

先执行：

```bash
export ARK_API_KEY="你的key"
```

再重试。

### 2. 报错 `No module named 'requests'`

说明 Python 依赖没装。

执行：

```bash
python3 -m pip install -r ~/.claude/skills/qiaomu-mondo-poster-design/requirements.txt
```

### 3. 图生图传本地文件失败

这是当前版本的已知限制。

当前仅支持：
- `https://...`
- `http://...`

不支持：
- `poster.jpg`
- `/Users/xxx/poster.png`

### 4. 这个 skill 会不会自动在多个模型之间切换？

不会。

当前逻辑是：
- 命中这个 skill
- 直接调用 Seedream 5.0

不是多 provider fallback。

---

## 推荐给最终用户的最短说明

只要给用户这 3 步就够了：

```bash
npx skills add Daily-AC/qiaomu-mondo-poster-design
python3 -m pip install -r ~/.claude/skills/qiaomu-mondo-poster-design/requirements.txt
export ARK_API_KEY="你的key"
```

然后直接对 Claude 说：

```text
用 Mondo 风格为《三体》生成一张书籍封面
```
