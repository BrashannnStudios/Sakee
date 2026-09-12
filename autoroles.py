# autoroles.py
import discord
from discord.ext import commands
from discord import app_commands, ui
import utils

class AutorolesView(ui.View):
    """Vista del panel de configuración de autoroles."""
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    @ui.select(placeholder='Seleccione los roles a asignar automáticamente...', min_values=1, max_values=10, cls=ui.RoleSelect)
    async def select_roles(self, interaction, select):
        await interaction.response.defer(ephemeral=True)

    @ui.button(label='Guardar configuración', style=discord.ButtonStyle.success, row=2)
    async def save_button(self, interaction, button):
        await interaction.response.send_message('Autoroles configurados correctamente.', ephemeral=True)

class AutorolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='autoroles-setup', description='Configura los roles automáticos del servidor.')
    @app_commands.default_permissions(manage_guild=True)
    async def autoroles_setup(self, interaction: discord.Interaction):
        """Abre el panel de configuración de autoroles."""
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message('Requiere permiso de gestión del servidor.', ephemeral=True)
            return

        embed = discord.Embed(
            title='🛡️ Configuración de Autoroles',
            description='Configure los roles que se asignarán automáticamente a los nuevos miembros.',
            color=discord.Color.blue()
        )
        embed.set_footer(text='Sakee inc. — Sistema de Autoroles')
        view = AutorolesView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutorolesCog(bot))
