import time
import requests,os
from scraper import scraper


class bot:
    def __init__(self,server_id:str,headers:str) -> None:
        self.scrap=scraper("https://launchmynft.io/mint/cosmic")
        self.mints=9
        self.messages=[]
        self.address={}
        self.path=""
        self.running=False
        self.prev=0
        self.server_id=server_id
        self.split=0
        self.ben=True
        self.mess_to_send=""
        self.privious=0
        self.top_message={}
        self.headers={"Authorization":headers}


    def command(self):
        while self.ben:
            if self.mints==0:
                self.path= os.path.join(self.scrap.download_dir,"recent-minters.csv")
                self.scrap.get_recent_minters()
                self.split=0
                
                try:
                    self.prev=len(self.messages)
                    with open(self.path,'r') as files:
                        lines=files.readlines()
                        self.messages=[lines[i] for i in range(1,len(lines))]
                    if os.path.exists(self.path):
                        os.remove(self.path)
                    for i in range(len(self.messages)):
                        some_shit=self.messages[i].split(',')
                        new_string=some_shit[self.split].rstrip("'")
                        self.address.update({i:new_string})
                    if self.prev <len(self.messages):
                        self.send_message()
                        print("message sent 0")            

                except Exception as e:
                    try:
                        print("ERROR READING FILE ",e)
                        if os.path.exists(self.path):
                          os.remove(self.path)
                    except Exception as e:
                        pass
            elif self.mints==1:
                self.split=1
                self.scrap.get_top_minters()
                self.path=os.path.join(self.scrap.download_dir,"top-minters.csv")
                try:
                    self.privious=len(self.top_messages)
                    with open(self.path,'r') as files:
                        lines=files.readlines()
                        self.top_message=[lines[i] for i in range(1,len(lines))]
                        self.address.clear()
                    if os.path.exists(self.path):
                        os.remove(self.path)
                    for i in range(len(self.top_message)):
                        some_shit=self.top_message[i].split(',')
                        new_string=some_shit[self.split].rstrip("'")
                        self.address.update({i:new_string})
                    if self.privious <len(self.top_message):
                        self.mess_to_send="latest top miner :"
                        self.send_message()
                        print("SENT BLYAT")
                except Exception as e:
                    try:
                        print("ERROR READING FILE ",e)
                        if os.path.exists(self.path):
                          os.remove(self.path)
                    except Exception as e:
                        pass

            elif self.mints==4:
                self.scrap.site.quit()
                exit()                           
    
            time.sleep(0.5)


    def send_message(self):
        try:
            requests.post(self.server_id,headers=self.headers,data={"content" : f"@everyone\n{self.mess_to_send}\nUser wallet : {self.address.get(0)}\nNUMBER: {len(self.address)}","mention_everyone": True})
        except Exception as e:
            print("can't take this shit  ",e)


