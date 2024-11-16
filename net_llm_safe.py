import requests
import networkx as nx
import matplotlib.pyplot as plt
import openai
import xml.etree.ElementTree as ET
import json
import pandas as pd
from openai import OpenAI
import re  # Import the regex module

# Initialize the OpenAI client with your API key
API_KEY = ''
client = OpenAI(api_key= API_KEY)

# Define the GPT model to use
GPT_MODEL = "gpt-4-1106-preview"  # You can change to another model if needed

df=pd.read_csv('./kegg/kegg_gene_network_hsa/hsa04310.tsv',sep='\t', header=0)
df

gene_tbl=pd.read_csv("./kegg/HUMAN_9606_idmapping.dat", sep="\t",names=["ID", "Database", "GeneSymbol"])

gt1=gene_tbl.loc[gene_tbl['Database']=='KEGG',]

gt2=gene_tbl.loc[gene_tbl['Database']=='Gene_Name',]

merged_gt = pd.merge(gt1, gt2, on='ID', how='left')


conversion_df=merged_gt.rename(columns={"ID":"ID", "Database_x":"Database", "GeneSymbol_x":"hsa", "GeneSymbol_y":"GeneSymbol"})

# Map KEGG IDs to Gene Symbols using the provided conversion table
id_to_symbol = dict(zip(conversion_df['hsa'], conversion_df['GeneSymbol']))
df['entry1'] = df['entry1'].map(id_to_symbol).fillna(df['entry1'])
df['entry2'] = df['entry2'].map(id_to_symbol).fillna(df['entry2'])

# Build a NetworkX graph from the data
G = nx.DiGraph()  # Directed graph for representing relations

# Add edges with attributes
for _, row in df.iterrows():
    G.add_edge(row['entry1'], row['entry2'], interaction=row['name'])

# Visualize the network with gene symbols as node labels
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42)  # Layout for consistent visualization
edge_labels = nx.get_edge_attributes(G, 'interaction')

# Draw nodes and edges
nx.draw(G, pos, with_labels=True, labels={node: node for node in G.nodes}, node_size=700, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

plt.title("Gene Interaction Network with Gene Symbols")
plt.show()


def validate_interaction_via_openai(gene1, gene2, interaction_type):
    """
    Validate an interaction between two genes using OpenAI's API.
    Query whether the first gene activates or inhibits the second gene.
    """
    prompt = (
        f"Gene {gene1} has a reported {interaction_type} relationship with gene {gene2}. "
        "Does gene {gene1} activate or inhibit gene {gene2} in biological pathways? Please explain."
    )

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a biological interaction expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        # Extract the response text
        answer = response['choices'][0].message['content']
        return answer

    except Exception as e:
        print(f"Error querying OpenAI API: {e}")
        return "Error in API call"

def check_network_interactions(G):
    """
    Iterate through the network graph and validate each interaction using OpenAI API.
    """
    results = []
    for edge in G.edges(data=True):
        gene1 = edge[0]
        gene2 = edge[1]
        interaction_type = edge[2].get('interaction', 'unknown')

        # Validate the interaction
        response = validate_interaction_via_openai(gene1, gene2, interaction_type)

        # Append the result
        results.append({
            "gene1": gene1,
            "gene2": gene2,
            "interaction_type": interaction_type,
            "validation": response
        })

        print(f"Checked interaction: {gene1} -> {gene2} ({interaction_type})")
        print(f"Response: {response}\n")

    return results



# Example Usage: Validate interactions in network G
results = check_network_interactions(G)

# Print or process the results
for result in results:
    print(result)

