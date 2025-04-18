from adkgc import start_chat_webhook_server
from google.genai import types as genai_types
from typing import Callable, List
from google.adk.agents import LlmAgent 

from dotenv import load_dotenv

import os

load_dotenv()

def lookup_order_status(order_id: str) -> dict:
  """Fetches the current status of a customer's order using its ID.

  Use this tool ONLY when a user explicitly asks for the status of
  a specific order and provides the order ID. Do not use it for
  general inquiries.

  Args:
      order_id: The unique identifier of the order to look up.

  Returns:
      A dictionary containing the order status.
      Possible statuses: 'shipped', 'processing', 'pending', 'error'.
      Example success: {'status': 'shipped', 'tracking_number': '1Z9...'}
      Example error: {'status': 'error', 'error_message': 'Order ID not found.'}
  """
  # ... function implementation to fetch status ...
  return {"status": 'processing', "tracking_number": '12312fw'} # Example structure


def generat_client(user_name, space_name, send_google_chat_message):
    # --- Example Agent using Gemma 2B running via Ollama ---
    return LlmAgent(
        # LiteLLM knows how to connect to a local Ollama server by default
        # model=LiteLlm(model="ollama/llama3.3"), # Standard LiteLLM format for Ollama
        model="gemini-2.5-pro-preview-03-25",
        name="ollama_gemma_agent",
        instruction="You are Gemma, running locally via Ollama. You are assistent that doing conversation with user but also can provide status of the order. ",
        tools=[lookup_order_status, send_google_chat_message]
        # ... other agent parameters
    )


# --- Example Usage (Placeholder - Adapt your agent generation) ---
if __name__ == '__main__':
    # --- Configuration ---
    # IMPORTANT: Set these environment variables or replace with your actual values
    ALLOWED_SPACES = os.environ.get("ALLOWED_SPACE_IDS", "").split(",") # Comma-separated list e.g., "spaces/AAA123,spaces/BBB456"
    # Filter out empty strings if the env var is empty
    ALLOWED_SPACES = [space_id for space_id in ALLOWED_SPACES if space_id]
    APP_NAME = "MyHttpChatBot"
    LISTEN_PORT = int(os.environ.get("PORT", 8080)) # Use PORT env var common for cloud platforms

    start_chat_webhook_server(
        allowed_space_ids=ALLOWED_SPACES,
        generate_agent_fn=generat_client, # Pass your actual agent generator
        app_name=APP_NAME,
        port=LISTEN_PORT,
        # bot_debug=BOT_DEBUG_MODE # You might want separate debug flags
    )

    # Note: The 'debug' parameter in start_chat_webhook_server now controls Flask's debug mode.
    # The 'debug' parameter passed to GoogleChatBotViaHttp controls the bot's internal print statements.
    # You might want to rename or pass both if needed. For simplicity, using one flag here.
