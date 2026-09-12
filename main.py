# main.py
import discord
from discord.ext import commands, tasks
import os
import logging

# Configuración de logging para auditoría y depuración
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('sakee')

# Intents necesarios para el funcionamiento del bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class SakeeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents, help_command=None)
        self.initial_extensions = [
            'welcome',
            'autoroles'
        ]

    async def setup_hook(self):
        """Carga las extensiones (cogs) al iniciar el bot."""
        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
                logger.info(f'Extensión cargada: {ext}')
            except Exception as e:
                logger.error(f'Error al cargar {ext}: {e}')

    async def on_ready(self):
        logger.info(f'Bot conectado como {self.user} (ID: {self.user.id})')
        logger.info(f'Conectado a {len(self.guilds)} servidores')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='la seguridad de tus servidores'))

    async def on_command_error(self, ctx, error):
        """Manejo centralizado de errores (seguridad: no filtrar trazas internas)."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond('No tienes permisos suficientes para ejecutar este comando.', ephemeral=True)
        elif isinstance(error, commands.CommandNotFound):
            pass  # Silencioso para no revelar comandos existentes
        else:
            logger.error(f'Error en comando {ctx.command}: {error}')
            await ctx.respond('Ocurrió un error inesperado. Por favor, intente nuevamente.', ephemeral=True)

bot = SakeeBot()

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError('La variable de entorno DISCORD_TOKEN no está definida.')
    bot.run(token)
