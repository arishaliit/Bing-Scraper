from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import re

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def fetch_results_bing(search_term, number_results, language_code,country_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    # print(escaped_search_term)
    duck_url = 'https://www.bing.com/search?q={}&count={}&hl={}&cc={}'.format(escaped_search_term, number_results, language_code,country_code)
    #print(duck_url)
    response = requests.get(duck_url, headers=USER_AGENT)
    response.raise_for_status()

    return (search_term, response.text)

def parse_results_bing(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    found_results2 = []
    rank = 1
    result_block = soup.find_all('li', attrs={'class': 'b_algo'})

    #print(len(result_block))
#     print(result_block)
#     print(len(result_block))
    for result in result_block:


        link = result.find('a')
        link = link['href']

        title = result.find('h2')
        title = title.get_text()
        description = result.find('p')
        desc = re.sub("<.*?>", "", str(description))
        found_results.append({'link':link, 'rank': rank, 'title': title, 'description': desc})
        rank += 1

    result_block2 = soup.find_all('div', attrs={'class': 'b_rs'})
#     children = result_block2.find("li")
    #print(len(result_block))
#     print(result_block)
#     childeren = result_block2.find_all('li')
    for result in result_block2:

#         print("ok")
        link = result.find_all('li')

        for i in link:
#             print("1")
            li = i.find('a')
            li = li.get_text()
            found_results2.append(li)
#             print(li)
#         title = result.find('h2')
#         title = title.get_text()
#         description = result.find('p')
#         desc = re.sub("<.*?>", "", str(description))
#         found_results.append({'link':link, 'rank': rank, 'title': title, 'description': desc})



    return(found_results,found_results2)

def scrape_bing(search_term, number_results, language_code,country_code):
    try:
        keyword, html = fetch_results_bing(search_term, number_results, language_code,country_code)
        results, results2 = parse_results_bing(html, keyword)
        return results, results2
        # print(html)
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

    
#__________________Front Interface Design (START) ________________________

root=Tk()
pane=Canvas(root)
pane.pack(expand=True, fill=BOTH)

data = [] # to store all data, searched from web
results2=[]

#__________________________________________________________________________________________
# Here is the Function that scrape data and disp[lay in Text widget                        |
#__________________________________________________________________________________________|
def scrap():                                                                              #|
    if input_keyword.get():                                                               #|
        data.clear()                                                                      #|
        T.configure(state='normal')                                                       #|
        T.delete(1.0,END)                                                                 #|
        keywords = [ input_keyword.get() ]                                                #|
        number_of_results = (int((result_variable.get())))                                #|
        country_code='country'+(cr_variable.get())                                                
        
        for keyword in keywords:                                                          #|
            try:                                                                          #|
                results,related_results = scrape_bing(keyword, number_of_results, "en",country_code)

                results2.clear()
                results2.extend(related_results)

                for result in results:                                                    #|
                    data.append(result)                                                   #|
            except Exception as e:                                                        #|
                print(e)
        for d in data:                                                                    #|
            T.insert(INSERT,"\n"+str(d['description'])+"\n")                              #|
        
        for d in data:                                                                    #|
            T.insert(INSERT,"\n"+str(d['title'])+"\n")                                    #|
        
        for r in results2:
            T.insert(INSERT,'\n'+r+"\n")
            
        for d in data:                                                                    #|
            T.insert(INSERT,'\n'+str(d['link'])+'\n')                                          #|
            
    else:                                                                                 #|
        messagebox.showerror("Error", "Keyword Field is Empty")                           #|
    T.configure(state='disabled')                                                         #|
#__________________________________________________________________________________________|
    

#_____________________________________________________________________________________________________________________________
# Here is the Function that export the file, user specifies the location and save the file                                    |
#_____________________________________________________________________________________________________________________________|
def export():                                                                                                                #|
    if data:                                                                                                                 #|
        root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file"                                 #|
                                                      ,filetypes = (("text file","*.txt"),("all files","*.*"))) #fILE cHOOSEr |
        file=open(root.filename+'.txt','w')                                                                                  #|


        for d in data:                                                                    
            file.write(str(d['description'])+'\n')                          

        file.write('\n')
        
        for d in data:                                                                  
            file.write(str(d['title'])+'\n')                                   

        file.write('\n')
        
        for r in results2:
            file.write(r+"\n")

        file.write('\n')

        for d in data:                                                                    
            file.write(str(d['link'])+'\n')                                          

        file.write('\n')
                                                                                                              #|
        file.close()                                                                                                         #|
    else:                                                                                                                    #|
        messagebox.showerror("Error", "No Searched Data Found To Export")                                                    #|
#_____________________________________________________________________________________________________________________________|


#______________________________________________|
#_          Setting Background Image         __|
#______________________________________________|
img=PhotoImage(file="background2.png")         #|
pane.image=img                                #|
pane.create_image(0, 0, anchor=NW, image=img) #|
#______________________________________________|

#_______________________________________________________________________________________________________________________________________________________|
#                                                 Setting up Coloumn 0 of Grid                                                                          |
#_______________________________________________________________________________________________________________________________________________________|
Label(pane, text=" WEB SCRAPER ",font=('consolas',30)).grid(row=0, column=0, padx=60, pady=100) #Label to display "WEB SCRAPER" text  On Right Side     |
#_______________________________________________________________________________________________________________________________________________________|

#_____________________________________________________________________________________________________________________________________________________________|
#                                                Setting up Coloumn 1 of Grid                                                                                 |
#_____________________________________________________________________________________________________________________________________________________________|
Label(pane, text="KEYWORD     ",font=('consolas',12)).grid(row=1, column=1, padx=15, pady= 5)  #Label to display "Keyword" text  with the keyword Text Entry  |
Label(pane, text="COUNTRY CODE",font=('consolas',12)).grid(row=3, column=1, padx=15, pady= 5)  #Label to display "Country Code" text  with the OptionMenu     |
Label(pane, text="RESULTS     ",font=('consolas',12)).grid(row=4, column=1, padx=15, pady= 5)  #Label to display "Results" text  with the OptionMenu          |
Label(pane, text="RESULT      ",font=('consolas',12)).grid(row=6, column=1, padx=15, pady= 5)  #Label to display "Result" text  with the OptionMenu           |
Label(pane, text="keyword1,keyword2,...",font=('consolas',10)).grid(row=2, column=2, padx=15, pady= 5)  #Label to display Keywords input hint                 |
#_____________________________________________________________________________________________________________________________________________________________|

#________________________________________|
#_   Set Choices For Result 1 to 50    __|
#________________________________________|
result_choice=[]                       # |
for i in range(1,51):                  # |
    result_choice.append(i)            # |
result_variable = StringVar(pane)      # |
result_variable.set(1)#Set 1st choice=1# |
#______________________________________#_|

#________________________________________|_______________________________________________________________________________________
#___ Set Choices For Result 1 to 50   ___|# Below List contain All country codes. User can select any code from option men      |
#________________________________________|______________________________________________________________________________________|
cr_choice=[ "AF","AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ" #|
            ,"BJ","BM","BT","BO","BQ","BA","BW","BV","BR","IO","BN","BG","BF","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN"#|
            ,"CX","CC","CO","KM","CG","CD","CK","CR","CI","HR","CU","CW","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER"#|
            ,"EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GI","GR","GL","GD","GP","GU","GT","GG"#|
            ,"GN","GW","GY","HT","HM","VA","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM","JP","JE","JO","KZ"#|
            ,"KE","KI","KP","KR","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","MV","ML","MT"#|
            ,"MH","MQ","MR","MU","YT","MX","FM","MD","MC","MN","ME","MS","MA","MZ","MM","NA","NR","NP","NL","NC","NZ","NI","NE"#|
            ,"NG","NU","NF","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PN","PL","PT","PR","QA","RE","RO","RU","RW"#|
            ,"BL","SH","KN","LC","MF","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB","SO","ZA","GS"#|
            ,"SS","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TL","TG","TK","TO","TT","TN","TR","TM","TC"#|
            ,"TV","UG","UA","AE","GB","US","UM","UY","UZ","VU","VE","VN","VG","US","VI","WF","EH","YE","ZM","ZW" ]#             |
cr_variable = StringVar(pane)          # |______________________________________________________________________________________|
cr_variable.set('US')#Set 1st choice=US# |
#______________________________________#_|

#_______________________________________________________________________________________________________________________________________________________|
#                                             Setting up Coloumn 2 of Grid                                                                              |
#_______________________________________________________________________________________________________________________________________________________|
input_keyword = Entry(pane,width=30 ,justify=LEFT)                                                                                          #           |
input_keyword.focus()                                                                                                                       #           |
input_keyword.bind("<Return>",scrap)                                                                                                        #           |
input_keyword.grid(row=1, column=2, padx=5, pady= 5)                                          #Entry field to input the keyword from user               |
OptionMenu(pane, cr_variable, *cr_choice).grid(row=3, column=2, padx=5, pady= 5)              #Option Menu for Selection Country                        |
OptionMenu(pane, result_variable,  *result_choice).grid(row=4, column=2, padx=5, pady= 5)      #Option Menu to Selection for Number of Results          |
Button(pane, text=" SEARCH ",command=scrap).grid(row=5, column=2, padx=5, pady= 5)            #Search Button                                            |
Button(pane, text=" EXPORT ",command=export).grid(row=7, column=2, padx=5, pady= 5)           #export Button                                            |
#_______________________________________________________________________________________________________________________________________________________|

#______________________________________________________________________
#This is the code for text widget that show result of user search      |
#______________________________________________________________________|
T = Text(pane, height=10, width=35)                                   #|
T.grid(row=6,column=2)                                                #|
scr=Scrollbar(pane, orient=VERTICAL, command=T.yview)                 #|
scr.grid(row=6, column=5, rowspan=1, columnspan=1, sticky=NS)         #|
T.grid(row=6, column=2, columnspan=3 , sticky=W)                      #|
T.config(yscrollcommand=scr.set, font=('Arial', 10))                  #|
#______________________________________________________________________|


#_______________________________________________________________________
#    Setting up window's size title                                     |
#_______________________________________________________________________|
root.title('Bing Scraper')         # set title of the frame              |
root.geometry("900x670")          # set size of the frame (width,height)|
root.resizable(False, False)      # set window un-resizable             |
#_______________________________________________________________________|
mainloop()

#__________________Front Interface Design (END) ________________________
