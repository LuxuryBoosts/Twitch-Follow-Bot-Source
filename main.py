import httpx,requests, gc,discord,time,calendar, traceback,threading, socks, random, json, tracemalloc, asyncio; from discord.utils import get;from discord import Member; from dotenv import load_dotenv; from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
from itertools import cycle
tracemalloc.start()

def get_config():
    config_file = open("config.json","r", encoding="utf8")
    configx = config_file.read()
    config_file.close()
    return configx

def get_prefix():
    config_file = get_config()
    config = json.loads(config_file)
    prefix = config['bot_config']["prefix"] 
    return prefix
    
config_file = get_config()
config = json.loads(config_file)
prefix = config['bot_config']["prefix"]
token = config['bot_config']["token"]

queue = []
proxies = []

with open('proxy.txt','r') as f:
    for line in f.readlines():
        proxies.append(line.strip('\n'))

def GetProxy():
    b = random.choice(proxies)
    return b.split(':')

load_dotenv()
intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=get_prefix(), help_command=None, intents=intents)

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run(token))
    threading.Thread(target=loop.run_forever).start()


@bot.command()
async def stock(ctx):
 if ctx.channel.type != discord.ChannelType.private:
     if ctx.author.guild_permissions.administrator:
        filefile = open('ttoken_follow.txt')
        fnum_lines = sum(1 for line in filefile)
        filefile.close()
        filefile = open('ttoken_spam.txt')
        snum_lines = sum(1 for line in filefile)
        filefile.close()
        embed=discord.Embed(title="Stock",color=10181046, description=f"Twitch Stock:\n \nSpam: **{snum_lines}**\nFollow: **{fnum_lines}** ")
        await ctx.send(embed=embed)
        
@bot.event
async def on_ready():
    print(f'Servers: {len(bot.guilds)}')
    for guild in bot.guilds:
        print(guild.name)
    print()
    # bot.loop.create_task(status())
    while True:
        members = sum([guild.member_count for guild in bot.guilds])
        activity = discord.Activity(type=discord.ActivityType.watching, name=f'{members} users!')
        await bot.change_presence(activity=activity)
        await asyncio.sleep(60)

@bot.command()
async def ticket(ctx):
    if ctx.channel.type != discord.ChannelType.private:
        channels = [str(x) for x in bot.get_all_channels()]
        if f'ticket-{ctx.author.id}' in str(channels):
            embed = discord.Embed(color=10181046, description='You already have a ticket open!')
            await ctx.send(embed=embed)
        else:
            ticket_channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.id}')
            await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            embed = discord.Embed(color=10181046, description='Please enter the reason for this ticket, type `/close` if you want to close this ticket.')
            await ticket_channel.send(f'{ctx.author.mention}', embed=embed)
            await ctx.message.delete()
            
@bot.command()
async def close(ctx):
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.name == f'ticket-{ctx.author.id}':
            await ctx.channel.delete()
        elif ctx.author.id in administrators and 'ticket' in ctx.channel.name:
            await ctx.channel.delete()
        else:
            embed = discord.Embed(color=10181046, description=f'You do not have permission to run this command!')
            await ctx.send(embed=embed)
    
@bot.command()
async def bronze(ctx):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    embed=discord.Embed(title="Free Bronze",color=10181046, description=f"**set .gg/twitchfollowerv4 in status, you will automatically get a rank Bronze**")
    await ctx.send(embed=embed)


def get_id(user):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept-Language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-Session-Id': '51789c1a5bf92c65',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.twitch.tv',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.twitch.tv/',
    }
    data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
    try:
        response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
        id = response.json()[0]['data']['user']['id']
        return id
    except:
        return None



@bot.event
async def on_member_update(before, after):
    role_id = 839178609192337480
    role = get(before.guild.roles, id=role_id)
    if '.gg/twitchfollowerv4' in str(before.activities):
      if '.gg/twitchfollowerv4' in str(after.activities):
        pass
      else:
        await after.remove_roles(role)
        channel = bot.get_channel(938832271832670228)
        embed=discord.Embed(description=f"Bronze has been removed from {after.mention}", color=discord.Color.red())
        await channel.send(embed=embed)

    if '.gg/twitchfollowerv4' in str(after.activities):
        await after.add_roles(role)
        channel = bot.get_channel(938832271832670228)
        embed=discord.Embed(description=f"{after.mention} has claimed Bronze!", color=discord.Color.green())
        await channel.send(embed=embed)
    
        
