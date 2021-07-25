import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
account_sid = "your sid goes here (from twilio)"
auth_token = "authentication token (from twilio)"
NEWS_API_KEY = "api key of https://newsapi.org"

news_parameters = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME
}

ALPHA_API_KEY = "api key of https://www.alphavantage.co"
parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
}
stock_Endpoint = "https://www.alphavantage.co/query"

market_stock = requests.get(stock_Endpoint, params=parameters)
market_stock.raise_for_status()
data = market_stock.json()

yest_stock = float(data["Time Series (Daily)"]["2021-07-23"]["4. close"])
yest_yest_stock = float(data["Time Series (Daily)"]["2021-07-22"]["4. close"])
print(yest_stock)
print(yest_yest_stock)

top_headlines_endpoint = "https://newsapi.org/v2/top-headlines"
news = requests.get(top_headlines_endpoint, params=news_parameters)
news.raise_for_status()
data_2 = news.json()

title_list = []
news_list = []
news = data_2["articles"]
for new in range(3):
    title_list.append(news[new]["title"])
    news_list.append(news[new]["description"])

change = round((yest_stock / yest_yest_stock - 1) * 100, 2)

if 0.05 <= change - 100:
    for n in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
             body=f"TSLA: 🔺{change}%\nHeadline: {title_list[n]}\nBrief: {news_list[n]}",
             from_="+185...",
             to="+998..."
            )
        print(message.status)
elif change - 100 <= -0.05:
    for n in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=f"TSLA: 🔻{change * -1}%\n\nHeadline: {title_list[n]}\n\nBrief: {news_list[n]}",
                from_="+185...",
                to="+998..."
            )
        print(message.status)

for n in range(3):
    print(f"TSLA: 🔻{change * -1}%\n\nHeadline: {title_list[n]}\n\nBrief: {news_list[n]}")
