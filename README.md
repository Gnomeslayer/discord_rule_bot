# discord_rule_bot
A rules bot for discord. Very basic. Spent as little time as possible developing it. About 20 minutes. Please don't eat my cookies.

Fill out the config.json file.
You will need to head on over to: https://discord.com/developers/applications to setup a discordbot and to get yourself a discord token and application id.

rules_channel - The channel you want the rules to be sent to.
managers - a list of role ids. These are the only roles who can edit/delete/add rules.
rules_embed_message - Leave as 0.

rules - a dictionary of rules. You can preset some to send or you can leave as empty.

Commands:
/addrule <rule>
Adds a new rule to the rules. Updates the rules channel.
/deleterule <rulenumber>
Deletes the targeted rule. Updates the rules channel.
/editrule <rulenumber> <rule>
Edits the targeted rule. Updates the rules channel.
/sendrules
Sends the rules embed (or edits the existing one)
