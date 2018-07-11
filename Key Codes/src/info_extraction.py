from src.img2txt import Img2Txt
import re
import json

i2t = Img2Txt(
    txt_folder='F:/Work/Chechup/img/categorize/report/ocr_txt/',
    img_folder='F:/Work/Chechup/img/categorize/report/',
    if_ocr=False
)

i2t.img2txt(filename='28.jpg', mode='full_info')

term_dict = {
    '白细胞': (3.5, 9.5),
    '淋巴细胞百分比': (20.0, 50.0),
    '单核细胞百分比': (3.0, 10.0),
    '嗜酸性粒细胞百分比': (0.4, 8.0),
    '嗜碱性粒细胞百分比': (0.0, 1.0),
    '中性粒细胞百分比': (40.0, 75.0),
    '淋巴细胞数绝对值': (1.1, 3.2),
    '单核细胞绝对值': (0.1, 0.6),
    '嗜酸性粒细胞绝对值': (0.02, 0.52),
    '嗜碱性粒细胞绝对值': (0.0, 0.1),
    '中性粒细胞绝对值': (1.8, 6.3),
    # '红细胞': (4.3, 5.8),
    '红细胞': (3.8, 5.1),
    # '血红蛋白': (130.0, 175.0),
    '血红蛋白': (115.0, 150.0),
    # --- Half here ---
    # '红细胞压积': (40.0, 50.0),
    '红细胞压积': (35.0, 45.0),
    '平均红细胞体积': (82.0, 100.0),
    '平均血红蛋白含量': (27.0, 34.0),
    '平均血红蛋白浓度': (320.0, 370.0),
    '红细胞分布宽度(CV)': (11.6, 14.5),
    '红细胞分布宽度(SD)': (37.0, 54.0),
    '血小板': (125.0, 350.0),
    '平均血小板体积': (6.5, 13.0),
    '血小板压积': (0.11, 0.28),
    '血小板分布宽度': (15.0, 18.0),
    '大型血小板比率': (11.0, 45.0),
    '大型血小板容积': (30.0, 90.0),
    '超敏C反应蛋白': (0.0, 3.0)
}


def clean_float(dirty):
    dirty = dirty.replace(',', '.')
    clean = dirty
    for bit in dirty:
        if ((ord(bit) < 48) and (ord(bit) != 46)) or (ord(bit) > 57):
            clean = clean.replace(bit, '')
    try:
        return float(clean)
    except:
        if clean == '':
            return ''
        raise TypeError('"%s" is not a float.' % clean)


def str_similarity(str_test, str_real):
    def get_item(string, loc):
        try:
            return string[loc]
        except IndexError:
            return None

    score = 0
    for i, character in enumerate(str_real):
        if character in str_test:
            caleb_i = str_test.find(character)
        else:
            caleb_i = i
        if get_item(str_test, caleb_i) is None:
            score += 0.5
        elif get_item(str_test, caleb_i) == character:
            score += 1
        else:
            score += 0.5
    score -= abs(len(str_test) - len(str_real)) * 0.2
    score /= len(str_real)
    return score


sorted_term = list(term_dict.keys())
sorted_term.sort(key=lambda x: len(x), reverse=True)

with open('../img/categorize/report/ocr_txt/28.txt') as f:
# with open('../img/controlled_best/txt/zxh.txt') as f:
    content = f.read()

content = eval(content)

chinese_list = []
for index, item in enumerate(content):
    tmp = []
    info = item[0]
    p2 = re.compile(r'[^\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh = p2.split(info)
    while '' in zh:
        zh.remove('')
    for char in zh:
        if char == '红细胞分布宽度':
            term_b = item[0].find(char)
            term_e = term_b + len(char) + 3
            char = item[0][term_b:term_e]
        tmp.append([index, char, item[0].find(char)])
    chinese_list += tmp

# print(chinese_list)

result = []
for term in sorted_term:
    sim_list = []
    for index, item in enumerate(chinese_list):
        if item[1] != '超敏':
            if item[1] == '反应蛋白':
                item[1] = '超敏C反应蛋白'
            similarity = round(str_similarity(item[1], term), 3)
            sim_list.append((similarity, index, item[1], term))

    sim_list.sort(reverse=True)
    similarity = sim_list[0][0]
    if similarity > 0.87:
        item = chinese_list[sim_list[0][1]]
        num_b = item[2] + len(item[1])
        num_e = num_b + 5
        i_dirty = content[item[0]][0][num_b:num_e]
        i_float = clean_float(i_dirty)
        # if item[1][:5] == '红细胞分布':
        #     print(content[item[0]][0][num_b:num_e])
        if i_float == '':
            try:
                i_float = float(content[item[0] + 1][0][:4])
            except ValueError:
                try:
                    i_float = float(content[item[0] + 2][0][:4])
                except ValueError:
                    i_float = 'Not found'
        result.append((list(term_dict.keys()).index(term), term, item, i_float))
    else:
        result.append((0, term, '', 'Not found'))


def reasonable(x, l, u):
    if not isinstance(x, float):
        print(x)
        return 'Not found'
    if l <= x <= u:
        return ''
    elif (x < l) and (x > l * 0.2):
        return '↓'
    elif (x > u) and (x < u * 1.8):
        return '↑'
    else:
        return 'alert'


result.sort()
result_dict = {}
for item in result:
    lower, upper = term_dict[item[1]]
    result_dict[item[1]] = item[3]
    # if item[3] == 'Not found':
    #     print('[FATAL] '+item[1]+' not found!')
    # else:
    #     print(item[1], item[3], reasonable(item[3], lower, upper))
print(json.dumps(result_dict, indent=4, ensure_ascii=False))
