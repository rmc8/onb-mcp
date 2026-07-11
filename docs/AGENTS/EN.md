# onb-mcp Agent Constitution (Survival Guide)

This file specifies the essential, minimal design guidelines and development rules for AI agents working in this repository.

## 1. Prime Directives (Survival Rules)
1. **Context Efficiency above All**: Do not return huge chunks of raw data directly. Return a summary + ID (or file path). Filtering and transformations must be performed in the execution environment (Python server-side).
2. **Standardized Tool Discovery (`search_capabilities`)**: To allow the AI to retrieve tool specifications incrementally, always keep the tool definitions up-to-date in the `CAPABILITIES` index.
3. **Never Log to stdout**: For STDIO transport, stdout is reserved for protocol frames. Writing debug logs or `print()` statements to stdout will crash the server. Always write logs to stderr using `logging`.
4. **Explicit Timeouts**: Set explicit, reasonable timeouts for all outbound API/network I/O requests.

## 2. Project Structure & Roles
- `src/onb_mcp/config.py`: Configuration constants and environment variable helpers.
- `src/onb_mcp/mcp_app.py`: FastMCP application instance (`mcp`).
- `src/onb_mcp/client.py`: Common HTTP communication helper (`make_request`).
- `src/onb_mcp/capabilities.py`: Main aggregate list of tool metadata (`CAPABILITIES` tuple).
- `src/onb_mcp/tools/`: Submodules containing all `@mcp.tool()` implementations grouped by functional domain.
- `src/onb_mcp/server.py`: Server entrypoint that loads all submodules and re-exports symbols for test compatibility.

## 3. Development Workflow for Adding Tools
1. **Update Metadata**: Append the new tool specification to the `CAPABILITIES` sub-tuple in the corresponding domain module.
2. **Implement Tool**: Write the tool function with `@mcp.tool()` decorator under the appropriate module in `src/onb_mcp/tools/`.
3. **Add Tests**: Write contract/verification tests in `tests/test_capabilities.py` to assert the shape of the return data.
4. **Verify**: Run `uv run pytest` and ensure all tests pass successfully.
