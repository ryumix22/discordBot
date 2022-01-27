import os
import time
import TableWrapper as tbl
from dotenv import load_dotenv
from discord.ext import commands, tasks
from dataclasses import dataclass
import discord


@dataclass
class Info:
    countOfGroups = 0
    currentPage = 0


info = Info()
time.sleep(120)
table = tbl.Table()
time.sleep(20)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents, help_command=None)

emojiNumList = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


@tasks.loop(seconds=60)
async def updateTableLoop():
    try:
        table.updateTable()
    except Exception:
        print('Google Flood sec')


@bot.event
async def on_ready():
    # my id 933787505591992363
    # kur id 933512604784148520
    await bot.get_channel(933512604784148520).send('Привет. Бот работает')


# @bot.event
# async def on_message(message):
#     if message.author.name == 'CinemaBot' and 'Отмечайте, будете ли вы смотреть кино' in message.content:
#         await message.add_reaction('✅')
#         await message.add_reaction('❌')
#         return
#     elif message.author.name == 'CinemaBot' and 'Список всех фильмов. Для отображения следующей страницы, воспользуйтесь кнопками снизу.' in message.content:
#         await message.add_reaction('⬆')
#         print(info.countOfGroups)
#         for i in range(info.countOfGroups):
#             await message.add_reaction(emojiNumList[i])
#         await message.add_reaction('⬇')
#     else:
#         await bot.process_commands(message)


# @bot.command()
# async def announcenext(ctx, *, time: list):
#     channel = bot.get_channel(933787505591992363)
#     nextFilm = table.getSoonestFilm()
#     await channel.send('{}, Через {} мы будем смотреть фильм! Текущий фильм для просмотра:\n'
#                        '    > {}\n\n Отмечайте, будете ли вы смотреть кино.'.format(
#         ctx.guild.get_role(934194081490415698).mention, ''.join(time), nextFilm.name))


@bot.command()
async def announcenext(ctx, *, time: list):
    # my id 934194081490415698
    # kur id 934185307933380608
    nextFilm = table.getSoonestFilm()
    message = await ctx.send('{}, Через {} мы будем смотреть фильм! Текущий фильм для просмотра:\n'
                             '    > {}\n\n Отмечайте, будете ли вы смотреть кино.'.format(
        ctx.guild.get_role(934185307933380608).mention, ''.join(time), nextFilm.name))
    await message.add_reaction('✅')
    await message.add_reaction('❌')


@bot.command()
async def watched(ctx):
    films = table.getWatchedFilms()
    retStr = 'Список просмотренных фильмов:\n'
    for film in films:
        retStr += ' > ' + film.name + '  -  ' + film.author + '  -  ' + film.rate + '\n'
    await ctx.send(retStr)


# @bot.command()
# async def hello(ctx):
#     # author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.
#     await ctx.send('hello')


# @bot.command()
# async def announce(ctx):
#     await ctx.send('@everyone Привет')


# @bot.command()
# async def getId(ctx):
#     authorId = ctx.message.author.id
#     await ctx.send(authorId)


# @bot.command()
# async def getRoleMembers(ctx):
#     roles = ctx.guild.get_role(934194081490415698)
#     print(roles.members)


# @bot.command()
# async def testText(ctx, *, arg):
#     print(arg)
#     await ctx.send('You sent {}'.format(arg))


@bot.command()
async def films(ctx):
    names = table.getAllFilms()
    retStr = 'Список всех фильмов:\n'
    for name in names:
        retStr += ' > ' + name + '\n'
    await ctx.send(retStr)


# @bot.command()
# async def react(ctx):
#     message = await ctx.send('Hi')
#     await message.add_reaction('✅')


def createContentForFilmInfo(groups):
    retStr = 'Список всех фильмов. Для управления, воспользуйтесь кнопками снизу.\nТекущая страница {}:\n'.format(info.currentPage + 1)
    for i, name in enumerate(groups[info.currentPage]):
        retStr.format(1)
        retStr += ' > ' + emojiNumList[i] + ' ' + name + '\n'
    return retStr


def createInfoAboutFilm(film):
    embed = discord.Embed(title=film.name, colour=discord.Colour.orange())
    embed.add_field(name='Статус:', value=film.status, inline=False)
    embed.add_field(name='Предложил:', value=film.author, inline=False)
    if film.description:
        embed.add_field(name='Комментарий:', value=film.description, inline=False)
    embed.add_field(name='Оценка:', value=film.rate, inline=False)
    return embed


