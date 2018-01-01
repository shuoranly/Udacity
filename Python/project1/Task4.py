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
任务4:
电话公司希望辨认出可能正在用于进行电话推销的电话号码。
找出所有可能的电话推销员:
这样的电话总是向其他人拨出电话，
但从来不发短信、接收短信或是收到来电


请输出如下内容
"These numbers could be telemarketers: "
<list of numbers>
电话号码不能重复，每行打印一条，按字母顺序输出。
"""

#sum_num_dict include never text, receive text messages or receive calls
sum_num_dict = {}
#get sum_num_dict from calls
for per_call in calls:
    sum_num_dict[per_call[1]] = sum_num_dict.get(per_call[1], 0) + 1
#get sum_num_dict from texts
for per_text in texts:
    sum_num_dict[per_text[1]] = sum_num_dict.get(per_text[1], 0) + 1

#call_dict include num which make a call
call_dict = {}
for per_rec in calls:
    call_dict[per_rec[0]] = call_dict.get(per_rec[0], 0) + 1

#Sort the call_dict
sort_dict = sorted(call_dict.items(), key=lambda d:d[0])

#Get the number that meets the requirements and print it
print("These numbers could be telemarketers: ")
for sort_num in sort_dict:
    if sort_num[0] not in sum_num_dict:
        print(sort_num[0])
    
    
