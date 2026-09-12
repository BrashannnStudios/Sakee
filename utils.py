# utils.py
import json
import os
import aiofiles
from pathlib import Path
from urllib.parse import urlparse
import discord

DATA_DIR = Path('./data')
DATA_DIR.mkdir(exist_ok=True)
os.chmod(DATA_DIR, 0o700)  # Restringir permisos del directorio

def _guild_file(guild_id: int, feature: str) -> Path:
    """Devuelve la ruta del archivo de configuración para un servidor."""
    return DATA_DIR / f'{guild_id}_{feature}.json'

async def load_config(guild_id: int, feature: str) -> dict:
    """Carga la configuración persistida para un servidor y característica."""
    file = _guild_file(guild_id, feature)
    if not file.exists():
        return {}
    try:
        async with aiofiles.open(file, 'r') as f:
            data = await f.read()
            return json.loads(data)
    except (json.JSONDecodeError, OSError) as e:
        raise ValueError(f'Error al leer configuración: {e}')

async def save_config(guild_id: int, feature: str, config: dict) -> None:
    """Persiste la configuración de forma segura."""
    file = _guild_file(guild_id, feature)
    os.chmod(file, 0o600)  # Solo el propietario puede leer/escribir
    async with aiofiles.open(file, 'w') as f:
        await f.write(json.dumps(config, indent=2, ensure_ascii=False))

def validate_url(url: str) -> bool:
    """Valida que una URL sea segura (solo https/http explícito, sin esquemas peligrosos)."""
    if not url:
        return True  # Campo opcional
    parsed = urlparse(url)
    return parsed.scheme in ('https', 'http') and parsed.netloc

def validate_channel(bot: commands.Bot, guild: discord.Guild, channel_id: int) -> bool:
    """Verifica que el canal exista y sea de tipo texto."""
    channel = guild.get_channel(channel_id)
    return isinstance(channel, discord.TextChannel)

def validate_role(guild: discord.Guild, role_id: int) -> bool:
    """Verifica que el rol exista en el servidor."""
    return guild.get_role(role_id) is not None

def build_embed(title: str, description: str, color: discord.Color, image_url: str = None, footer: str = None) -> discord.Embed:
    """Construye un embed de forma segura, sanitizando las URLs."""
    embed = discord.Embed(title=title, description=description, color=color)
    if image_url and validate_url(image_url):
        embed.set_image(url=image_url)
    if footer:
        embed.set_footer(text=footer)
    return embed
