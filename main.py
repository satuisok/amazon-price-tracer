import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib

load_dotenv()

amazon_endpoint = "https://www.amazon.com/Instant-Pot-Electric-Sterilizer-Stainless/dp/B09MZTP44L/ref=pd_rhf_ee_s_pd_sbs_rvi_d_sccl_1_2/138-1856029-6007022?pd_rd_w=t8SUr&content-id=amzn1.sym.a089f039-4dde-401a-9041-8b534ae99e65&pf_rd_p=a089f039-4dde-401a-9041-8b534ae99e65&pf_rd_r=DDNBM2FYK7YVHFPX2V6G&pd_rd_wg=VRevy&pd_rd_r=2b6b844d-c1e0-4f47-a073-4afd4b281838&pd_rd_i=B09MZTP44L&th=1"
connection = requests.get(url=amazon_endpoint)
print(connection.status_code)
page = connection.text

soup = BeautifulSoup(page, "html.parser")
# print(soup.prettify())

# Dig out the product name from the html
product = soup.select_one("#productTitle").getText().strip()
print(product)

# Dig the cooker price out of the html
price_span = soup.select("span.a-price-whole")[1]
cents_span = soup.select("span.a-price-fraction")[1]
whole_price = price_span.getText().split(".")[0]
cents = cents_span.getText()

# Concat the total price and change it to float
total_price = float(f"{whole_price}.{cents}")
print(total_price)

if total_price < 130.00:
    email = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        # 2. secure the connection:
        connection.starttls()
        # 3. login to your email by using the app password:
        connection.login(user=email, password=password)
        connection.sendmail(
            # 4. Sender email:
            from_addr=email,
            # 5. Recipient email:
            to_addrs=os.getenv("RECIVER_EMAIL"),
            # 6. Message. Notice the way to add the subject title:
            msg=f"Subject:Your Amazon Target on Sale Now!\n\n{product} is now ${total_price}".encode('utf-8'))


