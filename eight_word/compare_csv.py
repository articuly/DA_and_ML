import csv

# 打开原始CSV文件1
with open('eight_word_23.csv', 'r', encoding='utf-8') as file1:
    csv_reader1 = csv.reader(file1)
    data1 = list(csv_reader1)

# 打开原始CSV文件2
with open('eight_word_new.csv', 'r', encoding='utf-8') as file2:
    csv_reader2 = csv.reader(file2)
    data2 = list(csv_reader2)

# 确保两个CSV文件行数相同
if len(data1) != len(data2):
    print("CSV文件行数不同，请检查文件")

# 创建一个新的CSV文件，用于保存差异数据
with open('diff.csv', 'w', newline='', encoding='utf-8') as file_diff:
    csv_writer_diff = csv.writer(file_diff)

    # 遍历两个CSV文件的每一行数据，对比是否完全一致
    for i in range(len(data1)):
        if data1[i] != data2[i]:
            # 如果数据不一致，则将差异写入新的CSV文件中
            csv_writer_diff.writerow(["第{}行".format(i + 1), data1[i], data2[i]])
