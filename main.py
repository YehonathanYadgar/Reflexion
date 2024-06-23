
import os 
from openai import OpenAI
from dotenv import load_dotenv , find_dotenv
import prompts
import problems
import reflexion_prompts

# loading openai api
_  = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
    )

# Basic function, to easily generate LLM responses
def generate_text_with_conversation(messages,model):
    response = client.chat.completions.create(
        model = model,
        messages=messages
        )
    return response.choices[0].message.content

# initializing memory
mem = '''
Memory:\n|
'''

# Actor conversation structure
actor_messages = [
        {"role": "system", "content": reflexion_prompts.actor_prompt},
        {"role": "user", "content":f' {mem} + {problems.p2}' }
        ]

# Generating response to the actor convo, and printing it
actor_respones = generate_text_with_conversation(actor_messages,'gpt-3.5-turbo')
print(f'Actor: {actor_respones}')

# Evaluator conversation structure
evaluator_messages =  [
        {"role": "system", "content": reflexion_prompts.evaluator_prompt},
        {"role": "assistant", "content": problems.p2},
        {"role": "user", "content": actor_respones}
        ]

# Generating response to the evaluator convo, and printing it
evaluator_response = generate_text_with_conversation(evaluator_messages,'gpt-4')
print(f'Evaluator: {evaluator_response}')

# Reflector conversation structure
reflector_messeges = [
     {"role": "system", "content":reflexion_prompts.reflector_prompt },
     {"role": "assistant", "content": problems.p2},
     {"role": "user", "content": actor_respones},
     {"role": "user", "content": f'grade:{evaluator_response}'}
        ] 

# Generating response to the  reflector convo, and printing it
reflector_response = generate_text_with_conversation(reflector_messeges,'gpt-3.5-turbo')
print(f'Reflector: {reflector_response}')

# appending the reflection to memory, in order to help the agent in future responses
mem += reflector_response + '\n'
print(mem)

# doing the same thing in a loop
for i in range(3):

    # Generating response to the actor convo, and printing it
    actor_respones = generate_text_with_conversation(actor_messages,'gpt-3.5-turbo')
    print(f'Actor: {actor_respones}')

    # Generating response to the evaluator convo, and printing it
    evaluator_response = generate_text_with_conversation(evaluator_messages,'gpt-4')
    print(f'Evaluator: {evaluator_response}')

    # checking if the coding result is good, if it is breaking out of the loop else nothing happens
    if float(evaluator_response) >= 9:
        break

    # Generating response to the reflector convo, and printing it
    reflector_response = generate_text_with_conversation(reflector_messeges,'gpt-3.5-turbo')
    print(f'Reflector: {reflector_response}')

    # appending reflection to memory
    mem += reflector_response + '\n'

