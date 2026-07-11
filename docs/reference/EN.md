# Open Notebook MCP Tool Reference

[English] | [日本語](JA.md) | [简体中文](ZH.md)

This document is the official tool reference documenting all 44 tools provided by the `onb-mcp` server, including their parameters, return types, and descriptions.

## Meta Tools

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `search_capabilities` | Search tools exposed by this server with progressive detail levels. | `query: str`, `detail: Literal['name','summary','full']`, `limit: int` | `dict[str, Any]` |

## Notebooks Management

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `list_notebooks` | Get all notebooks with optional filtering and ordering. | `archived: Optional[bool]`, `order_by: str`, `limit: int` | `dict[str, Any]` |
| `get_notebook` | Get a specific notebook by ID. | `notebook_id: str` | `dict[str, Any]` |
| `create_notebook` | Create a new notebook. | `name: str`, `description: Optional[str]` | `dict[str, Any]` |
| `update_notebook` | Update a notebook. | `notebook_id: str`, `name: Optional[str]`, `description: Optional[str]`, `archived: Optional[bool]` | `dict[str, Any]` |
| `delete_notebook` | Delete a notebook. | `notebook_id: str` | `dict[str, Any]` |

## Sources Management

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `list_sources` | Get all sources with optional filtering. | `notebook_id: Optional[str]`, `limit: int`, `offset: int` | `dict[str, Any]` |
| `get_source` | Get a specific source by ID. | `source_id: str` | `dict[str, Any]` |
| `create_source` | Create a new source (link, upload, or text). | `notebook_id: str`, `type: str`, `url: Optional[str]`, `title: Optional[str]`, `embed: bool` | `dict[str, Any]` |
| `update_source` | Update a source. | `source_id: str`, `title: Optional[str]`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `delete_source` | Delete a source. | `source_id: str` | `dict[str, Any]` |

## Notes Management

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `list_notes` | Get all notes with optional filtering. | `notebook_id: Optional[str]`, `limit: int`, `offset: int` | `dict[str, Any]` |
| `get_note` | Get a specific note by ID. | `note_id: str` | `dict[str, Any]` |
| `create_note` | Create a new note. | `notebook_id: str`, `title: str`, `content: str`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `update_note` | Update a note. | `note_id: str`, `title: Optional[str]`, `content: Optional[str]`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `delete_note` | Delete a note. | `note_id: str` | `dict[str, Any]` |

## Search & AI Assistant

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `search` | Search content using vector or text search. | `query: str`, `type: str`, `notebook_id: Optional[str]`, `limit: int` | `dict[str, Any]` |
| `ask_question` | Ask a question about your content with detailed control. | `question: str`, `strategy_model: str`, `answer_model: str`, `final_answer_model: str` | `dict[str, Any]` |
| `ask_simple` | Ask a question about your content with simplified interface. | `question: str`, `strategy_model: str`, `answer_model: str`, `final_answer_model: str` | `dict[str, Any]` |

## AI Models Configuration

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `list_models` | Get all configured AI models. | `limit: int` | `dict[str, Any]` |
| `get_model` | Get a specific model by ID. | `model_id: str` | `dict[str, Any]` |
| `create_model` | Create a new AI model configuration. | `name: str`, `provider: str`, `type: str` | `dict[str, Any]` |
| `delete_model` | Delete a model configuration. | `model_id: str` | `dict[str, Any]` |
| `get_default_models` | Get default model configurations. | `None` | `dict[str, Any]` |
| `discover_models` | Discover available models from a specific credential provider. | `credential_id: str` | `dict[str, Any]` |
| `register_models` | Register discovered models for use in the system. | `credential_id: str` | `dict[str, Any]` |

## Chat Sessions Management

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `list_chat_sessions` | Get all chat sessions with optional filtering. | `notebook_id: Optional[str]`, `limit: int` | `dict[str, Any]` |
| `create_chat_session` | Create a new chat session. | `notebook_id: str`, `title: str` | `dict[str, Any]` |
| `get_chat_session` | Get a specific chat session by ID. | `session_id: str` | `dict[str, Any]` |
| `update_chat_session` | Update a chat session. | `session_id: str`, `title: Optional[str]` | `dict[str, Any]` |
| `delete_chat_session` | Delete a chat session. | `session_id: str` | `dict[str, Any]` |
| `execute_chat` | Send a message in a chat session. | `session_id: str`, `message: str`, `context: Optional[dict]` | `dict[str, Any]` |
| `get_chat_context` | Build context for a chat conversation. | `notebook_id: str`, `context_config: Optional[dict]` | `dict[str, Any]` |

## Application Settings

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `get_settings` | Get application settings. | `None` | `dict[str, Any]` |
| `update_settings` | Update application settings. | `settings: dict` | `dict[str, Any]` |

## AI Transformations (AI Actions)

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `list_transformations` | List all custom transformation prompts. | `None` | `dict[str, Any]` |
| `create_transformation` | Create a new custom transformation prompt template. | `name: str`, `prompt: str`, `description: Optional[str]` | `dict[str, Any]` |
| `apply_transformation` | Apply a transformation prompt template to a source to extract insights. | `source_id: str`, `transformation_id: str` | `dict[str, Any]` |

## Podcast Audio Generation

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `generate_podcast` | Generate a new podcast episode asynchronously from selected sources. | `notebook_id: str`, `episode_name: str`, `episode_profile: str`, `speaker_profile: str`, `content: Optional[str]`, `briefing_suffix: Optional[str]` | `dict[str, Any]` |
| `retry_podcast` | Retry a failed podcast episode generation job. | `episode_id: str` | `dict[str, Any]` |
| `get_podcast_job_status` | Get the status of an asynchronous podcast generation job. | `job_id: str` | `dict[str, Any]` |

## Credential Providers Management

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `list_credentials` | List all stored credentials. | `provider: Optional[str]` | `dict[str, Any]` |
| `test_credential` | Test connection for a specific provider credential. | `credential_id: str` | `dict[str, Any]` |

## Embeddings Rebuild

| Tool Name | Description | Arguments | Return Type |
| --- | --- | --- | --- |
| `rebuild_embeddings` | Trigger a background job to rebuild the document vector embeddings. | `notebook_id: str` | `dict[str, Any]` |

