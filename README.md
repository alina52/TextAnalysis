# README

## 项目简介

文本情感分析基于已有的情感词典或情感知识库，对文本中带有情感或极性的词( 或词语单元) 进行加权求和，而后者主要是对文本提取具有类别表征意义的 特征， 再基于这些特征使用机器学习算法进行分类。
本项目运用情感词典与机器学习两种方法分别进行文本情感分析，并提供结果对比。

### 环境准备

- Windows/MacOS/Linux
- Python3.6
- PyCharm or other IDEs

### 导入项目
Open the file named"text-anlysis" with IDE

### 数据来源

数字代表读取的字典
1: "dict_zhiwang", 2: "dict_tsinghua", 3: "dict_ntusd", 4: "dict_extreme"

分析数据
textAnalysis/input/input.txt

### 运行项目
数字代表选取字典
python3 main.py [optional] 1
