import pygal

class ChartGenerator:

    def generate_chart(self, stock_data_dict, chart_type, symbol, start_date, end_date, time_series):

        if(chart_type == "1"):
            chart_object = pygal.Bar(x_label_rotation=45)
        else:
            chart_object = pygal.Line(x_label_rotation=45)

        if (time_series == "1"):
            chart_title = f"Stock Data for {symbol}: {str(start_date)}"
        else:
            chart_title = f"Stock Data for {symbol}: {str(start_date)} to {str(end_date)}"

        chart_object.title = chart_title
        chart_object.x_labels = stock_data_dict['dates']
        chart_object.add("Open", stock_data_dict['open'])
        chart_object.add("High", stock_data_dict['high'])
        chart_object.add("Low", stock_data_dict['low'])
        chart_object.add("Close", stock_data_dict['close'])
        
        chart_object.render_in_browser()

