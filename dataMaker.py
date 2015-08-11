import requests  
import json  
import pandas as pd
import datetime as dt
import os
import strip
os.chdir("/Users/yuki/Desktop/nba")

players = []  
player_stats = {'name':None,'avg_dribbles':None,'avg_touch_time':None,'avg_shot_distance':None,'avg_defender_distance':None}
data=[]

teamids=["1610612738","1610612741","1610612737","1610612751","1610612739","1610612766","1610612752","1610612765","1610612748","1610612755","1610612754","1610612753","1610612761","1610612749","1610612764",\
"1610612743","1610612744","1610612742","1610612750","1610612746","1610612745","1610612760","1610612747","1610612763","1610612757","1610612756","1610612740","1610612762","1610612758","1610612759"]

ids=pd.DataFrame()
def player_getter(teamid):
    url="http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID="+teamid+"&VsConference=&VsDivision="
    response = requests.get(url)
    data = json.loads(response.text)
    headers = data['resultSets'][1]['headers']
    player_data = data['resultSets'][1]['rowSet']
    temp = pd.DataFrame(player_data,columns=headers)
    temp=temp[temp.GP>=82*0.75]
    temp=temp.ix[:,[1,2]]
    temp["TEAM_ID"]=teamid
    return(temp)


for teamid in teamids:
    res=player_getter(teamid)
    ids=ids.append(res)


raw=pd.DataFrame()
def find_stats(playerid):  
    #NBA Stats API using selected player ID
    # url = "http://stats.nba.com/stats/playerdashptshotlog?"+\
    # "GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0"+\
    # "&OpponentTeamID=0&Outcome=&Period=0&playerid="+playerid+"&Season=2014-15"+\
    # "&SeasonSegment=&SeasonType=Playoffs&TeamID=0&VsConference="+\
    # "&VsDivision="
    url="http://stats.nba.com/stats/playerdashptshotlog?"+\
    "DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00"+\
    "&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID="+playerid+\
    "&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision="
 

    response = requests.get(url)
    # shots = response.json()['resultSets'][0]['rowSet']
    data = json.loads(response.text)
    headers = data['resultSets'][0]['headers']
    shot_data = data['resultSets'][0]['rowSet']
    df = pd.DataFrame(shot_data,columns=headers) 
    df["PLAYER_ID"]=playerid
    # df["PLAYER_NAME"]=
    # avg_def = df['CLOSE_DEF_DIST'].mean()
    # avg_dribbles = df['DRIBBLES'].mean()
    # avg_shot_distance = df['SHOT_DIST'].mean()
    # avg_touch_time = df['TOUCH_TIME'].mean()

    # #add Averages to dictionary then to list
    # player_stats['name'] = name
    # player_stats['avg_defender_distance']=avg_def
    # player_stats['avg_shot_distance'] = avg_shot_distance
    # player_stats['avg_touch_time'] = avg_touch_time
    # player_stats['avg_dribbles'] = avg_dribbles
    # players.append(player_stats.copy())
    return(df)

raw=pd.DataFrame()
for i in ids.PLAYER_ID.iteritems():
    try:
        res=find_stats(str(i[1]))
        raw=raw.append(res)
    except:
        pass


print raw.head()
ids.PLAYER_ID=ids.PLAYER_ID.astype(str)
raw=pd.merge(raw,ids,on="PLAYER_ID",how="left")
raw.to_pickle("nba.pkl")
raw.to_csv("nba.csv",index=False)

raw["DATE"]=raw.MATCHUP.map(lambda x :x.split(" - ")[0])
raw["DATE"]=raw.DATE.map(lambda x:dt.datetime.strptime(x,"%b %d, %Y").strftime("%Y-%m-%d"))

def defender_maker(x):
    if len(x.strip().split(","))==2:
        return str(x).strip().split(",")[1]+" "+str(x).strip().split(",")[0]
    else:
        return x.strip()

raw["DEFENSE"]=raw["CLOSEST_DEFENDER"].map(lambda x:defender_maker(x))
raw=pd.read_pickle('nba.pkl')
agg_1=raw.groupby(["PLAYER_NAME"])["PLAYER_NAME"].unique()
