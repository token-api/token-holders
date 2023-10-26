# This code retrieves and analyzes the top token holders' data for two different Ethereum-based token contracts (USDT and USDC)
# on a specific date using Bitquery's GraphQL API. It then displays the data in DataFrames, calculates the sums of balances,
# and presents them side by side.

# Replace 'graphql_endpoint' with your GraphQL endpoint and consider signing up for Bitquery to access the API.

# Import necessary libraries
import requests
import pandas as pd
from IPython.display import HTML

# Define the GraphQL queries for both token contracts
query_template = '''
{
  EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "2023-10-23"
      tokenSmartContract: "%s"
      limit: {count: 11}
      orderBy: {descending: Balance_Amount}
    ) {
      Balance {
        Amount
      }
      Holder {
        Address
      }
    }
  }
}
'''

# Define the endpoint URL for Bitquery
url = 'https://streaming.bitquery.io/graphql'

# Token contract addresses
token_contract1 = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
token_contract2 = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # Replace with the second contract address

# Initialize data dictionaries for both contracts
data_contract1 = {}
data_contract2 = {}

# Function to shorten addresses for display
def shorten_address(address):
    return f"{address[:5]}...{address[-3:]}" if len(address) > 8 else address

# Function to convert numbers to millions or billions for display
def convert_to_millions_or_billions(number):
    if number >= 1_000_000_000:
        return f'{number / 1_000_000_000:.2f}B'
    if number >= 1_000_000:
        return f'{number / 1_000_000:.2f}M'
    return f'{number:.2f}'

# Retrieve and store data for both token contracts
for token_contract, data_container in [(token_contract1, data_contract1), (token_contract2, data_contract2)]:
    formatted_query = query_template % token_contract
    response = requests.post(url, json={'query': formatted_query})
    data = response.json()
    
    holders = data.get('data', {}).get('EVM', {}).get('TokenHolders', [])[1:] if token_contract == token_contract2 else data.get('data', {}).get('EVM', {}).get('TokenHolders', [])
    
    # Extract and store data
    data_container['Address'] = [shorten_address(holder['Holder']['Address']) for holder in holders]
    data_container['Balance'] = [float(holder['Balance']['Amount']) for holder in holders]

# Create DataFrames from the data
df_contract1 = pd.DataFrame(data_contract1)
df_contract2 = pd.DataFrame(data_contract2)

# Add titles to the tables
df_contract1 = df_contract1.rename_axis("USDT Top Holders")
df_contract2 = df_contract2.rename_axis("USDC Top Holders")

# Calculate the sums of balances for the first 10 holders of Contract 1 and the 2nd to 11th holders of Contract 2
sum_contract1 = df_contract1['Balance'].head(10).sum()
sum_contract2 = df_contract2['Balance'].iloc[1:11].sum()

# Display the sums
print(f"Sum of the first 10 balances for Contract 1: {sum_contract1:.2f} USDT")
print(f"Sum of balances 2-11 for Contract 2: {sum_contract2:.2f} USDC")

# Display DataFrames side by side
display_side_by_side = lambda *args: HTML(
    '<table><tr>{}</tr></table>'.format(
        ''.join(['<td valign="top">{}</td>'.format(a.to_html()) for a in args])
    )
)

display_side_by_side(df_contract1, df_contract2)

# Sign up for Bitquery to access Bitquery's API and explore more data: https://ide.bitquery.io/streaming