@bot.command()
async def help(ctx):
    config_file = get_config()
    json_object = json.loads(config_file)
    prefix = json_object['bot_config']["prefix"]

    embed=discord.Embed(color=10181046,description=f'***/help***\nDisplays this embed!\n***/ticket***\nOpens a ticket\n***/tfollow (channel)***\nBot sends twitch followers to the twitch channel!\n**/tfriend (channel)**\nBot sends twitch friend requests to the twitch channel!\n***/tspam (channel) (message)***\nBot spams a specified message in the twitch stream chat!\n***/treport*** (channel)\nBot reports the twitch channel!\n***/traid (channel)***\nBot raids the twitch channel!\n***/ttroll (channel)***\nBot trolls the twitch channel!\n ***/twhisper (channel) (message)***\nSpam private message to which you want!\n***/thost (channel)***\nSpam raid to which streamer you want\n***/bronze***\nHow to get free bronze role')
    await ctx.send(embed=embed)


@bot.command()
async def clear(ctx):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/950132318171963543/la-zAHHT0IjyHYQVZpCLUgQUWF_3UeiGSRPSk_jyyMrb_IH8stvvolQC2DoSBSN0eQHO')
    embed = DiscordEmbed(title='Twitch Follower V4', description=(f'**{ctx.author} | {ctx.author.id} -> {bot.command_prefix}clear**'), color='9B59B6')
    webhook.add_embed(embed)
    response = webhook.execute()
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=None)
            await ctx.send('**Cleared!😎**')
        else:
            await ctx.message.delete()

