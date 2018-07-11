from pymongo import MongoClient
import datetime
import json
import time
import random


class RecordLevel:
    def __init__(self):
        super().__init__()
        # self.test_type = name
        self.terms = None
        self.values = None
        self.ranges = None
        self.scales = None

    def __getattr__(self, item):
        if item == 'terms':
            return self.terms
        if item == 'values':
            return self.values
        if item == 'ranges':
            return self.ranges
        if item == 'scales':
            return self.scales
        if item == 'dict':
            return {
                'terms': self.terms,
                'values': self.values,
                'ranges': self.ranges,
                'scales': self.scales
            }


class Db2Pdf:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.col_num = 18
        self.db = client.health_care
        self.levels = None
        self.standards = list(self.db.blood_STD.find())
        self.records = list(self.db.blood_DATA.find())[8]
        self.construct_levels()
        self.data_length_check()

    def data_length_check(self):
        if len(self.levels.values) != self.col_num:
            print("Column number don't match!")
        for content in ['terms', 'values', 'ranges', 'scales']:
            self.levels.__setattr__(content, self.levels.__getattr__(content)[:18])

    def construct_levels(self):
        rl = RecordLevel()
        rl.terms = list(self.records.keys())[1:]
        rl.values = list(self.records.values())[1:]
        rl.ranges = [tuple(x['range']) for x in self.standards]
        rl.scales = self.scale_generator()
        self.levels = rl

    def scale_generator(self):
        std_dict = {}
        for std in self.standards:
            std_dict[std['term']] = std

        scale_list = []
        for term, value in self.records.items():
            if term == '_id':
                continue
            mmin, mmax = std_dict[term]['range']
            if value < mmin:
                scale_list.append(-1)
            elif value > mmax:
                scale_list.append(-2)
            else:
                scale_list.append(int((value - mmin) // ((mmax - mmin) / 10)))

        return scale_list


class BackendApiDev:
    def __init__(self):
        from random import random, randint
        values = [round(random() * 50 + 5, 1) for _ in range(18)]
        ranges = [(randint(0, 20), randint(30, 90)) for _ in range(18)]
        scales = [-2, 2, 3, 6, 1, 4, 5, 4, -1, 2, -2, -1, -2, 1, 2, 3, 4, 4]
        terms = [
            '白细胞计数', '红细胞计数', '血红蛋白浓度', '红细胞压积', '平均红细胞体积',
            '平均红细胞血红蛋白含量', '平均红细胞血红蛋白浓度', '血小板计数', '淋巴细胞比值',
            '单核细胞比例', '中性粒细胞比例', '淋巴细胞计数', '单核细胞计数', '中性粒细胞计数',
            '红细胞分布宽度', '血小板体积分布宽度', '平均血小板体积', '大血小板比例'
        ]
        self.levels = {
            'terms': terms,
            'values': values,
            'ranges': ranges,
            'scales': scales
        }
        self.result_text = {
            '白细胞计数': {
                'disc': '您可能发生了急性感染，请速前往医院就诊并进行治疗。',
                'value': -2
            },
            '淋巴细胞比值': {
                'disc': '您的细胞免疫功能可能较弱，请择日前往医院进一步检查确认。',
                'value': -1
            },
            '中性粒细胞比例': {
                'disc': '您可能患有伤寒、副伤寒，若伴有淋巴细胞计数和比例增加则可能出现了病毒性感染、请速前往医院就诊并进行治疗。',
                'value': -2
            },
            '淋巴细胞计数': {
                'disc': '您的细胞免疫功能可能较弱，请择日前往医院进一步检查确认。',
                'value': -1
            },
            '单核细胞计数': {
                'disc': '您可能有慢性炎症，若有发热症状则可能有细菌感染，请速前往医院就诊并进行治疗，避免感染加重，注意慎用抗生素。',
                'value': -2
            }
        }
        self.title = '血常规报告'
        self.summary = '您MCV、MCH、MCHC三项均偏低，可能患有小细胞低色素贫血（常见病因为癌或感染引起的继发性贫血，铅中毒及CO中毒）' \
                       '或全身性溶血性贫血（常见病因为地中海贫血、遗传性球形红细胞增多症、先天性丙酮酸激酶缺乏症），请速前往医院就诊' \
                       '并进行治疗。'


class DevGenerator:
    @staticmethod
    def rules_generator():
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

        standards = []
        for key, value in term_dict.items():
            target_dict = {}
            target_dict['term'] = key
            target_dict['range'] = list(value)
            target_dict['rules'] = [
                ['GT', 0, 'greater_test_work!'],
                ['LT', 0, 'smaller_test_work!']
            ]
            target_dict['update'] = datetime.datetime.now().strftime('%Y/%m/%d_%H:%M:%S.%m')
            standards.append(target_dict)

        result_string = json.dumps(standards, indent=4, ensure_ascii=False)
        print(result_string)
        # with open('./standards.json', 'w') as f:
        #     f.write(result_string)
        # print('Save finished!')

    @staticmethod
    def std_generator():
        with open('./standards.json', encoding='utf-8') as f:
            standards = json.load(f)
        for item in standards:
            item['update'] = datetime.datetime.utcnow()
            time.sleep(0.1)
        client = MongoClient('localhost', 27017)
        db = client.health_care
        # Remove documents
        # db.blood.remove({})
        # Insert documents
        ids = db.blood_STD.insert_many(standards).inserted_ids
        print('Insertion complete, ObjIds are as follows:')
        for id in ids:
            print(id)
        pass

    @staticmethod
    def data_generator():
        with open('./standards.json', encoding='utf-8') as f:
            standards = json.load(f)
        # print(standards)
        record = {}
        for std in standards:
            term = std['term']
            mmin, mmax = std['range']
            record[term] = mmin - (mmax - mmin) / 2 + random.random() * (mmax - mmin) * 2
        # print(record)
        client = MongoClient('localhost', 27017)
        db = client.health_care
        id = db.blood_DATA.insert_one(record).inserted_id
        pass


if __name__ == '__main__':
    # Data generation
    # dg = DevGenerator()
    # dg.rules_generator()
    # dg.std_generator()
    # dg.data_generator()

    dp = Db2Pdf()
    print(dp.levels.dict)
    # dp.data_length_check()

    pass
