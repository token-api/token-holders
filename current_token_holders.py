# This code sends a GraphQL query to Bitquery's API to retrieve the number of token holders for USDC and USDT,
# and then visualizes the data using a bar chart.

# Replace 'graphql_endpoint' with your GraphQL endpoint and consider signing up for Bitquery to access the API.

import requests
import matplotlib.pyplot as plt

# Define the GraphQL query
query = '''
{
  USDT: EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "2023-10-21"
      tokenSmartContract: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
      where: {Balance: {Amount: {gt: "0"}}}
    ) {
      uniq(of: Holder_Address)
    }
  }
  USDC: EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "2023-10-21"
      tokenSmartContract: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
      where: {Balance: {Amount: {gt: "0"}}}
    ) {
      uniq(of: Holder_Address)
    }
  }
}
'''
# Set the GraphQL endpoint (Replace with your Bitquery GraphQL endpoint)
graphql_endpoint = "https://streaming.bitquery.io/graphql"

# Define the request headers
headers = {
    "Content-Type": "application/json",
}

# Send the GraphQL query using the requests library
response = requests.post(graphql_endpoint, json={"query": query}, headers=headers)
data = response.json()

# Extract the number of token holders for USDC and USDT
usdc_token_holders = int(data["data"]["USDC"]["TokenHolders"][0]["uniq"])
usdt_token_holders = int(data["data"]["USDT"]["TokenHolders"][0]["uniq"])

# Create a bar chart to visualize the results side by side
tokens = ["USDC", "USDT"]
token_holders = [usdc_token_holders, usdt_token_holders]

plt.bar(tokens, token_holders)
plt.xlabel("Token")
plt.ylabel("Number of Token Holders (in millions)")
plt.title("Number of Token Holders for USDC and USDT")
plt.show()


# Sign up for Bitquery to access Bitquery's API and explore more data: https://ide.bitquery.io/streaming
