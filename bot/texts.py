"""
Common
"""

ERROR = "Извините, что-то пошло не так"

WE_ARE_WORKING = "Бот скоро запустится! Мы уже работаем!"

"""
User
"""
FAQ = (
    'Вот небльшая информация как работать с нашим ботом 😊:\n\n'
    'Меню (/start)\n'
    '*Выбор режима*: Каждый режим использует свою языковую модель. Чем лучше режим, тем дороже запрос. Старайтесь прибегать '
    'к умным моделям только в ситуациях, когда это действительно необходимо! Базовая модель очень дешевая (~40-20 коп.)'
    'и сообразительная для своих денег, скорее всего вам её хватит.\n'
    '*Пополнить баланс*: Здесь через СБП можно пополнить свой баланс. Деньги поступят на ваш баланс в течении суток. '
    'Отправляйте чек, только после нажатия на эту кнопку!\n'
    '*Реферальная ссылка*: Если вы скопируете выданную ссылку и пригласите друга, то получите 5 руб на ваш счет за каждого.\n'
    '\n/clear - В процессе беседы наш бот запоминает ваш диалог, если вы хотите очистить память бота, нажмите на эту команду.'
    '_(Мы не храним ваш диалог в базе данных, но иногда ваш контекст может быть утерян)_'
    'Для решения всех вопросов обращайтесь в поддержку в шапке бота.\n\n'
)

LC_TEXT = """
Добро пожаловать в ваш личный кабинет! 🎄 
"""

MENU_TEXT = 'Меню'

GREETING_TEXT = 'Привет, я твой ИИ-помощник.\nЯ очень рад, что вы выбрали меня! <3'

HELP_TEXT = 'По вопросам можно обратиться в чат поддержки https://t.me/+hNOJ9VWB_1k2ZjI6'

MODEL_TEXT = 'Выберите модель ИИ которую вы хотите приобрести'

CHOICE_TEXT = 'Доступные для вас планы'

NOT_IN_DB_TEXT = "Пожалуйста, напишите /start \nЕсли ничего не поменялось сообщите нам /help"

BUY_TEXT = "Доступные для покупки модели:"

PAY_INFO = ("Пополнить баланс можно через СБП, по номеру 89083375199 Т-Банк с сообщением "
            "'ИИ-бот'. Ваш чек нужно отправить прямо сюда, в этом окне.\n\n") + HELP_TEXT

BALANCE_TEXT = "История всех ваших транзакций:\n\n"

"""
Admin
"""
