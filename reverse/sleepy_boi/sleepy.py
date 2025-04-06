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