import pdfminer.high_level
import glob, os
import string

# Meeting minutes are stored as pdfs scraped from the wiki.
path = 'Minutes/'
out_path = path[:-1]+'_out/'

files = sorted(glob.glob(path+'*.pdf'))

if not os.path.exists(out_path):
    os.mkdir(out_path)

for file in files:

    # In case on Windows
    file = file.replace('\\','/')
    
    # PDF -> text
    text = pdfminer.high_level.extract_text(file)
    
    if '2012126-Minutes.pdf' not in file:
        
    
        # Remove wiki tag
        text = text.split('From MTU LUG wiki')[1]
        text = text.split('Retrieved from')[0]
        text = text.strip()
        
        # Clean up into templating markdown format.
        # To keep the archive sane, I only view the files as a large chunk of
        # unformatted info, hence the ``` ticks surrounding the text.
        filename = file.split('/')[-1].replace('.pdf','')
        date = filename[:4]+'-'+filename[4:6]+'-'+filename[6:]
        text = """---
date: """ + date + """
title: Minutes """ + date + """
tags: minutes,minutes"""+date[:4]+"""
template: minutes
---

```text
""" + text + """
```"""
        text = ''.join(filter(lambda x: x in set(string.printable), text))
        
        # Save to output file
        open(out_path+filename+'.md','w').write(text)

# 20120126 is in a different format. I'll just manually write it down.
text = """---
date: 2012-01-26
title: Minutes 2012-01-26
tags: minutes,minutes2012
template: minutes
---
```text
Attendees:
Josh Knight
Jacob Wiltse
Jay Vana
Peter Marheine
Jared Ledvina
Zhuoyu Zhou

Meeting called to order
Officer report:
    T-shirts available

Server status:
    New 1 TB drive
    New server potential
    
Discussed upgrading to a Gigabit connection. Funds still come from CS Gift Account. We can't afford it.
Need to get stuff out of 317. Plan on moving the stuff this weekend. Email with more info coming.

Installathon:
    Looking at March
    Location requests: MUB Commons
    Helping out Chris' LAN party. He needs hardware, we can most likely help.

Linux certifications:
    Need to be looked into more.
    Info on what it takes to get certified.
    Offer help (hopefully) next semester.
    Cost?
    
Penguicon:
    Email will be sent to list

Student cluster competition:
    G is going.
    We can probably help pay for it.
    Competition for building clusters.
    Will need more info from G.
    
Budget hearing:
    Jan. 31st
    Ideas:
        Start high to work Low.
        Mitch will be attending meeting for budget.
        Last year's budget available on wiki.

Open floor:
    Social gathering before/after meetings?
    Other ways to get the group to be more like a group.
```
"""
open(out_path+'20120126.md','w').write(text)
