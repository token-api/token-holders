''' 
This Python script fetches and visualizes historical token holder data with 
balances greater than 1,000,000 for two Ethereum-based tokens: USDC and USDT. 
It utilizes Bitquery's GraphQL API to fetch data, and Matplotlib for plotting. 
The data is collected for the past 30 days and presented in two separate subplots for each token.

To explore more blockchain data and gain deeper insights, 
sign up for Bitquery at https://ide.bitquery.io/streaming#utm_source=github&utm_medium=token_api_org&utm_campaign=token_holders_api.
'''

import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the GraphQL queries for both token contracts
query_template = '''
{
  EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "%s"  # Date parameter for the query
      tokenSmartContract: "%s"  # Token contract address parameter
      where: {Balance: {Amount: {gt: "1000000"}}}
    ) {
      uniq(of: Holder_Address)
    }
  }
}
'''

# Define the endpoint URL for GraphQL API
url = 'https://streaming.bitquery.io/graphql'

# Start date and end date for the data retrieval period
end_date = datetime(2023, 10, 21)
start_date = end_date - timedelta(days=30)  # You can adjust the number of days as needed

# Token contract addresses
token_contract1 = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
token_contract2 = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

# Initialize lists to store data for both contracts
dates = []  # List to store dates
holder_counts_contract1 = []  # List to store holder counts for token_contract1
holder_counts_contract2 = []  # List to store holder counts for token_contract2

# Loop to retrieve and store data for each date
current_date = end_date
while current_date >= start_date:
    for token_contract in [token_contract1, token_contract2]:
        formatted_query = query_template % (current_date.strftime("%Y-%m-%d"), token_contract)
        response = requests.post(url, json={'query': formatted_query})
        data = response.json()
        token_holders = data.get('data', {}).get('EVM', {}).get('TokenHolders', [{}])[0].get('uniq', '0')
        
        # Append the date and holder count to the respective lists
        if token_contract == token_contract1:
            holder_counts_contract1.append(int(token_holders))
        else:
            holder_counts_contract2.append(int(token_holders))
    
    # Append the date to the 'dates' list
    dates.append(current_date.strftime("%Y-%m-%d"))
    
    # Move to the previous date
    current_date -= timedelta(days=1)

# Reverse the lists for correct plotting order
dates.reverse()
holder_counts_contract1.reverse()
holder_counts_contract2.reverse()

# Plot the data for both token contracts side by side
plt.figure(figsize=(14, 6))

# Create two subplots, one for each token contract
plt.subplot(1, 2, 1)
plt.plot(dates, holder_counts_contract2, marker='o')
plt.title('USDC Whale History')
plt.xlabel('Date')
plt.ylabel('Number of Whales')
plt.xticks(rotation=45)
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(dates, holder_counts_contract1, marker='o')
plt.title('USDT Whale History')
plt.xlabel('Date')
plt.ylabel('Number of Whales')
plt.xticks(rotation=45)
plt.grid(True)

# Adjust the layout to prevent subplot overlap and show the plot
plt.tight_layout()
plt.show()
