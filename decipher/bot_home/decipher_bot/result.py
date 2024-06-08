def extract():
    context = {}
    intro = ""
    links_google = []
    links_yt  = [] 
    title_yt = []
    with open('C:/dev/ai/decipher/decipher/decipher/bot_home/decipher_bot/result_files/intro.txt', "r") as file:
        for line in file:
            for char in line:
                if char != '*':
                    intro += char

    context["intro"] = intro
    with open('C:/dev/ai/decipher/decipher/decipher/bot_home/decipher_bot/result_files/gsrch_results_filtered.txt', "r") as file:
        for line in file:
            links_google.append(line)
    context['google'] = links_google
    with open('C:/dev/ai/decipher/decipher/decipher/bot_home/decipher_bot/result_files/ytresultsLinks.txt', "r") as file:
        for line in file:
            links_yt.append(line)

    with open('C:/dev/ai/decipher/decipher/decipher/bot_home/decipher_bot/result_files/ytresultsTitle.txt', "r") as file:
        for line in file:
            title_yt.append(line)

    ytcode = []
    for i in links_yt:
        initial = ""
        for j in range(0,len(i)):
            if i[j] == '=':
                j += 1
                for k in range(j,len(i)):
                    if i[k] == "\n":
                        break
                    initial += i[k]
        ytcode.append(initial)

    context['videos'] =  zip(links_yt, ytcode, title_yt)
    return context


