import telebot
from telebot import types
from flask import Flask, request, render_template

# Создаем объект бота с помощью токена
bot = telebot.TeleBot('6450176384:AAHy-gmwbB5xVvwX7nUKH9ZX0RJPBDUYUek')

app = Flask(__name__)
applications = []

# Определяем маршрут для веб-приложения
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        telegram_tag = request.form['telegram_tag']
        email = request.form['email']
        service = request.form['service']

        # Создаем сообщение с данными пользователя
        message_text = f"Пользователь {telegram_tag} подал заявку на услугу {service}. Email: {email}"

        # Отправляем сообщение владельцу бота
        bot.send_message('5814570764', message_text)  # Замените '5814570764' на ID владельца бота

        # Добавляем данные о заявке в список
        applications.append({'telegram_tag': telegram_tag, 'email': email, 'service': service})

        # Возвращаем сообщение об успешной подаче заявки
        return "Заявка успешно подана!"

    return render_template('index.html')

# Создаем словарь для хранения реквизитов оплаты
payment_details = {
    '1 тир': 'xxxxxxxxxxxxx\nxxxxxxxxxxxxx\nxxxxxxxxxxxxx',
    '2 тир': 'xxxxxxxxxxxxx\nxxxxxxxxxxxxx\nxxxxxxxxxxxxx',
    '3 тир': 'xxxxxxxxxxxxx\nxxxxxxxxxxxxx\nxxxxxxxxxxxxx',
    'орлы': 'xxxxxxxxxxxxx\nxxxxxxxxxxxxx\nxxxxxxxxxxxxx'
}

