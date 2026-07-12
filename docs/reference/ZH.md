# Open Notebook MCP 工具参考手册

[简体中文] | [English](EN.md) | [日本語](JA.md)

本文档是 `onb-mcp` 服务器提供的全部 54 个工具的官方参考手册，包含参数、返回值类型及功能说明。

## 元工具

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `search_capabilities` | 通过渐进式细节级别搜索该服务器提供的工具。 | `query: str`, `detail: Literal['name','summary','full']`, `limit: int` | `dict[str, Any]` |

## 笔记本管理

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_notebooks` | 获取所有笔记本，支持过滤和排序. | `archived: Optional[bool]`, `order_by: str`, `limit: int` | `dict[str, Any]` |
| `get_notebook` | 通过 ID 获取特定的笔记本。 | `notebook_id: str` | `dict[str, Any]` |
| `create_notebook` | 创建新笔记本。 | `name: str`, `description: Optional[str]` | `dict[str, Any]` |
| `update_notebook` | 更新笔记本信息或归档状态。 | `notebook_id: str`, `name: Optional[str]`, `description: Optional[str]`, `archived: Optional[bool]` | `dict[str, Any]` |
| `delete_notebook` | 删除特定笔记本。 | `notebook_id: str` | `dict[str, Any]` |

## 内容源管理

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_sources` | 获取特定笔记本内的所有内容源。 | `notebook_id: Optional[str]`, `limit: int`, `offset: int` | `dict[str, Any]` |
| `get_source` | 通过 ID 获取特定内容源。 | `source_id: str` | `dict[str, Any]` |
| `create_source` | 创建新内容源（链接、文件或文本，可选生成向量）。 | `notebook_id: str`, `type: str`, `url: Optional[str]`, `title: Optional[str]`, `embed: bool` | `dict[str, Any]` |
| `update_source` | 更新内容源的标题或标签。 | `source_id: str`, `title: Optional[str]`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `delete_source` | 删除特定内容源。 | `source_id: str` | `dict[str, Any]` |

## 笔记管理

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_notes` | 获取所有笔记，支持过滤。 | `notebook_id: Optional[str]`, `limit: int`, `offset: int` | `dict[str, Any]` |
| `get_note` | 通过 ID 获取特定笔记。 | `note_id: str` | `dict[str, Any]` |
| `create_note` | 创建新笔记。 | `notebook_id: str`, `title: str`, `content: str`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `update_note` | 更新笔记的标题、内容或标签。 | `note_id: str`, `title: Optional[str]`, `content: Optional[str]`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `delete_note` | 删除特定笔记。 | `note_id: str` | `dict[str, Any]` |

## 搜索与 AI 问答

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `search` | 使用向量或全文检索进行内容搜索。 | `query: str`, `type: str`, `notebook_id: Optional[str]`, `limit: int` | `dict[str, Any]` |
| `ask_question` | 指定 AI 模型与推理策略，对内容进行深度问答。 | `question: str`, `strategy_model: str`, `answer_model: str`, `final_answer_model: str` | `dict[str, Any]` |
| `ask_simple` | 对内容进行简易的智能问答。 | `question: str`, `strategy_model: str`, `answer_model: str`, `final_answer_model: str` | `dict[str, Any]` |

## AI 模型配置

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_models` | 获取系统已配置的所有 AI 模型列表。 | `limit: int` | `dict[str, Any]` |
| `get_model` | 通过 ID 获取特定的 AI 模型配置。 | `model_id: str` | `dict[str, Any]` |
| `create_model` | 创建新的 AI 模型配置。 | `name: str`, `provider: str`, `type: str` | `dict[str, Any]` |
| `delete_model` | 删除特定的 AI 模型配置。 | `model_id: str` | `dict[str, Any]` |
| `get_default_models` | 获取系统默认的 AI 模型配置。 | `无` | `dict[str, Any]` |
| `discover_models` | 动态发现特定服务商提供的可用 AI 模型。 | `credential_id: str` | `dict[str, Any]` |
| `register_models` | 在系统中注册已发现的 AI 模型。 | `credential_id: str` | `dict[str, Any]` |

