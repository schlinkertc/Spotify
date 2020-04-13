import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_top100(year):
    year = str(year)
    
    page = requests.get(f"http://billboardtop100of.com/{year}-2/")
    bs = BeautifulSoup(page.content)
    
    # first try 
    p_tags = bs.find_all('p')

    text = [p.getText(strip=True) for p in p_tags]

    records = []
    for n,p_tag in enumerate(p_tags):
        try:
            record = {
                "rank":int(p_tag.getText(strip=True)),
                "song":p_tags[n+1].getText(strip=True),
                "artist":p_tags[n+2].getText(strip=True),
                "year":year
            }
            records.append(record)
        except:
            continue 
    
    if len(records)==100:
        return records
    else: #<-- if the first method didn't work..
        # second method
        ranks = [x.getText(strip=True) for x in bs.find_all(attrs={'class':"ye-chart-item__rank"})]

        songs = [x.getText(strip=True) for x in bs.find_all(attrs={'class':"ye-chart-item__title"})]

        artists = [x.getText(strip=True) for x in bs.find_all(attrs={'class':"ye-chart-item__artist"})]
    
        records = [{'rank':rank,'song':song,'artist':artist,'year':year} for rank,song,artist in zip(ranks,songs,artists)]
        
        if len(records)==100:
            return records
        else:
            # 3rd method
            dfs = pd.read_html(f"http://billboardtop100of.com/{year}-2/")
            df=dfs[0]
            df.columns = ['rank','artist','song']
            df['year']=year
            records = df.to_dict(orient='records')
            if len(records)==100:
                return records
            

records = []
errors = []
for year in list(range(2000,2020)):
    try:
        records.extend(scrape_top100(year))
        print('o')
    except:
        print("x")
        errors.append(year)
        
data = pd.DataFrame.from_records(records)

# 2013 was formatted differently
page = requests.get("http://billboardtop100of.com/2013-2/")
bs = BeautifulSoup(page.content)

entries = bs.find('small').getText().split('\n')

records = []
for e in entries:
    try:
        record = {}
        record["rank"] = e.split('.')[0]
        e = "".join(x for x in e.split('.')[1:])
        song_artist = e.replace('\xa0','').strip()
        record['song'], record["artist"] = song_artist.split(" – ")
        record['year']='2013'
        records.append(record)
    except:
        continue

records.extend([
    {'rank':40,
     'artist':"Mike WiLL Made-It Featuring Miley Cyrus, Wiz Khalifa & Juicy J",
     "song":"23",
     'year':'2013'},
    {'rank':100,
     'artist':"Big Sean Featuring Lil Wayne & Jhene Aiko",
     'song':'Beware',
     'year':'2013'}
])

data = data.append(pd.DataFrame.from_records(records))

data.to_csv('resources/data/billboard_hot100.csv',index_label=False)