#!/usr/bin/env python3
"""
Пример базового использования FIAS Public API

Этот скрипт демонстрирует основные возможности библиотеки:
- Получение токена
- Поиск адресов
- Получение деталей объекта
"""

from fias_public_api import FiasPublicApi, get_token

def main():
    print("🚀 FIAS Public API - Пример использования\n")

    try:
        # Получаем токен
        print("1. Получаем токен аутентификации...")
        token = get_token()
        print(f"✅ Токен получен: {token[:20]}...")

        # Создаем клиент
        print("\n2. Создаем API клиент...")
        api = FiasPublicApi(token)
        print("✅ Клиент создан")

        # Ищем адрес
        print("\n3. Ищем адрес 'Москва, Красная площадь'...")
        search_results = api.search("Москва, Красная площадь")
        print(f"✅ Найдено результатов: {len(search_results)}")

        if search_results:
            # Показываем первый результат
            first_result = search_results[0]
            print(f"\n4. Первый результат:")
            print(f"   ID: {first_result.get('id', 'N/A')}")
            print(f"   Адрес: {first_result.get('address', 'N/A')}")
            print(f"   Тип: {first_result.get('type', 'N/A')}")

            # Получаем детали по ID
            if "id" in first_result:
                print(f"\n5. Получаем детали объекта {first_result['id']}...")
                try:
                    details = api.details(first_result["id"])
                    print("✅ Детали получены:")
                    for key, value in details.items():
                        if isinstance(value, (str, int, float, bool)) and value:
                            print(f"   {key}: {value}")
                except Exception as e:
                    print(f"❌ Ошибка при получении деталей: {e}")

        # Дополнительные примеры поиска
        print("\n6. Дополнительные примеры поиска:")

        searches = ["Санкт-Петербург, Невский проспект", "Тверская улица", "Арбат"]

        for search_query in searches:
            try:
                results = api.search(search_query)
                print(f"   '{search_query}': {len(results)} результатов")
            except Exception as e:
                print(f"   '{search_query}': ошибка - {e}")

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        print("\n💡 Убедитесь, что:")
        print("   - У вас есть доступ к интернету")
        print("   - Сервис ФИАС доступен")
        print("   - Все зависимости установлены")


if __name__ == "__main__":
    main()
