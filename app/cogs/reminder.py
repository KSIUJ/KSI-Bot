import discord
import app.bot
import datetime

from discord.ext import commands


class Reminder(commands.Cog):
    def __init__(self, bot: app.bot.Bot) -> None:
        self.bot = bot

    def _get_date(self, value: int, unit: str) -> datetime.datetime:
        if unit == "minute":
            return datetime.datetime.now() + datetime.timedelta(minutes=value)

        if unit == "hour":
            return datetime.datetime.now() + datetime.timedelta(hours=value)

        if unit == "day":
            return datetime.datetime.now() + datetime.timedelta(days=value)

        return datetime.datetime.now()

    @commands.slash_command(
        name="remindme",
        description="set a reminder",
        guild_ids=[848921520776413213],
    )
    @commands.cooldown(rate=1, per=60)
    @discord.option("value", description="enter the value")
    @discord.option("unit", description="choose the unit", choices=["minute", "hour", "day"])
    @discord.option(
        "message",
        description="message which u want to get with the reminder",
        min_length=1,
        max_length=50,
    )
    async def _remindme(
        self, ctx: discord.ApplicationContext, value: int, unit: str, message: str
    ) -> None:
        await ctx.defer()

        remind_date = self._get_date(value, unit).replace(second=0, microsecond=0)
        self.bot.database_handler.execute(
            "INSERT INTO Reminders (UserID, RemindDate, ChannelID, Message) VALUES (?, ?, ?, ?)",
            ctx.user.id,
            str(remind_date),
            str(ctx.channel_id),
            message,
        )
        self.bot.database_handler.commit()

        await ctx.respond(f"reminder set for {value} {unit}")

    async def _respond_with_reminder(self, userID: int, channelID: int) -> None:
        target_user = await self.bot.get_or_fetch_user(userID)

        if target_user:
            await target_user.send("You have been reminded!")
        else:
            self.bot.logger.error("No target user with given ID found in response to a reminder!")


def setup(bot: app.bot.Bot) -> None:
    bot.add_cog(Reminder(bot))
