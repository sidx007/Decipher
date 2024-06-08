import notion
import notion.query
from notion_client import Client
import re, json

def configureNotion(parent_page_title, token):
    
    global homepage
    global client
    global page_id

    client = Client(auth=token)
    result = client.search(query= parent_page_title)['results'][0]['id']
    print(result)
    page_id = result
    homepage = notion.Page(page_id)
    # check if the page exists and if the token is valid
    print("Notion Configured\nHomePage ID: " + homepage.id)

def CreateNewEntry(db_id, title, url):
    new_entry = {
        "parent": {"database_id": db_id},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "URL": {"url": url}, # URL column
        },
    }

    client.pages.create(**new_entry)
    
def FileToEntries(db_id, title_file, links_file):
    title_file = open(title_file, 'r')
    links_file = open(links_file, 'r')
    titles = title_file.readlines()
    links = links_file.readlines()
    for i in range(len(titles)):
        CreateNewEntry(db_id, titles[i], links[i])
    title_file.close()
    links_file.close()

def process_intro_text(intro_text, page):
    segments = re.split(r'(\_\_[^_]+\_\_)', intro_text)

    for segment in segments:
        if '__' in segment:
            text = segment.replace('__', '')
            para_block = notion.Block.paragraph(
                parent_object=page,
                rich_text=[{
                    "type": "text",
                    "text": {"content": text},
                    "annotations": {"bold": True}
                }]
            )
        elif '_' in segment:
            # If '_' is still present, create a bulleted list
            text = segment.replace('_', '')
            list_block = notion.Block.bulleted_list(
                parent_object=page,
                rich_text=[{
                    "type": "text",
                    "text": {"content": text}
                }]
            )
        else:
            para_block = notion.Block.paragraph(
                parent_object=page,
                rich_text=segment
            )
        


def MakeNotionPage(page_title, heading1, intro, linksdb_title, ytlinksdb_title, links_file, title_file, ytlinks_file, yttitle_file):

    print("Creating new page")
    print("At page: " + homepage.id)
    new_page = notion.Page.create(
    parent_instance=homepage,
    page_title="Hello World!",
    )
    if new_page.id:
        print("Page created successfully")
    heading_block = notion.Block.heading_2(
        parent_object=new_page,
        rich_text=heading1,
    )
    
    # process_intro_text(intro, new_page)

    link_db = notion.Database.create(
        parent_instance=new_page,
        database_title=linksdb_title,
        title_column="Title", # This is the column containing page names. Defaults to "title".
        is_inline=True, # can also toggle inline with setters.
    )
    notion.Database.url_column(link_db,"URL")
    linkdb_id = link_db.id

    ytlink_db = notion.Database.create(
        parent_instance=new_page,
        database_title=ytlinksdb_title,
        title_column="Title", # This is the column containing page names. Defaults to "title".
        is_inline=True, # can also toggle inline with setters.
    )
    notion.Database.url_column(ytlink_db,"URL")
    ytlinkdb_id = ytlink_db.id

    FileToEntries(linkdb_id, title_file, links_file)
    FileToEntries(ytlinkdb_id, yttitle_file, ytlinks_file)



