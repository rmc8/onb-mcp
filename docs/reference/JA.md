# Open Notebook MCP ツールリファレンス

[日本語] | [English](EN.md) | [简体中文](ZH.md)

本ドキュメントは、`onb-mcp` サーバーが提供するすべてのツール（全44種）の引数、戻り値の型、および説明をまとめた公式リファレンスです。

## メタツール

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `search_capabilities` | サーバーが公開しているツールを段階的な詳細レベルで検索・探索します。 | `query: str`, `detail: Literal['name','summary','full']`, `limit: int` | `dict[str, Any]` |

## ノートブック管理

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `list_notebooks` | フィルタリングとソート順を指定して、すべてのノートブックを取得します。 | `archived: Optional[bool]`, `order_by: str`, `limit: int` | `dict[str, Any]` |
| `get_notebook` | 指定されたIDのノートブックを取得します。 | `notebook_id: str` | `dict[str, Any]` |
| `create_notebook` | 新しいノートブックを作成します。 | `name: str`, `description: Optional[str]` | `dict[str, Any]` |
| `update_notebook` | ノートブックの名称、説明、またはアーカイブ状態を更新します。 | `notebook_id: str`, `name: Optional[str]`, `description: Optional[str]`, `archived: Optional[bool]` | `dict[str, Any]` |
| `delete_notebook` | ノートブックを削除します。 | `notebook_id: str` | `dict[str, Any]` |

## コンテンツソース管理

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `list_sources` | ノートブック内のすべてのコンテンツソースをフィルタリング指定して取得します。 | `notebook_id: Optional[str]`, `limit: int`, `offset: int` | `dict[str, Any]` |
| `get_source` | 指定されたIDのソースを取得します。 | `source_id: str` | `dict[str, Any]` |
| `create_source` | 新しいソース（リンク、ファイルアップロード、または直接テキスト）を作成します（ベクトル化オプションあり）。 | `notebook_id: str`, `type: str`, `url: Optional[str]`, `title: Optional[str]`, `embed: bool` | `dict[str, Any]` |
| `update_source` | ソースのタイトルやタグトピックを更新します。 | `source_id: str`, `title: Optional[str]`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `delete_source` | ソースを削除します。 | `source_id: str` | `dict[str, Any]` |

## ノート管理

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `list_notes` | すべてのノートをフィルタリング指定して取得します。 | `notebook_id: Optional[str]`, `limit: int`, `offset: int` | `dict[str, Any]` |
| `get_note` | 指定されたIDのノートを取得します。 | `note_id: str` | `dict[str, Any]` |
| `create_note` | 新しいノートを作成します。 | `notebook_id: str`, `title: str`, `content: str`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `update_note` | ノートのタイトル、本文、またはトピックを更新します。 | `note_id: str`, `title: Optional[str]`, `content: Optional[str]`, `topics: Optional[list[str]]` | `dict[str, Any]` |
| `delete_note` | ノートを削除します。 | `note_id: str` | `dict[str, Any]` |

## 検索とAIアシスタント

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `search` | ベクトル検索または全文テキスト検索を使用してコンテンツを検索します。 | `query: str`, `type: str`, `notebook_id: Optional[str]`, `limit: int` | `dict[str, Any]` |
| `ask_question` | 複数のAIモデルと推論戦略を指定して、コンテンツに関する質問を詳しく行います。 | `question: str`, `strategy_model: str`, `answer_model: str`, `final_answer_model: str` | `dict[str, Any]` |
| `ask_simple` | コンテンツに対するシンプルな質問応答（ask）インターフェースです。 | `question: str`, `strategy_model: str`, `answer_model: str`, `final_answer_model: str` | `dict[str, Any]` |