# Создаем функцию для отправки приветственного сообщения с фотографией и текстом
def send_welcome_message(message):
    with open('photo.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=f'Приветствую, {message.from_user.first_name}! Предлагаем услуги партнерской программы в следующих играх:\n\n1. War Thunder Mobile \n2. Modern Warships \n3. Tanks (от ARTSTORM)\n4. Другая игра\n\nЧтобы выбрать свой вариант введите цифру игры которая вам подходит. Например: 1')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('1', '2', '3', '4', 'Остаток')  # Добавляем кнопку "Остаток" в главное меню
        markup.add('Новости', 'Акции')
        bot.send_message(message.chat.id, text='Выберите номер услуги или раздел:', reply_markup=markup)

# Создаем функцию для отправки информации о партнерской программе War Thunder Mobile
def send_war_thunder_info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('1 тир', '2 тир', '3 тир', 'орлы')
    bot.send_message(message.chat.id, text='Партнёрская программа War Thunder Mobile включает в себя три тира:\n\n1. Золотые Орлы: до 5 000 + две единицы любой стандартной техники + любой премиумный взвод + повторение всех этих бонусов при крупном обновлении. Примерная стоймость подписки в орлах: 13500.\nСтоймость подписки в месяц: 3000₽ + единичная оплата услуги в размере 2000₽: подключение к партнерской программе. Пример:если вы подключили первый тир партнёрства и оплатили его, то в будущем вам нужно будет платить только за сами начисления, так как вас уже внесли в программу поддержки.\n\n2. Второй тир включает в себя 15 000 орлов ежемесячно + добавление стандарт­ной техники (до 5).Дополнительные бону­сы в том же размере под крупные обновлен­ия. До двух премиумных взвода или корабля. Оценка второго тира в орлах: 40000. Стоймость подписки 8000р/месяц+4000р подключение партнерской программы навсегда.\n\n3. Третий тир партнёрства включает в себя 30000 орлов в месяц+добавление любой стандартной техники до 10 (в месяц) + любые премиумные взводы до трех (в месяц). Общая оценка партнёрства: 80000 орлов. Стоймость подписки: 14000₽/месяц+6000₽ внесение в программу поддержки.\n\nТакже мы продаем золотые орлы по курсу 1 рубль=5,2 золотых орла (5000р=26000). Минимальная сумма покупки 2000р. Начисления происходят орлами+премиумной техникой, чтобы сумма в конечном итоге вышла 26000 орлов. Вы также можете купить за месяц до 60000 орлов. Чтобы покупать данные наборы выгодно, нужно также оформить подключение в размере 5000р (Платите 5000₽ и можете неограниченно каждый месяц покупать до 60000 орлов).\n\nВыберите какую услугу хотите купить:', reply_markup=markup)

# Создаем функцию для отправки реквизитов оплаты и запроса скриншота
def send_payment_info(message):
    text = message.text
    if text in payment_details:
        details = payment_details[text]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Назад')
        bot.send_message(message.chat.id, text=f'Оплата по следующим реквизитам: {details}\n\nЕсли вы оформляйте партнёрство/покупку орлов первый раз,то не забудьте оплатить подключение партнерской программы.После оплаты пришлите скриншот,мы его проверим и свяжемся лично. Если скриншот отправлен не будет/у вас не будет имя пользователя в телеграмме (тег,например:@DonationAllianceBot), обратной связи можно не ждать. \n\nВажное примечание: срок выполнения подключения к партнерской программе составляет до недели. Если вы уже подключены, то мы выполним ваш заказ в течении дня. Мы несем полную отвественность за начисления на ваш аккаунт и его полную сохранность до тех пор, пока покупатель самостоятельно не расскажет любому лицу о природе происхождения начислений. \n\nЕсли вы оформляйте покупку золотых орлов, то сумма заказа должна быть не менее 2000р и не превышать 60000 орлов. Умножайте вашу сумму оплаты в рублях на 5.2 и получите колличество орлов которые мы вам начислим техникой и самими орлами.\n\nВАЖНО: ВСЕ ПОДПИСКИ КРОМЕ 3 ТИРА БЕРУТСЯ ТОЛЬКО НА 2+ МЕСЯЦА. В данный момент мы не оформляем подписки лишь на один месяц из-за технических проблем. В связи с этим мы предоставляем хорошие скидки на длительные подписки. Следите за нами в разделах "Новости" и "Акции".\n\nНе забудьте выслать скриншот оплаты!' , reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text='Неверный выбор. Пожалуйста, выберите одну из услуг.')

# Создаем функцию для отправки скриншота владельцу бота и тега пользователя
def send_screenshot(message):
    if message.photo:
        photo = message.photo[-1]
        file = bot.get_file(photo.file_id)
        bytes = bot.download_file(file.file_path)
        with open('screenshot.jpg', 'wb') as f:
            f.write(bytes)
        with open('screenshot.jpg', 'rb') as f:
            bot.send_photo('5814570764', f, caption=f'@{message.from_user.username}')
    else:
        bot.send_message(message.chat.id, text='Пожалуйста, пришлите скриншот оплаты.')

# Функция для отправки информации о новостях
def send_news_info(message):
    news_text = "Новостей нет. В ближайшее время бот обслуживаться не будет."
    bot.send_message(message.chat.id, text=news_text)

# Функция для отправки информации об акциях
def send_promotions_info(message):
    promotions_text = "1) Для всех, кто первый раз оформляет подключение к возможности покупать орлы, мы предоставляем любой премиальный взвод на выбор в подарок!\n\n2) При подключении подписки на первый тир сроком в три месяца, стоймость подписки вместе с подключением к партнерской программе составит 8000p вместо 11000p.\n\n3) При подключении подписки на второй тир сроком в 2 месяца, стоймость подписки вместе с подключением к партнерской программе составит 15000p вместо 20000p\n\n4) При подключении подписки на 3 тир сроком в два месяца, стоймость подписки вместе с подключением к партнерской программе составит 25000p вместо 34000p\n\n5) Для тех, кто заказывает орлы, акции не прошли стороной! Всем, кто в общей сложности заказал орлы на сумму в 10000p, на следующую покупку скидка 20%!"
    bot.send_message(message.chat.id, text=promotions_text)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    send_welcome_message(message)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def text(message):
    text = message.text
    if text in ['1', '2', '3', '4']:
        if text == '1':
            send_war_thunder_info(message)
        else:
            bot.send_message(message.chat.id,
                             text='Извините, пока что мы предлагаем партнерскую программу только для игры War Thunder Mobile. Пожалуйста, выберите эту игру.')
    elif text in payment_details:
        send_payment_info(message)
    elif text == 'Новости':
        send_news_info(message)
    elif text == 'Акции':
        send_promotions_info(message)
    elif text == 'Остаток':  # Обработка нажатия на кнопку "Остаток"
        send_balance_info(message)
    elif text == 'Назад':
        send_welcome_message(message)
    else:
        bot.send_message(message.chat.id, text='Неверный ввод. Пожалуйста, выберите один из предложенных вариантов.')

# Обработчик фотографий
@bot.message_handler(content_types=['photo'])
def photo(message):
    send_screenshot(message)

# Функция для отправки информации о балансе
def send_balance_info(message):
    # Здесь вы можете добавить код для получения и отправки информации о балансе
    balance_text = "Текущее колличество доступных партнерских программ без ожидания подключения: 1. Если же колличество равно 0, то при заказе партнерства ожидание подключения составляет до двух месяцев"  # Пример текста с балансом
    bot.send_message(message.chat.id, text=balance_text)

# Запускаем бота в бесконечном цикле
if __name__ == '__main__':
    bot.polling()
    app.run(debug=True)


















1