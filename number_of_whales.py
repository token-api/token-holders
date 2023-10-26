# This code queries Bitquery's GraphQL API to retrieve the number of "whales" (holders with a balance greater than 1,000,000) 
# for two Ethereum-based token contracts (USDT and USDC) on a specific date (2023-10-23). It then displays the data in a bar chart.

# Replace 'graphql_endpoint' with your GraphQL endpoint and consider signing up for Bitquery to access the API.

# Import necessary libraries
import requests
import matplotlib.pyplot as plt

# Define the GraphQL queries for the two token contracts
query_template = '''
{
  EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "2023-10-23"
      tokenSmartContract: "%s"
      where: {Balance: {Amount: {gt: "1000000"}}}
    ) {
      uniq(of: Holder_Address)
    }
  }
}
'''

# Define the endpoint URL for Bitquery
url = 'https://streaming.bitquery.io/graphql'

# Token contract addresses
token_contract1 = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT
token_contract2 = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC

# Initialize data dictionaries
data_contract1 = {}
data_contract2 = {}

# Function to retrieve data
def get_data_for_contract(contract_address):
    formatted_query = query_template % contract_address
    response = requests.post(url, json={'query': formatted_query})
    data = response.json()
    return int(data.get('data', {}).get('EVM', {}).get('TokenHolders', [{}])[0].get('uniq', '0'))

# Retrieve and store data for both contracts
usdt_holders = get_data_for_contract(token_contract1)
usdc_holders = get_data_for_contract(token_contract2)

# Create a bar chart
contracts = ['USDT', 'USDC']
holders = [usdt_holders, usdc_holders]

plt.bar(contracts, holders, color=['blue', 'green'])
plt.xlabel('Token Contracts')
plt.ylabel('Number of Whales')
plt.title('Number of Whales for USDT and USDC on 2023-10-23')
plt.show()

# Sign up for Bitquery to access Bitquery's API and explore more data: https://ide.bitquery.io/streaming