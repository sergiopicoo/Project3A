import requests
from datetime import datetime
import lxml

class StockData:
    def build_url(self, symbol, time_series, api_key):
        symbol_options = {"1": "TIME_SERIES_INTRADAY",
                          "2": "TIME_SERIES_DAILY_ADJUSTED",
                          "3": "TIME_SERIES_WEEKLY",
                          "4": "TIME_SERIES_MONTHLY"}
        
        if (time_series == "1"):
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=15min&apikey=CFSBLCRTK0NRBSA4'
        elif (time_series == "2"):
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=15min&apikey=CFSBLCRTK0NRBSA4'
        else:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=15min&apikey=CFSBLCRTK0NRBSA4"

            return url
        

def query_api(self, url):

    response = requests.get(url)
    response_data = response.json()
    return response_data

def append_data_to_lists(self, open, high, low, close, data_dict):
    open.append(float(data_dict['1. open']))
    high.append(float(data_dict['2. high']))
    low.append(float(data_dict['3. low']))
    close.append(float(data_dict['4. close']))
    return

def get_data_from_json(self, json_data, time_series, start_date, end_date):
    series_field = {"1": "Time Series (15min)", 
                    "2": "Time Series (Daily)",
                    "3": "Weekly Time Series",
                    "4": "Monthly Time Series"}
    
    dates, open, high, low, close = [], [], [], [], []

    for current_date in json_data[series_field[time_series]]:
        if (time_series == "1"):
            date_parts = current_date.split(" ")
            data_date = datetime.strptime(date_parts[0], "%Y-%m-%d")

            if(start_date == data_date):
                dates.append(current_date)
                self.append_data_to_lists(open, high, low, close, json_data[series_field[time_series]][current_date])

        else:
            data_date = datetime.strptime(current_date, "%Y-%m-%d")
            if (start_date <= data_date <= end_date):
                dates.append(current_date)
                self.append_data_to_lists(open, high, low, close, json_data[series_field[time_series]][current_date])

    dates.reverse()
    open.reverse()
    high.reverse()
    low.reverse()
    close.reverse()

    return dates, open, high, low, close

def get_stock_data(self, symbol, time_series, start_date, end_date):
    api_key = "CFSBLCRTK0NRBSA4"

    url = self.build_url(symbol, time_series, api_key)

    json_data = self.query_api(url)

    dates, open, high, low, close = self.get_data_from_json(json_data, time_series, start_date, end_date)

    return {"dates":dates,
            "open":open,
            "high":high,
            "low":low,
            "close":close}