@bot.command() # good; later connect kinopoisk api
async def filmsinfo(ctx):
    info.currentPage = 0
    filmsArr = table.films
    names = [film.name for film in filmsArr]
    filmsGroup = [filmsArr[d:d + 10] for d in range(0, len(filmsArr), 10)]
    groups = [names[d:d + 10] for d in range(0, len(names), 10)]
    info.countOfGroups = len(groups)
    retStr = createContentForFilmInfo(groups)
    message = await ctx.send(retStr)
    print(info.countOfGroups)
    for i in range(len(groups[0])):
        await message.add_reaction(emojiNumList[i])
    await message.add_reaction('⬇')

    def check(reaction, user):
        return user == ctx.author and (str(reaction.emoji) in emojiNumList or str(
            reaction.emoji) == '⬆' or str(
            reaction.emoji) == '⬇')

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=300.0, check=check)
            if str(reaction.emoji) in emojiNumList:
                for i, curEmoji in enumerate(emojiNumList):
                    if str(reaction.emoji) == curEmoji:
                        curFilm = filmsGroup[info.currentPage][i]
                        filmString = createInfoAboutFilm(curFilm)
                        await ctx.send(embed=filmString)
                        await message.clear_reactions()
                        return
            if str(reaction.emoji) == '⬇':
                if info.currentPage == 0:
                    await message.clear_reaction('⬇')
                    await message.add_reaction('⬆')
                    await message.add_reaction('⬇')
                info.currentPage += 1
                retStr = createContentForFilmInfo(groups)
                await message.edit(content=retStr)
                # await message.remove_reaction('⬇', user)
                if info.currentPage == len(groups) - 1:
                    await message.clear_reaction('⬇')

            if str(reaction.emoji) == '⬆':
                if user != ctx.author:
                    await message.remove_reaction('⬆', user)
                    continue
                if info.currentPage == len(groups) - 1:
                    await message.add_reaction('⬇')
                info.currentPage -= 1
                retStr = createContentForFilmInfo(groups)
                await message.edit(content=retStr)
                # await message.remove_reaction('⬆', user)
                if info.currentPage == 0:
                    await message.clear_reaction('⬆')

            if reaction.count >= 2:
                await message.remove_reaction(str(reaction.emoji), user)
        except TimeoutError:
            await ctx.send('timeout')


# @bot.command()
# async def users(ctx):
#     users = table.getUserNames()
#     retStr = 'List of all users:\n'
#     for user in users:
#         retStr += ' > ' + user + '\n'
#     await ctx.send(retStr)


@bot.command()
async def planned(ctx):
    names = table.getPlannedFilms()
    retStr = 'Список запланированных фильмов:\n'
    for name in names:
        retStr += ' > ' + name + '\n'
    await ctx.send(retStr)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Список Команд', colour=discord.Colour.orange())
    embed.add_field(name='-films', value='Выводит список всех фильмов', inline=False)
    embed.add_field(name='-planned', value='Выводит список запланированных фильмов', inline=False)
    embed.add_field(name='-filmsinfo', value='Вывовид список всех фильмов с возможностью просмотра подробной информации', inline=False)
    embed.add_field(name='-watched', value='Выводит список просмотренных фильмов', inline=False)
    embed.add_field(name='-announcenext "время(без ковычек)"', value='Создает оповещение о просмотре фильма. В начале сообщения имеется слово "Через", учитывайте это при указания времени в команде', inline=False)
    embed.add_field(name='-tablelink', value='Выводит ссылку на гугл таблицу', inline=False)
    embed.add_field(name='-votefilm "название фильма(в ковычках)"', value='Создает оповещение с голосованием, о том что будем смотреть указанный фильм', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def tablelink(ctx):
    await ctx.send('Сслыка на таблицу.\nhttps://docs.google.com/spreadsheets/d/1UeX3KFw_7Ed5zosY1cBok2fX5iSui13-VIYwjG-qzmY/edit#gid=0')


@bot.command()
async def votefilm(ctx, *, args):
    channel = bot.get_channel(933512604784148520)
    filmStr = ''.join(args)
    if filmStr[0] == '"' and filmStr[len(filmStr) - 1] == '"':
        filmStr = filmStr[1:-1]
        for film in table.films:
            print(film.name.lower(), filmStr.lower())
            if film.name.lower().find(filmStr.lower()) > -1:
                embed = createInfoAboutFilm(film)
                message = await channel.send(content='{},\n Сегодня вечером смотрим `{}`. Точное время определится позже.\nГолосуйте будете ли вы смотреть.'.format(
                    ctx.guild.get_role(934185307933380608).mention, film.name), embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('❌')
                return
        await channel.send('Фильм не найден(\nПроверьте правильно ли написано название.')
    else:
        await ctx.send('Название фильма указывается внутри ковычек: -votefilm "film name"')


updateTableLoop.start()
bot.run(TOKEN)
