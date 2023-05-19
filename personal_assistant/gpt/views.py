from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from gpt.services.conversation import conversation
from gpt.services.checking_sentences import check_sentence


@login_required
def tasks(request):
    """
    The tasks function is a view that renders the tasks.html template.

    :param request: Pass the request object to the view
    :return: The render template 'gpt/html.tasks'
    """
    return render(request, 'gpt/tasks.html')


@csrf_exempt
@login_required
def chat(request, messages=[]):
    """
    The chat function is the main function of this file. It takes in a request object and an optional list of messages,
    and returns a JsonResponse containing the response to be sent back to the user. The chat function first checks if it has
    received a POST request or not; if it has, then it will add any new message from the user into its list of messages and
    then call conversation() with that updated list as an argument. Then, after receiving both role and content from
    conversation(), chat() adds those two values into its own message list before returning them as part of a JsonResponse.

    :param request: Get the request from the client
    :param messages: Store the messages that have been sent
    :return: The response of the chatbot
    """

    if request.method == "POST":
        if len(messages) >= 20:
            messages = messages[3:]
        message = request.POST.get("message", "")

        messages.append({"role": "system",
                         "content": "You are a helpful assistant and English teacher, which will show users' mistakes in last line after every user line. "
                                    "Then answer user question."})

        messages.append({"role": "user", "content": message})
        response_role, response_content = conversation(messages)
        messages.append({"role": response_role, "content": response_content})

        return JsonResponse({'response': f'YOU: {message.strip()}\n'
                                         f'{response_role.upper()}: {response_content.strip()}'})
    if request.method == 'GET':
        messages = []
        return render(request, 'gpt/chat_ai.html')


@csrf_exempt
@login_required
def text_correction(request):
    """
    The text_correction function is a view that takes in a POST request from the text_correction.html page,
    which contains the user's inputted message. The function then passes this message to check_sentence() and returns
    the corrected sentence as well as the original sentence back to text_correction.html.

    :param request: Get the data from the user
    :return: A json response with the original message and the corrected message
    """

    if request.method == 'POST':
        message = request.POST.get('message')

        chatbot_response = check_sentence(message)

        return JsonResponse({'response': f'Original: {message}\n'
                                         f'Correct: {chatbot_response.strip()}'})

    return render(request, 'gpt/text_correction.html')
