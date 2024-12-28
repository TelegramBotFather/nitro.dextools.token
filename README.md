# Hot Pairs Telegram Bot

A powerful Telegram bot that tracks and notifies users about hot new trading pairs across different blockchain networks using the Dextools API.

## Features

- 🔥 Real-time hot pairs tracking
- 📊 Multi-chain support (Solana, etc.)
- 👥 User management system
- 📢 Broadcast messaging
- 🔐 Admin controls
- 💬 Forum/Topic support
- ⚡ Async architecture

## Prerequisites

- Python 3.8+
- MongoDB database
- Telegram Bot Token
- Dextools API Key

## Environment Variables

Create a `config.env` file in the root directory:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
DATABASE_URL=your_mongodb_url
DATABASE_NAME=tg_bot
OWNER_ID=your_telegram_id
DEXTOOLS_API_KEY=your_dextools_api_key

# Optional
WEB_SERVER=False
DEBUG=False

# Main Chat Config
MAIN_CHAT_ID=your_chat_id
MAIN_CHAT_TOPIC_ID=your_topic_id
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/Ashrafmdmatin41/new.token.notification.channels
cd new.token.notification.channels
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the bot
```bash
python main.py
```

## Commands

### User Commands
- `/start` - Start the bot

### Admin Commands
- `/admin` - Show admin commands
- `/adduser` - Add authorized user
- `/auth_users` - List authorized users
- `/removeuser` - Remove authorized user
- `/users` - List all users
- `/user` - Get user details
- `/broadcast` - Send broadcast message

## Architecture

The bot is built with a modular architecture:

- `bot/` - Core bot functionality
  - `plugins/` - Command handlers
  - `utils/` - Helper functions
  - `config.py` - Configuration management
- `database/` - Database models and operations
## Features in Detail

### Hot Pairs Tracking
The bot monitors new trading pairs using the Dextools API and sends notifications based on configurable thresholds. It supports:

- Real-time pair monitoring
- Customizable time thresholds
- Multi-chain support
- Price impact tracking

### User Management
Comprehensive user management system with:

- User registration
- Ban/unban functionality
- Admin authorization levels
- User statistics

### Broadcasting
Advanced broadcasting system with:

- Rate limiting
- Progress tracking
- Delivery statistics
- Error handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Pyrogram](https://docs.pyrogram.org/) - MTProto API framework
- [Motor](https://motor.readthedocs.io/) - Async MongoDB driver
- [Dextools API](https://www.dextools.io/app/api) - Trading pair data
