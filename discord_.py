import discord
import requests
cats = ["кот", "котик", "кошка", "кошечка", "коты", "котики", "кошки", "кошечки",
        "котёнок", "котенок", "котятки"]
dogs = ["пес", "пёс", "песик", "пёсик", "собака", "собачка",
        "псы", "пёсики", "собаки", "собачки",
        "щенок", "щенки", "щеночек", "щеночки"]
TOKEN = None


def clean_str(a):
    return ''.join(i for i in a if i not in ',./\\!@"№#$;%^:&?*()~`' + "'<>-+=_")


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            for channel in guild.text_channels:
                await channel.send('Могу отправить картинку с котиком или собачкой!')
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if any(i in clean_str(message.content.lower()) for i in cats):
            await message.channel.send(requests.get("https://api.thecatapi.com/v1/images/search?format=json").json()[0]
                                       ['url'])
        elif any(i in clean_str(message.content.lower()) for i in dogs):
            await message.channel.send(requests.get("https://dog.ceo/api/breeds/image/random").json()["message"])


client = YLBotClient()
client.run(TOKEN)