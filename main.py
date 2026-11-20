from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, time

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION1 = os.environ.get("SESSION1", "")

client = TelegramClient(StringSession(SESSION1), API_ID, API_HASH)

SUDO = set()
MIRROR = [False]
AUTOREPLY = [False]
AUTOREPLY_TEXT = ["KASHYAP BHAI ABHI BUSY HAI!"]
AUTOREACT = [False]
AUTOREACT_EMOJI = ["❤️"]

def is_allowed(e):
    if e.out:
        return True
    if e.sender_id in SUDO:
        return True
    return False

@client.on(events.NewMessage(pattern="^.ping$"))
async def ping(e):
    if not is_allowed(e):
        return
    s = time.time()
    await e.edit("PINGING...")
    ms = round((time.time() - s) * 1000)
    await e.edit(f"KASHYAP PRIME\nPING : {ms}ms")

@client.on(events.NewMessage(pattern="^.alive$"))
async def alive(e):
    if not is_allowed(e):
        return
    await e.edit("KASHYAP USERBOT PRIME\nSTATUS : ONLINE")

@client.on(events.NewMessage(pattern="^.help$"))
async def help_cmd(e):
    if not is_allowed(e):
        return
    await e.edit(".ping .alive .help .addsudo .sudolist\n.mirror on/off .autoreply on/off\n.autoreact on/off .offline .online")

@client.on(events.NewMessage(pattern="^.addsudo"))
async def addsudo(e):
    if not e.out:
        return
    p = e.text.split(" ", 1)
    if len(p) < 2:
        await e.edit(".addsudo <id> likh!")
        return
    SUDO.add(int(p[1].strip()))
    await e.edit(f"SUDO ADD HO GAYA : {p[1]}")

@client.on(events.NewMessage(pattern="^.sudolist$"))
async def sudolist(e):
    if not is_allowed(e):
        return
    await e.edit(str(SUDO) if SUDO else "Koi SUDO nahi hai!")

@client.on(events.NewMessage(pattern="^.mirror"))
async def mirror_cmd(e):
    if not is_allowed(e):
        return
    if "on" in e.text.lower():
        MIRROR[0] = True
        await e.edit("MIRROR ON!")
    else:
        MIRROR[0] = False
        await e.edit("MIRROR OFF!")

@client.on(events.NewMessage(pattern="^.autoreply"))
async def autoreply_cmd(e):
    if not is_allowed(e):
        return
    if "on" in e.text.lower():
        AUTOREPLY[0] = True
        await e.edit("AUTOREPLY ON!")
    else:
        AUTOREPLY[0] = False
        await e.edit("AUTOREPLY OFF!")

@client.on(events.NewMessage(pattern="^.autoreact"))
async def autoreact_cmd(e):
    if not is_allowed(e):
        return
    if "on" in e.text.lower():
        AUTOREACT[0] = True
        await e.edit("AUTOREACT ON!")
    else:
        AUTOREACT[0] = False
        await e.edit("AUTOREACT OFF!")

@client.on(events.NewMessage(pattern="^.offline$"))
async def offline_on(e):
    if not is_allowed(e):
        return
    await e.edit("OFFLINE MODE ON!")

@client.on(events.NewMessage(pattern="^.online$"))
async def online_off(e):
    if not is_allowed(e):
        return
    await e.edit("ONLINE AA GAYA!")

@client.on(events.NewMessage(incoming=True))
async def auto(e):
    if e.out:
        return
    if not e.is_private:
        return
    if AUTOREACT[0]:
        try:
            await e.react(AUTOREACT_EMOJI[0])
        except:
            pass
    if AUTOREPLY[0]:
        await e.reply(AUTOREPLY_TEXT[0])

print("KASHYAP USERBOT PRIME START HO GAYA!")
client.start()
print("ID ON!")
client.run_until_disconnected()
