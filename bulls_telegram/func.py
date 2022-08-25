import random

def check_duplicates(num: int) -> bool:         # проверяем на повторяющиеся значения: True, если повторов нет
    some_number = get_list(num)                 
    return len(some_number) == len(set(some_number))

def get_list(num: int) -> list:                 # превращаем число в список
    return[int(i) for i in str(num)]

def generate_num() -> int:     
    while True:
        num = random.randint(1000,9999)          # генерируем 4значное число
        if check_duplicates(num):               # если повторяющихся значений нет, оставляем его
            return num

def bulls_and_cows(num: int, guess: int):
    bull_cow = [0,0]
    num_list = get_list(num)
    guess_list = get_list(guess)
    for i, j in zip(num_list, guess_list):
        if j in num_list:
            if j == i:
                bull_cow[0] += 1
            else: 
                bull_cow[1] += 1
    return bull_cow
