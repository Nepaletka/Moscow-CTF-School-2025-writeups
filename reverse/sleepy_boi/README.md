# sleepy_boi

Видим, что программа печатает флаг, но делает это очень долго. Смотрим в код и понимаем что задержки для функции sleep считаются по формуле чисел Фибоначчи.

```
v5 = tmp + v3;
v3 = tmp;
tmp = v5;
```
После каждого сна вычисляется общее время с начала выполнения программы, берется символ из DATA по индексу числа % 4096, и он выводится. Сумма всех чисел Фибоначчи до n считается по формуле S(n) = F(n+3) - 2

---
Напишем код который считает все индексы в массиве из которых собирается флаг
```
for n in range(1, 100):
    S_n = fibonacci(n + 3) - 2
    pos = S_n % 4096
    char = data_bytes[pos]
    print(pos)
```
```
1
3
6
11
19
32
53
87
142
231
...
```
---
Извлечём массив из .data и пройдёмся по нему с нашими  индексами
```
from elftools.elf.elffile import ELFFile
from PIL import Image
import numpy as np
elf_file_path = 'sleepy-boi'

with open(elf_file_path, 'rb') as f:
    elf = ELFFile(f)
    section = elf.get_section_by_name('.rodata')
    
    if section:
        data_bytes = section.data()
        print(f"Извлечено {len(data_bytes)} байт из секции .data")
        data_bytes = data_bytes[32:]
        data_bytes = data_bytes.decode()


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


flag = ""
for n in range(1, 100):
    S_n = fibonacci(n + 3) - 2
    pos = S_n % 4096
    char = data_bytes[pos]
    print(pos, data_bytes)
    flag += char
    if char == '}':
        break

print("Flag:", flag)
```
---
# Flag: MSKCTF{you just cheated time, didn't ya?}

