import random
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Logging for debugging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to generate a random Bangladeshi number
def generate_number(operator_code):
    endnum = random.randint(10000000, 99999999)
    return f"01{operator_code}{endnum}"

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the *Number Generator Bot*! 🎉\n\n"
        "Send /generate to generate random Bangladeshi mobile numbers.",
        parse_mode="Markdown"
    )

# Generate numbers based on user input
def generate(update: Update, context: CallbackContext) -> None:
    operators = {
        "1": ("Grameenphone", "7"),
        "2": ("Robi", "8"),
        "3": ("Airtel", "6"),
        "4": ("Banglalink", "9"),
        "5": ("Teletalk", "5"),
        "6": ("All Operators", None)
    }

    msg = "*Choose your operator:*\n"
    for key, value in operators.items():
        msg += f"{key}. {value[0]} ({value[1] if value[1] else 'All'})\n"

    msg += "\n_Reply with the operator number and amount in this format:_\n`1 5` (for 5 Grameenphone numbers)"
    
    update.message.reply_text(msg, parse_mode="Markdown")

# Handle user input for operator and amount
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.split()
    
    if len(user_input) != 2 or not user_input[0].isdigit() or not user_input[1].isdigit():
        update.message.reply_text("*Invalid format!* Use: `1 5` (operator number, amount)", parse_mode="Markdown")
        return

    operator_choice, amount = user_input
    amount = int(amount)

    operators = {
        "1": ("Grameenphone", "7"),
        "2": ("Robi", "8"),
        "3": ("Airtel", "6"),
        "4": ("Banglalink", "9"),
        "5": ("Teletalk", "5"),
        "6": ("All Operators", None)
    }

    if operator_choice not in operators or amount <= 0:
        update.message.reply_text("*Invalid operator or amount!* Please try again.", parse_mode="Markdown")
        return

    operator_name, operator_code = operators[operator_choice]
    result_msg = f"*Generating {amount} numbers for {operator_name}:*\n"

    if operator_choice == "6":
        for _ in range(amount):
            op_name, op_code = random.choice(list(operators.values())[:-1])
            result_msg += f"{op_name}: {generate_number(op_code)}\n"
    else:
        for _ in range(amount):
            result_msg += generate_number(operator_code) + "\n"

    update.message.reply_text(result_msg, parse_mode="Markdown")

# Main function to run the bot
def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot token from BotFather

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
