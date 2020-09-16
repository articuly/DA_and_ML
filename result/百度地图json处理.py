# coding:utf-8
with open('bank-2020-09-15.txt', 'r', encoding='utf-8') as f:
    lst = []
    for l in f.readlines():
        line = eval(l)
        name = line['name']
        lat = line['location']['lat']
        lng = line['location']['lng']
        address = line['address'].replace(',', '、')
        province = line['province']
        city = line['city']
        area = line['area']
        tag = line['detail_info']['tag']
        lst.append([name, lat, lng, province, city, area, address, tag])

# print(lst)

with open('bank-2020-09-15.csv', 'w', encoding='utf-8') as c:
    c.write('name, lat, lng, province, city, area, address, tag\n')
    for i in lst:
        c.write(str(i)[1:-1])
        c.write('\n')

print('处理完毕！')
