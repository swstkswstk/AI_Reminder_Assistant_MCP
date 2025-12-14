# MCP Reminders Server

## Project Title
**AI-Powered Reminder Assistant using Model Context Protocol (MCP)**

---

## Project Description

### Problem Statement
In today's fast-paced world, managing tasks and reminders effectively is crucial for productivity. Traditional reminder apps require manual interaction and context-switching between applications. Users often forget to set reminders or find it cumbersome to open separate apps just to create a simple reminder.

### Objective
Build an intelligent reminder management system that integrates directly with AI assistants (like Claude) using the **Model Context Protocol (MCP)**. This allows users to create, manage, and track reminders through natural language conversation without leaving their AI chat interface.

### Methodology

1. **MCP Server Architecture**: Built a FastMCP server that exposes reminder management tools to AI clients
2. **Natural Language Time Parsing**: Implemented flexible time parsing supporting both relative ("in 30 minutes") and absolute ("2024-12-15 14:00") formats
3. **Persistent Storage**: Reminders are stored in a local JSON file for data persistence across sessions
4. **CRUD Operations**: Full Create, Read, Update, Delete functionality for reminder management

### Key Features

- **Create Reminders**: Set reminders with natural language time expressions
- **List Reminders**: View all pending, completed, or all reminders
- **Due Alerts**: Check which reminders are currently overdue
- **Complete Reminders**: Mark reminders as done
- **Delete Reminders**: Remove unwanted reminders permanently

### Scope of Solution

- **Integration**: Works with any MCP-compatible AI client (Claude Desktop, etc.)
- **Flexibility**: Supports multiple time input formats for user convenience
- **Scalability**: JSON-based storage can be extended to database backends
- **Extensibility**: FastMCP decorator pattern makes adding new tools trivial

### Technical Architecture

```
┌─────────────────┐     MCP Protocol     ┌──────────────────┐
│  Claude Desktop │ ◄──────────────────► │  MCP Server      │
│  (AI Client)    │      (stdio)         │  (FastMCP)       │
└─────────────────┘                      └────────┬─────────┘
                                                  │
                                                  ▼
                                         ┌──────────────────┐
                                         │ ~/.mcp_reminders │
                                         │     .json        │
                                         └──────────────────┘
```

---

## Frameworks & Tools

- **Python 3.10+** - Core programming language
- **FastMCP** - Model Context Protocol server framework
- **uv** - Fast Python package installer and runner
- **Claude Desktop** - AI client for MCP integration
- **JSON** - Data persistence format

---

## Snapshots

> *Add screenshots demonstrating:*
> 1. Creating a reminder through Claude conversation
> 2. Listing pending reminders
> 3. Checking due/overdue reminders
> 4. Completing a reminder

---

## Video Link

> *Host a demo video showing the reminder workflow on YouTube/Vimeo and paste link here*

---

## Presentation

> *Upload presentation file (.ppt, .pptx, .pdf) explaining the project*

---

## Demo Link

> *If hosted remotely, provide the demo URL here*

**Local Setup:**
```bash
# Install dependencies
uv run --with fastmcp fastmcp run main.py
```

---

## Project Source

### Repository Link
> *Add your GitHub/BitBucket repository URL here*

### How to Run

1. **Prerequisites**: Python 3.10+, uv package manager

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp
   ```

3. **Configure Claude Desktop**: Copy `claude_desktop_config.json` to Claude Desktop's config directory

4. **Run the server**:
   ```bash
   uv run --with fastmcp fastmcp run main.py
   ```

5. **Use in Claude**: Open Claude Desktop and start creating reminders!

---

## Usage Examples

### Creating a Reminder
```
User: "Remind me to submit the report in 2 hours"
Claude: Creates reminder using create_reminder tool
```

### Listing Reminders
```
User: "Show me all my pending reminders"
Claude: Uses list_reminders tool with status="pending"
```

### Checking Due Reminders
```
User: "Are any of my reminders overdue?"
Claude: Uses get_due_reminders tool
```

---

## Source Code

**Main Files:**
- `main.py` - MCP server with all reminder tools
- `claude_desktop_config.json` - Claude Desktop configuration
- `pyproject.toml` - Python project configuration

---

## Team

> *Add team member names here*

---

## License

MIT License
