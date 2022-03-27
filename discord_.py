import asyncio
import discord

TOKEN = None


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            for channel in guild.text_channels:
                await channel.send('set_timer in X hours Y minutes')
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        args = message.content.split()
        if len(args) == 6 and [args[0], args[1], args[3], args[5]] == ["set_timer", "in", "hours", "minutes"] and \
                args[2].isdigit() and args[4].isdigit():
            seconds = int(args[2]) * 60 * 60 + int(args[4]) * 60
            await message.channel.send("The timer should start in " + args[2] + " hours " + args[4] + " minutes")
            await asyncio.sleep(seconds)
            await message.channel.send(":alarm_clock:Time X has come!")


client = YLBotClient()
client.run(TOKEN)