## 会话管理

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_chat_sessions` | 获取所有聊天会话，支持过滤。 | `notebook_id: Optional[str]`, `limit: int` | `dict[str, Any]` |
| `create_chat_session` | 创建新的聊天会话。 | `notebook_id: str`, `title: str` | `dict[str, Any]` |
| `get_chat_session` | 通过 ID 获取特定的聊天会话记录。 | `session_id: str` | `dict[str, Any]` |
| `update_chat_session` | 更新聊天会话标题。 | `session_id: str`, `title: Optional[str]` | `dict[str, Any]` |
| `delete_chat_session` | 删除特定的聊天会话。 | `session_id: str` | `dict[str, Any]` |
| `execute_chat` | 在会话中发送消息并获取 AI 的回复。 | `session_id: str`, `message: str`, `context: Optional[dict]` | `dict[str, Any]` |
| `get_chat_context` | 为聊天会话构建关联的上下文数据。 | `notebook_id: str`, `context_config: Optional[dict]` | `dict[str, Any]` |

## 应用程序设置

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `get_settings` | 获取应用程序的系统设置。 | `无` | `dict[str, Any]` |
| `update_settings` | 更新应用程序的系统设置。 | `settings: dict` | `dict[str, Any]` |

## 数据转换 (AI 动作)

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_transformations` | 获取所有自定义转换（AI动作）提示词模板。 | `无` | `dict[str, Any]` |
| `create_transformation` | 创建新的自定义转换提示词模板。 | `name: str`, `prompt: str`, `description: Optional[str]` | `dict[str, Any]` |
| `apply_transformation` | 对内容源应用转换模板以提取摘要或洞察。 | `source_id: str`, `transformation_id: str` | `dict[str, Any]` |

## 播客音频生成

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `generate_podcast` | 从选定内容源异步生成播客对话音频任务。 | `notebook_id: str`, `episode_name: str`, `episode_profile: str`, `speaker_profile: str`, `content: Optional[str]`, `briefing_suffix: Optional[str]` | `dict[str, Any]` |
| `retry_podcast` | 重新尝试失败的播客生成任务。 | `episode_id: str` | `dict[str, Any]` |
| `get_podcast_job_status` | 获取异步播客生成任务的进度与状态。 | `job_id: str` | `dict[str, Any]` |

## 声音人设管理 (Speaker Profiles)

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_speaker_profiles` | 获取所有已注册的声音人设配置。 | 无 | `dict[str, Any]` |
| `get_speaker_profile` | 通过 ID 获取特定的声音人设。 | `profile_id: str` | `dict[str, Any]` |
| `create_speaker_profile` | 创建新的声音人设。 | `name: str`, `description: Optional[str]`, `voice_model: str`, `speakers: list`, `tts_provider: Optional[str]`, `tts_model: Optional[str]` | `dict[str, Any]` |
| `update_speaker_profile` | 更新现有的声音人设。 | `profile_id: str`, `name: Optional[str]`, `description: Optional[str]`, `voice_model: Optional[str]`, `speakers: Optional[list]`, `tts_provider: Optional[str]`, `tts_model: Optional[str]` | `dict[str, Any]` |
| `delete_speaker_profile` | 删除特定的声音人设。 | `profile_id: str` | `dict[str, Any]` |

## 单期节目格式管理 (Episode Profiles)

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_episode_profiles` | 获取所有已注册的单期节目格式配置。 | 无 | `dict[str, Any]` |
| `get_episode_profile` | 通过 ID 获取特定的单期节目格式配置。 | `profile_id: str` | `dict[str, Any]` |
| `create_episode_profile` | 创建新的单期节目格式配置。 | `name: str`, `description: Optional[str]`, `speaker_config: Optional[str]`, `outline_llm: Optional[str]`, `transcript_llm: Optional[str]`, `language: Optional[str]`, `default_briefing: Optional[str]`, `num_segments: Optional[int]`, `max_tokens: Optional[int]`, `outline_provider: Optional[str]`, `outline_model: Optional[str]`, `transcript_provider: Optional[str]`, `transcript_model: Optional[str]` | `dict[str, Any]` |
| `update_episode_profile` | 更新现有的单期节目格式配置。 | `profile_id: str`, `name: Optional[str]`, `description: Optional[str]`, `speaker_config: Optional[str]`, `outline_llm: Optional[str]`, `transcript_llm: Optional[str]`, `language: Optional[str]`, `default_briefing: Optional[str]`, `num_segments: Optional[int]`, `max_tokens: Optional[int]`, `outline_provider: Optional[str]`, `outline_model: Optional[str]`, `transcript_provider: Optional[str]`, `transcript_model: Optional[str]` | `dict[str, Any]` |
| `delete_episode_profile` | 删除特定的单期节目格式配置。 | `profile_id: str` | `dict[str, Any]` |

## 凭据管理

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `list_credentials` | 获取所有已保存的凭据列表。 | `provider: Optional[str]` | `dict[str, Any]` |
| `test_credential` | 测试特定凭据的 API 连通性。 | `credential_id: str` | `dict[str, Any]` |

## 向量重构

| 工具名称 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| `rebuild_embeddings` | 触发特定笔记本内所有内容源的向量化重新构建任务。 | `notebook_id: str` | `dict[str, Any]` |

