import discord
from discord.ext import commands, tasks
from TikTokLive import TikTokLiveClient
import os

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

CANAL_ID = 1386403960319119420
USUARIO_TIKTOK = "094pn"
bot = commands.Bot(command_prefix="!", intents=intents)
live_enviada = False

@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')


    if not verificar_live.is_running():
        verificar_live.start()

@bot.command()
async def entrar(ctx):
    if ctx.author.voice:
        canal = ctx.author.voice.channel
        await canal.connect()
        await ctx.send("Entrei na call.")
    else:
        await ctx.send("Você precisa estar em uma call.")

@bot.command()
async def sair(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Saí da call.")

@tasks.loop(minutes=1)
async def verificar_live():
    print("Verificando live do TikTok...")
    global live_enviada
    try:
        client = TikTokLiveClient(unique_id=USUARIO_TIKTOK)

        ao_vivo = await client.is_live()

        if ao_vivo and not live_enviada:
            canal = bot.get_channel(CANAL_ID)

            if canal:
                await canal.send(
                    "🔴 **094pn ESTÁ AO VIVO NO TIKTOK!**\n"
                    "https://www.tiktok.com/@094pn/live"
                )

            live_enviada = True

        elif not ao_vivo:
            live_enviada = False

    except Exception as erro:
        print(f"Erro ao verificar live: {erro}")

bot.run(TOKEN)