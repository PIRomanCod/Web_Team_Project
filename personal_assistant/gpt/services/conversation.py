import openai

def conversation(messages):
    """
    The conversation function takes in a list of messages and returns the role (speaker)
    and content (message) of the response. The model used is gpt-3.5-turbo, which is
    the largest model available on OpenAI's API.

    :param messages: Pass in the messages that have been sent so far
    :return: A tuple of (role, message)
    """
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    return response.choices[0].message.role, response.choices[0].message.content

