# Analyzing and plotting data for USDT and USDC wallet liquidations over a 30-day period

# Replace 'graphql_endpoint' with your GraphQL endpoint and consider signing up for Bitquery to access the API.

# Import necessary libraries
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the GraphQL queries for both token contracts
query_template = '''
{
  EVM(dataset: archive, network: eth) {
    TokenHolders(
      limit: {count: 100}
      tokenSmartContract: "%s"
      date: "%s"
      where: {BalanceUpdate: {LastDate: {is: "%s"}, OutAmount: {gt: "0"}}, Balance: {Amount: {eq: "0"}}}
    ) {
      uniq(of: Holder_Address)
    }
  }
}
'''

# Define the endpoint URL for Bitquery
url = 'https://streaming.bitquery.io/graphql'

# Start date and end date for the analysis
end_date = datetime(2023, 10, 23)
start_date = end_date - timedelta(days=30)  # Adjust the number of days as needed

# Token contract addresses for USDT and USDC
token_contract1 = "0xdac17f958d2ee523a2206206994597c13d831ec7"  # USDT contract address
token_contract2 = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC contract address

# Initialize lists to store data for both contracts
dates = []  # List to store dates
holder_counts_contract1_l = []  # List to store USDT liquidation counts
holder_counts_contract2_l = []  # List to store USDC liquidation counts

# Loop to retrieve and store data for each date
current_date = end_date
while current_date >= start_date:
    for token_contract in [token_contract1, token_contract2]:
        formatted_query = query_template % (token_contract, current_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d"))
        response = requests.post(url, json={'query': formatted_query})
        data = response.json()
        token_holders = data.get('data', {}).get('EVM', {}).get('TokenHolders', [{}])[0].get('uniq', '0')
        
        # Append the date and holder count to the respective lists
        if token_contract == token_contract1:
            holder_counts_contract1_l.append(int(token_holders))
        else:
            holder_counts_contract2_l.append(int(token_holders))
    
    # Append the date
    dates.append(current_date.strftime("%Y-%m-%d"))
    
    # Move to the previous date
    current_date -= timedelta(days=1)

# Reverse the lists for correct plotting order
dates.reverse()
holder_counts_contract1_l.reverse()
holder_counts_contract2_l.reverse()

# Plot the data for both token contracts side by side
plt.figure(figsize=(14, 6))

# Plot for USDT wallet liquidations
plt.subplot(1, 2, 2)
plt.plot(dates, holder_counts_contract1_l, marker='o')
plt.title('USDT Wallet Liquidations')
plt.xlabel('Date')
plt.ylabel('Number of Liquidations')
plt.xticks(rotation=45)
plt.grid(True)

# Plot for USDC wallet liquidations
plt.subplot(1, 2, 1)
plt.plot(dates, holder_counts_contract2_l, marker='o')
plt.title('USDC Wallet Liquidations')
plt.xlabel('Date')
plt.ylabel('Number of Liquidations')
plt.xticks(rotation=45)
plt.grid(True)

# Ensure proper layout and display the plots
plt.tight_layout()
plt.show()

# Sign up for Bitquery to access Bitquery's API and explore more data: https://ide.bitquery.io/streaming
