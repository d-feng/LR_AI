import pandas as pd
import openai

# Read the table (assuming it's a CSV)
df = pd.read_csv('protein_table.csv')

# Replace with your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Function to ask GPT-4 about binding, classify the result, and return interpretation
def check_protein_binding(protein_a, protein_b):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a biology expert."},
            {"role": "user", "content": f"Does protein '{protein_a}' bind to protein '{protein_b}'? Please explain."}
        ]
    )
    
    # Extract the response content
    response_content = response['choices'][0]['message']['content'].lower()

    # Classify the response
    if "bind" in response_content and ("yes" in response_content or "likely" in response_content):
        binding_result = "yes"
    elif "does not bind" in response_content or "no" in response_content:
        binding_result = "no"
    else:
        binding_result = "tbd"

    # Return both the binding result and the full explanation
    return binding_result, response['choices'][0]['message']['content']

# Sentiment Analysis function to score confidence level of the interpretation
def analyze_sentiment(interpretation_text):
    confident_keywords = ["definitely", "certainly", "clearly", "strong evidence", "without a doubt"]
    uncertain_keywords = ["likely", "possibly", "may", "could", "somewhat", "uncertain"]

    # Checking for confident vs uncertain keywords
    if any(word in interpretation_text for word in confident_keywords):
        return "confident"
    elif any(word in interpretation_text for word in uncertain_keywords):
        return "lack of confidence"
    else:
        return "confident"  # Default to confident if no clear uncertain language is detected

# Apply the function to each row, storing the classification, interpretation, and sentiment analysis
df['Binding_Result'], df['Interpretation'] = zip(*df.apply(lambda row: check_protein_binding(row['A'], row['B']), axis=1))

# Apply sentiment analysis on the 'Interpretation' column
df['Sentiment'] = df['Interpretation'].apply(analyze_sentiment)

# Save the results to a new CSV file
df.to_csv('protein_binding_with_interpretation_and_sentiment.csv', index=False)

print("Binding check complete. Results with sentiment saved to 'protein_binding_with_interpretation_and_sentiment.csv'")
