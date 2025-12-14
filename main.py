# import random
# from fastmcp import FastMCP  # type: ignore

# mcp = FastMCP(name="Demo Server")

# @mcp.tool
# def roll_dice(n_dice: int = 1) -> list[int]:
#     """Roll n_dice 6-sided dice and return the results."""
#     return [random.randint(1, 6) for _ in range(n_dice)]

# @mcp.tool
# def add_numbers(a: float, b: float) -> float:
#     """Add two numbers together."""
#     return a + b

# @mcp.tool
# def multiply_numbers(a:float,b:float)->float:
#     """Multiply two numbers together."""
#     return a*b


# if __name__ == "__main__":
#     mcp.run()

import random
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from fastmcp import FastMCP  # type: ignore

mcp = FastMCP(name="Demo Server")


# @mcp.tool
# def roll_dice(n_dice: int = 1) -> list[int]:
#     """Roll n_dice 6-sided dice and return the results."""
#     return [random.randint(1, 6) for _ in range(n_dice)]


# @mcp.tool
# def add_numbers(a: float, b: float) -> float:
#     """Add two numbers together."""
#     return a + b


# @mcp.tool
# def multiply_numbers(a: float, b: float) -> float:
#     """Multiply two numbers together."""
#     return a * b


# Storage file for reminders
REMINDERS_FILE = Path.home() / ".mcp_reminders.json"


def load_reminders() -> dict:
    """Load reminders from JSON file"""
    if not REMINDERS_FILE.exists():
        return {}
    
    try:
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_reminders(reminders: dict) -> None:
    """Save reminders to JSON file"""
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)


def parse_time(time_str: str) -> datetime:
    """
    Parse various time formats into a datetime object
    Supports:
    - Relative: "in 30 minutes", "in 2 hours", "in 1 day"
    - Absolute: "2024-12-15 14:00", "2024-12-15T14:00:00"
    """
    time_str = time_str.strip().lower()
    
    # Handle relative time (in X minutes/hours/days)
    relative_pattern = r'in (\d+)\s*(minute|minutes|min|hour|hours|hr|day|days)'
    match = re.match(relative_pattern, time_str)
    
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        
        now = datetime.now()
        
        if unit.startswith('min'):
            return now + timedelta(minutes=amount)
        elif unit.startswith('hour') or unit.startswith('hr'):
            return now + timedelta(hours=amount)
        elif unit.startswith('day'):
            return now + timedelta(days=amount)
    
    # Handle absolute time formats
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse time format: {time_str}")



@mcp.tool
def create_reminder(message: str, time: str) -> str:
    """
    Create a new reminder with a message and time.
    Time can be relative (e.g., 'in 30 minutes', 'in 2 hours') 
    or absolute (e.g., '2024-12-15 14:00').
    """
    try:
        reminder_time = parse_time(time)
    except ValueError as e:
        return f"Error: {str(e)}"
    
    # Generate a unique ID
    reminders = load_reminders()
    reminder_id = f"reminder_{len(reminders) + 1}_{int(datetime.now().timestamp())}"
    
    # Create reminder
    reminder = {
        "id": reminder_id,
        "message": message,
        "time": reminder_time.isoformat(),
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    
    reminders[reminder_id] = reminder
    save_reminders(reminders)
    
    return (f"Reminder created successfully!\n"
            f"ID: {reminder_id}\n"
            f"Message: {message}\n"
            f"Due: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")


@mcp.tool
def list_reminders(status: str = "pending") -> str:
    """
    List all reminders, optionally filtered by status.
    Status can be: 'pending', 'completed', or 'all'.
    """
    reminders = load_reminders()
    
    if not reminders:
        return "No reminders found."
    
    # Filter by status
    filtered = []
    for r in reminders.values():
        if status == "all" or r["status"] == status:
            filtered.append(r)
    
    if not filtered:
        return f"No {status} reminders found."
    
    # Sort by time
    filtered.sort(key=lambda x: x["time"])
    
    output = [f"{'='*60}"]
    output.append(f"Total {status} reminders: {len(filtered)}")
    output.append(f"{'='*60}\n")
    
    for r in filtered:
        reminder_time = datetime.fromisoformat(r["time"])
        now = datetime.now()
        
        if r["status"] == "pending":
            if reminder_time <= now:
                status_emoji = "OVERDUE"
            else:
                time_left = reminder_time - now
                hours = int(time_left.total_seconds() / 3600)
                minutes = int((time_left.total_seconds() % 3600) / 60)
                status_emoji = f"Due in {hours}h {minutes}m"
        else:
            status_emoji = "Completed"
        
        output.append(f"ID: {r['id']}")
        output.append(f"Message: {r['message']}")
        output.append(f"Due: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Status: {status_emoji}")
        output.append(f"{'-'*60}\n")
    
    return "\n".join(output)


@mcp.tool
def get_due_reminders() -> str:
    """Get all reminders that are currently due or overdue."""
    reminders = load_reminders()
    now = datetime.now()
    
    due = []
    for r in reminders.values():
        if r["status"] == "pending":
            reminder_time = datetime.fromisoformat(r["time"])
            if reminder_time <= now:
                due.append(r)
    
    if not due:
        return "No reminders are currently due."
    
    output = [f"{'='*60}"]
    output.append(f"{len(due)} reminder(s) are DUE!")
    output.append(f"{'='*60}\n")
    
    for r in due:
        reminder_time = datetime.fromisoformat(r["time"])
        time_ago = now - reminder_time
        hours_ago = int(time_ago.total_seconds() / 3600)
        minutes_ago = int((time_ago.total_seconds() % 3600) / 60)
        
        output.append(f"ID: {r['id']}")
        output.append(f"Message: {r['message']}")
        output.append(f"Was due: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Overdue by: {hours_ago}h {minutes_ago}m")
        output.append(f"{'-'*60}\n")
    
    return "\n".join(output)


@mcp.tool
def complete_reminder(reminder_id: str) -> str:
    """Mark a reminder as completed."""
    reminders = load_reminders()
    
    if reminder_id not in reminders:
        return f"Error: Reminder '{reminder_id}' not found."
    
    reminders[reminder_id]["status"] = "completed"
    reminders[reminder_id]["completed_at"] = datetime.now().isoformat()
    save_reminders(reminders)
    
    return f"Reminder '{reminder_id}' marked as completed!"


@mcp.tool
def delete_reminder(reminder_id: str) -> str:
    """Delete a reminder permanently."""
    reminders = load_reminders()
    
    if reminder_id not in reminders:
        return f"Error: Reminder '{reminder_id}' not found."
    
    deleted = reminders.pop(reminder_id)
    save_reminders(reminders)
    
    return (f"Reminder deleted successfully!\n"
            f"Message: {deleted['message']}")


if __name__ == "__main__":
    mcp.run()