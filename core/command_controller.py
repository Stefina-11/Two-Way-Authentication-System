def execute_command(command: str) -> str:
    command = command.lower()
    if "open tab" in command:
        return "Opening a new tab"
    elif "close tab" in command:
        return "Closing the current tab"
    else:
        return "Unknown command"
