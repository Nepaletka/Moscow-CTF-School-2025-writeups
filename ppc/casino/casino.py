'''
PPC Casino

Основная идея выйгрыша в игре заключается в том,
чтобы продержатся 1000 раздач в блекджеке.

Код в начале игры делает ставку на весь баланс,
в случае проигрыша игра наинается заново,
в случае выйгрыша - следущяя ставка изменяется на 1.

Таким образом с 200 монет код играет 1000 раундов,
код берет карту если сумма его карт меньше 11,
что исключает проигрыш от перебора карт.

Также тут реализован подсчет и перевод карт дилера,
который на практике оказался не нужен.
'''
from pwn import *
import re
from time import sleep

conn = remote('casino.tasks.2025.ctf.cs.msu.ru', 25051)


def d(dealer):
    if 'дилера' in dealer:
        return 'blackj'
    elif 'K' in dealer or 'J' in dealer or 'Q' in dealer:
        return 10
    elif "A" in dealer:
        return 1
    else:
        return int(dealer)


def main(conn):
    for num, i in enumerate(range(5000)):
        response = conn.recv().decode('utf-8')
        print(num)
        if "MSKCTF" in response:
            print(response)
            break
        elif 'Ваш начальный баланс' in response:
            conn.sendline(bytes('100', 'utf-8'))
            continue
        elif "Новый баланс: 0" in response:
                conn.close()
                print('WASTED')
                sleep(.1)
                main(remote('casino.tasks.2025.ctf.cs.msu.ru', 25051))

        elif 'Ничья' in response:
            conn.sendline(bytes('1', 'utf-8'))
            continue

        elif "выигрыш" in response or "Вы выйграли" in response:
            sleep(.1)
            conn.sendline(bytes('2', 'utf-8'))
            conn.sendline(bytes('1', 'utf-8'))
            continue
        elif 'Вы проиграли' in response or 'Дилер имеет блэкджек!' in response:
            conn.sendline(bytes('1', 'utf-8'))
            continue

        elif 'Дилер показывает туза!' in response:
            conn.sendline(bytes('нет', 'utf-8'))
            continue
        else:
            conn.sendline(bytes('1', 'utf-8'))

        try:
            dealer = d(response.split('\n')[-3].split(' ')[2].replace('♠', '').replace('♣', '').replace('♦', '').replace('♥', '').replace(',', ''))
            my_cards = int(response.split('\n')[-2].split(' ')[-1])
            print(my_cards, dealer)
        except ValueError:
            continue


        if my_cards < 11:
            conn.sendline(bytes('hit', 'utf-8'))
        else:
            conn.sendline(bytes('stand', 'utf-8'))


if __name__ == '__main__':
    main(conn)

