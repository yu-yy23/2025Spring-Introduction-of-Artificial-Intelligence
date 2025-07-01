# 使用说明

## 环境配置

本代码包基于`python3.11.11`，安装`requirements.txt`中的依赖即可运行。

## 运行方式

在`/Code/`目录下使用`python3 main.py --model [model name] --learning_rate [learning rate] --batch_size [batch size] --num_epochs [epoch numbers]`即可进行模型训练，其中`--model`参数为必须项，可选择的模型有`cnn`, `lstm`, `gru`, `mlp`, `bert`，其余参数为可选项，可以用于提供训练超参数。

示例：命令`python3 main.py --model cnn --learning_rate 0.001 --batch_size 64 --num_epochs 10`可启动一次CNN模型的训练，学习率为0.001，批次大小为64，迭代次数为10。

## 项目结构

`/Code/`**目录用于存放所有代码：**
- `main.py`用于接收启动命令和训练参数，启动模型训练过程；
- `models.py`提供所有模型的实现；
- `dataset.py`实现用于加载文本情感分类数据的`TextDataset`数据集；
- `utils.py`提供数据加载和处理相关的工具函数；
- `train.py`包含模型训练的主要逻辑，用于完成训练过程并保存模型，其中使用wandb的部分在提交时已被注释掉；
- `config.py`包含模型配置、路径配置、训练超参数，其中与wandb有关的参数在提交时已被隐去。

`/Models/`**目录用于存放训练好的模型**，其中已有本次试验训练的所有模型的最终版本（固定迭代次数训练完成后保存的版本）

`/Dataset/`**目录用于存放数据集和预训练词向量**，其中包含本次实验提供的数据集和预训练词向量。

运行时请务必保证以上提到的目录**存在**且其中含有应该含有的文件，若要修改数据/模型存放位置，请修改`/Code/config.py`中`path`类中的文件路径。
