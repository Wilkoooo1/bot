import discord
from discord.ext import commands
from discord import app_commands

ITEM_PRICES = {
    "car": 1000,
    "wheel": 50,
    "spoiler": 100,
    "engine": 500,
    "seat": 75
}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="order", description="Calculate total for an order")
@app_commands.describe(items="Type items and quantities like: car 1 wheel 2")
async def order(interaction: discord.Interaction, items: str):
    try:
        split_items = items.lower().split()
        summary = []
        total = 0

        for i in range(0, len(split_items), 2):
            name = split_items[i]
            qty = int(split_items[i + 1])
            price = ITEM_PRICES.get(name)

            if price is None:
                summary.append(f"- ❌ `{name}` is not a valid item.")
                continue

            line_total = price * qty
            total += line_total
            summary.append(f"- {name.capitalize()} x{qty} = ${line_total} (${price} each)")

        summary.append(f"\n**Total: ${total}**")
        embed = discord.Embed(title="🛒 Order Summary", description="\n".join(summary), color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception:
        await interaction.response.send_message("❌ Invalid format. Use: `item quantity item quantity`", ephemeral=True)

@bot.event
async def on_ready():
    GUILD_ID = 1270770823669747803  # Replace with your server ID
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Bot is ready as {bot.user}")

import os
bot.run(os.environ["TOKEN"])
