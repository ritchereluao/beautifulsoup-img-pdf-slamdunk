from bs4 import BeautifulSoup
import requests
import os
import img2pdf
from natsort import natsorted
from glob import glob

url = f"https://mangaclash.com/manga/slam-dunk/chapter-193/"
response = requests.get(url=url)
soup = BeautifulSoup(response.text, "html.parser")

heading = soup.find(name="h1", id="chapter-heading").getText()
print(heading)

reading_content = soup.find_all("div", class_="page-break")

image_urls = []
for url in reading_content:
    img = url.find("img")
    if img is not None:
        image_url = img.get("data-src")
        if image_url is not None:
            image_urls.append(image_url.strip("\t\n"))
print(image_urls)

# Creates Folder
folder_name = f"./{heading}"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Saves images to the folder
page_number = 1
for url in image_urls:
    response = requests.get(url)
    with open(f"{folder_name}/Page_{page_number}.jpg", "wb") as file:
        file.write(response.content)
        page_number += 1

# Converts images to single PDF file
with open(f"{heading}.pdf", "wb") as file:
    file.write(img2pdf.convert(natsorted(glob(f"{folder_name}/*.jpg"))))
