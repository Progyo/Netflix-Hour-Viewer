import pandas as pd

files = ["NetflixViewingHistoryNadim.csv","NetflixViewingHistoryNadimJan2020.csv"]

f = pd.DataFrame(columns=["Title","Date"])


def recent(date1,date2):

    date1 = date1.split("/")
    date2 = date2.split("/")

    #Year is larger
    if int(date1[2]) > int(date2[2]): 
        return date2 
    elif int(date1[2]) < int(date2[2]):
        return date1

    #Month is larger
    if int(date1[1]) > int(date2[1]): 
        return date2 
    elif int(date1[1]) < int(date2[1]):
        return date1

    #Day is larger
    if int(date1[0]) > int(date2[0]): 
        return date2 
    elif int(date1[0]) < int(date2[0]):
        return date1


#Reverse date for sorting
def reverse(date):
    date = date.split("/")
    date = "/".join([date[2],date[1],date[0]])
    return date


def merge(files,csvName):
    global f
    
    for file in files:

        #Imports csv and creates a dataframe
        temp = pd.read_csv(file)

        #Foreach row in the dataframe
        for index, row in temp.iterrows():
            selected = None

            #Foreach row in the parent dataframe
            for ind, ro in f.iterrows():

                #Makes sure that no copies are added
                if ro["Title"].lower() == row["Title"].lower() and reverse(ro["Date"]) == row["Date"]:
                    selected = 1
                
                #If row is already in parent dataframe
                if ro["Title"].lower() == row["Title"].lower() and reverse(ro["Date"]) != row["Date"]:

                    #Find out which title is older
                    selected = recent(reverse(ro["Date"]),row["Date"])


                    #Overwrites entry in parent dataframe
                    if selected != ro["Date"] and selected != reverse(ro["Date"]):

                        #Reverse date for sorting
                        if int(selected[0]) > 2000:
                            print("REVERSE ======= Title: {0} Date 1: {1} Date 2: {2} Older:{3}".format(str(row["Title"]),str(row["Date"]),str(ro["Date"]),reverse("/".join(selected))))                     
                            ro["Date"] = "/".join(selected)
                        else:
                            print("Title: {0} Date 1: {1} Date 2: {2} Older:{3}".format(str(row["Title"]),str(row["Date"]),str(ro["Date"]),reverse("/".join(selected))))                     
                            ro["Date"] = reverse("/".join(selected))

                
            if selected == None:
                f = f.append({"Title": row["Title"], "Date": reverse(row["Date"])}, ignore_index=True)
                #print(row["Title"])


    f = f.sort_values(by=["Date"],ascending=False)
    f.to_csv(csvName)
#merge(files,"NadimMergedApril2020.csv")





def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False






#######################################         GET DURATION        ###########################################


from bs4 import BeautifulSoup
#import urllib.request
import requests


def clean(lis):
    newL = []
    for l in lis:
        if l != "":
            newL.append(l)
    return newL

