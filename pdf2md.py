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

```
""" + text + """
```"""
    text = ''.join(filter(lambda x: x in set(string.printable), text))
    
    # Save to output file
    open(out_path+filename+'.md','w').write(text)
