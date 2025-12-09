# 遇到的问题：

## 本质问题：
data-collection-guide.md与datasource-schema.json等文件存在冲突，目测是**data-collection-guide.md依然遵循旧标准**

## 1. 数据源类别划分不明确：
在对单个数据源进行获取时，如何确定其是属于哪一个类别，当前仅仅是让agent自行决定，可能会导致分类错误，json文件放置在错误的位置，更新错误的进度文件。（如获取学术研究中的NBER Data Library - 国家经济研究局时，agent误认为其属于international类别）

旧的json结构中保留了category字段，但新的字段定义中已经去掉该字段，改为通过文件路径来隐式表示类别。因此给agent指定任务的时候需要明确告诉其该数据源所属的类别，以确保其将数据源信息存放在正确的位置。

目前想到的解决方案：
- 提前在tasks中对数据源进行类别划分，并在使用skill获取数据源时明确传入类别信息。
- 在skill中增加对数据源类别的判断逻辑，考虑加入用户确认的干预指令。
## 2. 数据源评分标准：
目前发现整个项目目录中存在三个不同的数据源评分标准，具体见[评分标准对比](RATING_SYSTEM_ANALYSIS.md).

## 3. json字段定义不统一：
在对数据源进行获取时，发现不同的评分标准中对json字段的定义不统一，具体见[字段定义对比](SCHEMA_COMPARISON.md).

## 4. 是否要提前定义好数据源的url：
在tasks中，有一些数据源已经给出了明确的URL，此时直接使用web_search以及webfetch工具访问url即可；但大部分数据源尚未给出明确的url，对这些数据源进行爬取尝试时发现web_search以及webfetch工具往往会失效，需要使用playwright工具进行爬取。
因此需要考虑是否要在tasks中提前定义好数据源的url，还是只告诉agent数据源的名称和所属类别，让其自行搜索。
（是否单独写一个skill，让其根据task中的数据源自动获取url，并列举在tasks中）