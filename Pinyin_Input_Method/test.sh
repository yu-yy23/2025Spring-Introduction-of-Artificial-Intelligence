testcase='input.txt'
judgescript='test.py'

unzip xxxxxx.zip

cp -r sina_news_gbk corpus/

cp $testcase data/input.txt

pip install -r requirements.txt

python main.py <data/input.txt >data/output.txt

cp $judgescript ./judge.py

python judge.py