import socket
from itertools import product

def calc(pswd, secret):
    #Считаем совпадения
    return sum(g == s for g, s in zip(pswd, secret))

def solve_password(s):
    paroli = [''.join(p) for p in product('0123456789', repeat=4)]
    
    for i in range(1, 17):
        
        # Берём подходящий вариант
        pswd = paroli[0]  
        print(f"Попытка {i}: {pswd}")
        
        # Отправляем пароль серверу
        s.sendall(pswd.encode() + b'\n')
        
        # Получаем ответ сервера
        r = s.recv(1024).decode().strip()
        print(r)
        
        if "Wrong pass" in r:
            # Парсим ответ сервера
            try:
                matches = int(r.split(' ')[-8])
            except (IndexError, ValueError):
                return False
            
            #Отсеиваем неподходящие пароли
            paroli = [c for c in paroli if calc(pswd, c) == matches]
        
        elif "right" in r:
            print(f"Пароль угадан: {pswd}")
            return True

# Коннект
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('krzeworzech.tasks.2025.ctf.cs.msu.ru', 25069))

# Приветствие не надо
print(s.recv(1024).decode())

for i in range(1, 101):
    print(f"\n!!!!!!{i}")
    
    if not solve_password(s):
        break

s.close()
