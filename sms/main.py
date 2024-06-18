import time
import json
import requests


with open('data.json', 'r') as file:
    data = json.load(file)

login = data['smsc-login']                      # Логин в smsc
password = data['smsc-password']                # Пароль в smsc

 
def send_sms(phones, text, total_price=0):
    # Возможные ошибки
    errors = {
        1: 'Ошибка в параметрах.',
        2: 'Неверный логин или пароль.',
        3: 'Недостаточно средств на счете Клиента.',
        4: 'IP-адрес временно заблокирован из-за частых ошибок в запросах. Подробнее',
        5: 'Неверный формат даты.',
        6: 'Сообщение запрещено (по тексту или по имени отправителя).',
        7: 'Неверный формат номера телефона.',
        8: 'Сообщение на указанный номер не может быть доставлено.',
        9: 'Отправка более одного одинакового запроса на передачу SMS-сообщения либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты. '
    }
    # Отправка запроса
    url = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&fmt=3" % (login, password, phones, text, total_price)
    print(url)
    answer = requests.get(url).json()
    if 'error_code' in answer:
        # Возникла ошибка
        return errors[answer['error_code']]
    else:
        if total_price == 1:
            # Не отправлять, узнать только цену
            print('Будут отправлены: %d SMS, цена рассылки: %s' % (answer['cnt'], answer['cost'].encode('utf-8')))
        else:
            # СМС отправлен, ответ сервера
            return answer
 

phones = (data['my_phone_number'],)
text = 'Hello first message'

for number in phones:
    send = send_sms(number, text)
    if 'cnt' in send:
        print('На номер %s, сообщение отправлено успешно!' % number)
        time.sleep(30) # Засыпаем передачу на 30 сек - ограничение...
    else:
        print(send)
        print('Ошибка...')