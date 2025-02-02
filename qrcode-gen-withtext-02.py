'''
This Python script generates a QR code for a user-provided URL and adds a title, 
website name, and URL text to the image. The title "This code generated by Yara's QR Code App" is displayed in red above the QR code, 
the website name in blue below the QR code, and the URL in pink at the bottom. 
The final image is saved in the project folder as "qrcode_with_text.png".
'''

import qrcode
from PIL import Image, ImageDraw, ImageFont

# Greet the user
print("Hello! Welcome to the QR Code Generator.")

# Request the website name from the user
website_name = input("Please enter the website name: ")

# Request the URL from the user
url = input("Please enter the website address: ")

# Generate the QR code
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR Code
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Controls the error correction used for the QR Code
    box_size=10,  # Controls how many pixels each “box” of the QR code is
    border=4,  # Controls how many boxes thick the border should be
)

qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# Define fonts and sizes
title_font_size = 12
text_font_size = 15
try:
    title_font = ImageFont.truetype("arial.ttf", title_font_size)
    text_font = ImageFont.truetype("arial.ttf", text_font_size)
except IOError:
    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()

# Calculate the width and height of the texts to be added
draw = ImageDraw.Draw(img)
title_text = "This code is generated by Yaras python QR Code"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]

website_name_bbox = draw.textbbox((0, 0), website_name, font=text_font)
website_name_width, website_name_height = website_name_bbox[2] - website_name_bbox[0], website_name_bbox[3] - website_name_bbox[1]

url_bbox = draw.textbbox((0, 0), url, font=text_font)
url_width, url_height = url_bbox[2] - url_bbox[0], url_bbox[3] - url_bbox[1]

# Create a new image with extra space for the title and texts
new_img_height = title_height + img.size[1] + website_name_height + url_height + 30  # Add some padding
new_img = Image.new("RGB", (img.size[0], new_img_height), "white")

# Draw the title text onto the new image
draw = ImageDraw.Draw(new_img)
title_position = ((new_img.size[0] - title_width) // 2, 10)  # Center the title text and add padding
draw.text(title_position, title_text, fill="blue", font=title_font)  # Title in red

# Paste the QR code onto the new image
qr_code_position = (0, title_height + 20)  # Add padding between title and QR code
new_img.paste(img, qr_code_position)

# Draw the website name onto the new image
website_name_position = ((new_img.size[0] - website_name_width) // 2, title_height + img.size[1] + 10)  # Add padding
draw.text(website_name_position, website_name, fill="red", font=text_font)  # Website name in blue

# Draw the URL text onto the new image
url_position = ((new_img.size[0] - url_width) // 2, title_height + img.size[1] + website_name_height + 20)  # Add padding
draw.text(url_position, url, fill="green", font=text_font)  # URL in pink

# Save the image
image_path = "00_qrcode_with_text.png"
new_img.save(image_path)

print(f"QR code generated and saved as {image_path}")
