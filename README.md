# Crypto Trading Bot

## Overview
The Crypto Trading Bot is an application designed to automate trading operations based on messages received from a Telegram group. It parses trading-related messages, stores relevant data in a PostgreSQL database, and interacts with MEXC and Kraken exchanges to manage trading positions.

## Features
- Collects and parses crypto trading messages from a Telegram group.
- Stores parsed data in a PostgreSQL database.
- Opens, monitors, and closes trading positions on MEXC and Kraken exchanges using their APIs.
- Validates message formats to ensure data integrity.

## Project Structure
```
crypto-trading-bot
├── src
│   ├── main.ts                # Entry point of the application
│   ├── telegram
│   │   ├── client.ts          # Manages Telegram API connection
│   │   └── handlers.ts        # Handles incoming Telegram messages
│   ├── parser
│   │   ├── messageParser.ts    # Parses trading messages
│   │   └── validators.ts       # Validates parsed message data
│   ├── database
│   │   ├── connection.ts       # Database connection setup
│   │   ├── migrations.ts       # Handles database migrations
│   │   └── queries.ts          # Executes database queries
│   ├── exchanges
│   │   ├── mexc.ts            # Interacts with MEXC exchange API
│   │   ├── kraken.ts          # Interacts with Kraken exchange API
│   │   └── baseExchange.ts     # Defines common interface for exchanges
│   ├── trading
│   │   ├── positionManager.ts  # Manages active trading positions
│   │   ├── monitor.ts          # Monitors open positions
│   │   └── executor.ts         # Executes trades based on messages
│   ├── config
│   │   └── index.ts           # Configuration settings
│   └── types
│       └── index.ts           # TypeScript interfaces and types
├── .env.example                # Example environment variables
├── package.json                # npm configuration file
├── tsconfig.json              # TypeScript configuration file
└── README.md                   # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd crypto-trading-bot
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in the required values.

## Usage
1. Start the application:
   ```
   npm run start
   ```

2. The bot will connect to the specified Telegram group and begin processing messages.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.