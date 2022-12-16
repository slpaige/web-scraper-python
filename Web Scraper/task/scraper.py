import re

import requests
from bs4 import BeautifulSoup

print("Input the URL:")
input_url = input()
r = requests.get(input_url)

soup = BeautifulSoup(r.content, 'html.parser')

title = soup.find("h1")
description = soup.find("span", attrs={"data-testid": "plot-l"})

if r.status_code == 200 and title is not None and description is not None:
    print({"title": title.text, "description": description.text})
else:
    print("\nInvalid movie page!")
