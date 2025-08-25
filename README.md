# 🏠 FIAS Public API Python Client

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Not%20Published-red.svg)](https://pypi.org/project/fias-public-api/)

> 🚀 **Простой и удобный Python клиент для работы с публичным API ФИАС (Федеральная информационная адресная система) России**

## ✨ Возможности

| Функция               | Описание                                              | Статус |
| --------------------- | ----------------------------------------------------- | ------ |
| 🔍 **Поиск адресов**  | Поиск по текстовой строке с поддержкой русского языка | ✅     |
| 📋 **Детали объекта** | Получение полной информации об объекте адресации      | ✅     |
| 🔐 **Токен**      | Автоматическое получение токена аутентификации        | ✅     |

## 🚀 Быстрый старт

### Минимальный пример

```python
from fias_public_api import FiasPublicApi, get_token

# Получаем токен автоматически
token = get_token()

# Создаем клиент
api = FiasPublicApi(token)

# Ищем адрес
results = api.search("Москва, Красная площадь")
print(f"Найдено: {len(results)} результатов")

# Получаем детали первого результата
if results:
    details = api.details(results[0]['id'])
    print(f"Адрес: {details.get('address', 'N/A')}")
```

## 📦 Установка

```bash
pip install https://github.com/invoxy/fias-public-api

```

```bash
pip install fias-public-api
```

### Зависимости

| Пакет      | Версия     | Описание                         |
| ---------- | ---------- | -------------------------------- |
| `requests` | `>=2.32.5` | HTTP библиотека для API запросов |

## 🔧 Использование

### Основные сценарии

#### 1. Поиск адресов

```python
# Простой поиск
results = api.search("Москва")

# Поиск с кастомным URL
results = api.search("Санкт-Петербург", custom_url="https://custom-fias.ru/api")

# Обработка результатов
for result in results:
    print(f"ID: {result['id']}")
    print(f"Адрес: {result['address']}")
    print(f"Тип: {result['type']}")
    print("---")
```

#### 2. Получение деталей объекта

```python
# Получаем детали по ID
object_id = 12345
details = api.details(object_id)

# Анализируем структуру ответа
print("Доступные поля:")
for key, value in details.items():
    if isinstance(value, (str, int, float, bool)) and value:
        print(f"  {key}: {value}")
```

#### 3. Обработка ошибок

```python
from requests.exceptions import HTTPError, RequestException

try:
    results = api.search("Несуществующий адрес")
except HTTPError as e:
    if e.response.status_code == 404:
        print("Адрес не найден")
    elif e.response.status_code == 401:
        print("Неверный токен")
    else:
        print(f"HTTP ошибка: {e}")
except RequestException as e:
    print(f"Ошибка сети: {e}")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
```

## 📚 API Reference

### Класс `FiasPublicApi`

Основной класс для работы с API ФИАС.

#### Конструктор

```python
FiasPublicApi(token: str)
```

**Параметры:**

- `token` (str) - Токен аутентификации для доступа к API

#### Методы

##### `search(search_string: str, url: str = None) -> List[Dict]`

Поиск адресов по текстовой строке.

**Параметры:**

- `search_string` (str) - Строка для поиска (адрес, улица, город и т.д.)
- `url` (str, опционально) - Кастомный URL API endpoint

**Возвращает:** Список найденных адресов в виде словарей

**Пример ответа:**

```json
[
  {
    "id": 12345,
    "address": "г Москва, Красная площадь",
    "type": "город",
    "level": 1
  }
]
```

##### `details(object_id: int) -> Dict`

Получение детальной информации об объекте адресации.

**Параметры:**

- `object_id` (int) - ID объекта в системе ФИАС

**Возвращает:** Словарь с детальной информацией об объекте

### Функции

#### `get_token(url: str = "https://fias.nalog.ru/") -> str`

Получение токена аутентификации от сервиса ФИАС.

**Параметры:**

- `url` (str) - Базовый URL сервиса ФИАС

**Возвращает:** Строка с токеном аутентификации

**Исключения:**

- `ValueError` - Если получение токена не удалось
- `requests.HTTPError` - Если HTTP запрос завершился с ошибкой

#### `STANDART_HEADERS(token: str) -> Dict[str, str]`

Генерация стандартных заголовков для HTTP-запросов.

**Параметры:**

- `token` (str) - Токен аутентификации

**Возвращает:** Словарь с заголовками для HTTP-запросов

## 💡 Примеры

### Пример 1: Поиск улиц в городе

```python
def find_streets_in_city(city_name: str, street_pattern: str = ""):
    """Поиск улиц в указанном городе"""
    api = FiasPublicApi(get_token())

    # Ищем город
    cities = api.search(city_name)
    if not cities:
        print(f"Город '{city_name}' не найден")
        return

    city = cities[0]
    print(f"Найден город: {city['address']}")

    # Ищем улицы
    search_query = f"{city_name}, {street_pattern}" if street_pattern else city_name
    streets = api.search(search_query)

    print(f"\nНайдено улиц: {len(streets)}")
    for street in streets[:10]:  # Показываем первые 10
        print(f"  - {street.get('address', 'N/A')}")

# Использование
find_streets_in_city("Москва", "Тверская")
```

### Пример 2: Получение иерархии адреса

```python
def get_address_hierarchy(address_id: int):
    """Получение полной иерархии адреса"""
    api = FiasPublicApi(get_token())

    try:
        details = api.details(address_id)

        print("🏠 Иерархия адреса:")
        print(f"  Уровень: {details.get('level', 'N/A')}")
        print(f"  Тип: {details.get('type', 'N/A')}")
        print(f"  Название: {details.get('name', 'N/A')}")
        print(f"  Полный адрес: {details.get('address', 'N/A')}")

        # Дополнительная информация
        if 'coordinates' in details:
            coords = details['coordinates']
            print(f"  Координаты: {coords.get('lat', 'N/A')}, {coords.get('lon', 'N/A')}")

    except Exception as e:
        print(f"❌ Ошибка при получении деталей: {e}")

# Использование
get_address_hierarchy(12345)
```

### Пример 3: Массовый поиск адресов

```python
import time
from typing import List, Dict

def batch_address_search(queries: List[str], delay: float = 0.1) -> Dict[str, List]:
    """Массовый поиск адресов с задержкой между запросами"""
    api = FiasPublicApi(get_token())
    results = {}

    print(f"🔍 Начинаем поиск {len(queries)} адресов...")

    for i, query in enumerate(queries, 1):
        try:
            print(f"  [{i}/{len(queries)}] Ищем: {query}")
            search_results = api.search(query)
            results[query] = search_results
            print(f"     Найдено: {len(search_results)} результатов")

            # Задержка между запросами
            if i < len(queries):
                time.sleep(delay)

        except Exception as e:
            print(f"     ❌ Ошибка: {e}")
            results[query] = []

    return results

# Использование
addresses_to_search = [
    "Москва, Красная площадь",
    "Санкт-Петербург, Дворцовая площадь",
    "Казань, Кремль",
    "Новосибирск, Красный проспект"
]

results = batch_address_search(addresses_to_search, delay=0.2)
```

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для деталей.

## 🔗 Полезные ссылки

- [🌐 Официальный сайт ФИАС](https://fias.nalog.ru/)
- [📡 Публичное API ФИАС](https://fias-public-service.nalog.ru/)
- [📖 Документация API](https://fias.nalog.ru/Home/GetSpasSettings)
- [🐍 Python Package Index](https://pypi.org/)
- [📚 Документация requests](https://requests.readthedocs.io/)

## 📊 Статистика проекта

![GitHub stars](https://img.shields.io/github/stars/invoxy/fias-public-api?style=social)
![GitHub forks](https://img.shields.io/github/forks/invoxy/fias-public-api?style=social)
![GitHub issues](https://img.shields.io/github/issues/invoxy/fias-public-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/invoxy/fias-public-api)

---

<div align="center">

**Сделано с ❤️**

[![GitHub](https://img.shields.io/badge/GitHub-invoxy-black?style=flat-square&logo=github)](https://github.com/invoxy)

</div>
