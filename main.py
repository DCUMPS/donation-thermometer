#!/usr/bin/python3

import requests 
from bs4 import BeautifulSoup 
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import random
from thermometer_config import loop_times, url, output_file, border_color, mercury_color, font_path, font_size

def create_donation_thermometer(goal, current_donation, image_width=400, image_height=700):
  
    image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, size=font_size)
    border_width = 10
    fixed_image_height = 700
    thermometer_width = 90
    draw.rectangle([(image_width // 2 - thermometer_width // 2, 250), (image_width // 2 + thermometer_width // 2, fixed_image_height - 100)], outline=border_color, width=border_width)

    max_thermometer_height = image_height
    bar_height = current_donation
    if current_donation >= goal:
        bar_height = goal

    mercury_height = (int((bar_height / goal) * max_thermometer_height)) / 2

    mercury_top = fixed_image_height - 95 - mercury_height + border_width
    mercury_bottom = fixed_image_height - 105 - border_width
    mercury_left = image_width // 2 - thermometer_width // 2 + 5 + border_width
    mercury_right = image_width // 2 + thermometer_width // 2 - 5 - border_width
    draw.rectangle([(mercury_left, mercury_top), (mercury_right, mercury_bottom)], fill=mercury_color)

    text = f"{current_donation} / {goal}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((image_width - text_width) // 2, fixed_image_height - 70), text, font=font, fill=(255, 255, 255))

    text = f"DONATION\nPROGRESS"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((image_width - text_width) // 2, fixed_image_height - 600), text, font=font, fill=(255, 255, 255))

    return image

for i in range(loop_times):
    URL = url
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
    r = requests.get(url=URL, headers=headers) 
    soup = BeautifulSoup(r.content, 'html5lib')
    current_donation = soup.find('div', attrs = {'class':'ifs-right-fundraisers-head'}) 
    donation_target = soup.find('div', attrs = {'class':'support-cause'}) 
    current_donation_amount = int(str(current_donation).split()[3].split("€")[1].split("<")[0].replace(",",""))
    goal_amount = int(str(donation_target).split("€")[1].split("<")[0].replace(",",""))
    thermometer_image = create_donation_thermometer(goal_amount, current_donation_amount)
    thermometer_image.save(output_file)
    cropped_image = Image.open(output_file)
    cropped_image = cropped_image.crop((0, 110, 400, 700))
    cropped_image.save(output_file)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Donation Count Updated ({current_time}): €{current_donation_amount} out of €{goal_amount}")
    time.sleep(random.randint(100, 300))
