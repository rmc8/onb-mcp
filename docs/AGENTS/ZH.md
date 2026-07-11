# onb-mcp Agent Constitution (生存指南)

本文件是为在此代码库中进行开发工作的 AI 智能体（Agent）所制定的、最核心且最精简的设计原则和开发规程。

## 1. 最重要原则 (生存法则)
1. **死守上下文效率**: 决不能直接返回海量原始数据。必须返回摘要 ＋ ID（或文件路径）。过滤和转换必须在执行环境（Python 服务器端）中进行。
2. **标准工具发现 (`search_capabilities`)**: 为了允许 AI 渐进式地获取工具规范，请务必在 `CAPABILITIES` 索引中保持最新的工具定义。
3. **禁止向标准输出 (stdout) 写入日志**: 对于 STDIO 传输，stdout 专用于协议帧交互。向 stdout 写入调试日志或使用 `print()` 会导致服务器崩溃。必须始终使用 `logging` 向标准错误输出 (stderr) 写入日志。
4. **明确的超时设置**: 对所有外部 API 或网络 I/O 请求设置明确、合理的超时时间。

## 2. 项目结构与角色
- `src/onb_mcp/config.py`: 配置常量和环境变量辅助函数。
- `src/onb_mcp/mcp_app.py`: FastMCP 应用程序实例 (`mcp`)。
- `src/onb_mcp/client.py`: 共通 HTTP 通信辅助函数 (`make_request`)。
- `src/onb_mcp/capabilities.py`: 工具元数据汇总列表 (`CAPABILITIES` 元组)。
- `src/onb_mcp/tools/`: 按功能领域分组的所有 `@mcp.tool()` 实现的子模块。
- `src/onb_mcp/server.py`: 服务器入口点，加载所有子模块并为了测试兼容性重新导出符号。

## 3. 添加工具时的开发流程
1. **更新元数据**: 将新工具规格追加到对应领域模块的 `CAPABILITIES` 子元组中。
2. **实现工具**: 在 `src/onb_mcp/tools/` 下对应的领域模块中编写带有 `@mcp.tool()` 装饰器的工具函数。
3. **添加测试**: 在 `tests/test_capabilities.py` 中编写契约/验证测试，以断言返回数据的结构。
4. **验证**: 运行 `uv run pytest` 并确保所有测试顺利通过。
