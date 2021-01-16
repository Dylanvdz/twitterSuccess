import tweepy
import time
import discord
import re
import requests
import os

# Twitter Credentials
API_KEY = ''
API_KEY_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# Discord token
DISCORD_TOKEN = ''

# Discord channel id
general_chat = 000000000000000000
success_channel = 000000000000000000

class TweetBot():

    def authenticate(self):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # API objec
        api = tweepy.API(auth)
        # Verify credentials
        try:
            api.verify_credentials()
            return api
        except:
            return False

# Authenticate
api = TweetBot().authenticate()
client = discord.Client()

if api == False:
    print('Error verifying api...')
    time.sleep(2)
    exit()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # Commands used to check if the program is still running
    if message.channel.id == general_chat:

        if message.content.startswith('beep'):
            await message.channel.send('boop')
            
        if message.content.startswith('boop'):
            await message.channel.send('beep')
        
        if message.content.startswith('ping'):
            await message.channel.send('pong')

    if message.channel.id == success_channel:
        
        if message.attachments:
            # Find the link in the message attachment
            data = re.findall(r'url=\'(.+?)\'>', str(message.attachments)) #Find link
            temp = data[0].split('/')
            image_path = f'images/{temp[6]}'
            discord_tag = str(message.author).split('#')
            user = discord_tag[0]

            # GET the picture posted in the channel
            response = requests.get(data[0], headers={
            	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            	})

            # Temporarily save the image on the local device to be able to post online
            file = open(image_path, 'wb') #Temp[6] = image name
            file.write(response.content)
            file.close()
            # Sleep to avoid errors
            time.sleep(0.5)

            #Upload image to twitter
            media = api.media_upload(image_path)
            tweet_text = f'Success from {user}'
            tweet = api.update_status(status=tweet_text, media_ids=[media.media_id])
            print(f'Success posted to twitter by {message.author}')

            # Notify user the success picture has been posted
            embedVar = discord.Embed(title='Posted success to twitter! :partying_face:', description='Check the tweet in the link below!\nDon\'t want your success on twitter? Ask the admin to delete it!', color=242424)
            embedVar.add_field(name='Tweet', value= f'[Click here!](https://twitter.com/twitter/statuses/{tweet.id})')
            embedVar.add_field(name='Member', value='{0.author.mention}'.format(message))
            embedVar.set_footer(text='XXXX tools | Developed by XXXX', icon_url='Your groups logo')
            await message.channel.send(embed=embedVar)

            # Remove the image file from local machine after posting to twitter
            time.sleep(1)
            os.remove(image_path)
client.run(DISCORD_TOKEN)
