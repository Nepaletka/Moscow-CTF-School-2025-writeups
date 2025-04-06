# libgastral

Проанализировав достаточно небольшой код мы понимаем, что программа берёт информацию о картинке из секции .data и по пиксельно рисует её на экране.
```
if ( (unsigned int)gastral_init(argc, argv, envp) )
  errx(1, "gastral_init() failed");
v3 = gastral_image_alloc();
v4 = v3;
if ( !v3 )
  errx(1, "gastral_image_alloc() failed");
if ( (unsigned int)gastral_image_set_data(v3, &unk_4040, 24LL, 1190LL, 58LL) )
  errx(1, "gastral_image_set_data() failed");
if ( (unsigned int)gastral_image_show(v4) )
  errx(1, "gastral_image_show() failed");
gastral_image_free(v4);
return 0;
```
---
Перепишем этот код на python, начнём с извлечения секции .data из файла
```
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

```
```
Извлечено 207076 байт из секции .data
```
---
Предполагаем, что размеры изображения 1190 на 58 исходя из кода задачи. Допишем скрипт для отрисовки нашего изображения в формате RGB
```
rgb_data = data_bytes[:expected_size]
img_array = np.frombuffer(rgb_data, dtype=np.uint8).reshape((height, width, 3))

img = Image.fromarray(img_array, mode='RGB')
img.save('output_rgb.png')
```
![](./output_rgb.png)
---
# Flag: MSKCTF{photoshop_or_gimp?_whatever_works}

