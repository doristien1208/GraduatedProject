from openai import OpenAI

client = OpenAI(api_key='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')

prompt= "What's the most popular ski resort in Europe?"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role":"user",
            "content": prompt
        }    
    ],
    model="gpt-3.5-turbo"
)

print(chat_completion.choices[0].message.content)