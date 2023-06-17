import discord
import random
import requests
import json
import time
from discord.ext import commands
import datetime
import asyncio
from bs4 import BeautifulSoup as bs
import re
import psycopg2
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")
DB_HOST = os.environ.get("DB_HOST")
token = os.environ.get("token")

crackwatchChannelID = "690848303491055657"
fitgirlChannelID = "691633387735351297"


def connect():
  con = psycopg2.connect(database = DB_NAME, user = DB_USER, password = DB_PASS,host= DB_HOST,port= DB_PORT)
  return con

print('connected')
def read(rowName):
  con = connect()
  cur = con.cursor()
  # cur.execute("INSERT INTO discordbot (NAME,GAME) VALUES('crack', 'testcrack')")
  # cur.execute("INSERT INTO discordbot (NAME,GAME) VALUES('fitgirl', 'testfitgirl')")
  cur.execute(f"SELECT GAME FROM discordbot WHERE NAME = '{rowName}'")
  rows = cur.fetchall()
  name = rows[0][0]
  #print(rows[0][0])
  #print(f'selected game {name} from {rowName}')
  con.close()
  return name

def update(rowName,gameName):
  con = connect()
  cur = con.cursor()
  # cur.execute("INSERT INTO discordbot (NAME,GAME) VALUES('crack', 'testcrack')")
  # cur.execute("INSERT INTO discordbot (NAME,GAME) VALUES('fitgirl', 'testfitgirl')")
  cur.execute(f"UPDATE discordbot set GAME = '{gameName}' WHERE NAME = '{rowName}'")
  con.commit()
  #print(f'updated {rowName} with game {gameName}')
  con.close()

# read('crack')
# update('crack','test game name')
# read('crack')
# &is_aaa=true  &sort_by=crack_date
insults = ['noob']
client = commands.Bot(command_prefix='.')
client.remove_command("help")

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game('Type .help'))
  print(f'the {client.user.name} is ready.')

@client.command()
async def help(ctx):
  author = ctx.message.author
  embed = discord.Embed(colour = discord.Colour.from_rgb(255, 192, 0))
  embed.set_author(name='Help',icon_url='https://upload.wikimedia.org/wikipedia/commons/f/f6/Lol_question_mark.png')
  embed.add_field(name='.ping', value='katla3 lek l ping dyal bot awld l9a7ba ach kaysab lek',inline = False)
  embed.add_field(name='.3ayr', value='bach t3ayr biha zwaml dyal server',inline = False)
  embed.add_field(name='.helpme', value='katsift lek Help message l DM dyalek',inline = False)
  embed.add_field(name='.help', value='katsift lek Help message f discord server',inline = False)
  embed.add_field(name='.crackwatch/.crack/.watch ["all";"aaa";"indie"] [1=>25]', value='katsift lek ga3 new cracked games li kaynin f crackwatch ex: .crack AAA 10 or .crackwatch all 20',inline = False)
  embed.add_field(name='.fitgirl/.fit-girl/.fit [1=>8]', value='katsift lek ga3 new repacks li kaynin FitGirl ex: .fitgirl or .fit 5',inline = False)
  embed.add_field(name='more info',value='Bot was made by MicroGOD#7389, more commands will be added in the future',inline = False)
  embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def helpme(ctx):
  author = ctx.message.author
  embed = discord.Embed(colour = discord.Colour.from_rgb(255, 192, 0))
  embed.set_author(name='Help',icon_url='https://upload.wikimedia.org/wikipedia/commons/f/f6/Lol_question_mark.png')
  embed.add_field(name='.ping', value='katla3 lek l ping dyal bot awld l9a7ba ach kaysab lek',inline = False)
  embed.add_field(name='.3ayr', value='bach t3ayr biha zwaml dyal server',inline = False)
  embed.add_field(name='.helpme', value='katsift lek Help message l DM dyalek',inline = False)
  embed.add_field(name='.help', value='katsift lek Help message f discord server',inline = False)
  embed.add_field(name='.crackwatch/.crack/.watch ["all";"aaa";"indie"] [1=>25]', value='katsift lek ga3 new cracked games li kaynin f crackwatch ex: .crack AAA 10 or .crackwatch all 20',inline = False)
  embed.add_field(name='.fitgirl/.fit-girl/.fit [1=>9]', value='katsift lek ga3 new repacks li kaynin FitGirl ex: .fitgirl or .fit 5',inline = False)
  embed.add_field(name='more info',value='Bot was made by MicroGOD#7389, more commands will be added in the future',inline = False)
  embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
  await author.send(embed=embed)

