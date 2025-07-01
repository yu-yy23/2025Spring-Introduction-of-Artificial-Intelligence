import os

MODEL_DIR = './model'
DATA_DIR='./data'
SOURCE_DIR='./src'

CORPUS_DIR='./corpus'
SINA_NEWS_DIR=os.path.join(CORPUS_DIR, 'sina_news_gbk')

PINYIN_CHAR_TABLE_FILE = os.path.join(DATA_DIR, '拼音汉字表.txt')
PINYIN_CHAR_TABLE_UTF8_FILE = os.path.join(DATA_DIR, '拼音汉字表_utf8.txt')
CHAR_TABLE_FILE = os.path.join(DATA_DIR, '一二级汉字表.txt')
CHAR_TABLE_UTF8_FILE = os.path.join(DATA_DIR, '一二级汉字表_utf8.txt')

INPUT_FILE = os.path.join(DATA_DIR, 'input.txt')
OUTPUT_FILE = os.path.join(DATA_DIR, 'output.txt')
ANSWER_FILE = os.path.join(DATA_DIR, 'answer.txt')

CORPUS_UTF8_DIR = os.path.join(MODEL_DIR, 'corpus_utf8')
FREQUENCY_DIR = os.path.join(MODEL_DIR, 'frequency_counter')
PROBABILITY_DIR = os.path.join(MODEL_DIR, 'probability')

PREPROCESS = os.path.join(SOURCE_DIR, 'preprocess.py')
PROCESS = os.path.join(SOURCE_DIR, 'process.py')
BINARY_GENERATE = os.path.join(SOURCE_DIR, 'binary_generate.py')
MULTI_GENERATE = os.path.join(SOURCE_DIR, 'multi_generate.py')
TEST = os.path.join(SOURCE_DIR, 'test.py')
