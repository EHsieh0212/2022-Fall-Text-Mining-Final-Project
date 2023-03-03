# 取得有得獎或入圍金曲最佳華語男歌手的所有名單的所有歌！
artist = ['陶喆', '張學友', '方大同', '周華健', '庾澄慶', '齊秦', '張信哲', '蕭敬騰', '曹格', 
            '吳青峰', '王力宏', '周杰倫', '林俊傑', '陳奕迅', '伍佰', '許志安', '信', '王傑', 
            '張雨生', '李宗盛', '蘇永康', '蕭煌奇', '吳克群', '楊培安', '小宇', '李榮浩', '張震嶽', 
            '盧廣仲', '林宥嘉', '黃明志', '韋禮安', '費玉清', '林志炫']
import requests
from bs4 import BeautifulSoup as bs4
import re
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def getAllPrizedMaleArtists(list, href):
    resp = requests.get(href)
    soup = bs4(resp.text, 'html.parser')
    allPrizedArtists = soup.select(".s_listA > li > a")
    domain = 'https://mojim.com'
    hrefs = []
    names = []
    for i in allPrizedArtists:
        if i.get_text() in list:
            href = i.get('href')
            hrefs.append(domain+href)
            name = i.get_text()
            names.append(name)
    res = {"allMaleArtists": names, "allHrefs": hrefs}
    return res


#example: https://mojim.com/twh100012.htm
# get only chinese tracks
def getArtistAllTracks(href):
    resp = requests.get(href)
    soup = bs4(resp.text, 'html.parser')
    bigSection = soup.select("dd")
    href = []
    name = []
    for section in bigSection:
        if len(section) == 8:
            try:
                result = section.select('.hc2')[0].get_text()
                if "國語" in result:
                    track_html = section.select('.hc3 > a')
                    track_href = [i.get('href') for i in track_html]
                    track_name = [i.get_text() for i in track_html]
                    href.extend(track_href)
                    name.extend(track_name)
            except:
                print("no tag")
    res = {'trackNames':name, 'trackHrefs': href}
    print("Finish Retrieving Hrefs.")
    return res


# example: https://mojim.com/twy100012x78x1.htm
def exportOneTrackLyrics(href):
    try:
        # 1. get html
        domain = 'https://mojim.com'
        res = requests.get(domain+href)
        # 2. parse into tree
        soup2 = bs4(res.text, 'html.parser')
        # 3. get track name, get lyrics
        trackName = soup2.select('#fsZx2')[0].get_text().strip()
        print(f"Start Processing {trackName}...")
        # 4. text cleaning:
            # 去除最下面的感謝tag: <ol>
        lyrics = soup2.select('#fsZx3')[0]
        for br in lyrics('br'):
            br.replace_with('\n')
        for i in lyrics("ol"): 
            i.extract()

        #切分段落、句子
        tmp = [i for i in lyrics.strings]
        seperate = "".join(tmp).split("\n\n")
        paragraph = [i.replace("\n", " ") for i in seperate]

        #去除雜訊
        result = []
        for line in paragraph:
            if "更多更詳盡歌詞" in line or "魔鏡歌詞網" in line or "Mojim.com" in line:
                continue
            if "："in line: 
                continue
            if line.find('[') != -1 or line.find(']') != -1 : 
                continue
            if "無歌詞" in line:
                continue
            if "---" in line:
                continue
            if len(re.findall('[　１２３４５６７８９０＊●＃＠＄％＾＆！＿『』｜，。？a-zA-Z0-9～【】\]\[＿\"\!\&\.\?\(\)\~\-\…\,]', line)) != 0:
                line = re.sub('[　１２３４５６７８９０＊●＃＠＄％＾＆！＿『』｜，。？a-zA-Z0-9～【】\]\[＿\"\!\&\.\?\(\)\~\-\…\,]', "", line)
            if "'" in line or "\"" in line or "[" in line or "]" in line:
                line = re.sub('[\'\"\[\]]', "", line)
            line = line.strip()
            if line == "":
                continue
            result.append(line)

            #4-c: 製作最終版本
        nos2 = ["，".join(i.split()) for i in result]
        nos2 = "。".join(nos2)
        # 5. 製作json, 輸出
        r = {'trackName': trackName, 'lyric_line': result, 'lyric_full': nos2}
        print("Export Over.")
        return r
    except:
        print("no data.")
        return None
    

# produce lyrics of artist tracks
def exportArtistAllTracks(href, fileName):
    alltracks = getArtistAllTracks(href)['trackHrefs']
    data = pd.DataFrame(columns=['trackName', 'lyric_line', 'lyric_full'])
    for i in range(len(alltracks)):
        result = exportOneTrackLyrics(alltracks[i])
        if result != None and len(result['lyric_line']) > 0:
            data = data.append({'trackName': result['trackName'], 'lyric_line': result['lyric_line'], 'lyric_full': result['lyric_full']}, ignore_index=True)
    data.to_csv(f"text/{fileName}.csv", encoding='utf-8-sig', index=False)
    print("Finish Processing.")
    return



def getAllMaleArtistsSongs(list, href):
    getAllMale = getAllPrizedMaleArtists(list, href)
    maleNames = getAllMale["allMaleArtists"]
    maleHrefs = getAllMale['allHrefs']
    data = pd.DataFrame(columns=['artistName', 'trackName', 'lyric_line', 'lyric_full'])

    for i in range(len(maleNames)):
        alltracks = getArtistAllTracks(maleHrefs[i])['trackHrefs']
        for j in range(len(alltracks)):
            print(f"Now processing: {maleNames[i], alltracks[j]}")
            result = exportOneTrackLyrics(alltracks[j])
            if result != None and len(result['lyric_line']) > 0:
                data = data.append({'artistName': maleNames[i], 'trackName': result['trackName'], 'lyric_line': result['lyric_line'], 'lyric_full': result['lyric_full']}, ignore_index=True)
        print(f"=======Finished processing: {maleNames[i]} songs.=======")
    
    data.to_csv(f"text/AllMalePrizedArtist.csv", encoding='utf-8-sig', index=False)
    print("Finish Processing.")


getAllMaleArtistsSongs(artist, "https://mojim.com/twza1.htm")



print("hello")

print("jjjj")