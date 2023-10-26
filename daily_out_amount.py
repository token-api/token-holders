# This code queries Bitquery's GraphQL API to retrieve and display daily out amounts for USDT and USDC token contracts for the last 30 days,
# starting from 30 days ago to October 23, 2023. It then plots side-by-side graphs to visualize the daily out amounts over time.

# Replace 'graphql_endpoint' with your GraphQL endpoint and consider signing up for Bitquery to access the API.

# Import necessary libraries
import requests
import matplotlib.pyplot as plt
import datetime

# Define the GraphQL queries for USDT and USDC
usdt_query = '''
{
  EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "%s"
      tokenSmartContract: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    ) {
      sum(of: BalanceUpdate_OutAmount)
    }
  }
}
'''

usdc_query = '''
{
  EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "%s"
      tokenSmartContract: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    ) {
      sum(of: BalanceUpdate_OutAmount)
    }
  }
}
'''

# Define the endpoint URL for Bitquery
url = 'https://streaming.bitquery.io/graphql'

# Initialize lists to store dates and daily out amounts for USDT and USDC
dates = []
usdt_daily_out_amounts = []
usdc_daily_out_amounts = []

# Calculate the start date (30 days ago from October 23, 2023)
end_date = datetime.date(2023, 10, 23)
start_date = end_date - datetime.timedelta(days=30)

# Function to retrieve the sum of out amounts for a specific date and token
def get_daily_out_amount(query, date):
    formatted_query = query % date
    response = requests.post(url, json={'query': formatted_query})
    data = response.json()
    sum_out_amount = float(data.get('data', {}).get('EVM', {}).get('TokenHolders', [{}])[0].get('sum', 0))
    return sum_out_amount

# Calculate daily out amounts for the last 30 days for USDT and USDC
current_date = start_date
while current_date <= end_date:
    dates.append(current_date)
    usdt_out_amount = get_daily_out_amount(usdt_query, current_date)
    usdc_out_amount = get_daily_out_amount(usdc_query, current_date)
    usdt_previous_out_amount = get_daily_out_amount(usdt_query, current_date - datetime.timedelta(days=1))
    usdc_previous_out_amount = get_daily_out_amount(usdc_query, current_date - datetime.timedelta(days=1))
    usdt_daily_out_amount = usdt_out_amount - usdt_previous_out_amount
    usdc_daily_out_amount = usdc_out_amount - usdc_previous_out_amount
    usdt_daily_out_amounts.append(usdt_daily_out_amount)
    usdc_daily_out_amounts.append(usdc_daily_out_amount)
    current_date += datetime.timedelta(days=1)

# Create side-by-side graphs for USDT and USDC
plt.figure(figsize=(12, 6))

# Plot the USDT graph
plt.subplot(1, 2, 1)
plt.plot(dates, usdt_daily_out_amounts, marker='o')
plt.xlabel('Date')
plt.ylabel('USDT Daily Out Amount (Float)')
plt.title('USDT Daily Out Amount for the Last 30 Days')
plt.grid(True)
plt.xticks(rotation=45)

# Plot the USDC graph
plt.subplot(1, 2, 2)
plt.plot(dates, usdc_daily_out_amounts, marker='o')
plt.xlabel('Date')
plt.ylabel('USDC Daily Out Amount (Float)')
plt.title('USDC Daily Out Amount for the Last 30 Days')
plt.grid(True)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Sign up for Bitquery to access Bitquery's API and explore more data: https://ide.bitquery.io/streaming
