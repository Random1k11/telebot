from flask import Flask, request
import telegram

import settings_telegram
from get_data import engine


URL = settings_telegram.URL
TOKEN = settings_telegram.TOKEN

REQUEST_KWARGS = {
    'proxy_url': f'socks5://{settings_telegram.SOCKS5_PROXY}',
    'urllib3_proxy_kwargs': {
        'username': f'{settings_telegram.LOGIN_PROXY}',
        'password': f'{settings_telegram.PASSWORD_PROXY}',
    }
}

proxy_url = f'socks5://{settings_telegram.LOGIN_PROXY}:{settings_telegram.PASSWORD_PROXY}@{settings_telegram.SOCKS5_PROXY}'
socks5_proxy = telegram.utils.request.Request(proxy_url=proxy_url)

bot = telegram.Bot(token=TOKEN, request=socks5_proxy)


app = Flask(__name__)


@app.route('/', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    if text == "/start":
        result = engine.execute('SELECT * FROM "VACANCY"')
        for r in result:
            text = r[2]
            if r[1] == None:
                continue
            bot.sendMessage(chat_id='-1001163262865', text=str(r[2]) + str(r[1]))
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.hello'


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
