# Initial question
messages = [
    {"role": "system", "content": "You are a science tutor who explains reasoning step by step."},
    {"role": "user", "content": "Why is the sky blue? Think step by step."}
]

# First response
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=messages,
    max_tokens=300,
    temperature=0.7
)
print("First Query Response:")
print(response.choices[0].message["content"].strip())

# Add the assistant's response and ask a follow-up question
messages.append({"role": "assistant", "content": response.choices[0].message["content"].strip()})
messages.append({"role": "user", "content": "Now explain why sunsets appear red. Think step by step."})

# Second response
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=messages,
    max_tokens=300,
    temperature=0.7
)
print("\nFollow-Up Query Response:")
print(response.choices[0].message["content"].strip())
