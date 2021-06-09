#############################################
#
#    Author : Chris Fan
#    Date : 2021/06/07
#    Version : 0.1
#    Description : Parse the COVID19 report from https://covid-19.nchc.org.tw/
#    Change log:
#                - initial version to get the comfirm data
#
#############################################
import requests
import json

#import colorama
#from colorama import Fore
#from colorama import Style

source_uri = "https://covid-19.nchc.org.tw/amchartsSource/output/chartdiv_023_backlog.min.js"
pattern_start = "chart023_backlog.data="
pattern_start_len = len(pattern_start)
pattern_end = ";var baseWidth="

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def COVID19_INFO_GET():
    reponse = requests.get(source_uri, verify=False)
    #reponse = requests.get(source_uri)
    t = reponse.text
    #print(t)


    find_s = t.find('chart023_backlog.data=')
    find_e =  t.find(';var baseWidth=')

    if find_s == -1 or find_e == -1 :
        print("COVID19_INFO_GET fail")
    else :

        find_s = find_s + pattern_start_len
        comfirmed = (t[find_s:find_e])

        # replace string
        comfirmed = comfirmed.replace("y", "\"date\"").replace("x","\"recover\"").replace("value","\"value\"");
        # remove unused data "color"

        comfirmed = comfirmed.replace(",color:colors.critical","").replace(",color:colors.bad","").replace(",color:colors.medium","").replace(",color:colors.good","").replace(",color:colors.verygood","")
        data_json = json.loads(comfirmed)
        #print(comfirmed)

        print("COVID19 -- Taiwan daily report , reference : CDC daily update")

        date = data_json[0]["date"]
        value = data_json[0]["value"]

        for idx, c in enumerate(data_json):
            if c["date"] == date :
                continue
            else :
                print("Date=%s, Confirmed=%d" % (date, value))
                date = c["date"]
                value = c["value"]

                # dump the last item
                if idx == len(data_json)-1 :
                    # colorama.init()
                    # print(Fore.BLUE + Style.BRIGHT + "Date=%s, Confirmed=%d" + Style.RESET_ALL % (date, value))
                    print("Date=%s, Confirmed=%d" % (date, value))
                    # print(bcolors.OK + "Date=%s, Confirmed=%d" + bcolors.RESET % (date, value))
                    # print(bcolors.OK + "Date=, Confirmed= " + bcolors.RESET)



if __name__ == '__main__':
    COVID19_INFO_GET()
