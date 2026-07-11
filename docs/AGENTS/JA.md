# onb-mcp Agent Constitution (生存ガイド)

本ファイルは、本リポジトリで作業する AI エージェントのための、本質的かつ最小限の設計指針および開発ルールです。

## 1. 最重要ルール（生存ガイド）
1. **コンテキスト効率の死守**: 巨大なデータを直接返さず、サマリー ＋ ID（またはファイルパス）を返却すること。フィルタリング等は必ずサーバー（Python）側で実行してください。
2. **標準の機能検出 (`search_capabilities`)**: AIがツール仕様を段階的に取得（ディスカバリー）できるよう、`search_capabilities` ツールに新たなツール定義を追加し続けてください。
3. **標準出力（stdout）へのロギング禁止**: STDIO トランスポートが破壊されるため、絶対に `print()` やデバッグログを標準出力に流さないでください。ログはすべて `logging` で標準エラー出力（stderr）に出力してください。
4. **タイムアウトの明示**: すべての外部 I/O 処理には明示的なタイムアウトを設定してください。

## 2. プロジェクト構造と役割
- `src/onb_mcp/config.py`: 定数および環境変数ヘルパー
- `src/onb_mcp/mcp_app.py`: FastMCP インスタンス (`mcp`)
- `src/onb_mcp/client.py`: HTTP通信用ヘルパー (`make_request`)
- `src/onb_mcp/capabilities.py`: ツールメタデータ定義 (`CAPABILITIES` タプル)
- `src/onb_mcp/tools.py`: 全ての `@mcp.tool()` 実装（新規ツールはここに実装）
- `src/onb_mcp/server.py`: 各モジュールを読み込み、テスト互換用にシンボルを再エクスポートするエントリーポイント

## 3. ツール追加時の開発フロー
1. **メタデータ更新**: `capabilities.py` の `CAPABILITIES` タプルに新しいツールの定義を必ず追記します。
2. **ツール実装**: `tools.py` に `@mcp.tool()` デコレータ付きで関数を実装します。
3. **テスト追加**: `tests/test_capabilities.py` に動作検証および返却データの契約テストを追加します。
4. **検証**: `uv run pytest` を実行し、すべてのテストがパスすることを確認します。
