# Trama Caribe 🤖

A friendly Slack bot that ensures teammates greet each other properly after periods of inactivity. If someone returns after 4 hours of silence and forgets to say hello, the bot steps in with an enthusiastic, elaborate greeting!

## Features

- 🕐 **Inactivity Detection**: Tracks when users haven't sent messages for 4+ hours
- 👋 **Greeting Recognition**: Detects common salutations in Catalan, Spanish, and English
- 💬 **Automated Responses**: Sends friendly, elaborate greetings when salutations are missed
- 🔧 **Configurable**: Customize inactivity threshold and salutation list
- 🌐 **Multi-channel Support**: Works in channels and direct messages

## How It Works

1. The bot monitors all messages in channels where it's invited
2. It tracks the last message timestamp for each user in each channel
3. When a user sends a message after 4 hours of inactivity:
   - If the message starts with a greeting (e.g., "hola", "bon dia", "ei") → No action
   - If the message has no greeting → Bot responds with an elaborate greeting

## Setup

### Prerequisites

- Python 3.7 or higher
- A Slack workspace where you have permission to install apps
- Slack App with the following configurations (see [Creating a Slack App](#creating-a-slack-app))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/trevSmart/trama-caribe.git
   cd trama-caribe
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Slack tokens:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token-here
   SLACK_APP_TOKEN=xapp-your-app-token-here
   INACTIVITY_HOURS=4
   ```

4. **Run the bot:**
   ```bash
   python bot.py
   ```

The bot will start and begin monitoring messages!

## Creating a Slack App

### Step 1: Create the App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Name your app (e.g., "Trama Caribe") and select your workspace
5. Click **"Create App"**

### Step 2: Enable Socket Mode

1. In your app settings, go to **"Socket Mode"** in the sidebar
2. Enable Socket Mode
3. Generate an app-level token with `connections:write` scope
4. Save this token as your `SLACK_APP_TOKEN`

### Step 3: Configure Bot Token Scopes

1. Go to **"OAuth & Permissions"** in the sidebar
2. Under **"Scopes"** → **"Bot Token Scopes"**, add:
   - `app_mentions:read` - View messages that directly mention @your_bot
   - `chat:write` - Send messages as the bot
   - `channels:history` - View messages in public channels
   - `groups:history` - View messages in private channels
   - `im:history` - View messages in direct messages
   - `mpim:history` - View messages in group direct messages

### Step 4: Install App to Workspace

1. Scroll to **"OAuth Tokens for Your Workspace"**
2. Click **"Install to Workspace"**
3. Authorize the app
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)
5. Save this as your `SLACK_BOT_TOKEN`

### Step 5: Enable Event Subscriptions

1. Go to **"Event Subscriptions"** in the sidebar
2. Turn on **"Enable Events"**
3. Under **"Subscribe to bot events"**, add:
   - `message.channels` - Listen to messages in public channels
   - `message.groups` - Listen to messages in private channels
   - `message.im` - Listen to direct messages
   - `message.mpim` - Listen to group direct messages
   - `app_mention` - Listen when the app is mentioned
4. Click **"Save Changes"**

### Step 6: Invite Bot to Channels

In Slack, invite the bot to channels:
```
/invite @trama-caribe
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token (required) | - |
| `SLACK_APP_TOKEN` | App-Level Token (required) | - |
| `INACTIVITY_HOURS` | Hours of inactivity before triggering | 4 |

### Customizing Salutations

Edit the `SALUTATIONS` set in `bot.py` to add or remove acceptable greetings:

```python
SALUTATIONS: Set[str] = {
    "hola", "bon dia", "bones", "ei", "hey", "hello",
    # Add your custom greetings here
}
```

### Customizing Responses

Edit the `GREETING_RESPONSES` list in `bot.py` to customize the bot's greetings:

```python
GREETING_RESPONSES = [
    "Hola! Què tal? Com estàs? I com et va la tarda?",
    # Add your custom responses here
]
```

## Examples

### Scenario 1: User Returns and Forgets to Greet

```
[Last message from Alice: 09:00]
[Current time: 14:30 - 5.5 hours later]

Alice: Can someone review my PR?
Bot: Hola! Què tal? Com estàs? I com et va la tarda?
```

### Scenario 2: User Returns with Proper Greeting

```
[Last message from Bob: 09:00]
[Current time: 14:30 - 5.5 hours later]

Bob: Hola! Can someone review my PR?
[Bot stays silent - greeting detected]
```

### Scenario 3: User Sends Messages Frequently

```
[Last message from Carol: 14:00]
[Current time: 14:15 - 15 minutes later]

Carol: Quick question...
[Bot stays silent - less than 4 hours]
```

## Deployment

### Running on a Server

For production deployment, consider using a process manager like `systemd` or `supervisor`:

**Example systemd service file** (`/etc/systemd/system/trama-caribe.service`):

```ini
[Unit]
Description=Trama Caribe Slack Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/trama-caribe
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable trama-caribe
sudo systemctl start trama-caribe
sudo systemctl status trama-caribe
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t trama-caribe .
docker run --env-file .env trama-caribe
```

## Troubleshooting

### Bot doesn't respond to messages

1. **Check bot is invited to channel**: `/invite @trama-caribe`
2. **Verify event subscriptions**: Ensure `message.channels`, `message.groups`, etc. are enabled
3. **Check bot scopes**: Verify all required OAuth scopes are granted
4. **Review logs**: Check console output for errors

### Bot responds to its own messages

The bot filters out messages with `bot_id` or `subtype` fields. If issues persist, check the event filtering logic.

### Missing environment variables

```
ValueError: SLACK_BOT_TOKEN environment variable is required
```

Ensure your `.env` file exists and contains the required tokens.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Slack Bolt for Python](https://slack.dev/bolt-python/)
- Inspired by the need for friendly team communication 💙