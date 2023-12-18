from PIL import Image, ImageDraw, ImageFont
import requests 
from bs4 import BeautifulSoup 

def draw_rounded_rectangle_with_semicircles(image_size, corner_radius, text, font_size):
    # Create a new RGBA image with a transparent background
    img = Image.new('RGBA', image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_path = "GaretHeavy.ttf"
    font = ImageFont.truetype(font_path, size=font_size)
    text_width, text_height = draw.textsize(text, font)

    rectangle_size = (text_width + 2 * corner_radius, text_height + 2 * corner_radius)

    # Draw the rectangle with semi-circle ends
    x1, y1 = (image_size[0] - rectangle_size[0]) // 2, (image_size[1] - rectangle_size[1]) // 2
    x2, y2 = x1 + rectangle_size[0], y1 + rectangle_size[1]

    fill_colour = (166, 229, 228)
    outline_colour = fill_colour

    # Draw the main rectangle with transparent edges
    draw.rectangle([x1 + corner_radius, y1, x2 - corner_radius, y2], fill=fill_colour, outline=outline_colour)
    draw.rectangle([x1, y1 + corner_radius, x2, y2 - corner_radius], fill=fill_colour, outline=outline_colour)

    # Draw semi-circle ends with transparent edges
    draw.pieslice([x1, y1, x1 + 2 * corner_radius, y1 + 2 * corner_radius], 180, 270, fill=fill_colour, outline=outline_colour)
    draw.pieslice([x2 - 2 * corner_radius, y1, x2, y1 + 2 * corner_radius], 270, 360, fill=fill_colour, outline=outline_colour)
    draw.pieslice([x1, y2 - 2 * corner_radius, x1 + 2 * corner_radius, y2], 90, 180, fill=fill_colour, outline=outline_colour)
    draw.pieslice([x2 - 2 * corner_radius, y2 - 2 * corner_radius, x2, y2], 0, 90, fill=fill_colour, outline=outline_colour)


    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
    draw.text(text_position, text, font=font, fill=(255, 255, 255))  # Black text

    # Save or display the image
    img.save("latest_donation.png")

URL = "https://www.idonate.ie/fundraiser/MediaProductionSociety"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
r = requests.get(url=URL, headers=headers) 

soup = BeautifulSoup(r.content, 'html5lib')
supporters = soup.find('div', attrs = {'class':'ifs-right-fundraisers-supportes-personal'}) 
name = str(supporters).split(">")[5].split("<")[0].strip()
amount = str(supporters).split(">")[13].split("<")[0].strip()

# Example usage
image_size = (1600, 400)  # Width, Height
corner_radius = 25
font_size = 75
text = f"{name} - {amount}"
#text = "I"
draw_rounded_rectangle_with_semicircles(image_size, corner_radius, text, font_size)
