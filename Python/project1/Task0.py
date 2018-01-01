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
任务0:
短信记录的第一条记录是什么？通话记录最后一条记录是什么？
输出信息:
"First record of texts, <incoming number> texts <answering number> at time <time>"
"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"
"""

#Incoming number of first record of texts
texts_in_num_f = texts[0][0]

#Answering number of first record of texts
texts_ans_num_f = texts[0][1]

#Time of first record of texts
texts_time_f = texts[0][2]

#Incoming number of last record of calls
calls_in_num_f = calls[-1][0]

#Answering number of last record of calls
calls_ans_num_f = calls[-1][1]

#Time of last record of calls
calls_time_f = calls[-1][2]

#Lasting seconds of last record of calls
calls_last_sec_f = calls[-1][3]

#"First record of texts, <incoming number> texts <answering number> at time <time>"
print("First record of texts, {} texts {} at time {}".format(texts_in_num_f, texts_ans_num_f, texts_time_f))

#"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"
print("Last record of calls, {} calls {} at time {}, lasting {} seconds".format(calls_in_num_f, calls_ans_num_f, calls_time_f, calls_last_sec_f))
