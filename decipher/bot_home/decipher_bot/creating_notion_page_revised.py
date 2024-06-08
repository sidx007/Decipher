import re
from notion_client import Client

def configureNotion(parent_page_title, token):
    global homepage
    global client
    global page_id

    client = Client(auth=token)
    search_result = client.search(query=parent_page_title)
    if search_result['results']:
        page_id = search_result['results'][0]['id']
        print(f"Notion Configured\nHomePage ID: {page_id}")
    else:
        raise Exception(f"Page titled '{parent_page_title}' not found.")

def create_new_entry(db_id, title, url):
    new_entry = {
        "parent": {"database_id": db_id},
        "properties": {
            "Name": {"title": [{"text": {"content": title.strip()}}]},
            "URL": {"url": url.strip()},
        },
    }
    client.pages.create(**new_entry)

def file_to_entries(db_id, title_file, links_file):
    with open(title_file, 'r') as tf, open(links_file, 'r') as lf:
        titles = tf.readlines()
        links = lf.readlines()
        for title, link in zip(titles, links):
            create_new_entry(db_id, title, link)

def process_intro_text(intro_text, page_id):
    segments = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', intro_text)
    blocks = []

    for segment in segments:
        if segment.startswith('**') and segment.endswith('**'):
            text = segment[2:-2]
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": text},
                        "annotations": {"bold": True}
                    }]
                }
            })
        elif segment.startswith('*') and segment.endswith('*'):
            text = segment[1:-1]
            if '**' in text:
                parts = re.split(r'(\*\*[^*]+\*\*)', text)
                rich_text = []
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        part = part[2:-2]
                        rich_text.append({
                            "type": "text",
                            "text": {"content": part},
                            "annotations": {"bold": True}
                        })
                    else:
                        rich_text.append({
                            "type": "text",
                            "text": {"content": part}
                        })
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": rich_text
                    }
                })
            else:
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": text}
                        }]
                    }
                })
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": segment}
                    }]
                }
            })
    
    client.blocks.children.append(block_id=page_id, children=blocks)

def make_notion_page(page_title, heading1, intro, linksdb_title, ytlinksdb_title, links_file, title_file, ytlinks_file, yttitle_file):
    print("Creating new page")
    new_page = client.pages.create(
        parent={"type": "page_id", "page_id": page_id},
        properties={"title": [{"type": "text", "text": {"content": page_title}}]},
    )

    if 'id' in new_page:
        new_page_id = new_page['id']
        print("Page created successfully")

        client.blocks.children.append(
            block_id=new_page_id,
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": heading1}}]}
                }
            ]
        )
        
        process_intro_text(intro, new_page_id)

        link_db = client.databases.create(
            parent={"type": "page_id", "page_id": new_page_id},
            title=[{"type": "text", "text": {"content": linksdb_title}}],
            is_inline=True,
            properties={
                "Name": {"title": {}},
                "URL": {"url": {}},
            }
        )
        linkdb_id = link_db['id']

        ytlink_db = client.databases.create(
            parent={"type": "page_id", "page_id": new_page_id},
            title=[{"type": "text", "text": {"content": ytlinksdb_title}}],
            is_inline=True,
            properties={
                "Name": {"title": {}},
                "URL": {"url": {}},
            }
        )
        ytlinkdb_id = ytlink_db['id']

        file_to_entries(linkdb_id, title_file, links_file)
        file_to_entries(ytlinkdb_id, yttitle_file, ytlinks_file)
    else:
        print("Failed to create page")

# Example usage:
# configureNotion('Parent Page Title', 'your_notion_token')
# make_notion_page('Page Title', 'Heading 1', 'Intro text __bold__ _bullet_', 'Links DB', 'YT Links DB', 'links.txt', 'titles.txt', 'ytlinks.txt', 'yttitles.txt')
