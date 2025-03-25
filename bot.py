import random
import telebot
from google_images_search import GoogleImagesSearch
import os
import time

API_KEY = 'Information goes here.'
CX = 'Information goes here.'

gis = GoogleImagesSearch(API_KEY, CX)

BOT_TOKEN = 'Information goes here.'

bot = telebot.TeleBot(BOT_TOKEN)

IMAGE_DIR = 'Information goes here.'

def download_image(query):
    try:
        num_images = random.randint(1, 5)
        _search_params = {
            'q': query,
            'num': num_images,
        }
        gis.search(search_params=_search_params, path_to_dir=IMAGE_DIR, custom_image_name='sender_image')
        print("Image downloaded successfully.")

        return os.path.join(IMAGE_DIR, 'sender_image.jpg')

    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

@bot.message_handler(commands=['search'])
def send_image(message):
    command = message.text.split('/search ')[1]
    if command:
        query = command
    else:
        query = 'dog'

    try:
        image_path = download_image(query)
        time.sleep(5)
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo)
            print(f"Image of '{query}' sent successfully.")

            os.remove(image_path)
            print("Image removed successfully.")

            for filename in os.listdir(IMAGE_DIR):
                if filename.startswith('sender_image'):
                    file_path = os.path.join(IMAGE_DIR, filename)
                    os.remove(file_path)
                    print(f"Image '{filename}' successfully removed.")
        else:
            bot.reply_to(message, "We were unable to find an image for this search.")
            print("No images found.")

    except Exception as e:
        bot.reply_to(message, f"Error sending image: {e}")
        print(f"Error sending image: {e}")

bot.infinity_polling()
