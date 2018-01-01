"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
任务1：
短信和通话记录中一共有多少电话号码？每个号码只统计一次。
输出信息：
"There are <count> different telephone numbers in the records."
"""

#Sum records of texts and calls
records = texts        #Prevent the destruction of raw data
records.extend(calls)

#Different telephone numbers counts dict of records
counts_dict = {}

#Count the number of times each number appears
for per_rec in records:
    for per_num in per_rec[:2]:
        counts_dict[per_num] = counts_dict.get(per_num, 0) + 1

#Different telephone numbers counts of records
counts = len(counts_dict)

#"There are <count> different telephone numbers in the records."
print("There are {} different telephone numbers in the records.".format(counts))