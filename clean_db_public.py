#pip install pandas wikipedia-api


import pandas as pd
import openai
from openai import OpenAI
# Set up OpenAI API key (replace with your key)
openai.api_key = API_KEY

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

# Set the GPT model
GPT_MODEL = "gpt-4-1106-preview"  # Or "gpt-3.5-turbo-1106"

# Function to get a GPT-4 response from OpenAI for ligand-receptor binding
def check_ligand_receptor_with_gpt(ligand, receptor):
    query = f"Does the ligand {ligand} specifically bind to the receptor {receptor}? Please provide a 'yes' or 'no' answer."
    
    # Define the messages for the GPT model
    messages = [
        {"role": "system", "content": "You are a knowledgeable assistant that answers questions about ligand-receptor binding."},
        {"role": "user", "content": query},
    ]
    
    # Use the OpenAI client to generate a response
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )
    
    # Extract the reply from GPT-4
    return response.choices[0].message.content.strip()

# Function to check the ligand-receptor pair using GPT alone
def score_ligand_receptor(ligand, receptor):
    gpt_response = check_ligand_receptor_with_gpt(ligand, receptor)
    
    # If GPT confirms the binding by returning 'yes', return TRUE; otherwise, return FALSE
    if 'yes' in gpt_response.lower():
        return 'TRUE'
    else:
        return 'FALSE'

# Read the CSV file into a pandas DataFrame
file_path = 'L_R_table.csv'  # Your input file
df = pd.read_csv(file_path)

# Assuming the columns are named 'A' for ligands and 'B' for receptors
df['score'] = df.apply(lambda row: score_ligand_receptor(row['A'], row['B']), axis=1)

# Save the updated DataFrame with the new 'score' column
output_file = 'ligand_receptor_table_with_scores.csv'
df.to_csv(output_file, index=False)

print(f"Ligand-receptor binding scores added and saved to {output_file}")
