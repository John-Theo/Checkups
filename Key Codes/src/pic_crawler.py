import re
import requests
import time
from urllib import parse

TOTAL_PIC_NUM = 600
IMG_START_INDEX = 785
KEY_WORD = '作文 草稿'
PIC_ROOT = '../img/add/'

i = IMG_START_INDEX
processed = 0
downloaded = []

for pn in range(0, TOTAL_PIC_NUM, 20):
    word = parse.quote(KEY_WORD)
    # print(word)
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&word='+word+'&pn=' + str(pn)
    html = requests.get(url).text
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)

    for each in pic_url:
        processed += 1
        if each in downloaded:
            print('[Alert] Previous downloaded!')
            continue
        try:
            pic = requests.get(each, timeout=10)
            try:
                print('[%d/%d/%d]' % (i, processed, TOTAL_PIC_NUM*3), pic.headers['Content-Length'])
                if int(pic.headers['Content-Length']) < 50000:
                    print('[Alert] Pic too small!')
                    continue
            except KeyError:
                print('[Alert] Pic size unknown!')
                continue
        except:
            print('[Error] Url expired!')
            continue
        string = PIC_ROOT + str(i) + '.jpg'
        fp = open(string, 'wb')
        fp.write(pic.content)
        fp.close()
        downloaded.append(each)
        i += 1
        print(each)

        time.sleep(0.5)
