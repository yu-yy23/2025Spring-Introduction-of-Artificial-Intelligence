import os
from settings import SINA_NEWS_DIR, PINYIN_CHAR_TABLE_FILE, PINYIN_CHAR_TABLE_UTF8_FILE
from settings import CHAR_TABLE_FILE, CHAR_TABLE_UTF8_FILE, CORPUS_UTF8_DIR

#print('Transforming corpus coding from GBK to UTF-8...')
os.makedirs(CORPUS_UTF8_DIR, exist_ok=True)
months = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
for i in range(4, 12):
    in_file = os.path.join(SINA_NEWS_DIR, f'2016-{months[i]}.txt')
    out_file = os.path.join(CORPUS_UTF8_DIR, f'2016-{months[i]}.txt')
    os.system(f'iconv -f GBK -t UTF-8 {in_file} > {out_file}')
#print('Transforming corpus coding from GBK to UTF-8 completed.')

#print('Transforming data coding from GBK to UTF-8...')
os.system(f'iconv -f GBK -t UTF-8 {PINYIN_CHAR_TABLE_FILE} > {PINYIN_CHAR_TABLE_UTF8_FILE}')
os.system(f'iconv -f GBK -t UTF-8 {CHAR_TABLE_FILE} > {CHAR_TABLE_UTF8_FILE}')
#print('Transforming data coding from GBK to UTF-8 completed.')
