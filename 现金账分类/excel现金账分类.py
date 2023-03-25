# coding:utf-8
import re
import pandas as pd

# 输入输出路经
path = './26-31号收支.xlsx'
out_path = './26-31号收支_edited.xlsx'

# 读取文件
df = pd.read_excel(path, sheet_name=0, header=1, engine='openpyxl')

# 填充空值，设定初始值
df.fillna('', inplace=True)
df['租金'] = 0
df['管理费'] = 0
df['水费'] = 0
df['电费'] = 0
df['设备设施维护费'] = 0
df['停车费'] = 0
df['场地+球场+卫生费+杂费'] = 0
df['押金'] = 0
df['利息'] = 0
df.head()

# 处理收入项
for i, row in df.iterrows():
    c = row['摘要']
    if c != '合计' or c is not None:
        recv1 = re.findall(r'租金(\d+\.?\d*)', c)
        recv11 = re.search(r'租金', c)
        recv21 = re.search(r'收.*?月.*?欠款', c)
        recv91 = re.search(r'多交了(\d+\.?\d*)', c)
        if recv1:
            if len(recv1) > 1:
                rents = [float(r) for r in recv1]
                rent = sum(rents)
            else:
                rent = float(recv1[0])
            if recv91:
                rent = rent + float(recv91[0])
            df.loc[i, '租金'] = rent
        if not recv1 and (recv11 or recv21):
            rent = float(df.loc[i, '收'])
            if recv91:
                rent = rent + float(recv91[0])
            df.loc[i, '租金'] = rent

        recv2 = re.findall(r'管理费(\d+\.?\d*)', c)
        recv12 = re.search(r'管理费|收.*?应缴费用', c)
        if recv2:
            if len(recv2) > 1:
                admins = [float(a) for a in recv2]
                admin = sum(admins)
            else:
                admin = float(recv2[0])
            df.loc[i, '管理费'] = admin
        if not recv2 and recv12:
            admin = float(df.loc[i, '收'])
            df.loc[i, '管理费'] = admin

        recv3 = re.findall(r'收.*?水费(\d+\.?\d*)', c)
        recv13 = re.search(r'收.*?水费', c)
        if recv3:
            if len(recv3) > 1:
                waters = [float(w) for w in recv3]
                water = sum(waters)
            else:
                water = float(recv3[0])
            df.loc[i, '水费'] = water
        if not recv3 and recv13:
            water = float(df.loc[i, '收'])
            df.loc[i, '水费'] = water

        recv4 = re.findall(r'收.*?电费(\d+\.?\d*)', c)
        recv14 = re.search(r'收.*?电费', c)
        if recv4:
            if len(recv4):
                electrics = [float(e) for e in recv4]
                electric = sum(electrics)
            else:
                electric = float(recv4[0])
            df.loc[i, '电费'] = electric
        if not recv4 and recv14:
            electric = float(df.loc[i, '收'])
            df.loc[i, '电费'] = electric

        recv6 = re.search(r'停车费(\d+\.?\d*)', c)
        recv16 = re.search(r'月保停车费|收临保停车费', c)
        recv26 = re.search(r'收优惠停车券款', c)
        recv0 = re.search(r'手续费(\d+\.?\d*)', c)
        if recv6:
            fee = 0
            parking = float(recv6.group(1))
            if recv0:
                fee = float(recv0.group(1))
            df.loc[i, '停车费'] = parking - fee
        if not recv6 and (recv16 or recv26):
            parking = float(df.loc[i, '收'])
            df.loc[i, '停车费'] = parking

        recv5 = re.findall(r'设施维护\D?(\d+\.?\d*)', c)
        recv15 = re.search(r'设备设施维护费', c)
        if recv5:
            fee = 0
            if len(recv5):
                maintains = [float(m) for m in recv5]
                maintain = sum(maintains)
            else:
                maintain = float(recv5[0])
            if recv0:
                fee = float(recv0.group(1))
            if not recv6:
                df.loc[i, '设备设施维护费'] = maintain - fee
            else:
                df.loc[i, '设备设施维护费'] = maintain
        if not recv5 and recv15:
            maintain = float(df.loc[i, '收'])
            df.loc[i, '设备设施维护费'] = maintain

        recv7 = re.search(r'押金(\d+\.?\d*)', c)
        recv17 = re.search(r'押金|保证金|仓库款', c)
        recv27 = re.search(r'保证金(\d+\.?\d*)|保证金差额(\d+\.?\d*)', c)
        recv37 = re.search(r'水电周转金(\d+\.?\d*)', c)
        if recv7:
            guarantee = float(recv7.group(1))
            df.loc[i, '押金'] = guarantee
        if recv27:
            guarantee = float(recv27.group(1))
            df.loc[i, '押金'] = guarantee
        if recv37:
            guarantee = float(recv37.group(1))
            df.loc[i, '押金'] = guarantee
        if not (recv7 or recv27 or recv37) and recv17:
            guarantee = df.loc[i, '收']
            df.loc[i, '押金'] = guarantee

        recv8 = re.search(r'利息(\d+\.?\d*)', c)
        recv18 = re.search(r'利息|收结息', c)
        if recv8:
            interest = float(recv8.group(1))
            df.loc[i, '利息'] = interest
        if not recv8 and recv18:
            maintain = float(df.loc[i, '收'])
            df.loc[i, '利息'] = maintain

        recv9 = re.search(r'场使用费(\d+\.?\d*)', c)
        recv19 = re.search(r'场地借用费(\d+\.?\d*)', c)
        recv29 = re.search(r'场地使用费|场使用费|场地借用费|稳岗返还款|产业发展专项资金|收社保退费', c)
        if recv9:
            space = float(recv9.group(1))
            df.loc[i, '场地+球场+卫生费+杂费'] = space
        if recv19:
            space = float(recv19.group(1))
            df.loc[i, '场地+球场+卫生费+杂费'] = space
        if not (recv9 or recv19) and recv29:
            space = float(df.loc[i, '收'])
            df.loc[i, '场地+球场+卫生费+杂费'] = space

