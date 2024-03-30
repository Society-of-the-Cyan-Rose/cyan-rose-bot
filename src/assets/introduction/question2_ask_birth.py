from discord.ui import Button, View, Modal, TextInput, button
from discord import Embed, ButtonStyle, Interaction
from database.tables import Introduction

from . import question2_point_5_pnts_birth, question3_ask_reason

import logging

logger = logging.getLogger("cyan")

birth_embed = Embed(title="When were you born?", 
                    description="Hint: Click the button below and enter your date of birth! If you don't feel comfortable sharing your date of birth, you can click the 'Prefer not to share' button!\n\nPlease do note we don't accept applicants under the age of 13 due to Discord's Terms of Service.",
                    color=0x00ffff,)
birth_embed.set_thumbnail(url="https://raw.githubusercontent.com/Society-of-the-Cyan-Rose/cyan-rose-discord-bot/main/src/assets/cyan-rose.png")

class birth_modal(Modal):
    def __init__(self):
        super().__init__(timeout=None, title="Enter your date of birth!")
        
        self.birth_input = TextInput(label="Enter your date of birth here:", placeholder="DD/MM/YYYY", min_length=10, max_length=10, required=True)
        self.add_item(self.birth_input)
    
    async def interaction_check(self, interaction: Interaction):
        
        Introduction.create(user_id=interaction.user.id, part=1, introduction=f"{self.birth_input.value}")
        await interaction.response.edit_message(embed=question3_ask_reason.reason_embed, view=question3_ask_reason.reason_view())

class birth_view(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Enter your date of birth", style=ButtonStyle.primary)
    async def get_birth_button(self, interaction : Interaction, button : Button):
        logger.debug(f"Button: Get Birth | User: {interaction.user}")
        await interaction.response.send_modal(birth_modal())
    
    @button(label="Prefer not to share", style=ButtonStyle.danger)
    async def prefer_not_to_share_button(self, interaction : Interaction, button : Button):
        logger.debug(f"Button: Prefer Not To Share | User: {interaction.user}")
        await interaction.response.edit_message(embed=question2_point_5_pnts_birth.birth_embed, view=question2_point_5_pnts_birth.birth_view())