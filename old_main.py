from core.models import Portfolio, Plot
from core.utils import get_data, get_latest_date, set_values, render_template, send_email
from core.constants import Email, Graph, Simfonia, Diverso, Total

# ----- Simfonia -----
# Name will be used to print the plot name.
name = Simfonia.NAME

# Data is a list of integers calculated by multiplying VUAN and UNITS.
data = set_values(get_data(Simfonia.URL), Simfonia.UNITS)

# Gain refers to actual gain over the invested amount.
gain = data[0] - Simfonia.INVESTED
max_gain = max(data) - Simfonia.INVESTED

# We plot the latest date.
latest_date = get_latest_date(Simfonia.URL)

# To correctly plot any range of values we use a pixel delimiter defined in Graph constants.
# In short, we set the maximum height for the highest value and 50 pixels for lowest value.
# Each plot has a gradient so we define a start and end color.
plot = Plot(Graph.PLOT_MAX_PIXELS, Simfonia.START_COLOR, Simfonia.END_COLOR)

# Instantiate portfolio.
simfonia = Portfolio(name, data, gain, max_gain, latest_date, plot)

# ----- Diverso -----

# Name will be used to print the plot name.
name = Diverso.NAME

# Data is a list of integers calculated by multiplying VUAN and UNITS.
data = set_values(get_data(Diverso.URL), Diverso.UNITS)

# Gain refers to actual gain over the invested amount.
gain = data[0] - Diverso.INVESTED
max_gain = max(data) - Diverso.INVESTED

# We plot the latest date.
latest_date = get_latest_date(Diverso.URL)

# To correctly plot any range of values we use a pixel delimiter defined in Graph constants.
# In short, we set the maximum height for the highest value and 50 pixels for lowest value.
# Each plot has a gradient so we define a start and end color.
plot = Plot(Graph.PLOT_MAX_PIXELS, Diverso.START_COLOR, Diverso.END_COLOR)

# Instantiate portfolio.
diverso = Portfolio(name, data, gain, max_gain, latest_date, plot)

# ----- Total -----

# Total doesn't actually use NAME anywhere, we might remove it later on.
name = Total.NAME

# We add the data from the portfolios here so that total data is sum of all data.
data = []
if len(simfonia.data) > len(diverso.data):
    data_range = len(diverso.data)
else:
    data_range = len(simfonia.data)

for index in range(data_range):
    data.append(simfonia.data[index] + diverso.data[index])

gain = simfonia.gain + diverso.gain
max_gain = simfonia.max_gain + diverso.max_gain

# Not that important, can be the first portfolio date.
latest_date = simfonia.latest_date

plot = Plot(Graph.PLOT_MAX_PIXELS, Total.START_COLOR, Total.END_COLOR)

total = Portfolio(name, data, gain, max_gain, latest_date, plot)


def local():
    """
        This is used to run the render locally. Upon run it will open
        a new tab in firefox and plot the portfolios data.
    """
    render_template(simfonia, diverso, total, Graph.PLOT_MAX_PIXELS, True)


def lambda_handler(event, context):
    """
        This is the function AWS Lambda will call when running the application.
    """
    email_body = render_template(simfonia, diverso, total,
                                 Graph.PLOT_MAX_PIXELS)
    send_email(Email.SUBJECT, email_body, Email.AWS_REGION, Email.RECIPIENT,
               Email.CHARSET, Email.SENDER)
    return {'statusCode': 200}


if __name__ == '__main__':
    local()
