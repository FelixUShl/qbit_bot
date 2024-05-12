import qbittorrentapi, telebot, os, dotenv

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
paths = {
        "distr": "C:\\net_ssd\\HDD\\torrents\\distr",
        "serial": "C:\\net_ssd\\HDD\\torrents\\media\\serials",
        "film": "C:\\net_ssd\\HDD\\torrents\\media\\films"
        }
save_path = paths["distr"]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Hellow\nТекущая папка сохранения данных\n{save_path}.")
    bot.send_message(message.chat.id, f"Для изменения пути сохранения выбери в меню какой тип торрента ты загружаешь")


@bot.message_handler(commands=["programm"])
def set_path_program(message):
    global save_path
    save_path = paths["distr"]
    bot.send_message(message.chat.id, f"Данные будут сохранены в\n{save_path}\nОжидаю торрент файл")


@bot.message_handler(commands=["serial"])
def set_path_serial(message):
    global save_path
    save_path = paths["serial"]
    bot.send_message(message.chat.id, f"Данные будут сохранены в\n{save_path}\nОжидаю торрент файл")


@bot.message_handler(commands=["film"])
def set_path_film(message):
    global save_path
    save_path = paths["film"]
    bot.send_message(message.chat.id, f"Данные будут сохранены в\n{save_path}\nОжидаю торрент файл")


@bot.message_handler(content_types="document")
def create_torrent_task(message):
    if message.document.file_name[-8:] == ".torrent":
        bot.send_message(message.chat.id, f"Вау!!! торрент файл")
        with open("temp.torrent", "wb") as torrent:
            torrent.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
        client = qbittorrentapi.Client(host=SERVER_URL, port=SERVER_PORT, username=LOGIN, password=PASSWORD)
        client.torrents_add(torrent_files="temp.torrent", save_path=save_path)
        client.auth_log_out()
        os.remove("temp.torrent")

    else:
        bot.send_message(message.chat.id, f"Ты втираешь мне какую-то дичь")


if __name__ == '__main__':
    bot.infinity_polling()
