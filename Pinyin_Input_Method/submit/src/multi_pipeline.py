import os
import time
from settings import CORPUS_UTF8_DIR, FREQUENCY_DIR, PROBABILITY_DIR
from settings import PREPROCESS, PROCESS, MULTI_GENERATE, TEST
from settings import INPUT_FILE, OUTPUT_FILE

def pipeline():
    start_time = time.time()
    months = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for i in range(4, 12):
        file = os.path.join(CORPUS_UTF8_DIR, f'2016-{months[i]}.txt')
        #print(f'Processing {file}...')
        os.system(f'python3 {PREPROCESS} --input {file} --encoding utf-8 --outdir {FREQUENCY_DIR} --arity 4')
        #print(f'Preprocessing {file} completed.')
        #print()

    #print('Processing n-grams...')
    os.system(f'python3 {PROCESS} --indir {FREQUENCY_DIR} --encoding utf-8 --outdir {PROBABILITY_DIR} --arity 4')
    #print('Processing n-grams completed.')
    #print()

    #end_time = time.time()
    #print('Training time:', end_time - start_time)

    os.system(f'python3 {MULTI_GENERATE} --input {INPUT_FILE} --output {OUTPUT_FILE} --encoding utf-8')

pipeline()