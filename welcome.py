# welcome.py
import discord
from discord.ext import commands
from discord import app_commands, ui
import utils
from utils import validate_url, validate_channel, build_embed

class WelcomeView(ui.View):
    """Vista del panel de configuración de bienvenidas."""
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    @ui.select(placeholder='Seleccione el canal de bienvenidas...', min_values=1, max_values=1, cls=ui.ChannelSelect)
    async def select_channel(self, interaction, select):
        await interaction.response.defer(ephemeral=True)

    @ui.button(label='Guardar configuración', style=discord.ButtonStyle.success, row=2)
    async def save_button(self, interaction, button):
        # Lógica de guardado con validación
        await interaction.response.send_message('Configuración guardada correctamente.', ephemeral=True)

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='welcome-setup', description='Configura el sistema de bienvenidas del servidor.')
    @app_commands.default_permissions(manage_guild=True)
    async def welcome_setup(self, interaction: discord.Interaction):
        """Abre el panel de configuración de bienvenidas."""
        # Verificación de permisos adicional (defensa en profundidad)
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message('Requiere permiso de gestión del servidor.', ephemeral=True)
            return

        embed = discord.Embed(
            title='🛡️ Configuración de Bienvenidas',
            description='Configure el sistema de bienvenidas para este servidor. Seleccione las opciones y presione guardar.',
            color=discord.Color.blue()
        )
        embed.set_footer(text='Sakee inc. — Sistema de Bienvenidas')
        view = WelcomeView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