## AIモデル設定

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `list_models` | システムに構成されているすべてのAIモデル一覧を取得します。 | `limit: int` | `dict[str, Any]` |
| `get_model` | 指定されたIDのAIモデル設定を取得します。 | `model_id: str` | `dict[str, Any]` |
| `create_model` | 新しいAIモデルの構成を追加します。 | `name: str`, `provider: str`, `type: str` | `dict[str, Any]` |
| `delete_model` | AIモデル構成を削除します。 | `model_id: str` | `dict[str, Any]` |
| `get_default_models` | システムのデフォルトのAIモデル構成（LLM、TTS等）を取得します。 | `なし` | `dict[str, Any]` |
| `discover_models` | 指定のプロバイダー（API）から、利用可能なAIモデルを動的に探索・取得します。 | `credential_id: str` | `dict[str, Any]` |
| `register_models` | 探索されたAIモデルをシステムに登録し、使用可能にします。 | `credential_id: str` | `dict[str, Any]` |

## チャットセッション管理

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `list_chat_sessions` | チャットセッション一覧を取得します。 | `notebook_id: Optional[str]`, `limit: int` | `dict[str, Any]` |
| `create_chat_session` | 新しいチャットセッションを作成します。 | `notebook_id: str`, `title: str` | `dict[str, Any]` |
| `get_chat_session` | 指定されたIDのチャット履歴と詳細を取得します。 | `session_id: str` | `dict[str, Any]` |
| `update_chat_session` | チャットセッションのタイトルを更新します。 | `session_id: str`, `title: Optional[str]` | `dict[str, Any]` |
| `delete_chat_session` | チャットセッションを削除します。 | `session_id: str` | `dict[str, Any]` |
| `execute_chat` | チャットセッションにメッセージを送信し、AIの返答を生成します。 | `session_id: str`, `message: str`, `context: Optional[dict]` | `dict[str, Any]` |
| `get_chat_context` | チャットで使用するためのコンテキスト（関連情報ソース）を構築します。 | `notebook_id: str`, `context_config: Optional[dict]` | `dict[str, Any]` |

## アプリケーション設定

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `get_settings` | アプリケーションの基本システム設定を取得します。 | `なし` | `dict[str, Any]` |
| `update_settings` | アプリケーションの基本システム設定を更新します。 | `settings: dict` | `dict[str, Any]` |

## AIデータ変換 (AI Actions)

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `list_transformations` | すべてのカスタムデータ変換（AIアクション）用プロンプトテンプレートを一覧取得します。 | `なし` | `dict[str, Any]` |
| `create_transformation` | 新しいカスタムデータ変換（AIアクション）用プロンプトテンプレートを作成します。 | `name: str`, `prompt: str`, `description: Optional[str]` | `dict[str, Any]` |
| `apply_transformation` | コンテンツソースに対して指定のデータ変換テンプレートを適用し、要約やインサイト抽出を行います。 | `source_id: str`, `transformation_id: str` | `dict[str, Any]` |

## ポッドキャスト音声生成

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `generate_podcast` | 選択されたソース群から、対談音声（ポッドキャスト）の生成ジョブを非同期で開始します。 | `notebook_id: str`, `episode_name: str`, `episode_profile: str`, `speaker_profile: str`, `content: Optional[str]`, `briefing_suffix: Optional[str]` | `dict[str, Any]` |
| `retry_podcast` | 失敗したポッドキャスト生成ジョブを再試行します。 | `episode_id: str` | `dict[str, Any]` |
| `get_podcast_job_status` | 非同期で進行しているポッドキャスト生成ジョブの進捗とステータスを取得します。 | `job_id: str` | `dict[str, Any]` |

## プロバイダー認証情報管理

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `list_credentials` | データベースに保存されているすべてのプロバイダー認証設定の一覧を取得します。 | `provider: Optional[str]` | `dict[str, Any]` |
| `test_credential` | 指定されたプロバイダー認証設定のAPI接続テスト（疎通確認）を実行します。 | `credential_id: str` | `dict[str, Any]` |

## ベクトル埋め込み再構築

| ツール名 | 説明 | 引数 | 戻り値 |
| --- | --- | --- | --- |
| `rebuild_embeddings` | 指定ノートブック内の全ソースのベクトル埋め込み（インデックス）再構築ジョブを非同期で開始します。 | `notebook_id: str` | `dict[str, Any]` |

