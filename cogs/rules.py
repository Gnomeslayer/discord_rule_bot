import json
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get


class Rules(commands.Cog):
    def __init__(self, client):
        print("[Cog] Rules has been initiated")
        self.client = client
    with open("./json/config.json", "r") as f:
        config = json.load(f)

    @app_commands.command(name="addrule", description="Adds a rule")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(*config['additional']['managers'])
    async def addrule(self, interaction: discord.Interaction, rule: str):
        with open("./json/config.json", "r") as f:
            config = json.load(f)
        rulenumber = len(config['rules'])
        config['rules'][rulenumber] = rule
        with open("./json/config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
        embed = await self.rulesembed()
        rules_channel = interaction.guild.get_channel(
            config['additional']['rules_channel'])

        if config['cogs']['rules_embed_message']:
            rules_embed = await rules_channel.fetch_message(config['cogs']['rules_embed_message'])
            await rules_embed.edit(embed=embed)
        else:
            message = await rules_channel.send(embed=embed)
            config['cogs']['rules_embed_message'] = message.id
            with open("./json/config.json", "w") as f:
                f.write(json.dumps(config, indent=4))
        await interaction.response.send_message(f"added the following rule:\n```{rule}```Rules embed has also been updated.", ephemeral=True)

    @app_commands.command(name="deleterule", description="Deletes a rule")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(*config['additional']['managers'])
    async def deleterules(self, interaction: discord.Interaction, rulenumber: str):
        with open("./json/config.json", "r") as f:
            config = json.load(f)
        deletedrule = config['rules'][rulenumber]
        del config['rules'][rulenumber]
        count = 0
        rules = {}
        for rule in config['rules']:
            rules[count] = config['rules'][rule]
            count += 1
        config['rules'] = rules
        with open("./json/config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
        embed = await self.rulesembed()
        rules_channel = interaction.guild.get_channel(
            config['additional']['rules_channel'])

        if config['cogs']['rules_embed_message']:
            rules_embed = await rules_channel.fetch_message(config['cogs']['rules_embed_message'])
            await rules_embed.edit(embed=embed)
        else:
            message = await rules_channel.send(embed=embed)
            config['cogs']['rules_embed_message'] = message.id
            with open("./json/config.json", "w") as f:
                f.write(json.dumps(config, indent=4))
        await interaction.response.send_message(f"removed the following rule:\n```[{rulenumber}] {deletedrule}```Reconjigured(yes that's a word. No I did not make it up.) the rules\n```{config['rules']}```Rules embed has also been updated.", ephemeral=True)

    @app_commands.command(name="editrule", description="Edits a rule!")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(*config['additional']['managers'])
    async def editrule(self, interaction: discord.Interaction, rulenumber: str, rule: str):
        with open("./json/config.json", "r") as f:
            config = json.load(f)
        original_rule = f"[{rulenumber}] - {config['rules'][rulenumber]}"
        new_rule = f"[{rulenumber}] - {rule}"
        config['rules'][rulenumber] = rule
        with open("./json/config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
        embed = await self.rulesembed()
        rules_channel = interaction.guild.get_channel(
            config['additional']['rules_channel'])

        if config['cogs']['rules_embed_message']:
            rules_embed = await rules_channel.fetch_message(config['cogs']['rules_embed_message'])
            await rules_embed.edit(embed=embed)
        else:
            message = await rules_channel.send(embed=embed)
            config['cogs']['rules_embed_message'] = message.id
            with open("./json/config.json", "w") as f:
                f.write(json.dumps(config, indent=4))

        await interaction.response.send_message(f"Updated ```{original_rule}```to```{new_rule}```Updated the rules embed.", ephemeral=True)

    @app_commands.command(name="sendrules", description="Sends the rules")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(*config['additional']['managers'])
    async def sendrules(self, interaction: discord.Interaction):
        with open("./json/config.json", "r") as f:
            config = json.load(f)
        embed = await self.rulesembed()
        rules_channel = interaction.guild.get_channel(
            config['additional']['rules_channel'])

        if config['cogs']['rules_embed_message']:
            rules_embed = await rules_channel.fetch_message(config['cogs']['rules_embed_message'])
            await rules_embed.edit(embed=embed)
        else:
            message = await rules_channel.send(embed=embed)
            config['cogs']['rules_embed_message'] = message.id
            with open("./json/config.json", "w") as f:
                f.write(json.dumps(config, indent=4))

        await interaction.response.send_message("Rules sent and updated.", ephemeral=True)

    async def rulesembed(self):
        with open("./json/config.json", "r") as f:
            config = json.load(f)
        rules = config['rules']
        rules_string = None
        for rule in rules:
            if rules_string:
                rules_string += f"\n[{rule}] - {rules[rule]}"
            else:
                rules_string = f"[{rule}] - {rules[rule]}"
        if not rules_string:
            rules_string = "No rules set!"
        embed = discord.Embed(
            title="Server rules!", description=f"{rules_string}")
        return embed

    @sendrules.error
    async def sendrules_handler(self, ctx, error):
        if isinstance(error, app_commands.MissingAnyRole):
            await ctx.response.send_message("You do not have permission to use this command.", ephemeral=True)

    @editrule.error
    async def editrules_handler(self, ctx, error):
        if isinstance(error, app_commands.MissingAnyRole):
            await ctx.response.send_message("You do not have permission to use this command.", ephemeral=True)

    @deleterules.error
    async def deleterules_handler(self, ctx, error):
        if isinstance(error, app_commands.MissingAnyRole):
            await ctx.response.send_message("You do not have permission to use this command.", ephemeral=True)

    @addrule.error
    async def addrules_handler(self, ctx, error):
        if isinstance(error, app_commands.MissingAnyRole):
            await ctx.response.send_message("You do not have permission to use this command.", ephemeral=True)


async def setup(client):
    await client.add_cog(Rules(client))
