# 🛠️ MCP Server & Client Configuration Setup

This subdirectory contains the codebase and setup details for custom Model Context Protocol (MCP) servers and clients.

---

## ⚡ 1. Local MCP Server (`local-mcp`)

The local MCP server is built using the **FastMCP** framework in Python. It exposes core arithmetic and utility helper tools.

* **Server Script**: [`server.py`](./server.py)
* **Status**: Running and integrated locally.

### 📦 Installation & Dependencies
Ensure you have the virtual environment activated and the required package installed:
```bash
pip install fastmcp
```

### 🛠️ Exposed Tools & Resources
1. **`add_numbers(a, b)`**: Sums two given float numbers.
2. **`reverse_string(text)`**: Reverses the character order of the provided string.
3. **Resource `info://about`**: Provides information about the basic server.

---

## 🧭 2. Customized MCP Server (`mcp-ilaya`)

A second isolated server designed to provide specific custom details about Ilaya.
* **Server Script Location**: `d:\mcp_test\mcp\server1.py`
* **Exposed Tool**: `ilaya_details(a, b)` which returns the profile details:
  > *ilaya is data engineer working in EPAM, he is from Chennai, he is 27 years old*

---

## ⚙️ 3. Client Integration (`mcp_config.json`)

To enable Claude/Gemini Desktop or other clients to discover these servers, the following configurations are defined in your `mcp_config.json` configuration file:

```json
{
  "mcpServers": {
    "local-mcp": {
      "command": "d:\\my-projects\\.venv\\Scripts\\python.exe",
      "args": [
        "d:\\my-projects\\my-ai-agents\\my_mcp\\server.py"
      ]
    },
    "mcp-ilaya": {
      "command": "d:\\mcp_test\\.venv\\Scripts\\python.exe",
      "args": [
        "d:\\mcp_test\\mcp\\server1.py"
      ]
    }
  }
}
```