@client.command()
async def ping(ctx):
  await ctx.send(f'the ping is {round(client.latency * 1000)}ms')

@client.command(aliases=["3ayr"])
async def _3ayr(ctx, member : discord.Member):
  member = str(member).split("#")[0]
  await ctx.send(f'{member} {random.choice(insults)}')

jsonData = ''
@client.command(aliases=['crack','watch'])
async def crackwatch(ctx,sort_by='all',number=25):
  namelist = []
  isAAAlist = []
  grouplist = []
  urllist = []
  crackDatelist = []
  releaseDatelist = []
  imagelist = []
  deltalist = []
  if sort_by.strip().lower() in ['all']:
    crurl = 'https://api.crackwatch.com/api/games?page=0&is_released=true&is_cracked=true&sort_by=crack_date'
  else:
    if sort_by.lower().strip() in ['aaa']:
      crurl = 'https://api.crackwatch.com/api/games?page=0&is_released=true&is_cracked=true&is_aaa=true&sort_by=crack_date'
    elif sort_by.lower().strip() in ['indie']:
      crurl = 'https://api.crackwatch.com/api/games?page=0&is_released=true&is_cracked=true&is_aaa=false&sort_by=crack_date'
  g = requests.get(crurl)
  global jsonData
  jsonData = json.loads(g.text)
  for game in jsonData:
    name = game['title']
    isAAA = game['isAAA']
    group = ','.join(game['groups'])
    gameUrl = game["url"]
    crackDate = game["crackDate"].split("T")[0]
    deltaCrackDate = datetime.datetime.strptime(crackDate,"%Y-%m-%d")
    crackDate = datetime.datetime.strptime(crackDate,"%Y-%m-%d").date()
    crackDate = datetime.datetime.strftime(crackDate,"%d/%m/%Y")
    try:
      image = game['image']
    except:
      image = 'https://b2.crackwatch.com/file/crackwatch/public/Image.jpg'
    releaseDate = game['releaseDate'].split("T")[0]
    deltaReleaseDate = datetime.datetime.strptime(releaseDate,"%Y-%m-%d")
    releaseDate = datetime.datetime.strptime(releaseDate,"%Y-%m-%d").date()
    releaseDate = datetime.datetime.strftime(releaseDate,"%d/%m/%Y")
    delta = (deltaCrackDate - deltaReleaseDate).days
    deltalist.append(delta)
    #print(delta)
    namelist.append(name)
    isAAAlist.append(isAAA)
    grouplist.append(group)
    urllist.append(gameUrl)
    crackDatelist.append(crackDate)
    releaseDatelist.append(releaseDate)
    imagelist.append(image)
    embed = discord.Embed(title='CrackWatch List',url='https://crackwatch.com/games',colour = discord.Colour.from_rgb(218, 17, 6))
    #embed.set_image(url='https://i.imgur.com/hL2z8Gc.png')
    #embed.set_thumbnail(url='https://i.imgur.com/hL2z8Gc.png')
    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
    embed.set_author(name='Crackwatch Updates',icon_url='https://i.imgur.com/DsoTKfT.png')
    for i, name, isAAA, group, url, crackDate, releaseDate, image, delta in zip(range(1,number+1),namelist,isAAAlist,grouplist,urllist,crackDatelist,releaseDatelist,imagelist,deltalist):
      if isAAA == True:
        isAAA = "AAA Game"
      else:
        isAAA = "Indie Game"
      head = f'#{i}'
      if delta in [1,-1]:
        days = 'day'
      else:
        days = 'days'
      rzlt = f'[{name}]({url}) [{isAAA}] cracked in {crackDate} by {group} group after {delta} {days} from release'
      embed.add_field(name=head, value=rzlt,inline = False)
  await ctx.send(embed=embed)