# 处理支出项
for i, row in df.iterrows():
    c = row['摘要']
    if c != '合计' or c is not None:
        pay1 = re.search(r'电信费|汇划费|服务费|快递费|办公用品费|付工艺品款', c)
        pay11 = re.search(r'报销款|借支备用金', c)
        if pay1 or pay11:
            operation = float(df.loc[i, '支'])
            df.loc[i, '运营费'] = operation

        pay2 = re.search(r'工程款|工程费用|工程费', c)
        if pay2:
            project = float(df.loc[i, '支'])
            df.loc[i, '工程费'] = project

        pay3 = re.search(r'制作费|设计费|点心款|茶歇款', c)
        if pay3:
            marketing = float(df.loc[i, '支'])
            df.loc[i, '营销费'] = marketing

        pay4 = re.search(r'个人所得税|印花税|教育附加|增值税|城市维护建设税', c)
        if pay4:
            tax = float(df.loc[i, '支'])
            df.loc[i, '税费'] = tax

        pay5 = re.search(r'付.*?水费(\d+\.?\d*)', c)
        if pay5:
            try:
                water2 = float(pay5.group(1))
                df.loc[i, '水费.1'] = water2
            except Exception:
                print(f'水费：{pay5}')

        pay6 = re.search(r'付.*?电费(\d+\.?\d*)', c)
        if pay6:
            try:
                electric2 = float(pay6.group(1))
                df.loc[i, '电费.1'] = electric2
            except Exception:
                print(f'电费：{pay6}')

        pay7 = re.search(r'退保证金|退水电周转金|退.*?保证金', c)
        if pay7:
            refund = float(df.loc[i, '支'])
            df.loc[i, '退款'] = refund

# 格式化：替换0值，忽略错误，时间显示，列名
df.replace(0, '', inplace=True)
df['日期'] = pd.to_datetime(df['日期'], errors='coerce').dt.strftime('%Y/%#m/%#d')
df.rename(columns={'Unnamed: 5': ''}, inplace=True)

# 保存输出文件
df.to_excel(out_path, 'sheet1', index=False, startrow=1)

# 计算收支分类项的平衡，需要重新读取
df = pd.read_excel(out_path, sheet_name=0, header=1, engine='openpyxl')
df['收支分类'] = df.iloc[:, 6:25].sum(axis=1)
df['收支小计'] = df[['收', '支']].sum(axis=1)

# 保留两位小数再比较
df.round({'收支分类': 2, '收支小计': 2})
df['平衡'] = df.apply(lambda x: '是' if abs(x['收支分类'] - x['收支小计']) < 0.01 else '否', axis=1)

# 再次保存
imbalance = df['平衡'].str.count('否').sum()
df.to_excel(out_path, 'sheet1', index=False, startrow=1)
print(f'已经生成分类完成的Excel文件{out_path}，其中有{imbalance}处不平衡，请检查')