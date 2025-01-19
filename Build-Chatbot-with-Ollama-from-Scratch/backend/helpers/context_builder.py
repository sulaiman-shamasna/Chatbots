def create_context(messages, query):
    prompt = ''
    for message in messages:
        prompt += f"user: {message['prompt']}\nassistant: {message['response']}\n"
    prompt += f"user: {query}"
    return prompt
