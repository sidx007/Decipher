from django.shortcuts import render,redirect
from django.http import HttpResponse
from .decipher_bot import decipher
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User 

import json
from .models import AuthenticationId
# from .decipher_bot.telegram_bot.events import Publisher, Subscriber

# notion_page_id = "3411ec690b544b14bf57b99eb052f3e4"
# integeration_token = "secret_wAFuiNtCeIKJYg9YvElKNT2nVQ7RUAygBqQ1pAfthXz"
# integeration_token = "secret_z4uu8mdFb3249mmnxKAqOcG0w9hmzf1QL652fMvp3uP"
# notion_page_title = "Decipher-Bot"
details_confirmed:bool = False



# def set_user_details(_integeration_token, _notion_page_id):
#     global notion_page_id
#     global integeration_token
#     global details_confirmed
#     notion_page_id = _notion_page_id
#     integeration_token = _integeration_token
#     details_confirmed = True
#     redirect("chatbot_view")

# set_user_details_subscriber = Subscriber('details_confirmed', set_user_details)
# Publisher.register('details_confirmed', set_user_details_subscriber)

# def chatbot_view(request):
#     if request.method == 'POST':
#         prompt = request.POST.get('user-prompt')
#         print(prompt)
#         if prompt:
#             decipher.CreateNotionPage(notion_page_id, integeration_token, prompt)
#             context ={
#                 'prompt':prompt,
#                 'success': True
#             }
#             return render(request, "bot_home/chatbot.html", context)
#     return render(request, "bot_home/chatbot.html")
#     # if details_confirmed:
#     #     if request.method == 'POST':
#     #         prompt = request.POST.get('user-prompt')
#     #         print(prompt)
#     #         if prompt:
#     #             decipher.CreateNotionPage(notion_page_id, integeration_token, prompt)
#     #             context ={
#     #                 'prompt':prompt,
#     #                 'success': True
#     #             }
#     #             return render(request, "bot_home/chatbot.html", context)
#     #     return render(request, "bot_home/chatbot.html")
#     # else:
#     #     return HttpResponse("Please set your integration token and page id first " + details_confirmed.__str__() + " page id: "+ notion_page_id + " integration token " + integeration_token)
    

def chatbot_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('user-prompt')
        auth_id = AuthenticationId.objects.get(user_mail=request.user)
        notion_page_title = auth_id.page_title
        integeration_token = auth_id.integration_key
        print(prompt)
        if prompt:
            print(integeration_token)
            decipher.CreateNotionPage(notion_page_title, integeration_token, prompt)
            context ={
                'prompt':prompt,
                'success': True
            }
            return render(request, "bot_home/chatbot.html", context)
        return redirect("bot_home:chatbot_view")
    return render(request, "bot_home/chatbot.html")


def pages_view(request):
    user = request.user
    return render(request, "bot_home/pages.html")

def success_view(request):
    return redirect("bot_home:chatbot_view")