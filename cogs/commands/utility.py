import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    @commands.command(
        usage='``-info``',
        help='Provides you with some information about the bot.')
    async def info(self, ctx):

        info_embed = discord.Embed(
            title='Videonet - Information',
            description='**videonet** is a new youtube simulator discord bot with new features coming out regularly!'
                        ' videonet allows you and the members of your server to create a simulation of a '
                        f'youtube channel on Discord!\n\n videonet is in {len(self.bot.guilds)} servers and has made a '
                        f'total of {await self.database.get_channels_count()} channel simulations!',
            color=self.bot.embed)

        info_embed.set_footer(text=f'Check out {ctx.prefix}help, {ctx.prefix}credits and {ctx.prefix}stats for '
                                   f'more information!')

        info_embed.set_author(name='videonet', icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=info_embed)

    @commands.command(
        aliases=['stats'],
        usage='``-statistics``',
        help='Provides you with some in-depth statistics about the bot.')
    async def statistics(self, ctx):
        emb = discord.Embed(
            description=f'**Total Channel Simulations:** ``{await self.database.get_channels_count()}``\n'
            f'**Total Users:** ``{len(self.bot.users)} users``\n'
            f'**Total Guilds:** ``{len(self.bot.guilds)} servers``\n'
            f'**Total DMs:** ``{len(self.bot.private_channels)} DMs``\n'
            f'**Total TextChannels:** ``{len(list(self.bot.get_all_channels()))} channels``\n'
            f'**Latency:** ``{round(self.bot.latency * 1000, 2)} ms``\n',
            color=self.bot.embed)

        emb.set_author(name='videonet', icon_url='https://i.imgur.com/7mf0D6z.png')

        await ctx.send(embed=emb)

    @commands.command(
        aliases=["pong"],
        usage='``-ping``',
        help="Returns the bot's latency in milliseconds.")
    async def ping(self, ctx):
        if 'ping' in ctx.message.content.lower():
            reply = "Pong"
        else:
            reply = "Ping"

        ping_embed = discord.Embed(
            description=f'{self.bot.heartbeat} **{reply}!** ``{round(self.bot.latency * 1000, 2)} ms``',
            color=self.bot.embed
        )
        await ctx.send(embed=ping_embed)

    @commands.command(
        aliases=['creds'],
        usage='``-credits``',
        help='Lists some people and services that helped build vloger.')
    async def credits(self, ctx):
        credits_embed = discord.Embed(
            description='Some people and services that helped build vloger.',
            color=self.bot.embed)

        credits_embed.add_field(
            name='Developers',
            value='TrustedMercury#1953\nIapetus11#6821',
            inline=False)

        credits_embed.add_field(
            name='Design and Ideas',
            value='Credit to [ravy](https://ravy.xyz) for the Help Command design.',
            inline=False)

        credits_embed.add_field(
            name='Other',
            value='A special thanks to thebrownbatman for helping out with the videonet algorithm and it\'s formulas.')

        credits_embed.set_author(name='videonet', icon_url='https://i.imgur.com/7mf0D6z.png')

        await ctx.send(embed=credits_embed)

    @commands.command(
        aliases=['sp', 'setprefix', 'set_prefix'],
        usage='``-prefix``',
        help='Sets a different prefix for your server.')
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def prefix(self, ctx, *, prefix):

        if len(prefix) > 10:
            await ctx.send(f"{self.bot.no} **Your prefix is too long!** (Maximum length - 10)")
            return

        prefix = await self.database.set_prefix(ctx.guild, prefix)

        if prefix == 'Bad Arguments':
            await ctx.send(f"{self.bot.no} **Error.** Please make "
                           "sure your prefix only have alphabets, numbers, punctuation "
                           "and spaces.")
            return

        await ctx.send(f"{self.bot.yes} **Successfully set this bot's prefix to -** ``{prefix}``!")

    @commands.command(
        aliases=['s'],
        usage='``-suggest``',
        help='Broadcasts your suggestion to the videonet support server.')
    @commands.cooldown(1, 10, BucketType.user)
    async def suggest(self, ctx, *, suggestion):

        support_server = self.bot.get_guild(self.bot.support_server_id)
        suggestions_channel = support_server.get_channel(self.bot.suggestions_channel_id)

        suggestion_embed = discord.Embed(
            title=f'{self.bot.pencil} New Suggesstion!',
            description=suggestion,
            color=self.bot.embed)

        suggestion_embed.set_footer(text="Make your own suggestions with -suggest!")
        suggestion_embed.set_author(name=ctx.author.name+'#'+ctx.author.discriminator, icon_url=ctx.author.avatar_url)

        message = await suggestions_channel.send(embed=suggestion_embed)
        await ctx.send(f'{self.bot.yes} **Sent your suggestion to the videonet support server!**')

        await message.add_reaction(self.bot.yes)
        await message.add_reaction(self.bot.no)

    @commands.command(
        aliases=['report'],
        usage='``-bug``',
        help='Send your bug to the videonet support server!')
    @commands.cooldown(1, 10, BucketType.user)
    async def bug(self, ctx, *, bug):

        support_server = self.bot.get_guild(self.bot.support_server_id)
        bugs_channel = support_server.get_channel(self.bot.bugs_channel_id)

        bug_embed = discord.Embed(
            title=f'{self.bot.bug} New Bug!',
            description=bug,
            color=self.bot.embed)

        bug_embed.set_footer(text="Report your bug with -bug")
        bug_embed.set_author(
            name=ctx.author.name + '#' + ctx.author.discriminator,
            icon_url=ctx.author.avatar_url)

        await bugs_channel.send(embed=bug_embed)
        await ctx.send(f'{self.bot.yes} **Sent your suggestion to the videonet support server!**')

    @commands.command(
        aliases=['changes'],
        usage='``-changelog``',
        help='Shows you a list of recent changes made to the bot.')
    async def changelog(self, ctx):

        description = '**• Thursday, 16th April 2020' \
                      '\n' \


        changelog_embed = discord.Embed(
            title='Changelog - videonet',
            description=description,
            color=self.bot.embed)

        changelog_embed.add_field(
            name='**• Friday, 17th April 2020**',
            value='- Added channel ``delete`` command.'
        )

        changelog_embed.add_field(
            name='**• Thursday, 16th April 2020**',
            value='- Added ``ban`` and ``unban`` commands, to ban users from the bot.\n\n'
        )

        changelog_embed.add_field(
            name='**• Wednesday, 15th April 2020**',
            value='**• Wednesday, 15th April 2020**\n'
                  '- Added ``video {video_name}`` command, to search for videos by name.\n'
                  '- Added ``changelog`` command, to see new bot updates and changes.\n'
                  '- Added ``search`` command, to search for youtube videos (first result)\n'
                  '- Added ``invite`` command, provides you with a support server invite.\n'
                  '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯')

        await ctx.send(embed=changelog_embed)

    @commands.command(
        aliases=['inv'],
        usage='``-invite``',
        help='Sends an invite to the support server.')
    async def invite(self, ctx):

        await ctx.send(f'{self.bot.yes} **https://discord.gg/3MShhbr**')


def setup(bot):
    bot.add_cog(Utility(bot))
