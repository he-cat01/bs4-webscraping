# bs4-webscraping


Парсер сайта https://kolesa.kz

**Возможности:**

1) Парсер принимает ссылки по городам/по машинам формата:
https://kolesa.kz/cars/almaty/ https://kolesa.kz/cars/toyota/
2) Парсер собирает данные по объявлению: город/машина/цена/ссылка/номер телефона
3) Данные записываеются в формат csv
4) Поддержка pool multiprocces
5) Для каждого запроса уникальный User-Agent

### Запуск скрипта c без указания количества процессов (по стандарту 1 процесс на 1 ядро):
```
python scraping.py https://kolesa.kz/cars/almaty/
```
### С указанием количества процессов:
```
python scraping.py https://kolesa.kz/cars/almaty/ 10
```
