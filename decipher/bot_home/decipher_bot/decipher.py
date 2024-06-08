from . import googlesrch as gsearch
from . import youtubesrch as ytsearch
from . import ConfigureSettings as _conf
from . import create_notion as cnotion
from . import creating_notion_page_revised as cnp
import os, re

if not os.path.exists('bot_home/decipher_bot/result_files'):
    os.makedirs('bot_home/decipher_bot/result_files')

PATH = 'bot_home/decipher_bot/result_files/'

def SetUserPrompt(prompt):
    global userprompt
    userprompt = prompt
    print("User Prompt Set: " + userprompt)

def GetKeywords(chat_session):
    query = "Identify key topic word.Only technical words. Less than 5 words. Only from the prompt. User's prompt is: " + userprompt
    
    keywords = queryGemini(query, chat_session)
    
    gsearch.searchQuery(keywords)
    print(keywords)
    return keywords

def WriteAndFilterLinks(topic):
    gsearch.filter_links(topic)

def GetYoutubeLinks(topic):
    ytsearch.searchQuery(topic, 5)
    return True

def move_double_underscore(line):
    if line.startswith('__'):
        line_content = line[2:].strip()  # Remove the leading '__' and strip any trailing whitespace
        return f"__{line_content}__"  # Add '__' to both ends of the line content
    return line


def formatIntro(intro):
    # modified_intro = re.sub(r"\*","_", intro)
    modified_intro = intro
    # extract the first line as title
    lines = modified_intro.splitlines()
    intro_title = lines[0]
    modified_intro = modified_intro.replace(intro_title, "")
    modified_intro = re.sub(r"\n+", "\n", modified_intro).strip()
    intro_title = re.sub(r"\#","", intro_title).strip()

    introlen = len(modified_intro)

    _intro = {
        "title": intro_title,
        "intro": modified_intro
    }

    return _intro

def GetIntroduction(topic, chat_session):
    query = "Tell me about "+topic+" in brief. Include its origin, applications, and other relevant information. "

    introduction = queryGemini(query, chat_session)
    _intro = formatIntro(introduction)
    introduction = _intro.get("intro")
    intro_title = _intro.get("title")
    if not intro_title:
        print("No title found")
    print(intro_title)
    file = open(PATH+"intro.txt", 'w')
    file.write(introduction)
    file.close()
    file2 = open(PATH+"intro_title.txt", 'w+')
    file2.write(intro_title)
    file2.close()


    return introduction

def queryGemini(query, chat_session):
    #Find keywords
    response = chat_session.send_message(query)
    if response:
        return response.text
    return "No response"

def CreateNotionPage(parent_page_title, token, prompt):
    print("Configuring Notion...")
    # cnotion.configureNotion(parent_page_title, token)
    cnp.configureNotion(parent_page_title, token)
    print("Setting User Prompt...")
    SetUserPrompt(prompt)

    # create chat session
    model = _conf.configureGemini()
    chat_session = model.start_chat(history=[])

    keywords = GetKeywords(chat_session)
    GetIntroduction(keywords, chat_session)
    WriteAndFilterLinks(keywords)
    GetYoutubeLinks(keywords)
    intro_title_file = open(PATH+"intro_title.txt", 'r')
    intro_file = open(PATH+"intro.txt", 'r')

    print("Creating Notion Page...")
    # cnotion.MakeNotionPage(
    #     page_title=keywords,
    #     heading1=intro_title_file.read(),
    #     intro=intro_file.read(),
    #     linksdb_title="Links To Read",
    #     ytlinksdb_title="Youtube Links",
    #     links_file=PATH+"gsrch_results_filtered.txt",
    #     title_file=PATH+"gsrch_results_filtered.txt",
    #     ytlinks_file=PATH+"ytresultsLinks.txt",
    #     yttitle_file=PATH+"ytresultsTitle.txt"
    # )
    cnp.make_notion_page(
        page_title=keywords,
        heading1=intro_title_file.read(),
        intro=intro_file.read(),
        linksdb_title="Links To Read",
        ytlinksdb_title="Youtube Links",
        links_file=PATH+"gsrch_results_filtered.txt",
        title_file=PATH+"gsrch_results_filtered.txt",
        ytlinks_file=PATH+"ytresultsLinks.txt",
        yttitle_file=PATH+"ytresultsTitle.txt"
    )

    intro_title_file.close()
    intro_file.close()