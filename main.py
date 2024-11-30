#!/usr/bin/python3

import requests
import datetime
import time
import random
import re
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

font_path = "./assets/fonts/GaretHeavy.ttf"
image_path = "./assets/images/donation_thermometer.png"


def get_donation_count():
    URL = "https://www.idonate.ie/fundraiser/MediaProductionSociety12"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}

    data = {
        'totalRaised': 0,
        'targetAmount': 0
    }

    try:
        r = requests.get(url=URL, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html5lib')

        script_tag = soup.find('script', string=re.compile('totalRaised'))

        js_content = script_tag.string if script_tag else ''

        total_raised_match = js_content.replace('\\', '').split(',')

        for item in total_raised_match:
            if '"totalRaised":' in item:
                data['totalRaised'] = int(
                    float(item.split(':')[1].replace('"', '')))
            if '"targetAmount":' in item:
                data['targetAmount'] = int(
                    float(item.split(':')[1].replace('"', '')))

        return data

    except (requests.RequestException, ValueError, IndexError, AttributeError) as e:
        return data


def create_donation_thermometer(goal, current_donation, image_width=400, image_height=700):
    image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size=50)
    border_width = 10
    fixed_image_height = 700
    thermometer_width = 90

    draw.rectangle([(image_width // 2 - thermometer_width // 2, 250),
                    (image_width // 2 + thermometer_width // 2, fixed_image_height - 100)],
                   outline=(255, 255, 255), width=border_width)

    max_thermometer_height = fixed_image_height - 350
    bar_height = min(current_donation, goal)
    mercury_height = int((bar_height / goal) * max_thermometer_height)

    mercury_bottom = fixed_image_height - 105 - border_width
    mercury_top = mercury_bottom - mercury_height

    mercury_left = image_width // 2 - thermometer_width // 2 + 5 + border_width
    mercury_right = image_width // 2 + thermometer_width // 2 - 5 - border_width

    if mercury_height > 0:
        draw.rectangle([(mercury_left, mercury_top),
                       (mercury_right, mercury_bottom)], fill=(149, 239, 185))

    text = f"{current_donation} / {goal}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((image_width - text_width) // 2, fixed_image_height - 70),
              text, font=font, fill=(255, 255, 255))

    text = f"DONATION\nPROGRESS"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((image_width - text_width) // 2, fixed_image_height - 600),
              text, font=font, fill=(255, 255, 255))

    return image


while True:
    try:
        data = get_donation_count()
        current_donation_amount = data['totalRaised']
        goal_amount = data['targetAmount']

        thermometer_image = create_donation_thermometer(
            goal_amount, current_donation_amount)
        thermometer_image.save(image_path)

        cropped_image = Image.open(image_path)
        cropped_image = cropped_image.crop((0, 110, 400, 700))
        cropped_image.save(image_path)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"Donation Count Updated ({current_time}): €{current_donation_amount} out of €{goal_amount}")

        time.sleep(random.randint(10, 60))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        time.sleep(10)
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(10)
