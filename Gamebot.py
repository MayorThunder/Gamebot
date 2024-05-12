import logging
import aiohttp
import telegram.ext
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler

with open("../token/token.txt") as f:
    BOT_TOKEN = f.readline()

timer = 0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

main_rk = [['/classes', '/tech_tree', '/multi_class_assecories'], ['/enemies', '/mini_bosses', '/bosses'],
           ['/help', '/support', '/donate'], ['/our_offices', '/change_language']]
end_rk = [['/main_page']]
start_mup = ReplyKeyboardMarkup(main_rk, one_time_keyboard=True)
end_mup = ReplyKeyboardMarkup(end_rk, one_time_keyboard=True)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(rf"Привет {user.mention_html()}!" +
    " Я бот-помощник по игре 'Soul fight'. Выбери одну из кнопок ниже, чтобы получить интересующую информацию",
    reply_markup=start_mup)


async def help_command(update, context):
    await update.message.reply_text("/classes - осмотреть информацию по классам\n/tech_tree - посмотреть информаци\
     по деревьям исследований\n/multi_class_assecories - посмотерть аксессуары подходящие для всех классов\n\
/enemies - посмотреть информацию по всем обычным врагам\n/mini_bosses - посмотреть информацию по элитным врагам\
/bosses - посмотреть информацию по боссам\n/support - предложить свои идеи по оружию/врагам\n/donate - финансово\
поддержать\n/our_offices - наши офисы\n/change_language - сменить язык", reply_markup=end_mup)


async def mc_assecories(update, context):
    await update.message.reply_text("К сожалению, в игре пока отсутствуют такие аксессуары. Следите за обновлениями!\n\
                                    (Вы будете автоматически возвращены на главную страницу черз 15 секунд)",
                                    reply_markup=end_mup)


async def offices(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"

    dt = []
    LC, UC = None, None
    GEO = ["Новочеремушкинская+улица,34к1", "Большой+Знаменский+переулок,8к2"]
    for i in GEO:

        resp = await get_response(geocoder_uri, params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "format": "json",
            "geocode": i})
        r = resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"][
            "Envelope"]
        dt.append(resp["response"]["GeoObjectCollection"]["featureMember"][0]
                  ["GeoObject"]["Point"]["pos"])
        if LC is None:
            LC = [float(x) for x in r["lowerCorner"].split()]
            UC = [float(x) for x in r["upperCorner"].split()]
        else:
            if LC[0] > float(r["lowerCorner"].split()[0]):
                LC[0] = float(r["lowerCorner"].split()[0])
            if LC[1] > float(r["lowerCorner"].split()[1]):
                LC[1] = float(r["lowerCorner"].split()[1])
            if UC[0] < float(r["upperCorner"].split()[0]):
                UC[0] = float(r["upperCorner"].split()[0])
            if UC[1] < float(r["upperCorner"].split()[1]):
                UC[1] = float(r["upperCorner"].split()[1])
    coords, w, h = (f"{(float(LC[0]) + float(UC[0])) / 2},{(float(LC[1]) + float(UC[1])) / 2}",
                    (float(UC[0]) - float(LC[0])),
                    (float(UC[1]) - float(LC[1])))
    resp = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={w},{h}&pt={"~".join([f"{",".join(i.split())},vkbkm" for i in dt])}&l=map"
    await context.bot.send_photo(update.message.chat_id, resp)


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def bosses(update, context):
    await update.message.reply_text("К сожалению, в игру пока не добавлены боссы. Следите за обновлениями!\n\
(Вы будете автоматически возвращены на главную страницу черз 15 секунд)",
                                    reply_markup=end_mup)
    await ret(update, context)


async def mini_bosses(update, context):
    await update.message.reply_text("К сожалению, в игру пока не добавлены элитные враги. Следите за обновлениями!\n\
(Вы будете автоматически возвращены на главную страницу черз 15 секунд)",
                                    reply_markup=end_mup)
    await ret(update, context)


async def tech_tree(update, context):
    await update.message.reply_text("Древо исследований еще не добавлено в игру\n\
(Вы будете автоматически возвращены на главную страницу черз 15 секунд)",
                                    reply_markup=end_mup)
    await ret(update, context)


async def classes(update, context):
    await update.message.reply_text("Разработчику было лень переносить статьи по классам, поэтому тут ничего нет.\n\
(Вы будете автоматически возвращены на главную страницу черз 15 секунд)",
                                    reply_markup=end_mup)
    await ret(update, context)


async def enemies(update, context):
    await update.message.reply_text("Разработчику было лень написать статьи про врагов, поэтому тут ничего нет.\n\
(Вы будете автоматически возвращены на главную страницу черз 15 секунд)",
                                    reply_markup=end_mup)
    await ret(update, context)

    
async def change_lg(update, context):
    await update.message.reply_text("Пока здесь доступен только один язык - русский, но вы можете помочь с переводом\
/support", reply_markup=end_mup)
    await ret(update, context)


async def donate(update, context):
    await update.message.reply_text("Очень скоро по этой ссылке будет доступна финансовая помощь автору любимой игры.",
                                    reply_markup=end_mup)
    await ret(update, context)


async def support(update, context):
    await update.message.reply_text("Очень скоро по этой ссылке можно будет предложить свои идеи.",
                                    reply_markup=end_mup)
    await ret(update, context)


async def ret(update, context):
    global timer
    timer = 15
    chat_id = update.effective_message.chat_id
    context.job_queue.run_once(breaker, timer, chat_id=chat_id, name=str(chat_id), data=timer)


async def breaker(context):
    await context.bot.send_message(context.job.chat_id, text="А может и нет...")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("multi_class_assecories", mc_assecories))
    application.add_handler(CommandHandler("mini_bosses", mini_bosses))
    application.add_handler(CommandHandler("bosses", bosses))
    application.add_handler(CommandHandler("main_page", start))
    application.add_handler(CommandHandler("our_offices", offices))
    application.add_handler(CommandHandler("classes", classes))
    application.add_handler(CommandHandler("tech_tree", tech_tree))
    application.add_handler(CommandHandler("enemies", enemies))
    application.add_handler(CommandHandler("donate", donate))
    application.run_polling()


if __name__ == '__main__':
    main()
