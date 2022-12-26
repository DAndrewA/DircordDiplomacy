import discord
from handle_responses import handle_responses

bot_intents = discord.Intents.default()
bot_intents.messages = True
#bot_intents.message_content = True
print(f'{bot_intents=}')


async def send_message(message,user_message, is_private):
    try:
        response = handle_responses(user_message)
        if response is None:
            return
        
        if is_private:
            # if the message is to be private, send it to the author of the message
            await message.author.send(response)
        else:
            # otherwise, need to send the response to the channel the message was asked in
            await message.channel.send(response)
    except Exception as e:
        print(e)


def load_OAUTH_TOKEN(fname):
    with open(fname) as f:
        for line in f:
            if ':TOKEN' in line:
                TOKEN = next(f).split('\n')[0]
                return TOKEN


def run_discord_bot():
    TOKEN = load_OAUTH_TOKEN('oauth_data.txt')
    print(f'{TOKEN=}')
    client = discord.Client(intents=bot_intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return # stops the bot from responding to itself constantly
        author = str(message.author)
        message_text = str(message.content)
        channel = str(message.channel)
        print(f'{author} said "{message_text}" in {channel=}')

        print(message)
        print(f'{message.content=}')

        isPrivate = False
        if message_text[0] == '*': # allow users to get private responses by preceeding the message with a *
            message_text = message_text[1:]
            isPrivate = True

        await send_message(message, message_text, isPrivate)

    client.run(TOKEN)
