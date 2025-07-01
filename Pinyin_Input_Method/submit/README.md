# 使用说明

**于越洋**

## 项目架构

```shell
corpus/                     // 用于存放原始训练语料
data/
    answer.txt              // 下发的标准答案
    input.txt               // 下发的测试输入
    output.txt              // 程序的输出
    拼音汉字表.txt            // 下发的拼音汉字表
    一二级汉字表.txt          // 下发的一二级汉字表
src/
    settings.py             // 常量定义，各文件路径定义
    coding_transform.py     // 将下发文件和训练语料的编码从gbk转为utf-8
    preprocess.py           // 数据预处理，获得语料分词计数
    process.py              // 数据处理，获得n元词概率表
    binary_generate.py      // 使用二元模型生成语句
    binary_pipeline.py      // 二元模型作业流水线
    multi_generate.py       // 使用多元模型生成语句
    multi_pipeline.py       // 多元模型作业流水线
model/
    corpus_utf8/            // 转换编码后的训练语料
    frequency_counter/      // 分词计数
    probability/            // n元词概率表
main.py                     // 主程序入口
README.md                   // 使用说明
requirements.txt            // 依赖库
```

## 二元模型

要运行二元模型，保留`main.py`中的第6行，将第7行注释，在根目录下运行`main.py`即可。

## 多元模型

要运行多元模型，保留`main.py`中的第7行，将第6行注释，在根目录下运行`main.py`即可。
