# Open Notebook MCP サーバー (onb-mcp)

[日本語] | [English](../../README.md) | [简体中文](ZH.md)

<!-- mcp-name: io.github.Epochal-dev/open-notebook -->

[Open Notebook](https://github.com/lfnovo/open-notebook) API と対話するためのツールを提供する MCP (Model Context Protocol) サーバーです。このサーバーにより、Claude などの AI アシスタントが Open Notebook を通じてノートブック、ソース、ノートの管理、コンテンツ検索、AIモデルの呼び出しを行えるようになります。

## 主な機能

- **ノートブック管理 (Notebooks)**: ノートブックの作成、取得、更新、削除
- **ソース管理 (Sources)**: コンテンツソース (リンク、アップロード、テキスト) の追加と管理
- **ノート管理 (Notes)**: ノートブック内でのノートの作成と整理
- **検索とAI (Search & AI)**: ベクトル検索・テキスト検索によるコンテンツ検索および質問応答
- **モデル管理 (Models)**: AIモデル設定の構成と管理
- **チャットセッション (Chat Sessions)**: チャット会話の作成と管理
- **設定 (Settings)**: アプリケーション設定の取得と更新
- **段階的開示 (Progressive Disclosure)**: `search_capabilities` を用いた効率的なツール探索

## クイックスタート (uvx 推奨)

本パッケージは PyPI に公開されているため、手動でクローンやインストールを行う必要はありません。**`uvx`**（`uv` のツールランナー）を使用して、すぐに実行できます。

```bash
# MCPサーバーを即座に実行
uvx onb-mcp
```

### Claude Desktop での利用

Claude Desktop の設定ファイル（macOS の場合は `~/Library/Application Support/Claude/claude_desktop_config.json`、Windows の場合は `%APPDATA%\Claude\claude_desktop_config.json`）に以下を追記します。

```json
{
  "mcpServers": {
    "open-notebook": {
      "command": "uvx",
      "args": [
        "onb-mcp"
      ],
      "env": {
        "OPEN_NOTEBOOK_URL": "http://localhost:5055",
        "OPEN_NOTEBOOK_PASSWORD": "your_password_here"
      }
    }
  }
}
```

## 設定方法

サーバーを Open Notebook インスタンスに接続するための構成が必要です。

### 環境変数

MCP クライアント（Claude Desktop など）の設定ファイル内で、以下の環境変数を設定してください。

```bash
# 必須: Open Notebook インスタンスのURL
OPEN_NOTEBOOK_URL=http://localhost:5055

# 任意: 認証パスワード (Open Notebook 側で APP_PASSWORD が設定されている場合)
OPEN_NOTEBOOK_PASSWORD=your_password_here

# 任意: 通信トランスポート (デフォルト: stdio)
MCP_TRANSPORT=stdio  # リモートデプロイの場合は streamable-http
```

## ソースからのインストールと開発方法

コードの変更や、ローカルソースからの実行を行う場合:

### クローンと同期

```bash
# リポジトリをクローン
git clone https://github.com/rmc8/onb-mcp.git
cd onb-mcp

# 依存関係の同期
uv sync
```

### 開発用サーバーの起動

#### 開発モード (STDIO)

AI アシスタントからソースコードを直接指定してローカルで起動する場合:

```bash
uv run onb-mcp
```

#### 本番モード (Streamable HTTP)

リモートデプロイ用:

```bash
MCP_TRANSPORT=streamable-http HOST=0.0.0.0 PORT=8000 uv run onb-mcp
```

### ツール探索 (段階的開示)

本サーバーはコンテキスト効率を高めるため「段階的開示 (Progressive Disclosure)」を実装しています。利用可能な機能は `search_capabilities` ツールを用いて検索できます。

```python
# すべてのツールの概要一覧を取得
search_capabilities(query="", detail="summary", limit=50)

# 特定のキーワードでツールを検索
search_capabilities(query="notebook", detail="summary", limit=10)

# 特定のツールの詳細な引数や戻り値の型、使用例を取得
search_capabilities(query="create_notebook", detail="full", limit=1)
```

---

## 提供ツール一覧

本サーバーは、以下のカテゴリに分かれた合計 50 個のツールを公開しています。詳細は `search_capabilities` ツールで確認できます。

- **メタツール**: `search_capabilities`
- **ノートブック (5個)**: `list_notebooks`, `get_notebook`, `create_notebook`, `update_notebook`, `delete_notebook`
- **ソース (5個)**: `list_sources`, `get_source`, `create_source`, `update_source`, `delete_source`
- **ノート (5個)**: `list_notes`, `get_note`, `create_note`, `update_note`, `delete_note`
- **検索・AI (3個)**: `search`, `ask_question`, `ask_simple`
- **モデル (5個)**: `list_models`, `get_model`, `create_model`, `delete_model`, `get_default_models`
- **チャット (7個)**: `list_chat_sessions`, `create_chat_session`, `get_chat_session`, `update_chat_session`, `delete_chat_session`, `execute_chat`, `get_chat_context`
- **設定 (2個)**: `get_settings`, `update_settings`
- **データ変換 (3個)**: `list_transformations`, `create_transformation`, `apply_transformation`
- **ポッドキャスト (3個)**: `generate_podcast`, `retry_podcast`, `get_podcast_job_status`
- **認証情報管理 (4個)**: `list_credentials`, `test_credential`, `discover_models`, `register_models`
- **ベクトル再構築 (1個)**: `rebuild_embeddings`

## プロジェクト構造

```
onb-mcp/
├── src/
│   └── onb_mcp/
│       ├── __init__.py
│       ├── config.py         # 設定・定数
│       ├── mcp_app.py        # FastMCP インスタンス
│       ├── client.py         # API クライアント共通処理
│       ├── capabilities.py   # ツールメタデータ集約
│       ├── server.py         # エントリーポイント
│       └── tools/            # 機能ドメイン別モジュール
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
├── tests/                    # pytest 契約テスト
├── pyproject.toml
├── README.md
└── AGENTS.md
```
