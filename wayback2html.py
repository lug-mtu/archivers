import numpy as np
import os, shutil, glob
import subprocess

# The format is "lug-l-YYMMDD". Because we only go from 2001 to 2006, we cheat
# and only map 0+[1->6] for the year.
months = [x.zfill(2) for x in np.arange(1,13).astype(str)] # 01 to 12
years = [x.zfill(2) for x in np.arange(1,7).astype(str)]   # 01 to 06
for year_int,year in enumerate(years):
    for month_int,month in enumerate(months):
        
        # These times are not archived, or there were zero emails sent.
        if year_int == 2 and month_int < 1:
            pass
        elif year_int == 3 and month_int == 6:
            pass
        elif year_int == 6 and month_int > 3:
            pass
        else:
            # The time stamp: 20061113053117 is the most recent time before
            # /lists/ was redirected to a "technical difficulties" page, before
            # returning 404. lol. So, our latest archive is Nov, 2006.
            url = "http://lug.mtu.edu/lists/lug-l-0"+str(year)+str(month)+"/threads.html"
            command = "wayback-machine-scraper -f 20060707222054 -t 20060707222054 " + url
            print(command)
            subprocess.run(command.split(), stdout=subprocess.PIPE)

# After scraping archive.org, we need to process the data. 
files = sorted(glob.glob('website/**/*.snapshot', recursive=True))

# If you're on Windows, remove 
files = [path.replace('\\', '/') for path in files]

# index of lug.mtu.edu, I don't use this. If someone wants to see the homepage
# from back then, just use web.archive.org.
files = files[1:]

out_path = 'out/'

# Index of /lists/
file = files[0]
shutil.copy2(file, out_path+'index.html')

# Just change extension from .snapshot to .html and move to output folder.
for file in files[1:]:
    paths = file.split('/')[2:]
    if not os.path.exists(out_path+paths[0]):
        os.mkdir(out_path+paths[0])
    shutil.copy2(file, out_path+paths[0]+'/'+paths[1])