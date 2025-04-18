from adkgc import start_chat_webhook_server
from google.genai import types as genai_types
from typing import Callable, List
from google.adk.agents import LlmAgent 

import os


# --- Example Usage (Placeholder - Adapt your agent generation) ---
if __name__ == '__main__':
    # This is a placeholder. Replace with your actual agent generation logic.
    def my_agent_generator(user_name: str, space_name: str, send_google_chat_message: Callable) -> LlmAgent:
        # Example: Create a simple echo agent
        class EchoAgent(LlmAgent):
            def process(self, user_id: str, session_id: str, message: genai_types.Content) -> List[genai_types.Content]:
                input_text = message.parts[0].text if message and message.parts else "Empty message"
                print(f"EchoAgent processing in space {space_name} for user {user_name}: {input_text}")
                # Use the provided tool to send the response
                tool_result = send_google_chat_message(f"You said: {input_text}")
                print(f"Send tool result: {tool_result}")
                # Agent framework might expect a specific return format.
                # ADK's LlmAgent often expects content back, even if handled by tool.
                # Returning an empty list or a confirmation might be needed.
                # Let's assume the tool handles the final output and we just signal completion.
                return [] # Or potentially Content confirming action

        print(f"Generating agent for user {user_name} in space {space_name}")
        return EchoAgent() # Return an instance of your agent

    # --- Configuration ---
    # IMPORTANT: Set these environment variables or replace with your actual values
    ALLOWED_SPACES = os.environ.get("ALLOWED_SPACE_IDS", "").split(",") # Comma-separated list e.g., "spaces/AAA123,spaces/BBB456"
    # Filter out empty strings if the env var is empty
    ALLOWED_SPACES = [space_id for space_id in ALLOWED_SPACES if space_id]
    APP_NAME = "MyHttpChatBot"
    LISTEN_PORT = int(os.environ.get("PORT", 8080)) # Use PORT env var common for cloud platforms

    start_chat_webhook_server(
        allowed_space_ids=ALLOWED_SPACES,
        generate_agent_fn=my_agent_generator, # Pass your actual agent generator
        app_name=APP_NAME,
        port=LISTEN_PORT,
        # bot_debug=BOT_DEBUG_MODE # You might want separate debug flags
    )

    # Note: The 'debug' parameter in start_chat_webhook_server now controls Flask's debug mode.
    # The 'debug' parameter passed to GoogleChatBotViaHttp controls the bot's internal print statements.
    # You might want to rename or pass both if needed. For simplicity, using one flag here.