rightNumber = 8
@client.command(aliases=['FitGirl-Repacks','FitGirl-repacks','Fitgirl-repacks','Fit-Girl','Fit-girl','Fit-Girls','Fit-girls','FitGirl','Fitgirl','FitGirls','Fitgirls','Fit','fit','fitgirls','fit-girls','fit-girl','fitgirl-repacks'])
async def fitgirl(ctx,number=rightNumber):
  fitUrl = "https://fitgirl-repacks.site/"
  g = requests.get(fitUrl)
  soup = bs(g.text,'html.parser')
  articles = soup.findAll("article",{'class':re.compile(r'.+ category-lossless-repack')})
  global rightNumber
  rightNumber = len(articles)
  gameNames = []
  gameUrls = []
  gameImages = []
  gameGBs = []
  gameOriginalSizes = []
  gameMinSizes = []
  for article in articles:
    gameName = article.find('a',{'rel':'bookmark'}).getText()
    gameNames.append(gameName)
    gameUrl = article.find('a',{'rel':'bookmark'})['href']
    gameUrls.append(gameUrl)
    gameImage = article.find('img',{'class':'alignleft'})['src']
    gameImages.append(gameImage)
    gameGB= article.findAll("strong",text=re.compile(r'(GB|MB)'))
    if gameGB == []:
      gameOriginalSize = 'no OriginalSize'
      gameOriginalSizes.append(gameOriginalSize)
      gameMinSize = 'no MinSize'
      gameMinSizes.append(gameMinSize)
    else:
      gameOriginalSize = gameGB[0].getText()
      gameOriginalSizes.append(gameOriginalSize)
      gameMinSize = gameGB[1].getText()
      gameMinSizes.append(gameMinSize)
    #print(gameOriginalSize,gameMinSize)
  embed = discord.Embed(title='FitGirl Repacks List',url='https://fitgirl-repacks.site/',colour = discord.Colour.from_rgb(248, 135, 255))
  #embed.set_image(url='https://i.imgur.com/hL2z8Gc.png')
  #embed.set_thumbnail(url='https://i.imgur.com/hL2z8Gc.png')
  embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
  embed.set_author(name='FitGirl Updates',icon_url='https://fitgirl-repacks.site/wp-content/uploads/2016/08/cropped-icon-192x192.jpg')
  for i, gameName, gameUrl, gameImage, gameOriginalSize, gameMinSize in zip(range(1,number+1), gameNames, gameUrls, gameImages, gameOriginalSizes,gameMinSizes):
    head = f'#{i}'
    rzlt = f'[{gameName}]({gameUrl}): Original Size [{gameOriginalSize}] and Repack Size [{gameMinSize}]'
    embed.add_field(name=head, value=rzlt,inline = False)
  await ctx.send(embed=embed)


# async def rolekhayb(ctx, role: discord.Role):
#   await client.wait_until_ready()
#   role = discord.utils.get(ctx.message.server.roles, name="Dyal Lma3your")
#   if role is None:
#     print('no role')
#     return
#   empty = True
#   for member in ctx.message.server.members:
#     if role in member.roles:
#       channel = client.get_channel(689427519564153026)
#       await channel.say("it works")
#       empty = False
#   if empty:
#     print('ta7d ma3ndo had role')

async def fitloop():
  await client.wait_until_ready()
  while not client.is_closed():
    try:
      ref = read('fitgirl')
      # with open('fitgirls.txt','r') as txt:
      #   ref = txt.read().splitlines()[0].strip()
      print(f'fitgirl ref : {ref}')
      fitUrl = 'https://fitgirl-repacks.site/'
      g = requests.get(fitUrl)
      soup = bs(g.text,'html.parser')
      fitFirstGame = soup.findAll("article",{'class':re.compile(r'.+ category-lossless-repack')})[0]
      firstGameName = fitFirstGame.find('a',{'rel':'bookmark'}).getText().strip()
      print(f'fitgirl game : {firstGameName}')
      if firstGameName == ref:
        print("fitgirl no Game")
        await asyncio.sleep(30)
        continue
      elif firstGameName != ref:
        update('fitgirl',firstGameName)
        # with open('fitgirls.txt','w') as modify:
        #   modify.write(firstGameName.strip())
        firstGameUrl = fitFirstGame.find('a',{'rel':'bookmark'})['href']
        firstGameImage = fitFirstGame.find('img',{'class':'alignleft'})['src']
        firstGameGB = fitFirstGame.findAll("strong",text=re.compile(r'(GB|MB)'))
        if firstGameGB == []:
          firstGameOriginalSize = None
          firstGameMinSize = None
        else:
          firstGameOriginalSize = firstGameGB[0].getText()
          firstGameMinSize = firstGameGB[1].getText()
      embed = discord.Embed(title='FitGirl Latest Repack',url=firstGameUrl,colour = discord.Colour.from_rgb(248, 135, 255))
      if firstGameImage != None:
        embed.set_image(url=firstGameImage)
      else:
        pass
      embed.add_field(name=f'{firstGameName}',value=f'[{firstGameName}]({firstGameUrl}): Original Size [{firstGameOriginalSize}] and Repack Size [{firstGameMinSize}]')
      embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
      embed.set_author(name='FitGirl Updates',icon_url='https://fitgirl-repacks.site/wp-content/uploads/2016/08/cropped-icon-192x192.jpg')
      channel = client.get_channel(fitgirlChannelID)
      await channel.send(embed=embed)
      await asyncio.sleep(30)
      continue
    except Exception as e:
      print(e)
      with open('fitlogs.txt','a') as fitlogs:
        fitlogs.write(f'Exception : {e} \nTime : {datetime.datetime.now()}\n\n')
      continue

