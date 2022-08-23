""" 
crystalline-entity.py

Created by espais to fulfill the needs of the many (or the /r/startrekgifs users).

Based on the delightful bot by Frenza. Fingers crossed it lives beyond April 22.



TODO
* !list command
* !help command
"""

import discord
from dotenv import load_dotenv
import os, sys
import json
import asyncio
import random

class CrystallineClient(discord.Client):
  def update_gifs(self, gifs=None):
    if gifs:
      self.gifs = gifs
    else:
      self.gifs = {}

  # Make a copy of the database and write out the gif archive
  def backupDB(self):
    if os.path.exists(os.getenv('IMG_DB')):
      os.rename(os.getenv('IMG_DB'), os.getenv('IMG_DB_BAK'))
    with open(os.getenv('IMG_DB'), 'w') as f:
      f.write(json.dumps(self.gifs))

  async def on_ready(self):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for gif requests'))
    print('Logged in as {0}'.format(self.user))

  async def on_message(self, message):
    # ignore self
    if message.author == self.user:
      return

    if message.content == "!help":
      desc = "!list - list all gifs\n"
      desc += "Message espais for additional feature requests"
      embed = discord.Embed(title="Crystalline Entity Help", description=desc, color=discord.Color.blue())
      embed.set_thumbnail(url=self.user.avatar_url)
      msg = await message.channel.send(embed=embed)

      #await message.channel.send("TBD ಠ_ಠ")
    #elif message.content == "!list":
    #  await message.channel.send("TBD ಠ_ಠ")

    elif message.content[:5] == ".away": # away message
      # really need to make this a fxn
      isAdmin = False
      for r in message.author.roles:
        if r.name == 'Starfleet Command':
          isAdmin = True
          break

      # Only admins allowed
      if isAdmin:
        msg = message.content.split()
        if ((msg[1] == "streaming") or (msg[1] == "playing") or (msg[1] == "listening") or (msg[1] == "watching")):
          amsg = ""
          for i in range(2,len(msg)):
            amsg += msg[i] + " "
          amsg.strip()

          # set activity
          act = discord.ActivityType.watching
          if msg[1] == "streaming":
            act = discord.ActivityType.streaming
          elif msg[1] == "playing":
            act = discord.ActivityType.playing
          elif msg[1] == "listening":
            act = discord.ActivityType.listening
          else:
            act = discord.ActivityType.watching

          await client.change_presence(activity=discord.Activity(type=act, name="{0}".format(amsg)))
        else:
          await message.channel.send('Malformed away message: `.away playing|watching|streaming|listening your custom message`')

    elif message.content == "!list":
        _resp = ""
        _pages = []
        iter = 1
        page_iter = 0
        for k,v in self.gifs.items():
            next = "{0}: {1} | {2}\n".format(iter,k,v)

            if (len(_resp + next) > 2000):
                _pages.append(_resp)
                _resp = next
            else:
                _resp += next
            iter += 1

        embed = discord.Embed(title="GIFS page [{0}/{1}]".format(page_iter+1,len(_pages)), description=_pages[0], color=discord.Color.blue())
        msg = await message.channel.send(embed=embed)#_resp)

        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

        # user is the clicker,
        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" :

                    page_iter += 1
                    if page_iter > len(_pages)-1:
                        page_iter = 0

                    # edit and remove react
                    embed = discord.Embed(title="GIFS page [{0}/{1}]".format(page_iter+1,len(_pages)), description=_pages[page_iter], color=discord.Color.blue())
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️":
                    page_iter -= 1
                    if page_iter < 0:
                        page_iter = len(_pages)-1

                    # edit and remove react
                    embed = discord.Embed(title="GIFS page [{0}/{1}]".format(page_iter+1,len(_pages)), description=_pages[page_iter], color=discord.Color.blue())
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(reaction, user)




            except asyncio.TimeoutError:
                #await msg.add_reaction(reaction="◀️", member=self.user)
                #await msg.add_reaction(reaction="▶️", member=self.user)
                break


    elif message.content == "!gifme":
      _key = random.choice([k for k in self.gifs.keys()])
      _resp = "Use with: {0}\n{1}".format(_key, random.choice(self.gifs[_key]))
      await message.channel.send(_resp)
      #await message.channel.send(random.choice(self.gifs[_key]))

    elif message.content == "!scanchannel":
      isAdmin = False
      for r in message.author.roles:
        if r.name == 'Starfleet Command':
          isAdmin = True
          break

      # Only admins allowed
      if isAdmin:
        channel = self.get_channel(457943604200079371)
        messages = await channel.history(limit=5000).flatten()
        await message.channel.send("Scanning #bot-commands in progress")
        await message.channel.send("{0} messages scanned".format(len(messages)))
        for msg in messages:
          if ".acr" in msg.content:
            _msg = msg.content.split()
            if msg.content[:4] == ".acr" and len(_msg) == 3 and _msg[1][:2] == '"!' and (_msg[2][-5:] == ".gifv" or _msg[2][-4:] == ".gif" or "gfycat" in _msg[2]):
