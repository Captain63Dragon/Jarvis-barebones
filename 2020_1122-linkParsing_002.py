# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 9:26:09 2020

@author: Tim
Parse the export file from OneTab into a list of words. I have manually processed these words
and made some guesses as to which category each word falls into. Surprisingly, one or more
of the words are in most links or their descriptions. There were some that did not hit on 
anything. I grouped most of those into personal. More work should be done on the categories.
Some good Python practice was had in generating these word lists. 

This is now ALMOST working. The title is still problematic when exported as a file and causes
Windows to not recognize the output as a valid url file. A work-around I fount was to manually
update the filename in a browser. This works, but if you change it back to the exact filename,
it goes back to being unrecognized. Even if you move the file away and back, it does not 
recognize it. Something fishy is going on in the background here.

"""
import pathlib
import os.path as op  # operating system dependant
import re # regular expressions

class InternetShortcut(object):
    def __init__(self, url, title):
        super(InternetShortcut, self).__init__()
        self.lnk = url
        temp_title = re.sub('[\|\\\/:"<>\?\*]','-',title,0)
        self.title = temp_title
        self.categories = []

    categoryData = {'personal':['Personal', ("tim","captain","dragon","calendar","localhost","ourwondermill","priorities","resume","tasks","ucc")],
             'platform':['Programming', ("anaconda","auth","authentication","barebones","batch","bns","bolt","bootcamp",
                  "bootstrap","cloud","community","cypher","database","datastacktv","did","django",
                  "flask","git","graph","graphdb","identity","instances","internet","java","javascript",
                  "json","jspa","jsref","jwt","keep","master","messageid","navbar","nbt","nbtexplorer",
                  "online","overflow","php","platform","python","region","roles","script","scripting",
                  "templates")],
              'learning':['Training', ("articles","basics","beginner","beginners","careers","coding","course","demo","example",
                "examples","forums","lang","language","languages","learn","lecture","live","perpgaragesale",
                "intro","introduce","knowledge","simple","studio","topics","workshop","questions",
                "quickstart","recording","reference","roadmap","support","trial","try","tryit",
                "tutorial")],
             'companies':['Companies', ("amazon","athabasca","aws","github","hongkiat","iiwxxx","jansen","google",
                "canada","church","convid","dreamhost","dupeguru","eventbrite","facebook","gregabyte",
                "herokuapp","interac","jinja","marketplace","mdn","neo","npm","pingidentity","uport",
                "jarvis","linux","mediawiki","medium","minecraft","oracle","palletsprojects","plaid",
                "rockauto","rosborough","schools","scotiabank","scotiaonline","stackoverflow",
                "terminalman","toggl","udemy","visualstudio","youtube","zaudi","zoom")],
             'compSci': ['GenericComputer', ("filename","font","property","weight","method","dictionary","ref","blob","access","address",
              "api","aqs","aspen","aspx","base","blog","button","cgi","classes","classmethod","code","console",
              "dashboard","debugging","documentation","downloads","driver","encode","function","gmail","firewallsettings",
              "guides","help","host","inbox","index","instance","list","login","main","manual","microsoft","images",
              "png","programmer","programming","project","projects","random","range","results","reverse",
              "rfc","speechsynthesis","staticmethod","step","throw","tool","tools","top","transfer","update",
              "utilities","version","views","watch","worknotes","net","org","package","panel","ping","print",
              "profile","retry","return","srv","ssh","stack",
              "tab","text","utf","utm","view","web","windows","editor")]}
    ignore = ("http","https","file","chrome","css","cssref","www","asp","com","en","js","v1",
              "all","app","are","can","complete","doc","docs","documents","fetch","files","find","from",
              "browser","cannot","change","current","going","latest","purpose","search","services","session",
              "sheet","source","sourceid","summary","today","west","where","yourself","hello","home","how",
              "items","joe","meaning","nhxl","not","our","right","rlz","side","temp","the","then","there",
              "tree","untitle","use","why","with","you","your","users","tim","get",
              "on",'mail','and','for','html','google','Â','â')

    def add_category(self, cat):
      if not cat in self.categories:
        self.categories.append(cat)
        return True
      else:
        return False

    def get_title(self):
      return self.title

    def get_categories(self):
      return self.categories

    def get_url(self):
      return self.url
    
    def export_str(self):
      out = ''
      for cat in self.categories:
        out += (f"; #{cat}\n")
      out += (f"[InternetShortcut]\nURL={self.lnk}")
      return out

    def isCategory(self, word, linkDict):
      if word in InternetShortcut.ignore:
        return False
      if not self.lnk in linkDict:
        linkDict[self.lnk] = self
      one_found = False
      for value in InternetShortcut.categoryData.values():  
        if word in value[1] and not value[0] in self.categories: 
          one_found = True
          self.add_category(value[0])
      return one_found

f = pathlib.Path("c:/users/tim/_Incoming links/.oneTab-export/")
if f.exists() and f.is_dir():
    for path in f.iterdir():
        if path.is_file() and op.splitext(path)[1].lower() =='.txt':
          with open(path,"r") as lnk:
            oneLnks = [line.rstrip() for line in lnk.readlines()] 
            unclassified = {}
            counts = { name : 0 for name in InternetShortcut.categoryData.keys()}

            # some words that are common and not really surprising or interesting. There are certainly more
            # that could have been added, but quite a lot of them are not that frequent
            # links = {'url':['catname1','catname2']} # example format for links
            links = {}
            for oneLnk in oneLnks:
              aLink = oneLnk.split(' | ',1)
              if len(aLink) == 1:
                int_src = InternetShortcut(aLink[0], 'untitled')
              else:
                int_srt = InternetShortcut(aLink[0],aLink[1])
              if not aLink[0] == '':
                # This split is 'separated by non-word characters or 1 or more digit or an underscore.'
                # I didn't check to see if the underscore actually worked or not. Not that many of them.
                for word in re.split('[\W]|\d+|[\_]',oneLnk):
                  if word != "" and len(word) >= 3: # filter out single and double chars. Not interesting.
                    lword = word.lower()
                    if int_srt.isCategory(lword, links):
                      for name in counts.keys():
                        if InternetShortcut.categoryData[name][0] in int_srt.get_categories():
                          counts[name] += 1
                    else:
                      if not lword in unclassified:
                        unclassified[lword] = 1
                      else:
                        unclassified[lword] += 1
            
            # Summary of counts by category. 
            for key in counts.keys():
              print (f"Category: {key}, found {counts[key]}")
            print () # spacer

            # All categories with links. Links will be printed multiple times if they are
            # in multiple categories.
            # for name in names.values():
            #   print (f"Category: {name}")
            #   for lnk, cats in links.items():
            #     if name in cats:
            #       print (f"  {lnk}")

            for link_obj in links.values():
              filename = op.join(f, link_obj.get_title() + '.url')
              print(filename)
              with open(filename, 'w') as out:
                # print (f"(print this to file: {link_obj.get_title()}.lnk)")
                out.write(link_obj.export_str())

            print ("Uncategorized:")

            # currently all links have at least one category. Print in case that changes. 
            for key, link_obj in links.items():
              if len(link_obj.get_categories()) == 0: 
                print (f'{key}')
