import os
from dotenv import load_dotenv
from random import randint
from telegram import Bot, Update
from telegram.ext import Updater, CallbackContext, CommandHandler

load_dotenv()
TOKEN = os.environ.get('TOKEN')
print(f'TOKEN = {TOKEN}')

def verify_token() -> None:
    bot = Bot(token=TOKEN)
    try:
        print(f'Verified token | Bot details: {bot.get_me()}')
    except:
        print('Failed to verify token')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to 解密专家!\n' +
                              'Use /play to start a game.')

def play(update: Update, context: CallbackContext) -> None:
    game_in_progress = False
    if 'game_in_progress' in context.chat_data:
        game_in_progress = context.chat_data['game_in_progress']
    if game_in_progress:
        update.message.reply_text('Please finish the current game first.')
    else:
        secret_number = randint(0, 93300)
        context.chat_data['secret_number'] = secret_number
        context.chat_data['game_in_progress'] = True
        update.message.reply_text('A secret number between 0 and 93300 ' +
                                  '(both inclusive) has been randomly set.\n' +
                                  'Use "/guess [number]" to make your guess.')

def guess(update: Update, context: CallbackContext) -> None:
    game_in_progress = context.chat_data['game_in_progress']
    if not game_in_progress:
        update.message.reply_text('No game in progress. Use "/play" to ' +
                                  'start a game.')
    else:
        args = context.args
        if len(args) == 0:
            update.message.reply_text('No number registered. Use "/guess ' +
                                      '[number]" to make your guess.')
        else:
            try:
                guess = int(args[0])
                secret_number = context.chat_data['secret_number']
                if guess == secret_number:
                    context.chat_data['game_in_progress'] = False
                    update.message.reply_text('Congrats! The secret number ' +
                                             f'is {secret_number}.')
                elif guess < 0 or guess > 93300:
                    update.message.reply_text('Your guess exceeded the ' +
                                              'possible range of 0 to 93300.')
                elif guess > secret_number:
                    update.message.reply_text('Too high')
                elif guess < secret_number:
                    update.message.reply_text('Too low')
                else:
                    update.message.reply_text('Unknown error occurred. ' +
                                              'Please try again.')
            except ValueError:
                update.message.reply_text('No number registered. Use "/guess ' +
                                        '[number]" to make your guess')

def main() -> None:
    verify_token()

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('play', play))
    dispatcher.add_handler(CommandHandler('guess', guess))

    print('Starting bot...')

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
