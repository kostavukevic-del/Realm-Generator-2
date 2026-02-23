 import discord
from discord import app_commands
import os

# Get your Discord bot token from Render environment variables
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Function to get an account from stock
def get_account(filename):
    filepath = f"stock/{filename}.txt"

    if not os.path.exists(filepath):
        return None, "File does not exist."

    with open(filepath, "r") as f:
        accounts = f.readlines()

    if len(accounts) == 0:
        return None, "Out of stock."

    account = accounts[0].strip()

    # Remove used account from stock
    with open(filepath, "w") as f:
        f.writelines(accounts[1:])

    return account, None

# ---------------- FREE GEN ----------------
@tree.command(name="freegen", description="Generate a free account")
@app_commands.choices(service=[
    app_commands.Choice(name="Xbox Unchecked", value="xbox_unchecked"),
    app_commands.Choice(name="Roblox Unchecked", value="roblox_unchecked"),
    app_commands.Choice(name="Roblox Checked", value="roblox_checked"),
])
async def freegen(interaction: discord.Interaction, service: app_commands.Choice[str]):
    account, error = get_account(service.value)
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    await interaction.response.send_message(
        f"🎁 **Free {service.name} Account:**\n`{account}`",
        ephemeral=True
    )

# ---------------- PAID GEN ----------------
@tree.command(name="paidgen", description="Generate a paid account")
@app_commands.choices(service=[
    app_commands.Choice(name="Roblox Checked", value="roblox_checked"),
    app_commands.Choice(name="Crunchyroll Checked", value="crunchyroll_checked"),
    app_commands.Choice(name="Xbox Checked", value="xbox_checked"),
    app_commands.Choice(name="Netflix Unchecked", value="netflix_unchecked"),
    app_commands.Choice(name="Netflix Checked", value="netflix_checked"),
])
async def paidgen(interaction: discord.Interaction, service: app_commands.Choice[str]):
    account, error = get_account(service.value)
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    await interaction.response.send_message(
        f"💎 **Paid {service.name} Account:**\n`{account}`",
        ephemeral=True
    )

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run(TOKEN)