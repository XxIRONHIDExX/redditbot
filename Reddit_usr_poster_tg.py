import logging
import praw
import random
import asyncio
import telegram
from telegram.ext import Updater

telegram_token = ''
reddit_client_id = ''
reddit_client_secret = ''
usernames = ['alisha_xxxx', 'JadeRabbit_', 'petitelady18','Tab_kush', 'ariakhan00', 'ella_petite', 'Lost-Huckleberry7324', 'miaipanema', 'Raw_roxxx', 'X29771628','theawesomekate']  # Replace with the desired Reddit usernames

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent='Telegram Bot'
)

async def post_media(bot, chat_id):
    while True:
        username = random.choice(usernames)
        try:
            redditor = reddit.redditor(username)

            # Fetch the top posts from the user
            posts = redditor.hot(limit=20)  # Fetch only 10 top posts

            # Filter media posts (videos and gifs)
            media_posts = [
                post for post in posts
                if post.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.gifv', '.mp4'))
            ]

            if not media_posts:
                raise ValueError("No media posts found for the user.")

            # Select a random media post
            selected_post = random.choice(media_posts)

            # Prepare the message content with enhanced appearance
            message_title = selected_post.title
            message_content = f"Username: {username}\n" \
                              f"Post Link: {selected_post.shortlink}"

            # Send a video message
            await bot.send_video(chat_id=chat_id, video=selected_post.url, caption=message_content)

        except Exception as e:
            logging.error(f"Error posting media from Reddit user '{username}': {e}")

        await asyncio.sleep(10)  # Wait for 10 seconds before posting the next media

def main():
    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Set up the Telegram bot
    updater = Updater(token=telegram_token, use_context=True)
    bot = updater.bot
    chat_id = '-910357905'  # Replace with your desired chat ID

    # Start posting media
    asyncio.run(post_media(bot, chat_id))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
