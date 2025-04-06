from elftools.elf.elffile import ELFFile
from PIL import Image
import numpy as np

elf_file_path = 'flagg'

with open(elf_file_path, 'rb') as f:
    elf = ELFFile(f)
    section = elf.get_section_by_name('.data')
    
    if section:
        data_bytes = section.data()
        print(f"Извлечено {len(data_bytes)} байт из секции .data")
        width, height = 1190, 58
        expected_size = width * height * 3
        
        if len(data_bytes) >= expected_size:
            rgb_data = data_bytes[:expected_size]
    
            img_array = np.frombuffer(rgb_data, dtype=np.uint8).reshape((height, width, 3))
            
            img = Image.fromarray(img_array, mode='RGB')
            img.save('output_rgb.png')
            print("RGB-изображение сохранено как output_rgb.png")
        else:
            print("Недостаточно данных для заданных размеров")
    else:
        print("Секция .data не найдена")