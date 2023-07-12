from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
import discord
from discord.ext import commands
from discord import app_commands

class ApartmentCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(description="Apartment Check")
    async def apartment(self, ctx):
        await ctx.defer()
        text = await check()
        await ctx.reply(f"{text}")
        # await ctx.channel.send(f"{text}")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(ApartmentCog(bot))

async def check():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    
    driver = webdriver.Chrome(options=chrome_options) 
    driver.get("https://www.sdkvillagegreen.com/Floor-Plans.aspx") 

    def get_prices(name, button_id, table_id):
        element = driver.find_element(By.ID, button_id)
        element.click()

        sleep(2)

        element = driver.find_element(By.ID, table_id)
        print(element.text)

        message = f'# {name} Apartment Prices\n\n' + element.text + '\n\n'
        open('log.txt', 'a').writelines([str(datetime.now()),'\n>>> ', element.text, '\n\n'])
        return message

    messages = ''
    messages += get_prices('One Bed Den Deluxe', 'unit_show_hide_3557246', 'par_3557246')
    messages += get_prices('One Bed Den Premium', 'unit_show_hide_8602955', 'par_8602955')
    messages += get_prices('Two Bed Platinum', 'unit_show_hide_10960129', 'par_10960129')
    driver.close()
    return messages

# Email part

# import smtplib, ssl

# port = 465  # For SSL
# password = 'P3UZ55tp6vHu8eTF'

# # Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("pawkun14@gmail.com", password)
#     server.sendmail('pawkun14@gmail.com', 'willowlark@outlook.com', message)
