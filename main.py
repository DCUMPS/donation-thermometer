#!/usr/bin/python3


import requests 
from bs4 import BeautifulSoup 
from PIL import Image, ImageDraw, ImageFont
import datetime

URL = "https://www.idonate.ie/fundraiser/MediaProductionSociety"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
r = requests.get(url=URL, headers=headers) 

soup = BeautifulSoup(r.content, 'html5lib')
current_donation = soup.find('div', attrs = {'class':'ifs-right-fundraisers-head'}) 
donation_target = soup.find('div', attrs = {'class':'support-cause'}) 
current_donation_amount = int(str(current_donation).split()[3].split("€")[1].split("<")[0])
goal_amount = int(str(donation_target).split("€")[1].split("<")[0].replace(",",""))

def create_donation_thermometer(goal, current_donation, image_width=200, image_height=300):
    # Create a blank image with RGBA color mode (4 channels including Alpha)
    image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Set font and size
    font = ImageFont.load_default()

    # Define colors
    border_color = (255, 255, 255)
    mercury_color = (255, 0, 0, 128)  # Set alpha to 128 for semi-transparency

    # Draw border
    #draw.rectangle([(0, 0), (image_width - 1, image_height - 1)], outline=border_color)

    # Draw thermometer outline
    thermometer_width = 40
    draw.rectangle([(image_width // 2 - thermometer_width // 2, 50), (image_width // 2 + thermometer_width // 2, image_height - 50)], outline=border_color)

    # Calculate mercury height based on current donation and goal
    max_thermometer_height = image_height - 100
    mercury_height = int((current_donation / goal) * max_thermometer_height)

    # Draw mercury
    mercury_top = image_height - 45 - mercury_height
    mercury_bottom = image_height - 55  # Adjust the offset as needed
    mercury_left = image_width // 2 - thermometer_width // 2 + 5
    mercury_right = image_width // 2 + thermometer_width // 2 - 5
    draw.rectangle([(mercury_left, mercury_top), (mercury_right, mercury_bottom)], fill=mercury_color)

    # Draw text
    text = f"Donation Progress: ${current_donation} / ${goal}"
    text_width, text_height = draw.textsize(text, font)
    draw.text(((image_width - text_width) // 2, image_height - 30), text, font=font, fill=(255, 255, 255))

    return image

# Example usage
#goal_amount = 7000
#current_donation_amount = int(input("Enter the current donation amount, Example: 1234 (No Decimals): "))
#current_donation_amount = 7000
thermometer_image = create_donation_thermometer(goal_amount, current_donation_amount)
thermometer_image.show()
thermometer_image.save("donation_thermometer.png")
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Donation Count Updated ({current_time}): €{current_donation_amount} out of €{goal_amount}")