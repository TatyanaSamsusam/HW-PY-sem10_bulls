
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import os
from func import *
from config import TOKEN


token = TOKEN
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

guess = None
player, move = 0, 1
player_name = None

print('bot is working')

def start (update, context):
    global num, count
    num = generate_num()
    count = 1
    print (num)

    context.bot.send_message(update.effective_chat.id, 
                            f'Привет! сыграем в Быки и Коровы?\n'
                            f'Компьютер загадает четырехзначное число из цифр, к-е не повторяются, а ты должен его угадать\n' 
                            f'Введи число с таким же кол-вом символов. Если цифры твоего числа есть в загаданном - это корова\n'
                            f'Если есть совпадение и по позиции символа - это бык'
                            )
    context.bot.send_message(update.effective_chat.id, "Меня зовут Иа, а тебя?")
    return player

def get_name(update, context):
    global player_name, count
    player_name = update.message.text
    context.bot.send_message(update.effective_chat.id, 'Игра началась! У тебя есть 10 попыток. Введи число')
    context.bot.send_message(update.effective_chat.id, f'Попытка {count}...')
    return move

def take_move(update, context):
    global guess, count
    try:
        guess = int(update.message.text)
    except:
        context.bot.send_message(update.effective_chat.id, f'Введи число')
        return move
    if not check_duplicates(guess):
        context.bot.send_message(update.effective_chat.id, 'В загаданном числе цифры не повторяются')
        return move
    if guess < 1000 or guess > 9999:
        context.bot.send_message(update.effective_chat.id, 'Введи четырехзначное число!')
        return move
    count += 1
    bull_cow = bulls_and_cows(num, guess)
    if bull_cow[0] == 4:
        context.bot.send_message(update.effective_chat.id, f'Ты молодец! Отгадал число {num} за {count} попыток!')
        return ConversationHandler.END
    if count <= 10:
        context.bot.send_message(update.effective_chat.id,f'Быков - {bull_cow[0]} / коров - {bull_cow[1]}')
        context.bot.send_message(update.effective_chat.id,f'Попытка {count}')
        return move
    else: 
        context.bot.send_message(update.effective_chat.id,f'Увы, {player_name}, ты потратил свои {count-1} попыток, и проиграл...')
        return ConversationHandler.END

def exit(update, context):
    context.bot.send_message(update.effective_chat.id,'GAME OVER')
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states = {
        player: [MessageHandler(Filters.text, get_name)],
        move: [MessageHandler(Filters.text, take_move)]
    },
    fallbacks=[CommandHandler('exit', exit)]
)

dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()
print('Bot is off')
