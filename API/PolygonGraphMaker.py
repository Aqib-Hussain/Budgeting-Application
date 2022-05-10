import requests
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

api_key = 'p512p655R35DNWNBbVOWenkDy2PBdAVx'


def makeGraphForStock(stockName, fromDate, toDate):
    graph_data = requests.get(
        "https://api.polygon.io/v2/aggs/ticker/" + stockName + "/range/1/day/" + fromDate + "/" + toDate + "?adjusted=true&sort=asc&limit=50000&apiKey=" + api_key,
        timeout=30).json()
    stockName = graph_data['ticker']
    date_periods = []
    closing_prices = []
    for entry in graph_data['results']:
        date_periods.append(datetime.fromtimestamp((entry['t'] / 1000.0)))
        closing_prices.append(entry['c'])

    sns.set_style("darkgrid")
    sns.lineplot(date_periods, closing_prices)
    sns.set(rc={'figure.figsize': (40, 40)})
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title(stockName + " Closing Prices from: " + fromDate + " to: " + toDate)
    plt.savefig('static/images/stockClosingPriceGraph.jpg',bbox_inches='tight',dpi=300)
    plt.close()
