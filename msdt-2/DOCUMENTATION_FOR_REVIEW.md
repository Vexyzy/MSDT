# Documentation for review

## LINTERS

* Статические анализаторы

1. Используем linter [ruff](https://docs.astral.sh/ruff/linter/ "Официальная документация линтера ruff")
2. Конфиг для ruff:

```toml
[project]
requires-python = ">=3.9"

[tool.ruff]
line-length = 79
src = ["src"]

# rooles: https://docs.astral.sh/ruff/rules/
select = [
  "E", # pycodestyle
  "F", # pyflakes
  "UP", # pyupgrade
  "N", # pep8-naming
  "ERA", # found commented-out code
]
```

---

## План ревью (конвенции):
### Готовим файл для чтения:
* Прогоняем по статическим анализаторам;
* Проверка по [PEP8](https://peps.python.org/pep-0008/ "Официальная документация PEP8");
### Проверяем код
* Анализируем нужен ли вообще этот код;
* Проверяем алгоритмы / подходы / архитектуру
* После проверки алгоритмов проверяем в правильном ли месте расположен код
* Проверяем используются ли подходящие структуры данных
* Проверяем правильность именования пакетов/классов/фукнций (методов)/переменных

---

## Используемые материалы:
* Пиши код хорошо)) [Стив Маконнелл. Совершенный код](https://vk.com/doc159808884_629166854?hash=Zsz14B4aKrEC9A9JhIo0fShNn35xFkPjAJEVA9kMFzc&dl=ICjzP9ZjY9hgYeenrzDV8mXzrRfze4pF6vFfxvZgzRP, "Открой, тут классно");

