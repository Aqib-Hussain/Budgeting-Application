import requests
from datetime import datetime
from Visualisations.BuildGraphs import buildApiCharts

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

    buildApiCharts(date_periods, closing_prices, stockName, fromDate, toDate)
