import discord
import random
import os
import requests
import json
import urllib.request
import pytz
from discord.ext import tasks
from datetime import datetime
from discord import Spotify
import asyncio

#jambo pictures
jamboArray = ['https://tinyurl.com/bdmbntww',
              'https://tinyurl.com/2jhfjdsh',
              'https://tinyurl.com/bp89h77c',
              'https://tinyurl.com/45mw9n2u',
              'https://tinyurl.com/yt3b4mdh',
              'https://tinyurl.com/5e3kakhf',
              'https://tinyurl.com/2p8354ds',
              'https://tinyurl.com/27stuacp',
              'https://tinyurl.com/8x26wwrd',
              'https://tinyurl.com/mtpxu52v',
              'https://tinyurl.com/m8e3fjsh',
              'https://tinyurl.com/25f8ve7x',
             ]

#commands
cmdArr = ['0',
          'spam',
          'clean',
          'jambo',
          'pspsps',
          'game',
          'scran',
          'recipe',
          'birb',
          'trash',
          'mev',
          'panda',
          'duck',
          'fredge',
          'spotify',
          'cocktail'
         ]

#commands prefix
prefix = '.'

#APIKEY for RiotGames API
APIKEY = ''
#Discord Bot Token
TOKEN = ''
#NASA APIKEY
NASAKEY = 'insert key'
#Picture Links
cleangif = 'https://media.discordapp.net/attachments/356086277759827972/715367679690539028/emote.gif'
#File paths
path = r'/home/container/Mev'

#Riot API URLS
sv4url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
cgurl = 'https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'

#create a random jambo picture
def jamboRan():
  num = random.randint(0, len(jamboArray)-1)
  return jamboArray[num]

#game grabbing functionality
def makeBlue(data):
  blueStr = 'https://euw.op.gg/multisearch/euw?summoners='
  for i in range(0, 5):
    blueStr = blueStr + data['participants'][i]['summonerName'].replace(' ', '%20') + ','
  return '**Blue Team**\n'+blueStr

def makeRed(data):
  redStr = 'https://euw.op.gg/multisearch/euw?summoners='
  for i in range(5,10):
    redStr = redStr + data['participants'][i]['summonerName'].replace(' ', '%20') + ','
  return '**Red Team**\n'+redStr

#random recipe using the API
def makeRecipe(data):
  str1 = '\n**Ingredients:**\n'
  for i in range(1,20):
    if data['strIngredient'+str(i)] != "":
      str1 = str1 + data['strMeasure'+str(i)] + ' ' + data['strIngredient'+str(i)] + '\n'
  str1 = str1 + '\n`'+data['strInstructions']+'`'
  return str1

#help command outputs all commands
def commandsHelp():
  helpStr = '*Prefix is.*\n**Commands are:**\n`'
  for i in cmdArr:
    helpStr = helpStr + i + '\n'
  return helpStr + '`'

#urllib to get data from URL for API
def getRequest(inUrl):
  with urllib.request.urlopen(inUrl) as url:
    data = json.loads(url.read())
    return data

#discord setup
intents = discord.Intents.all()
intents.presences = True
client = discord.Client(intents=intents)

#Bot startup text
@client.event
async def on_ready():
  print("Bot is online as {0.user}".format(client))
  
