#!/home/jp/DiscordBot/gcoinbot/venv/bin/python3.7
import discord
from discord.ext import commands
import sqlite3
import datetime
import random
import time

msg_id = None
bot = commands.Bot(command_prefix='g ')
<<<<<<< HEAD
token = 'token'
conn = sqlite3.connect('coin.db')
=======
token = '*'
conn = sqlite3.connect('/home/jp/DiscordBot/gcoinbot/coin.db')
>>>>>>> 1fe8c047743f0891c02ad61d44864d38d4ade6f6
c = conn.cursor()

def get_balance(user):
    try:
        c.execute("SELECT balance FROM Clients WHERE client_name=?", (user,))
        results = c.fetchone()
        result = int(results[0])
        return(result)
    except:
        return(False)

def set_balance(balance, user):
    try:
        c.execute("UPDATE Clients SET balance=? WHERE client_name=?", (balance,user))
        conn.commit()
        return(True)
    except:
        return(False)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.command()
async def create(ctx):
    client_name = str(ctx.author)
    c.execute("SELECT client_name FROM Clients WHERE client_name=?", (client_name,))
    results = c.fetchall()
    print(results)
    if len(results) == 0:
        c.execute("INSERT INTO Clients(client_name, balance) VALUES(?,?)", (client_name, 0))
        await ctx.channel.send('GCoinBot a créé un compte pour ' + client_name)
    else:
        await ctx.channel.send('Tu as déjà un compte ' + client_name)
    conn.commit()

@bot.command()
async def give(ctx, receiver, amount):
    sender = str(ctx.author)
    amount = int(amount)
    receiver = str(receiver)
    if amount < 1:
        await ctx.channel.send("Tu dois donner un nombre plus grand que 0")
    else:
        balance = get_balance(sender)
        if balance is False:
            await ctx.channel.send("Tu ne possède pas de compte utilise: g create")
        else:
            rbalance = get_balance(receiver)
            if rbalance is False:
                await ctx.channel.send("Il n'existe pas de compte à ce nom: Username#0000")
            else:
                if balance < amount:
                    await ctx.channel.send('Pas assez de GCoin, tu as ' + str(balance) + ' GCoin')
                else:
                    newbalance = balance - amount
                    rnewbalance = amount + rbalance
                    receivercoin = set_balance(rnewbalance, receiver)
                    sendercoin = set_balance(newbalance, sender)
                    if receivercoin is True and sendercoin is True:
                        embed = discord.Embed(title='Transaction :money_with_wings:', color=0x15a227)
                        embed.add_field(name=sender, value="Tu as maintenant " + str(newbalance) + " GCoins.")
                        embed.add_field(name=receiver, value="Tu as maintenant "+ str(rnewbalance) + " GCoins.")
                        await ctx.channel.send(embed=embed)
                    else:
                        await ctx.channel.send("Something went wrong!")

@bot.command()
async def balance(ctx, *person):
    if len(person) == 0:
        sender = str(ctx.author)
    else:
        other = ""
        sender = other.join(person)
    result = get_balance(sender)
    if result is False:
        await ctx.channel.send("Ce compte n'existe pas: g create")
    else:
        embed = discord.Embed(title='Balance :moneybag:', color=0x15a227)
        embed.add_field(name=sender, value=str(result) + " GCoins")
        await ctx.channel.send(embed=embed)

@bot.command()
async def daily(ctx):
    sender = str(ctx.author)
    result = get_balance(sender)
    if result is False:
        await ctx.channel.send("Tu ne possède pas de compte utilise: g create")
    else:
        c.execute("SELECT last_daily FROM Clients WHERE client_name=?", (sender,))
        results = c.fetchone()
        print(str(results[0]))
        if str(results[0]) == 'None':
            price = random.randint(30, 80)
            newbalance = price + result
            last_daily = datetime.date.today()
            c.execute("UPDATE Clients SET last_daily=? WHERE client_name=?", (last_daily, sender))
            c.execute("UPDATE Clients SET balance=? WHERE client_name=?", (newbalance, sender))
            conn.commit()
            await ctx.channel.send(sender + ", tu as maintenant: " + str(newbalance) + " GCoins")
        elif (datetime.date.today() - datetime.date.fromisoformat(str(results[0]))).days > 0 :
            price = random.randint(30, 80)
            newbalance = price + result
            last_daily = datetime.date.today()
            c.execute("UPDATE Clients SET last_daily=? WHERE client_name=?", (last_daily, sender))
            c.execute("UPDATE Clients SET balance=? WHERE client_name=?", (newbalance, sender))
            conn.commit()
            await ctx.channel.send(sender + ", tu as maintenant: " + str(newbalance) + " GCoins")
        else:
            await ctx.channel.send("Tu as déjà eu tes coins pour la journée, reviens demain!")

@bot.command()
async def gamble(ctx, amount):
    sender = str(ctx.author)
    if int(amount) < 1:
        await ctx.channel.send("Tu dois donner un nombre plus grand que 0")
    else:
        balance = get_balance(sender)
        if balance < int(amount):
            await ctx.channel.send('Pas assez de GCoin, tu as ' + str(balance) + ' GCoin')
        else:
            fembed = discord.Embed(title=":four_leaf_clover: Gamble :four_leaf_clover:")
            fembed.add_field(name="Instructions", value="Tu as une chance sur trois de doubler ta mise.\nChoisis un numéro de 1 à 3")
            msg = await ctx.channel.send(embed=fembed)
            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")
            await msg.add_reaction("3️⃣")
            def check(reaction,user):
                return ctx.author == user and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣']
            reaction = await bot.wait_for('reaction_add', timeout=15.0, check=check)
            guess = reaction[0]
            await ctx.channel.send("Tu as répondu {}.".format(guess))
            if guess.emoji == '1️⃣':
                choice = 1
            elif guess.emoji == '2️⃣':
                choice = 2
            elif guess.emoji == '3️⃣':
                choice = 3
            randomizer = random.randint(1,3)
            print(str(choice) + " "+ str(randomizer))
            if choice == randomizer:
                newbalance = int(balance) + int(amount)
                c.execute("UPDATE Clients SET balance=? WHERE client_name=?", (newbalance,sender))
                conn.commit()
                embed = discord.Embed(title=':green_square:NOUS AVONS UN GAGNANT!:green_square:', color=0x00ff00)
                embed.add_field(name="Résultat", value="Tu as gagné " + str(amount) + " GCoins!")
                await ctx.channel.send(embed=embed)
            else:
                newbalance = int(balance) - int(amount)
                c.execute("UPDATE Clients SET balance=? WHERE client_name=?", (newbalance,sender))
                conn.commit()
                embed = discord.Embed(title=':x:Oups!:x:', color=0xff0000)
                embed.add_field(name="Résultat", value="Tu as perdu " + str(amount) + " GCoins.")
                embed.add_field(name="Réponse", value="La réponse était " + str(randomizer))
                await ctx.channel.send(embed=embed)
            
bot.run(token)
