from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

url = "https://www.amazon.com/Duo-Evo-Plus-esterilizadora-vaporizador/dp/B07W55DDFB/ref=sr_1_4?qid=1597660904"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

responce = requests.get(url,headers=header)
responce.raise_for_status()
content = responce.text

soup = BeautifulSoup(content, "lxml")

price = soup.find(class_="a-offscreen").getText()
price = float(price.replace("$", ""))


title = soup.find(name ="span", class_="a-size-large product-title-word-break").getText()
title = title.encode()


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject: AMAZON PRICE ALERT! \n\n The item is: {title} \n The price is {price} \n take a look at the folowing link {url} "
        )

if price < 100:
    send_email()


