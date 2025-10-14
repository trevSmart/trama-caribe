"""
Trama Caribe - Slack Greeting Bot

A Slack bot that detects when teammates send messages without proper salutations
after prolonged inactivity and responds with friendly, elaborate greetings.
"""

import os
import re
import time
from datetime import datetime, timedelta
from typing import Dict, Set
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Slack app will be initialized in main() to avoid import-time issues
app = None

# Configuration
INACTIVITY_HOURS = int(os.environ.get("INACTIVITY_HOURS", 4))
INACTIVITY_SECONDS = INACTIVITY_HOURS * 3600

# List of acceptable salutations (case-insensitive)
SALUTATIONS: Set[str] = {
    "hola", "bon dia", "bones", "ei", "hey", "hello",
    "hi", "bon vespre", "bona nit", "bona tarda",
    "què tal", "què hi ha", "com va", "com estàs",
    "com estas", "buenos días", "buenas", "buenas tardes",
    "buenas noches", "qué tal", "holi"
}

# Elaborate greeting responses
GREETING_RESPONSES = [
    "Hola! Què tal? Com estàs? I com et va la tarda?",
    "Ei! Bon dia! Espero que tinguis un dia fantàstic! Com va tot?",
    "Hola! Quant de temps! Com estàs? Què tal et va?",
    "Bon dia! Que tinguis un dia meravellós! Com et va tot?",
    "Ei! Hola! Fa temps que no et sentia! Com estàs? Tot bé?"
]

# Track user activity: {(user_id, channel_id): timestamp}
user_last_message: Dict[tuple, float] = {}


def has_greeting(text: str) -> bool:
    """
    Check if the message contains a proper salutation.

    Args:
        text: The message text to check

    Returns:
        True if the message contains a salutation, False otherwise
    """
    if not text:
        return False

    # Normalize text for comparison
    text_lower = text.lower().strip()

    # Check if any salutation appears at the beginning of the message
    for salutation in SALUTATIONS:
        # Check if salutation is at the start of the message (with word boundary)
        pattern = r'^\s*' + re.escape(salutation) + r'\b'
        if re.search(pattern, text_lower):
            return True

    return False


def should_respond(user_id: str, channel_id: str, current_time: float) -> bool:
    """
    Determine if the bot should respond based on user inactivity.

    Args:
        user_id: The Slack user ID
        channel_id: The Slack channel ID
        current_time: Current timestamp

    Returns:
        True if user has been inactive for more than INACTIVITY_HOURS, False otherwise
    """
    key = (user_id, channel_id)

    if key not in user_last_message:
        # First message from user in this channel - no response needed
        return False

    last_message_time = user_last_message[key]
    time_diff = current_time - last_message_time

    return time_diff >= INACTIVITY_SECONDS


def handle_message(event, say, logger):
    """
    Handle incoming messages and respond if necessary.

    Args:
        event: The Slack event data
        say: Function to send a message to the channel
        logger: Logger instance
    """
    try:
        # Skip bot messages and message subtypes (edits, deletes, etc.)
        if event.get("subtype") or event.get("bot_id"):
            return

        user_id = event.get("user")
        channel_id = event.get("channel")
        text = event.get("text", "")
        current_time = float(event.get("ts", time.time()))

        if not user_id or not channel_id:
            return

        key = (user_id, channel_id)

        # Check if user has been inactive and didn't greet
        if should_respond(user_id, channel_id, current_time) and not has_greeting(text):
            # Respond with an elaborate greeting
            import random
            greeting = random.choice(GREETING_RESPONSES)
            say(greeting)
            logger.info(f"Sent greeting to user {user_id} in channel {channel_id}")

        # Update the last message timestamp for this user in this channel
        user_last_message[key] = current_time

    except Exception as e:
        logger.error(f"Error handling message: {e}")


def handle_app_mention(event, say, logger):
    """
    Handle app mentions (optional - responds when bot is mentioned).

    Args:
        event: The Slack event data
        say: Function to send a message to the channel
        logger: Logger instance
    """
    try:
        say("Hola! Estic aquí per assegurar-me que tothom es saluda correctament! 👋")
    except Exception as e:
        logger.error(f"Error handling app mention: {e}")


def main():
    """
    Main entry point for the bot.
    """
    from slack_bolt import App
    from slack_bolt.adapter.flask import SlackRequestHandler
    from flask import Flask, request

    global app

    # Check for required environment variables
    if not os.environ.get("SLACK_BOT_TOKEN"):
        raise ValueError("SLACK_BOT_TOKEN environment variable is required")

    if not os.environ.get("SLACK_SIGNING_SECRET"):
        raise ValueError("SLACK_SIGNING_SECRET environment variable is required")

    # Initialize the Slack app
    app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )

    # Register event handlers
    @app.event("message")
    def handle_message_wrapper(event, say, logger):
        handle_message(event, say, logger)

    @app.event("app_mention")
    def handle_app_mention_wrapper(event, say, logger):
        handle_app_mention(event, say, logger)

    # Initialize Flask app
    flask_app = Flask(__name__)
    handler = SlackRequestHandler(app)

    @flask_app.route("/slack/events", methods=["POST"])
    def slack_events():
        return handler.handle(request)

    @flask_app.route("/slack/interactive", methods=["POST"])
    def slack_interactive():
        return handler.handle(request)

    print(f"🤖 Trama Caribe bot starting...")
    print(f"⏰ Inactivity threshold: {INACTIVITY_HOURS} hours")
    print(f"👋 Monitoring for missing greetings...")
    print(f"🌐 Webhook server ready!")

    # Start the Flask server
    flask_app.run(host="0.0.0.0", port=3000, debug=True)


if __name__ == "__main__":
    main()