#            try:
              # Break down the post into something manageable
              _title = _msg[1][1:]
              _title = _title[:-1]
  
              _resp = ""

              # create the entry and push the gif 
              if _title not in self.gifs.keys():
                self.gifs[_title] = []
              if _msg[2] not in self.gifs[_title]:
                self.gifs[_title].append(_msg[2])
                _resp = "Adding {0} with link {1} to database.".format(_title, _msg[2])
              #self.gifs[_title].append(msg[2])
              if _resp != "":
                print(_resp)


        # Move the old database to a backup and write
        self.backupDB()



    # Add a gif to the database (add to dictionary, write to file)
    elif message.content[:4] == ".acr": # add a gif
      isAdmin = False
      for r in message.author.roles:
        if r.name == 'Starfleet Command':
          isAdmin = True
          break

      # Only admins allowed
      if isAdmin:
        msg = message.content.split()
        if len(msg) == 3 and msg[1][:2] == '"!' and (msg[2][-5:] == ".gifv" or msg[2][-4:] == ".gif" or "gfycat" in msg[2]):
#          try:
            # Break down the post into something manageable
            _title = msg[1][1:]
            _title = _title[:-1]
  
            _resp = "Adding {0} with link {1} to database.".format(_title, msg[2])

            # create the entry and push the gif 
            if _title not in self.gifs.keys():
              self.gifs[_title] = []
            self.gifs[_title].append(msg[2])

            print(self.gifs)
  
            # Move the old database to a backup and write
            self.backupDB()
            #if os.path.exists(os.getenv('IMG_DB')):
            #  os.rename(os.getenv('IMG_DB'), os.getenv('IMG_DB_BAK'))
            #with open(os.getenv('IMG_DB'), 'w') as f:
            #  f.write(json.dumps(self.gifs))
  
            # Notify us that IT IS DONE
            await message.channel.send("Darmok and Jalad at {0}.".format(_title))
            print(_resp)
#          except:
#            print("Something went wrong!")

        else:
          await message.channel.send('Malformed image addition: .acr "!reaction" http://link-to-image.gifv')
      else:
        print("User {0} attempted to add gif without permission!".format(message.author))

    elif message.content in self.gifs.keys():
      await message.channel.send(random.choice(self.gifs[message.content]))


# Get environment variables in (so we mainly use the .env file)
load_dotenv()

# Load all gifs from file
# * Format: {'react':'link'}
the_gifs = {}
if os.path.exists(os.getenv('IMG_DB')):
  with open(os.getenv('IMG_DB'), 'r') as f:
    the_gifs = json.loads(f.read())
    print('Image database loaded.')
else:
  print('No images, starting from scratch!')

client = CrystallineClient()
# There's probably a better way to do this but it is late
# and I don't recall the syntax for overriding an existing
# Python class.
client.update_gifs(the_gifs)
client.run(os.getenv('TREK_TOKEN'))
