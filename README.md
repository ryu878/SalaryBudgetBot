# SalaryBudgetBot
A personal finance Telegram bot built with pyTelegramBotAPI . It helps you track income, spending, and daily budgets between your paydays.

---
✨ Features

💰 Add income (/income <amount>)

🛒 Track spending (/spend <amount>)

📊 Check balance, days until next salary, and daily allowance (/balance)

📜 View last 10 transactions (/history)

🗓 Salary dates automatically set to 13th and 28th of each month

💾 Stores data persistently in a JSON file


---
📖 Example Usage

```
/income 100000
/spend 10000
/balance
/history
```

---
⚙️ Installation

1. Clone the repo:
   ```
   git clone https://github.com/ryu878/SalaryBudgetBot.git
   cd SalaryBudgetBot
   ```
2. Install dependencies:

   ```
   pip install pytelegrambotapi
   ```

3. Create a Telegram bot with BotFatherand get the API token.
4. Replace YOUR_BOT_TOKEN in bot.py with your token.
5. Run the bot:
  ```
python bot.py
```