def getDuration(search, show, movie):


    search = " ".join(clean(search.split(" "))) #Gets rid of double spaces
    show = " ".join(clean(show.split(" ")))

    urlSearch = search#.replace("'","%27m")



    #Makes sure that enough data is sent to search
    #if len(search) < 12:
    #    urlSearch = show+"+"+search

    url = ""
    
    if movie == "false":
        url = "https://www.imdb.com/find?q="+"+".join(urlSearch.split(" "))+"&s=tt&ttype=ep&ref_=fn_ep" 
    else:
        url = "https://www.imdb.com/find?q="+"+".join(urlSearch.split(" "))+"&s=tt&ref_=fn_al_tt_mr"
    #print("Search:{0}   Url:{1} \n Show:{2}".format(urlSearch,url,show) )

    headers = {"Accept-Language": "en-US,en;q=0.5"}
    #fp = urllib.request.urlopen(url,headers=headers) #The+Ones+We+Leave+Behind
    #main = fp.read().decode("utf8")
    fp = requests.get(url, headers=headers)
    main = fp.text
    soup = BeautifulSoup(main, 'html.parser')

    found = False

    link = ""


    ## Find the link to the correct page
    
    for el in soup.find_all("tr", {"class": "findResult odd"}):

        if movie == "false":
            for a in el.find_all("small"):

        #### DEBUG STUFF
                #print("Comparing Show Name: "+a.text+" to "+show)
                #print("Comparing Episode Name: "+el.text+" to "+search)


                if (show in a.text or a.text in show) and search in el.text or len(show.split(" ")) > 1 and " ".join(show.split(" ")[1:]) in a.text and search in el.text:
                    #print(a.text)
                    #print("https://www.imdb.com"+a.find_all("a",href=True)[0]["href"])
                    found = True
            if found:
                parent = el.find("td", {"class": "result_text"})
                #print("https://www.imdb.com"+parent.find("a",href=True)["href"])
                link = "https://www.imdb.com"+parent.find("a",href=True)["href"]
                break
        else:


            
            #print(el.find("td", {"class": "result_text"}))
            if search in el.find("td", {"class": "result_text"}).text:
                found = True
                
            if found:
                parent = el.find("td", {"class": "result_text"})
                link = "https://www.imdb.com"+parent.find("a",href=True)["href"]
                break

            
    if found == False:
        for el in soup.find_all("tr", {"class": "findResult even"}):
            if movie == "false":
                for a in el.find_all("small"):
            #### DEBUG STUFF
                    #print("Comparing Show Name: "+a.text+" to "+show)
                    #print("Comparing Episode Name: "+el.text+" to "+search)
                    if (show in a.text or a.text in show) and search in el.text or len(show.split(" ")) > 1 and " ".join(show.split(" ")[1:]) in a.text and search in el.text:
                        found = True
                if found:
                    parent = el.find("td", {"class": "result_text"})
                    link = "https://www.imdb.com"+parent.find("a",href=True)["href"]
                    break
            else:


                
                if search in el.find("td", {"class": "result_text"}).text:
                    found = True
                    
                if found:
                    parent = el.find("td", {"class": "result_text"})
                    link = "https://www.imdb.com"+parent.find("a",href=True)["href"]
                    break


    print("{0}  {1}".format(show,search))
    print("Opening: "+link)

    if link == "":
        return 0
    
    #fp = urllib.request.urlopen(link,headers=headers)
    fp = requests.get(link, headers=headers)
    #main = fp.read().decode("utf8")
    main = fp.text
    soup = BeautifulSoup(main, 'html.parser')




    time = soup.find_all("time")
    time = time[0].text.replace(" ","").replace("\n","")

    duration = 0

    if "h" in time and "min" in time:
        duration = int(time.split("h")[0])*60 + int(time.split("h")[1].split("min")[0])
    elif "h" in time:
        duration = int(time.split("h")[0])*60
    elif "min" in time:
        duration = int(time.split("min")[0])
               
    return duration

    
    #print(soup.find_all("tr", {"class": "findResult even"}))



###############################################################################################################


###### JSON FILE STRUCTURE ######
"""
'<date>':
    {
        'episodes':
            {
                '<episode_name>':
                {
                    'duration':'<duration>',
                    'show_name':'<name>'
                }
            }
        },
        'total_episodes':'<episode_count>',
        'duration':'<duration>'
    }




"""
#"<date>": {"episodes": {"<episode_name>": {"duration": "<duration>", "show_name": "<show_name>"}}
#, "total_episodes": 1, "duration": 10}

#import json

def csv_to_json(csv):

    data = "{"   #Parent json
    date = ""
    episodes = "{"    #Episodes json
    totalEps = 0
    totalMovs = 0
    totalDuration = 0

    
    for index, row in csv.iterrows():
        
        if row["Date"] != date and date != "":

            episodes = episodes[:-1]

            data += '"{0}": {{"episodes": {1}}}, "total_episodes": {2}, "total_movies": {3}, "duration": {4}}},'.format(date,episodes,totalEps,totalMovs,totalDuration)

            
            date = row["Date"]
            episodes = "{"
            totalEps = 0
            totalMovs = 0
            totalDuration = 0
            
        elif row["Date"] != date:       #Should only be called once
            date = row["Date"]

            

        #Creates list of episodes

        movie = "false"

        if len(row["Title"].split(":")) > 2: #Checks if show or movie
            title = ":".join(row["Title"].split(":")[2:])#row["Title"].split(":")[len(row["Title"].split(":"))-1]
            title = title.replace("\t"," ")
            show = ""

            season = ""

            for s in row["Title"].split(":"): #Incase a show like Cosmos: A space odyssey appears 
                
                if "Season" in s or "Part" in s:
                    season = s.split(" ")[2]
                    break
                else:
                    show += ":"+s
                    
            show = show[1:]


            #Stranger things bug
            if season == "":
                season = row["Title"].split(":")[1].split(" ")[len(row["Title"].split(":")[1].split(" "))-1]

                if RepresentsInt(season) == False:
                    season = 1
                
                show = row["Title"].split(":")[0]
                
        else:   #If movie
            title = row["Title"]
            show = "NA"

            season = "NA"

            movie = "true"


        duration = 0
        try:
            duration = getDuration(title,show,movie)
        except IndexError:
            print("Oh No!")
        print(duration)

        episodes += '"{0}": {{"duration": {1}, "movie": {2},"show_name": "{3}", "season": "{4}"}},'.format(title,duration,movie,show,season)
        totalDuration+= duration

        if movie == "false":
            totalEps += 1
        else:
            totalMovs += 1

    data = data[:-1]
    data += "}"
    return data

with open('nadimApril2020.json', 'w') as outfile:
    outfile.write(csv_to_json(pd.read_csv("NadimMergedApril2020.csv")))