async def crackloop():
  await client.wait_until_ready()
  #_id = jsonData[0]['_id']
  while not client.is_closed():
    try:
      ref = read('crack')
      # with open('id.txt','r') as txt:
      #   ref = txt.read().splitlines()[0].strip()
      print(f'crack ref : {ref}')
      crloopurl = 'https://api.crackwatch.com/api/games?page=0&is_released=true&is_cracked=true&sort_by=crack_date'
      g = requests.get(crloopurl)
      idFirstGame = json.loads(g.text)[0]['title'].strip()
      print(f'crack game : {idFirstGame}')
      if idFirstGame == ref:
        print("crack no Game")
        await asyncio.sleep(30)
        continue
      elif idFirstGame != ref:
        print("new Game")
        update('crack',idFirstGame)
        # with open('id.txt','w') as modify:
        #   modify.write(idFirstGame.strip())
        FirstGame = json.loads(g.text)[0]
        name = FirstGame['title']
        isAAA = FirstGame['isAAA']
        if isAAA == True:
          isAAA = "AAA Game"
        else:
          isAAA = "Indie Game"
        group = ','.join(FirstGame['groups'])
        gameUrl = FirstGame["url"]
        crackDate = FirstGame["crackDate"].split("T")[0]
        deltaCrackDate = datetime.datetime.strptime(crackDate,"%Y-%m-%d")
        crackDate = datetime.datetime.strptime(crackDate,"%Y-%m-%d").date()
        crackDate = datetime.datetime.strftime(crackDate,"%d/%m/%Y")
        try:
          image = FirstGame['image']
        except:
          image = 'https://b2.crackwatch.com/file/crackwatch/public/Image.jpg'
        releaseDate = FirstGame['releaseDate'].split("T")[0]
        deltaReleaseDate = datetime.datetime.strptime(releaseDate,"%Y-%m-%d")
        releaseDate = datetime.datetime.strptime(releaseDate,"%Y-%m-%d").date()
        releaseDate = datetime.datetime.strftime(releaseDate,"%d/%m/%Y")
        delta = (deltaCrackDate - deltaReleaseDate).days
        embed = discord.Embed(title='CrackWatch Latest Game',url=gameUrl,colour = discord.Colour.from_rgb(218, 17, 6))
        if image != None:
          embed.set_image(url=image)
        else:
          pass
        if delta in [1,-1]:
          days = 'day'
        else:
          days = 'days'
        embed.add_field(name=f'{name}',value=f'[{name}]({gameUrl}): [{isAAA}] cracked in {crackDate} by {group} group after {delta} {days} from release')
        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
        embed.set_author(name='CrackWatch Updates',icon_url='https://i.imgur.com/DsoTKfT.png')
        channel = client.get_channel(crackwatchChannelID)
        await channel.send(embed=embed)
        await asyncio.sleep(30)
        continue
    except Exception as f:
      print(f)
      with open('cracklogs','a') as cracklogs:
        cracklogs.write(f'Exception : {f} \nTime : {datetime.datetime.now()}\n\n')
      continue



#client.loop.create_task(crackloop())
client.loop.create_task(fitloop())
client.run(token)