#Bot commands
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  #ratio command
  if 'ratio' in message.content.lower():
    if message.author.id != 199200554713481216:
      await message.add_reaction('👍')
      await message.add_reaction('⬆️')
      await message.add_reaction('🔼')
  
  #help command
  if message.content == (prefix + 'help'):
    await message.channel.send(commandsHelp())
    
  #spam
  if message.content.startswith(prefix + cmdArr[1] + ' '):
    target = message.content[6:]
    if target == '<@538768557971079178>':
      target = '<@'+str(message.author.id)+'>'
    for i in range(5):
      await message.channel.send(target)
  
  #clean command
  if message.content == (prefix + cmdArr[2]):
    for i in range(5):
      await message.channel.send(cleangif)
  
  #jambo random image
  if message.content == ( prefix + cmdArr[3]):
    await message.channel.send(jamboRan())
  
  #cat API image
  if message.content == (prefix + cmdArr[4]):
    data = getRequest('https://api.thecatapi.com/v1/images/search')
    await message.channel.send(data[0]['url'])
  
  # search live game LoL
  if message.content == (prefix + cmdArr[5]):
    name = message.content[5:].replace(' ', '%20')
    try:
      data = getRequest(sv4url+name+'?api_key='+APIKEY)
      pid = data['id'].replace(' ', '%20')
      lolProsLink = 'https://lolpros.gg/live/'+data['name'].replace(' ', '')
      try:
        data = getRequest(cgurl+pid+'?api_key='+APIKEY)
        await message.channel.send('**LOLPROS LINK:**\n'+lolProsLink+'\n'+makeBlue(data)+ '\n'+makeRed(data))
      except:
        await message.channel.send('User is not ingame')
    except:
      await message.channel.send('Not a real username on EUW')
  
  #random scran API
  if message.content == (prefix + cmdArr[6]):
    data = getRequest('https://foodish-api.herokuapp.com/api/')
    await message.channel.send(data['image'])
  
  #random recipe API
  if message.content == (prefix + cmdArr[7]):
    data = getRequest('https://www.themealdb.com/api/json/v1/1/random.php')
    await message.channel.send('**'+data['meals'][0]['strMeal']+'**')
    await message.channel.send(data['meals'][0]['strMealThumb'])
    await message.channel.send(makeRecipe(data['meals'][0]))
  
  #random bird API
  if message.content == (prefix + cmdArr[8]):
    data = getRequest('https://some-random-api.ml/animal/birb')
    await message.channel.send(data['image'])
    await message.channel.send('**FACT: **' + data['fact'])
  
  #random raccoon API
  if message.content == (prefix + cmdArr[9]):
    data = getRequest('https://some-random-api.ml/animal/raccoon')
    await message.channel.send(data['image'])
    await message.channel.send('**FACT: **' + data['fact'])
  
  #random mev picture
  if message.content == (prefix + cmdArr[10]):
    random_filename = random.choice([
      x for x in os.listdir(path)
      if os.path.isfile(os.path.join(path, x))
    ])
    if message.channel.id != 689832620304891919:
      await message.channel.send('go check <#689832620304891919>')
    await client.get_channel(689832620304891919).send(file=discord.File(path+'/'+random_filename))
  
  #random panda API
  if message.content == (prefix + cmdArr[11]):
    data = getRequest('https://some-random-api.ml/animal/panda')
    await message.channel.send(data['image'])
    await message.channel.send('**FACT: **' + data['fact'])
  
  #random duck API
  if message.content == (prefix + cmdArr[12]):
    num = random.randint(0,282)
    await message.channel.send('https://random-d.uk/api/' + str(num) + '.jpg')
  
  #fredbear
  if message.content == (prefix + cmdArr[13]):
    num = random.randint(0,100)
    if num == 0:
      await message.channel.send(file=discord.File(r'/home/container/goldenfred.png'))
    elif num == 1:
      await message.channel.send('https://media.discordapp.net/attachments/727225787648049286/966827807982366740/unknown.png')
    else:
      await message.channel.send(file=discord.File(r'/home/container/fredgebear.png'))     

  #this command is to scour spotify activity
  if message.content == (prefix + cmdArr[14]):
    GUILD = client.get_guild(664864328557658145)
    for member in GUILD.members:
      if isinstance(member.activity, Spotify):
        i = member.activity
        name = member.name
        track = i.title.replace('*', '#')
        album = i.album
        artist = i.artist
        duration = str(int(i.duration.total_seconds()//60)) +':'+ str('%02d' %int(i.duration.total_seconds()%60))
        end = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        start = datetime.strptime(str(i.start), '%Y-%m-%d %H:%M:%S.%f')
        current = str(end-start)[3:7]
        await message.channel.send('__**{0}**__\nListening to **{1}**\nBy **{2}**\nAlbum is **{3}**\nCurrently **{4}/{5}**\n'.format(name, track, artist, album, current, duration))
        
  #cocktail API
  if message.content.startswith(prefix+cmdArr[15]+' '):
    command = message.content[10:]
    if command.lower() == 'random':
      data = getRequest('https://www.thecocktaildb.com/api/json/v1/1/random.php')
      data = data['drinks'][0]
      buildMessage = '**Name:** {0}\n**Glass:** {1}\n**Ingredients:**\n'.format(data['strDrink'], data['strGlass'])
      for i in range(1,15):
        if data['strIngredient'+str(i)] != None:
          buildMessage = buildMessage + data['strIngredient'+str(i)] + ', '
    elif command.lower().startswith('using'):
      command = command[6:]
      embed = discord.Embed(title='Hello Test', description='command')
      await message.channel.send(embed=embed)
    
    await message.channel.send(buildMessage)
  
  
  #LOL TESTING
  if message.content.startswith('.gamecount'):
    name = message.content[10:].replace(' ', '%20')
    data1 = getRequest(sv4url+name+'?api_key='+APIKEY)
    puuid = data1['puuid']
    number = 0
    count = 0
    keepInLoop = True
    while keepInLoop == True:
      data = getRequest('https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?start={1}&count=100&type=ranked&api_key={2}'.format(puuid, number, APIKEY))
      number += 100
      if data != []:
        for i in data:
          count += 1
      else:
        keepInLoop = False
    await message.channel.send('**{0}** has **{1}** games since match history began! (2 years)'.format(data1['name'], count))
    
  if message.content.startswith('.test'):
    name = message.content[5:].replace(' ', '%20')
    data = getRequest(sv4url+name+'?api_key='+APIKEY)
    puuid = data['puuid']
    summoner = data['name']
    matchHistory = getRequest('https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?start=0&count=100&type=ranked&api_key={1}'.format(puuid, APIKEY))
    buildMsg = ''
    winCounter = 0
    lossCounter = 0
    thisDict = {}
    for i in range(90):
      gameData = getRequest('https://europe.api.riotgames.com/lol/match/v5/matches/{0}?api_key={1}'.format(matchHistory[i], APIKEY))
      summonerData = gameData['info']['participants']
      for j in range(10):
        if summonerData[j]['puuid'] == puuid:
          if summonerData[j]['championName'] in thisDict:
            thisDict[summonerData[j]['championName']] += 1
          else:
            thisDict.update({summonerData[j]['championName']: 1})
            
          buildMsg += '**{0} - {1} - '.format(summonerData[j]['championName'], summonerData[j]['lane'])
          if summonerData[j]['win'] == True:
            buildMsg += 'WIN**\n'
            winCounter += 1
          else:
            buildMsg += 'LOSS**\n'
            lossCounter += 1
    totalWinrate = round((winCounter/(winCounter + lossCounter))*100, 2)
    await message.channel.send('**{0}%** winrate'.format(totalWinrate))
    buildMsg = ''
    x = sorted(thisDict.items(), key=lambda x: x[1])
    for i in reversed(x):
      buildMsg = buildMsg + 'Played **{0}** games of **{1}**\n'.format(i[1], i[0])
    await message.channel.send(buildMsg)
      
      
  ##############################
  
  
  
  #testing for activity status
  #if message.content == ('test'):
  #  GUILD = client.get_guild(664864328557658145)
  #  builtString = ''
  #  for member in GUILD.members:
  #    if member.activity != None and 'bots' not in str(member.roles):
  #      if not isinstance(member.activity, discord.CustomActivity):
  #        for i in member.activities:
  #          if '<Activity type=<ActivityType.playing' in str(i):
  #            builtString += '{0} : {1}\n'.format(member.name, i.name)
  #  try:
  #    await message.channel.send(builtString)
  #  except:
  #    await message.channel.send('No users doing anything right now')
        
#voice channel recognition
#@client.event
#async def on_voice_state_update(member, before, after):
#  if after.channel and member.id == 538768557971079178:
#    if before.self_mute or after.self_mute:
#      channel = client.get_channel(689832620304891919)
#      personJoined = 538768557971079178
#      await channel.send('<@{0}> has MUTED'.format(personJoined))
    
#word of the day task loop
@tasks.loop(seconds = 1)
async def myLoop():
  now = datetime.now(pytz.timezone('Europe/London'))
  if now.hour == 1 and now.minute == 0 and now.second == 0:
    await client.wait_until_ready()
    channelLoop = client.get_channel(964634331286999120)
    currentTime = datetime.today().strftime('%d/%m/%y')
    data = getRequest('https://random-word-api.herokuapp.com/word')
    await channelLoop.send('Todays word of the day ('+currentTime+') isssss...... ||**'+data[0]+'**|| ✨')
    data = getRequest('https://api.dictionaryapi.dev/api/v2/entries/en/{0}'.format(data[0]))
    dLength = len(data[0]['meanings'][0]['definitions'])
    defString = '**Definitions**:\n||'
    for i in range(dLength):
      defString = defString + ' - ' + data[0]['meanings'][0]['definitions'][i]['definition'] + '\n'
    await channelLoop.send(defString + '||')

#NASA Picture of the day
@tasks.loop(seconds = 1)
async def nasaLoop():
  now = datetime.now(pytz.timezone('Europe/London'))
  currentTime = datetime.today().strftime('%d/%m/%y')
  if now.hour == 4 and now.minute == 0 and now.second == 0:
    await client.wait_until_ready()
    channel = client.get_channel(968617937143463946)
    data = getRequest('https://api.nasa.gov/planetary/apod?api_key='+NASAKEY)
    await channel.send('Todays NASA picture ({0}) is {1}.'.format(currentTime, data['title']))
    await channel.send(data['hdurl'])
    await channel.send('`{0}`'.format(data['explanation']))
    
            
#start sequence
myLoop.start()
nasaLoop.start()
client.run(TOKEN)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
