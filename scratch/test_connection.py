import subprocess
import json
import sys
import os

def test_mcp():
    env = os.environ.copy()
    
    # Load .env file manually
    env_path = "/home/rmc8/Desktop/Dev/MCP/open-notebook-mcp/.env"
    if os.path.exists(env_path):
        print(f"Loading environment variables from {env_path}...")
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env[key.strip()] = val.strip()
    
    print("Starting MCP server process...")
    process = subprocess.Popen(
        ["uv", "run", "onb-mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/home/rmc8/Desktop/Dev/MCP/open-notebook-mcp",
        env=env,
        text=True,
        bufsize=1
    )

    # 1. Initialize Request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "TestClient",
                "version": "1.0.0"
            }
        }
    }

    try:
        print("Sending 'initialize' request...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()

        stdout_line = process.stdout.readline()
        response = json.loads(stdout_line)
        if "result" in response:
            print("✅ SUCCESS: Initialize handshake succeeded!")
        else:
            print(f"❌ FAILED: Initialize failed. Error: {response.get('error')}")
            return

        # 2. List Tools Request
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        process.stdin.write(json.dumps(list_tools_request) + "\n")
        process.stdin.flush()
        stdout_line = process.stdout.readline()
        response = json.loads(stdout_line)
        if "result" in response and "tools" in response["result"]:
            print(f"✅ SUCCESS: Retreived {len(response['result']['tools'])} tools!")
        else:
            print("❌ FAILED: Tools list failed.")
            return

        # 3. Call Tool Request (list_notebooks) to verify actual Open Notebook API connection
        call_tool_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "list_notebooks",
                "arguments": {
                    "limit": 5
                }
            }
        }
        
        print("\nSending 'tools/call' for 'list_notebooks' (testing actual API connection)...")
        process.stdin.write(json.dumps(call_tool_request) + "\n")
        process.stdin.flush()
        
        stdout_line = process.stdout.readline()
        print("\n--- Tool Call Response ---")
        print(stdout_line[:1000] + "... (truncated)" if len(stdout_line) > 1000 else stdout_line)
        
        response = json.loads(stdout_line)
        if "result" in response and "content" in response["result"]:
            content = response["result"]["content"]
            # FastMCP returns text block inside content list
            if content and len(content) > 0:
                text_val = content[0].get("text", "")
                try:
                    data = json.loads(text_val)
                    if "notebooks" in data:
                        print("✅ SUCCESS: Successfully fetched notebooks list from API!")
                        print(f"Notebooks count: {len(data['notebooks'])}")
                        print(f"Notebooks names: {[n.get('name') for n in data['notebooks']]}")
                    else:
                        print(f"❌ FAILED: API response format unexpected: {data}")
                except Exception as parse_err:
                    print(f"✅ SUCCESS: Tool returned response, but text wasn't JSON: {text_val[:300]}")
            else:
                print("❌ FAILED: Tool call returned empty content list.")
        else:
            print(f"❌ FAILED: Tool call error: {response.get('error') or response}")

    except Exception as e:
        print(f"\n❌ ERROR during test execution: {e}")
        stderr_output = process.stderr.read()
        if stderr_output:
            print("\n--- Stderr Output ---")
            print(stderr_output)
    finally:
        print("\nTerminating process...")
        process.terminate()

if __name__ == "__main__":
    test_mcp()
