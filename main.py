import discord
import os
import requests
import json
import random
from replit import db
from discord.ext import commands
  
my_secret = os.environ['TOKEN']
words=["energy", "tired", "caffeine", "sluggish", "slugabed", "coffee"]

starter_prompts=[
  "Have a coffee!",
  "You NEED a coffee.",
  "Got a Starbucks giftcard?",
  "You need some caffeine :)"
]
bot=commands.Bot(command_prefix='/', description=None)
bot.remove_command("help")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    em = discord.Embed(title = "Slow down!", description = f'**Hey, {ctx.message.author.mention}... slow down!** Try again in {error.retry_after:.1f} seconds.', color = 0xe74c3c)
    await ctx.send(embed = em)

@bot.event
async def on_ready():
  print('We have successfully logged in as @{0.user}.'.format(bot))

@bot.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use /help <command> for extended information on a command.", color = 0x3498db)
  commands = ['/icedcoffee\n /icedespresso\n /coldbrew\n /frappucino\n /nitro\n /mazagran\n']
  description = ''.join(commands)
  em.add_field(name = "Coffee Education", value = description)
  interactiveCommands = ['/add\n /delete\n /index\n']
  description2 =''.join(interactiveCommands)
  em.add_field(name = "Interactive", value = description2)
  await ctx.send(embed = em)

response=requests.get("https://api.sampleapis.com/coffee/iced")
json_data=json.loads(response.text)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def icedcoffee(ctx):
  ingredients=json_data[0]['ingredients']
  ' '.join(ingredients)
  new = str(ingredients).replace('[','').replace(']','')
  file = discord.File('icedcoffee.png')
  em = discord.Embed(title = "Iced Coffee", description = f"**Try {json_data[0]['title']}:** {json_data[0]['description']} The ingredients are: {new}.", color = 0xe67e22)
  await ctx.send(file = file, embed = em)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def icedespresso(ctx):
  ingredients=json_data[1]['ingredients']
  ' '.join(ingredients)
  new = str(ingredients).replace('[','').replace(']','')
  em = discord.Embed(title = "Iced Espresso", description = f"**Try {json_data[1]['title']}:** {json_data[1]['description']} The ingredients are: {new}.", color = 0xe67e22)
  file=discord.File('icedespresso.jpeg')
  await ctx.send(file = file, embed = em)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def coldbrew(ctx):
  ingredients=json_data[2]['ingredients']
  ' '.join(ingredients)
  new = str(ingredients).replace('[','').replace(']','')
  em = discord.Embed(title = "Cold Brew", description = f"**Try {json_data[2]['title']}:** {json_data[2]['description']} The ingredients are: {new}.", color = 0xe67e22)
  file=discord.File('coldbrew.jpeg')
  await ctx.send(file = file, embed = em)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def frappucino(ctx):
  ingredients=json_data[3]['ingredients']
  ' '.join(ingredients)
  new = str(ingredients).replace('[','').replace(']','')
  em = discord.Embed(title = "Frappucino", description = f"**Try {json_data[3]['title']}:** {json_data[3]['description']} The ingredients are: {new}.", color = 0xe67e22)
  file=discord.File('frappucino.png')
  await ctx.send(file = file, embed = em)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def nitro(ctx):
  ingredients=json_data[4]['ingredients']
  ' '.join(ingredients)
  new = str(ingredients).replace('[','').replace(']','')
  em = discord.Embed(title = "Nitro", description = f"**Try {json_data[4]['title']}:** {json_data[4]['description']} The ingredients are: {new}.", color = 0xe67e22)
  file=discord.File('nitro.jpeg')
  await ctx.send(file = file, embed = em)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def mazagran(ctx):
  ingredients=json_data[5]['ingredients']
  ' '.join(ingredients)
  new = str(ingredients).replace('[','').replace(']','')
  em = discord.Embed(title = "Mazagran", description = f"**Try {json_data[5]['title']}:** {json_data[5]['description']} The ingredients are: {new}.", color = 0xe67e22)
  file=discord.File('mazagran.jpeg')
  await ctx.send(file = file, embed = em)

# Everything above this works
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def add(ctx, *, arg):
  prompt_messages=arg
  update_prompts(prompt_messages)
  em = discord.Embed(title = "Adding a message...", description = "Adding a message to the bot prompts", color = 0xe91e63)
  em.add_field(name = "**Message added:**", value = prompt_messages)
  await ctx.send(embed = em)

@bot.command()
async def index(ctx):
  em = discord.Embed(title = "__**Prompts**__", description = "Use /add <message> or /delete <message> for future references!", color=0xe91e63)
  for i in range(0, len(db["phrase"])):
    em.add_field(name = f"Index {i}", value = db['phrase'][i])
  await ctx.send(embed = em)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def delete(ctx, *, arg):
  deleted_phrases=[]
  index=int(arg)
  if "phrase" in db.keys():
      if index <=3:
        testEmbed = discord.Embed(title = "Failed to delete!", description = "Try a number greater than 3.", color=0xe74c3c)
        await ctx.send(embed = testEmbed)
      else:
        delete_prompts(index)
        realEmbed = discord.Embed(title = "Deleting...", description=f"Successfully deleted item at **index {arg}**.", color=0xc27c0e)
        await ctx.send(embed = realEmbed)
        
def delete_prompts(index):
  phrase=db["phrase"]
  if len(phrase) > index:
    del phrase[index]
    db["phrase"] = phrase
def update_prompts(prompt_messages):
  if "phrase" in db.keys():
    phrase=db["phrase"]
    phrase.append(prompt_messages)
    db["phrase"] = phrase
  else:
    db["phrase"] = [prompt_messages]

@bot.event
async def on_message(message):
  if message.author==bot.user:
    return
  options=starter_prompts
  if "phrase" in db.keys():
    options.extend(db["phrase"])
  if any(word in message.content for word in words):
    await message.channel.send(random.choice(options))
  await bot.process_commands(message)


bot.run(my_secret)
