# Open Notebook MCP 服务器 (onb-mcp)

[简体中文] | [English](../../README.md) | [日本語](JA.md)

<!-- mcp-name: io.github.Epochal-dev/open-notebook -->

这是一个 MCP (Model Context Protocol) 服务器，提供用于与 [Open Notebook](https://github.com/lfnovo/open-notebook) API 进行交互的工具。该服务器使 Claude 等 AI 助手能够通过 Open Notebook 管理笔记本、内容源、笔记，进行内容检索以及调用 AI 模型。

## 主要功能

- **笔记本管理 (Notebooks)**: 创建、获取、更新和删除笔记本
- **内容源管理 (Sources)**: 添加和管理内容源（链接、上传、文本）
- **笔记管理 (Notes)**: 在笔记本内创建和组织笔记
- **搜索与 AI (Search & AI)**: 使用向量/文本搜索内容，以及进行智能问答
- **模型管理 (Models)**: 配置和管理 AI 模型
- **会话管理 (Chat Sessions)**: 创建和管理聊天对话
- **设置 (Settings)**: 获取和更新应用程序设置
- **渐进式披露 (Progressive Disclosure)**: 使用 `search_capabilities` 进行高效的工具发现

## 安装方法

### 使用 uv (推荐)

```bash
# 克隆仓库
git clone https://github.com/rmc8/onb-mcp.git
cd onb-mcp

# 同步依赖项
uv sync
```

### 使用 pip

```bash
pip install -e .
```

## 配置方法

服务器需要进行配置以连接到您的 Open Notebook 实例。

### 环境变量

创建 `.env` 文件或设置以下环境变量：

```bash
# 必须：您的 Open Notebook 实例 URL
OPEN_NOTEBOOK_URL=http://localhost:5055

# 可选：身份验证密码（如果在 Open Notebook 中设置了 APP_PASSWORD）
OPEN_NOTEBOOK_PASSWORD=your_password_here

# 可选：传输协议配置（默认：stdio）
MCP_TRANSPORT=stdio  # 远程部署时使用 streamable-http
```

### 配置示例

使用默认 Open Notebook 设置的本地开发环境：

```bash
# .env
OPEN_NOTEBOOK_URL=http://localhost:5055
```

如果您的 Open Notebook 配置了身份验证：

```bash
# .env
OPEN_NOTEBOOK_URL=http://localhost:5055
OPEN_NOTEBOOK_PASSWORD=my_secure_password
```

## 使用方法

### 运行服务器

#### 开发模式 (STDIO)

供 AI 助手本地使用：

```bash
uv run onb-mcp
```

#### 生产模式 (Streamable HTTP)

用于远程部署：

```bash
MCP_TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 uv run onb-mcp
```

### 在 Claude Desktop 中使用

将其添加到您的 Claude Desktop 配置文件（例如 `~/Library/Application Support/Claude/claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "onb-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/onb-mcp",
        "onb-mcp"
      ],
      "env": {
        "OPEN_NOTEBOOK_URL": "http://localhost:5055",
        "OPEN_NOTEBOOK_PASSWORD": "your_password_if_needed"
      }
    }
  }
}
```

### 探索可用工具 (渐进式披露)

本服务器实现了渐进式披露以优化上下文效率。您可以使用 `search_capabilities` 工具来发现可用工具：

```python
# 获取所有工具的摘要列表
search_capabilities(query="", detail="summary", limit=50)

# 按关键字搜索特定工具
search_capabilities(query="notebook", detail="summary", limit=10)

# 获取特定工具的完整参数和返回值详情
search_capabilities(query="create_notebook", detail="full", limit=1)
```

---

## 可用工具列表

服务器在多个类别中提供了共 50 个工具。详细信息可通过 `search_capabilities` 工具查询：

- **元工具**: `search_capabilities`
- **笔记本 (5个)**: `list_notebooks`, `get_notebook`, `create_notebook`, `update_notebook`, `delete_notebook`
- **内容源 (5个)**: `list_sources`, `get_source`, `create_source`, `update_source`, `delete_source`
- **笔记 (5个)**: `list_notes`, `get_note`, `create_note`, `update_note`, `delete_note`
- **搜索与 AI (3个)**: `search`, `ask_question`, `ask_simple`
- **模型 (5个)**: `list_models`, `get_model`, `create_model`, `delete_model`, `get_default_models`
- **聊天 (7个)**: `list_chat_sessions`, `create_chat_session`, `get_chat_session`, `update_chat_session`, `delete_chat_session`, `execute_chat`, `get_chat_context`
- **设置 (2个)**: `get_settings`, `update_settings`
- **数据转换 (3个)**: `list_transformations`, `create_transformation`, `apply_transformation`
- **播客 (3个)**: `generate_podcast`, `retry_podcast`, `get_podcast_job_status`
- **凭据管理 (4个)**: `list_credentials`, `test_credential`, `discover_models`, `register_models`
- **向量重构 (1个)**: `rebuild_embeddings`

## 项目结构

```
onb-mcp/
├── src/
│   └── onb_mcp/
│       ├── __init__.py
│       ├── config.py         # 配置与常量
│       ├── mcp_app.py        # FastMCP 实例
│       ├── client.py         # 共通 API 请求处理
│       ├── capabilities.py   # 工具元数据收集
│       ├── server.py         # 入口点
│       └── tools/            # 领域特定模块
│           ├── __init__.py
│           ├── meta.py
│           ├── notebooks.py
│           ├── sources.py
│           ├── notes.py
│           ├── search.py
│           ├── models.py
│           ├── chat.py
│           ├── settings.py
│           ├── transformations.py
│           ├── podcasts.py
│           ├── credentials.py
│           └── rebuild.py
├── tests/                    # pytest 契约测试
├── pyproject.toml
├── README.md
└── AGENTS.md
```
