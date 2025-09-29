import telebot
import json
from datetime import datetime, timedelta
from _config import API_TOKEN, ALLOWED_USERS
import time



NAME = 'SalaryBudgetBot'
VER = '29092025'

bot = telebot.TeleBot(API_TOKEN)

DATA_FILE = "finance.json"


# ---- Helpers ----
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"balance": 0, "history": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def days_until_next_salary(today=None):
    today = today or datetime.now().date()
    year, month, day = today.year, today.month, today.day

    salary_days = [13, 28]
    for sd in salary_days:
        if day < sd:
            return (datetime(year, month, sd).date() - today).days

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    next_salary_date = datetime(next_year, next_month, 13).date()
    return (next_salary_date - today).days

def get_daily_budget(balance):
    days = days_until_next_salary()
    if days <= 0:
        return balance
    return round(balance / days, 2)


# ---- Decorator ----
def restricted(func):
    def wrapper(message, *args, **kwargs):
        if not is_allowed(message.from_user.id):
            bot.reply_to(message, "⛔ You are not allowed to use this bot.")
            return
        return func(message, *args, **kwargs)
    return wrapper


# ---- Commands ----
@bot.message_handler(commands=["start"])
@restricted
def start(message):
    bot.reply_to(message, "Welcome! Use /income, /spend, /balance to manage your money.")


@bot.message_handler(commands=["income"])
@restricted
def income(message):
    msg = bot.reply_to(message, "💰 How much income do you want to add?")
    bot.register_next_step_handler(msg, process_income)


def process_income(message):
    try:
        amount = float(message.text)
    except:
        bot.reply_to(message, "❌ Please enter a valid number.")
        return

    data = load_data()
    data["balance"] += amount
    data["history"].append({"type": "income", "amount": amount, "date": str(datetime.now())})
    save_data(data)

    bot.reply_to(message, f"✅ Income added: {amount}\nNew balance: {data['balance']}")


@bot.message_handler(commands=["spend"])
@restricted
def spend(message):
    msg = bot.reply_to(message, "🛒 How much did you spend?")
    bot.register_next_step_handler(msg, process_spend)


def process_spend(message):
    try:
        amount = float(message.text)
    except:
        bot.reply_to(message, "❌ Please enter a valid number.")
        return

    data = load_data()
    data["balance"] -= amount
    data["history"].append({"type": "spend", "amount": amount, "date": str(datetime.now())})
    save_data(data)

    bot.reply_to(message, f"✅ Spending added: {amount}\nNew balance: {data['balance']}")


@bot.message_handler(commands=["balance"])
@restricted
def balance(message):
    data = load_data()
    bal = data["balance"]
    daily = get_daily_budget(bal)
    days = days_until_next_salary()

    bot.reply_to(message, (
        f"💰 Balance: {bal}\n"
        f"📅 Days until salary: {days}\n"
        f"💵 Daily budget: {daily}"
    ))


@bot.message_handler(commands=["history"])
@restricted
def history(message):
    data = load_data()
    if not data["history"]:
        bot.reply_to(message, "📜 History is empty.")
        return

    lines = []
    for item in data["history"][-10:]:
        lines.append(f"{item['date'][:10]} - {item['type'].upper()}: {item['amount']}")
    bot.reply_to(message, "\n".join(lines))


# ---- Run ----
print(f"Bot {NAME} {VER} is running...")


while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"⚠️ Polling error: {e}")
        time.sleep(5)  # wait before retry