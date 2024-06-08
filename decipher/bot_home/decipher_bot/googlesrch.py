from googlesearch import search
import os

if not os.path.exists('bot_home/decipher_bot/result_files'):
    os.makedirs('bot_home/decipher_bot/result_files')

PATH = 'bot_home/decipher_bot/result_files/'

def searchQuery(query):
    
    # Define the number of results you want (max 10)
    num_results = 10

    # Perform the search and iterate over the results
    results = search(query, num_results=num_results)
    # Python code to create a file
    file = open(PATH+'gsrch_results.txt','w')


    for i, result in enumerate(results, 1):
        file.write(f"{result}\n")
        if i >= num_results:
            break

    file.close()

def count_matched_keywords(link, keywords):
    count = sum(keyword.lower() in link.lower() for keyword in keywords)
    return count

def filter_links(sentence):

    input_file = open(PATH+'gsrch_results.txt', "r")
    output_file = open(PATH+'gsrch_results_filtered.txt', "w")

    keywords = sentence.split()

    links = input_file.readlines()

    links_with_counts = [(link.strip(), count_matched_keywords(link, keywords)) for link in links]
    
    sorted_links = sorted(links_with_counts, key=lambda x: x[1], reverse=True)

    top_links = sorted_links[:6]

    # write filtered links
    for i, (link, count) in enumerate(top_links, start=1):
        output_file.write(f"{link}\n")
