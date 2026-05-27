 * Setup

```bash
uv python install 3.10        # Install Python 3.10
uv init --python 3.10         # Initialize project with Python 3.10
source .venv/bin/activate      # Activate virtual environment
uv add fastmcp                 # Add fastmcp dependency
uv sync                        # Sync dependencies
```

* Instrument client and server WITHOUT MCP host

```bash
# start the server
uv run my_server.py
fastmcp run my_server.py:mcp

# start the client
uv run my_client.py
```

* Without an MCP host, creating the client

```mermaid
sequenceDiagram
    participant Client as my_client.py
    participant Server as my_server.py (FastMCP)

    Client->>Server: spawn subprocess (stdio)
    Client->>Server: call_tool("greet", {"name": "Alex"})
    Server-->>Client: "Hello custom message, Alex!"
    Client->>Server: close connection
```

* With VS Code as MCP Host

```mermaid
sequenceDiagram
    participant User
    participant VSCode as VS Code (Copilot)
    participant Server as my_server.py (FastMCP)

    VSCode->>Server: spawn subprocess via .vscode/mcp.json (stdio)
    User->>VSCode: ask Copilot to use greet tool
    VSCode->>Server: call_tool("greet", {"name": "..."})
    Server-->>VSCode: "Hello custom message, ...!"
    VSCode-->>User: display result
```

---

### MCP vs FastMCP


* MCP is the official Python SDK

```bash
pip install mcp[cli]
# install the core library + the mcp CLI
uv add "mcp[cli]"

# launch server
mcp run <server_name.py>

# launch inspector
mcp dev <server_name.py>

# install a server
mcp install
``` 
* FastMCP is a high-level Python framework built on the of MCP SKD

```bash
uv add fastmcp
```
```python
from fastmcp import FastMCP
mcp = FastMCP("MyMCP")
```
```bash
# launch server
fastmcp run my_server.py:mcp

# launch inspector
fastmcp dev inspector my_server.py --host <host> --port <port>
``` 
