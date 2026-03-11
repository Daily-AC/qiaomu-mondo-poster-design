# Seedream 5.0 Integration Design

**Goal**
在保留现有 `qiaomu-mondo-poster-design` skill 使用方式与提示词逻辑的前提下，将底层生图能力切换为 Seedream 5.0。

## Scope

首版只支持：
- 文生图
- 远程图片 URL 的图生图
- 多图参考输入（当上层脚本已有此能力时透传）

首版暂不支持：
- 本地图片文件直传
- 流式输出展示
- 异步任务编排或轮询系统

## API Contract

目标接口：
- `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`

请求头：
- `Content-Type: application/json`
- `Authorization: Bearer $ARK_API_KEY`

默认参数：
- `model: doubao-seedream-5-0-260128`
- `size: 2K`
- `output_format: png`
- `watermark: false`

按需参数：
- `prompt`：必填
- `image`：可选，支持 `string` 或 `string[]`
- `sequential_image_generation`
- `sequential_image_generation_options.max_images`
- `stream`：首版默认不启用

## File Changes

### Modify
- `scripts/generate_mondo.py`
  - 保留 prompt 生成与 CLI 参数解析
  - 改为调用 Seedream client 生成图片
- `scripts/generate_mondo_enhanced.py`
  - 保留 AI prompt enhancement、style compare 等逻辑
  - 改为调用 Seedream client 生成图片
- `SKILL.md`
  - 更新底层生成引擎说明
  - 将环境变量说明改为 `ARK_API_KEY`
  - 明确首版图生图只支持远程 URL
- `README.md`
  - 更新安装后配置与脚本调用示例
- `README.en.md`
  - 同步英文说明

### Create
- `scripts/seedream_client.py`
  - 读取 `ARK_API_KEY`
  - 构建请求 payload
  - 发送请求
  - 解析响应
  - 保存返回图片到 `outputs/`

## Design

### 1. Thin Client Layer
新增 `scripts/seedream_client.py` 作为唯一 Seedream API 入口。

建议提供以下函数：
- `get_api_key()`
- `build_payload(...)`
- `generate_image(...)`
- `save_image_from_response(...)`

这样可以避免把 API 细节散落在两个现有脚本里。

### 2. CLI Compatibility
保持现有命令风格不变，尽量不破坏用户使用习惯：
- `generate_mondo.py` 继续负责基础 prompt 生成
- `generate_mondo_enhanced.py` 继续负责增强 prompt 与高级选项
- 仅替换底层出图实现

### 3. Image Input Rules
首版只接受：
- 无 `image`：文生图
- `image` 为公网 URL：图生图
- `image` 为 URL 数组：多图参考

如果用户传本地文件路径：
- 直接报清晰错误
- 提示当前版本仅支持远程 URL

### 4. Response Handling
实现时需兼容两类返回：
- 返回图片 URL
- 返回 base64 图片内容

若官方真实返回只支持其中一种，则按实际结果收敛代码路径。

## Validation

最低验证要求：
1. 文生图 payload 正确
2. 单图 URL 图生图 payload 正确
3. 多图 URL payload 正确
4. 缺少 `ARK_API_KEY` 时错误信息明确
5. 本地路径输入时报错明确
6. 成功响应后能落盘 PNG 到 `outputs/`

## Risks

- 官方示例展示了请求格式，但未完全确认响应字段结构
- 本地文件是否支持 base64/data URL 尚未确认，因此首版不承诺本地文件输入
- `stream: true` 的事件流格式未确认，首版不实现

## Success Criteria

满足以下条件即视为完成：
- 现有 skill 不改触发方式
- 现有脚本仍可用
- 底层实际出图改为 Seedream 5.0
- 使用 `ARK_API_KEY` 完成鉴权
- 文生图和远程 URL 图生图均可工作
