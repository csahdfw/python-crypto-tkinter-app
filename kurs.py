import json  # библиотека для работы с json-данными для api coingecko
import requests  # библиотека для выполнения запросов к api
from tkinter import *  # основная библиотека для создания виджетов
from tkinter import messagebox as mb  # модуль для отображения всплывающих сообщений
from tkinter import ttk  # расширенные виджеты tkinter combobox и другие

"""
словари с данными о валютах
"""
# соответствие кодов криптовалют их api-идентификаторам (dict: ключ - код, значение - api id)
crypto_api_ids = {'BTC': 'bitcoin', 'ETH': 'ethereum', 'DOGE': 'dogecoin', 'TRUMP': 'official-trump'}

# соответствие кодов валют их api-идентификаторам (dict: ключ - код, значение - api id)
cash_codes = {'USD': 'usd', 'EUR': 'eur', 'AED': 'aed', 'CNY': 'cny', 'RUB': 'rub'}

# отображаемые названия для пользовательского интерфейса (dict: ключ - код, значение - читаемое название)
crypto_display = {'BTC': 'Биткоин', 'ETH': 'Эфириум', 'DOGE': 'Догикоин', 'TRUMP': 'Трампкоин'}
cash_display = {'USD': 'Доллар США', 'EUR': 'Евро', 'AED': 'Дирхам ОАЭ', 'CNY': 'Китайский юань',
                'RUB': 'Российский рубль'}

"""
функция преобразует числовое значение в читаемый строковый формат
"""


def format_currency(val):
    num = float(val)  # преобразуем ввод в число с плавающей точкой
    # выбираем формат (с дробной частью или без) и добавляем разделители
    return ("{:,.0f}" if num.is_integer() else "{:,.2f}").format(num).replace(",", " ").replace(".", ",")
    # возвращает: str (отформатированная строка с валютой)


"""
функция выполняет запрос к api и отображает курс обмена
"""


def exchange():
    # получение выбранных значений
    crypto = b_cb.get()  # str: выбранный код криптовалюты (из combobox)
    cash = t_cb.get()  # str: выбранный код валюты (из combobox)

    # получение api-идентификаторов
    crypto_id = crypto_api_ids.get(crypto)  # str: api-ид криптовалюты
    cash_code = cash_codes.get(cash)  # str: api-ид валюты

    # проверка выбора валют
    if not crypto_id or not cash_code:
        return mb.showwarning('', 'Выберите криптовалюту и государственную валюту!')

    try:
        # формирование url запроса
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={cash_code}'

        # выполнение запроса (возвращает: словарь с данными курса)
        response_data = requests.get(url, timeout=5).json()

        # извлечение курса из ответа
        rate = response_data.get(crypto_id, {}).get(cash_code)

        if rate:
            # формирование сообщения для пользователя
            msg = f"1 {crypto_display[crypto]} = {format_currency(rate)} {cash_display[cash]}"
            mb.showinfo('', msg)  # показываем информационное окно
        else:
            mb.showerror('', 'Курс не найден!')
    except requests.RequestException as e:
        mb.showerror('', f'Ошибка сети: {e}')
    except Exception as e:
        mb.showerror('', f'Ошибка: {e}')


"""
функция создания элементов интерфейса
создает выпадающий список с меткой
"""


def create_selector(label_text, values, display_map):
    # 1. создание метки (label)
    Label(window, text=label_text).pack(pady=5)

    # 2. создание выпадающего списка (combobox)
    cb = ttk.Combobox(window, values=list(values))
    cb.pack(pady=5)

    # 3. создание метки для отображения выбранного значения
    lbl = Label(window, text="")
    lbl.pack(pady=5)

    # 4. настройка lambda-функции для обработки выбора
    cb.bind("<<ComboboxSelected>>", lambda e: lbl.config(text=display_map.get(cb.get(), "")))

    return cb  # возвращаем созданный combobox для дальнейшего использования


"""
создание графического интерфейса
"""
# создание главного окна
window = Tk()
window.title("Курсы обмена криптовалют")
window.geometry("360x300")

# создание элементов интерфейса:

# 1. combobox для выбора криптовалюты
b_cb = create_selector("Криптовалюта:", crypto_api_ids.keys(), crypto_display)

# 2. combobox для выбора государственной валюты
t_cb = create_selector("Государственная валюта:", cash_codes.keys(), cash_display)

# 3. кнопка для выполнения запроса
Button(window, text="Получить курс обмена", command=exchange).pack(pady=10)

# запуск главного цикл обработки событий
window.mainloop()