@bot.command()
async def tfollow(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel =json_object['bot_config']["twitch_channel"]
    genchannel2 =json_object['bot_config']["twitch_channel_2"]
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=10181046, description=f"**ERROR** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                filefile = open('ttoken_follow.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                filefile = open('ttoken_follow.txt', 'r')
                tokens = filefile.read().splitlines()
                filefile.close()
                
                if num_lines < follow_count:
                    
                    embed=discord.Embed(color=10181046, description=f"➣ Adding **{num_lines}** follows to **{arg}**")
                    await ctx.send(embed=embed)
                    
                    caunt_to_follow = num_lines
                else:
                    
                    embed=discord.Embed(color=10181046, description=f"➣ Adding **{follow_count}** Twitch Follows to **{arg}**")
                    await ctx.send(embed=embed)
                
                    caunt_to_follow = follow_count

                    
                class Follow():
                    sent = 0
                        
                def start_follow():

                        
                    for i in range(caunt_to_follow):
                        
                        try:
                            ttoken = random.choice(open("ttoken_follow.txt", "r" ).read().splitlines())
                            
                            payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                            headers = {
                                            "Authorization": f"OAuth {ttoken}",
                                            "Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                                            "Content-Type": "application/json"
                                        }
                            
                            response = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        
                            
                            try:
                                if response.json()[0]['data']['followUser']['error']:
                                    with open("ttoken_follow.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("ttoken_follow.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['error'] == "Unauthorized":
                                    with open("ttoken_follow.txt", "r") as f:
                                        lines = f.readlines()
                                        f.close()
                                    with open("ttoken_follow.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['data']['followUser']['follow'] == None:
                                        None
                            except:
                                None
                            try:
                                if response.json()[0]['data']['followUser']['follow']['user']:
                                    Follow.sent = Follow.sent + 1
                            except:
                                None   
                        except:
                            None
                x = threading.Thread(target=start_follow)
                x.start()
                break
                
                

@bot.command()
async def tspam(ctx, arg1, *, args):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"] 
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        role_config = json.loads(config_file)['tspam']
        for role_name in role_config:
            spam_count = json_object['tspam'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('ttoken_spam.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    embed=discord.Embed(color=10181046, description=f"**ERROR** Invalid **username** {arg1}")
                    await ctx.send(embed=embed)
                    break
                else:
                    None
                def start_spam():
                    for i in range(20):
                        try:
                            filefile = open("ttoken_spam.txt")
                            ttoken = random.choice(filefile.read().splitlines())
                            filefile.close()
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try:
                                        proxyfile = open("proxy.txt","r")
                                        proxy = random.choice(proxyfile.read().splitlines())
                                        proxyfile.close()
                                        session = requests.Session()
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                            s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                            s.send('CAP REQ :twitch.tv/commands twitch.tv/tags\r\n'.encode('utf-8'))
                            s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                            s.send(('PRIVMSG #' + arg1 + f' :/me {args} \r\n').encode('utf8'))
                            s.close()
                        except Exception as e:
                            print(e)
                            
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                            
                embed=discord.Embed(color=10181046, description=f"Sending **{x}** messages to **{arg1}**")
                await ctx.send(embed=embed)
                try:
                    for i in range(x):

                        threading.Thread(target=start_spam).start()
                except:
                    None
                break
    else:
        embed = discord.Embed(color=10181046, description='Only **Gold,Diamond,Premium and Premium +** can use this!')
        await ctx.send(embed=embed)


            
@bot.command()
async def treport(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]
    
                
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        
        role_config = json.loads(config_file)['treport']
        for role_name in role_config:
            spam_count = json.loads(config_file)['treport'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                
                num_lines = sum(1 for line in open('ttoken_follow.txt'))
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=10181046, description=f"**ERROR** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                
                def start_spam(ttoken):
                    xcc = open("report.txt","r")
                    reportndescription = random.choice(xcc.read().splitlines())
                    xcc.close()
                    try:
                        headers = {
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                            'Accept-Language': 'en-US',
                            'sec-ch-ua-mobile': '?0',
                            'Client-Version': 'fde6b5a8-2aa2-45b1-85d5-5036951737cc',
                            'Authorization': f'OAuth {ttoken}',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                            'Client-Session-Id': '32193c1413662035',
                            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                            'X-Device-Id': 'O1MrFLwPyZ2byJzoLFT0K5XNlORNRQ9F',
                            'sec-ch-ua-platform': '"Windows"',
                            'Accept': '*/*',
                            'Origin': 'https://www.twitch.tv',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.twitch.tv/',
                        }

                        data = '[{"operationName":"ReportUserModal_ReportUser","variables":{"input":{"description":"report context: USER_REPORT\\n\\nvideo > terrorism_mass_violence\\n\\ndescription: '+reportndescription+'","reason":"terrorism_mass_violence","content":"LIVESTREAM_REPORT","contentID":"","extra":"","targetID":"'+target_id+'","wizardPath":["video","terrorism_mass_violence"]}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"dd2b8f6a76ee54aff685c91537fd75814ffdc732a74d3ae4b8f2474deabf26fc"}}}]'

                        httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data).text

                    except:
                        None
                            
                            
                embed=discord.Embed(color=10181046, description=f"Sending **{spam_count}** reports to **{arg}**")
                await ctx.send(embed=embed)
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                    
                try:
                    
                    for i in range(x):
                        c = open("ttoken_follow.txt")
                        ttoken = random.choice(c.read().splitlines())
                        threading.Thread(target=start_spam,args=(ttoken,)).start()
                        c.close()
                        
                except:
                    None
                break
    
@bot.command()
async def tfriend(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]

    if ctx.channel.id == int(genchannel) or ctx.channel.id ==int(genchannel2): 
        role_config = json.loads(config_file)['tfriend']
        for role_name in role_config:
            spam_count = json.loads(config_file)['tfriend'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                filefile = open('ttoken_follow.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=10181046, description=f"ERROR Invalid username {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                def start_spam(ttoken):
                    
                    try:
                        headers = {
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                            'Accept-Language': 'en-US',
                            'sec-ch-ua-mobile': '?0',
                            'Client-Version': 'fde6b5a8-2aa2-45b1-85d5-5036951737cc',
                            'Authorization': f'OAuth {ttoken}',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                            'Client-Session-Id': '99ef7e05659bbca4',
                            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                            'X-Device-Id': 'O1MrFLwPyZ2byJzoLFT0K5XNlORNRQ9F',
                            'sec-ch-ua-platform': '"Windows"',
                            'Accept': '*/*',
                            'Origin': 'https://www.twitch.tv',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.twitch.tv/',
                        }

                        data = '[{"operationName":"FriendButton_CreateFriendRequest","variables":{"input":{"targetID":"'+target_id+'"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"380d8b19fcffef2fd8654e524444055dbca557d71968044115849d569d24129a"}}}]'

                        httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)

                    except:
                        None 
                embed=discord.Embed(color=10181046, description=f"Sending **{spam_count}** friends to **{arg}**")
                await ctx.send(embed=embed)
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                try:
                    for i in range(x):
                        xx = open("ttoken_follow.txt").read()
                        ttoken = random.choice(xx.splitlines())
                        threading.Thread(target=start_spam,args=(ttoken,)).start()
                except:
                    None
                break

@bot.command()
async def ttroll(ctx, arg1):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]  
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        role_config = json.loads(config_file)['tspam']
        for role_name in role_config:
            spam_count = json_object['ttroll'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('ttoken_spam.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    embed=discord.Embed(color=10181046, description=f"**ERROR** Invalid **username** {arg1}")
                    await ctx.send(embed=embed)
                    break
                else:
                    None
                def start_spam():
                    for i in range(20):
                        try:
                            filefile = open("ttoken_spam.txt")
                            ttoken = random.choice(filefile.read().splitlines())
                            filefile.close()
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try:
                                        proxyfile = open("proxy.txt","r")
                                        proxy = random.choice(proxyfile.read().splitlines())
                                        proxyfile.close()
                                        session = requests.Session()
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                            s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                            s.send('CAP REQ :twitch.tv/commands twitch.tv/tags\r\n'.encode('utf-8'))
                            s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                            s.send(('PRIVMSG #' + arg1 + f' :/me GET TROLLED LOL \r\n').encode('utf8'))
                            s.close()
                        except Exception as e:
                            print(e)
                            
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                            
                embed=discord.Embed(color=10181046, description=f"➣ **{arg1}** getting trolled for **{x}** times!")
                await ctx.send(embed=embed)
                try:
                    for i in range(x):

                        threading.Thread(target=start_spam).start()
                except:
                    None
                break
    else:
        embed = discord.Embed(color=10181046, description='Only **Gold,Diamond,Premium and Premium +** can use this!')
        await ctx.send(embed=embed)


@bot.command()
async def traid(ctx, arg1):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    genchannel2 = json_object['bot_config']["twitch_channel_2"]  
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2): 
        role_config = json.loads(config_file)['traid']
        for role_name in role_config:
            spam_count = json_object['traid'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('ttoken_spam.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    embed=discord.Embed(color=10181046, description=f"**ERROR** Invalid **username** {arg1}")
                    await ctx.send(embed=embed)
                    break
                else:
                    None
                def start_spam():
                    for i in range(20):
                        try:
                            filefile = open("ttoken_spam.txt")
                            ttoken = random.choice(filefile.read().splitlines())
                            filefile.close()
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try:
                                        proxyfile = open("proxy.txt","r")
                                        proxy = random.choice(proxyfile.read().splitlines())
                                        proxyfile.close()
                                        session = requests.Session()
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                            s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                            s.send('CAP REQ :twitch.tv/commands twitch.tv/tags\r\n'.encode('utf-8'))
                            s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                            s.send(('PRIVMSG #' + arg1 + f' :/me Get raided by {ctx.author} \r\n').encode('utf8'))
                            s.close()
                        except Exception as e:
                            print(e)
                            
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                            
                embed=discord.Embed(color=10181046, description=f"➣ **{arg1}** getting raided for **{x}** times!")
                await ctx.send(embed=embed)
                try:
                    for i in range(x):

                        threading.Thread(target=start_spam).start()
                except:
                    None
                break
    else:
        embed = discord.Embed(color=10181046, description='Only **Gold,Diamond,Premium and Premium +** can use this!')
        await ctx.send(embed=embed)


bot.run(token)