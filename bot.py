import discord
import asyncio

# === ENCRYPTED TOKEN SECTION ===
#key = ""
#encrypted_token = "

# Decrypt the token
#decrypted_chars = []
#for i, char in enumerate(encrypted_token):
#    key_char = key[i % len(key)]
#    decrypted_chars.append(chr(ord(char) ^ ord(key_char)))

#DISCORD_TOKEN = ''.join(decrypted_chars)
# === END ENCRYPTED TOKEN SECTION ===
DISCORD_TOKEN = ''
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    # Get all guilds
    for guild in client.guilds:
        print(f"\n🏰 Server: {guild.name} (ID: {guild.id})")
        
        # Delete all text channels
        text_channels_deleted = 0
        for channel in guild.text_channels:
            try:
                await channel.delete()
                print(f"   ❌ Deleted text channel: {channel.name}")
                text_channels_deleted += 1
                await asyncio.sleep(0.5)  # Rate limit prevention
            except Exception as e:
                print(f"   ⚠️ Failed to delete {channel.name}: {e}")
        
        # Delete all voice channels
        voice_channels_deleted = 0
        for channel in guild.voice_channels:
            try:
                await channel.delete()
                print(f"   ❌ Deleted voice channel: {channel.name}")
                voice_channels_deleted += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"   ⚠️ Failed to delete {channel.name}: {e}")
        
        # Delete all categories
        categories_deleted = 0
        for category in guild.categories:
            try:
                await category.delete()
                print(f"   ❌ Deleted category: {category.name}")
                categories_deleted += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"   ⚠️ Failed to delete {category.name}: {e}")
        
        print(f"   📊 Summary: {text_channels_deleted} text, {voice_channels_deleted} voice, {categories_deleted} categories deleted")
    
    print("\n✅ All channels deleted from all servers!")
    print("The bot will stay online. Press Ctrl+C to exit.")
    
    # Keep bot running
    while True:
        await asyncio.sleep(3600)  # Sleep for 1 hour

@client.event
async def on_message(message):
    # Only respond to bot owner
    if message.author == client.user:
        return
    
    # Stop command
    if message.content.lower() == "!stop":
        await message.channel.send("🛑 Stopping deletion bot...")
        await client.close()
        return
    
    # Status command
    if message.content.lower() == "!status":
        guild_count = len(client.guilds)
        total_channels = sum(len(guild.channels) for guild in client.guilds)
        await message.channel.send(f"🤖 **Deletion Bot Status**\nServers: {guild_count}\nTotal Channels: {total_channels}")
        return

# Run the bot
try:
    client.run(DISCORD_TOKEN)
except KeyboardInterrupt:
    print("\nBot stopped by user")
except Exception as e:
    print(f"Error: {e}")
