from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
from .core import Command


class Roll(Command):

    async def action(self, message, match):
        text = main()
        await message.channel.send(f"{text}")


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    
    driver = webdriver.Chrome(options=chrome_options) 
    driver.get("https://www.sdkvillagegreen.com/Floor-Plans.aspx") 

    def get_prices(name, button_id, table_id):
        element = driver.find_element(By.ID, button_id)
        element.click()

        sleep(5)

        element = driver.find_element(By.ID, table_id)
        print(element.text)

        message = f'Subject: {name} Apartment Prices\n\n' + element.text
        open('log.txt', 'a').writelines([str(datetime.now()),'\n', element.text, '\n\n'])

    get_prices('One Bed Den Deluxe', 'unit_show_hide_3557246', 'par_3557246')

    driver.close()

# Email part

# import smtplib, ssl

# port = 465  # For SSL
# password = 'P3UZ55tp6vHu8eTF'

# # Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("pawkun14@gmail.com", password)
#     server.sendmail('pawkun14@gmail.com', 'willowlark@outlook.com', message)
