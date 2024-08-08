from openai import OpenAI

client = OpenAI(api_key='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')

def generate_character_description_with_openai(prompt):
    chat_completion = client.chat.completions.create(
       messages=[
        {
            "role":"user",
            "content": prompt
        }    
    ],
    model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content

# Example usage
character_traits = {
    "occupation": "engineer",
    "personality": "creative and analytical",
    "skills": "machine learning and data analysis",
    "scenario": "developing a revolutionary technology"
}

prompt = f"Write a detailed character prompt for a {character_traits['occupation']} with {character_traits['personality']} personality, skilled in {character_traits['skills']}. The character should be involved in {character_traits['scenario']}."

# Generate the character description
description = generate_character_description_with_openai(prompt)
print(description)
