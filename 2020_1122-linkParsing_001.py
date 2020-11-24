# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 9:26:09 2020

@author: Tim
Parse the export file from OneTab into a directory of lnk files
 OneTab seperates the link from the title provided with a ' | '. Many websites
 provide a bar in their title as well. This script looks a the qualifiers in the title
 and looks for commonalities. Links are grouped and printed at the end

I noticed that there are 'duplicates' in the Singletons section. These are not links that 
are duplicated, but multiple qualifiers in one link that are added sequentially. They
are thus printed out once for each qualifier.

Something of questionable interest is what splitting everything into word like chunks
would look like. Some portions like .com or html or https would not be very useful
but there would likely be some programming words, file words etc.

"""
import pathlib
import os.path as op
import re #regular expressions

f = pathlib.Path("c:/users/tim/_Incoming links/.oneTab-export/")
if f.exists() and f.is_dir():
    for path in f.iterdir():
        if path.is_file() and op.splitext(path)[1].lower() =='.txt':
          with open(path,"r") as lnk:
            oneLnks = [line.rstrip() for line in lnk.readlines()] 
            qualifiers = {}
            types = {}
            dups = {}
            for oneLnk in oneLnks:
              onBars = oneLnk.split(' | ')
              if not onBars[0] == '':
                if not oneLnk in dups:
                  dups[oneLnk] = 1
                  link, type = onBars[0], str.lower(onBars[0].split('://')[0])
                  if not type in types:
                    types[type] = 1
                  else:
                    types[type] += 1
                  del onBars[0]
                  for qual in onBars:
                    if not qual in qualifiers:
                      qualifiers[qual] = [1, [oneLnk]]
                    else:
                      qualifiers[qual][0] += 1
                      qualifiers[qual][1].append(oneLnk)
                  # print (type, link, onBars)
                else:
                  dups[oneLnk] +=1
            print (types)
            for key, value in qualifiers.items():
              if value[0] > 1:
                print (f"Qualifier: {key}")
                for link in value[1]:
                  print(f"  {link}")
            for key, value in dups.items():
              if value > 1:
                print (f"Link: {key} (seen {value} times)")
            print("Singleton qualifiers:")
            for value in qualifiers.values():
              if value[0] == 1:
                print(f"  {value[1][0]}")
            # header_columns = header.split(",")
            # header_columns[0]='name'
            # lines = [line.rstrip() for line in csv.readlines()]
            # for line in lines:
            #     # we assume here that there is one long line that has " at the beginning and end
            #     # we also assume that there are no \n (bad assumption!) in the middle
            #     left,description = re.split(',\s*"',line,1)
            #     description,right = re.split('",\s*',description,1)
            #     line_columns = left.split(",")
            #     line_columns.append(description)
            #     line_columns.extend(right.split(","))
                
            #     for i in range(len(header_columns)):
            #         print(header_columns[i] + ":" + line_columns[i])
            #     print("------------------")
