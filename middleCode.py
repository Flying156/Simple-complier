"""
    中间代码生成
"""
res = []  # 生成结果
total = []  # 存储输入的程序
print_str = []  # 存储打印信息


#  在程序字符串中查找下一个运算符的位置
def find(idx):
    for i in range(idx, len(total)):
        if total[i] in "=+-*/":
            return i
    return -1


# 中间代码生成
def generate_code(tmp):
    global total
    tt, index, cnt, idx = 0, 0, 0, 1

    total = tmp
    while index < len(total) or index != -1:
        index = find(index + 1)
        if index == -1:
            break
        # 处理赋值语句
        if total[index] == "=" and total[index + 2] not in "+-*/":
            res.append(total[index - 1])
            res.append(total[index + 1])
            print("{}(=,{},_,{})".format(idx, res[cnt + 1], res[cnt]))
            print_str.append("{}(=,{},_,{})".format(idx, res[cnt + 1], res[cnt]))
            cnt += 1
            res.pop()
            res.pop()
            res.append(total[index - 1])
            idx += 1
        # 处理四则运算
        elif total[index] in "+-*/":
            print("{}({},{},{},T{})".format(idx, total[index], total[index - 1], total[index + 1], tt))
            print_str.append("{}({},{},{},T{})".format(idx, total[index], total[index - 1], total[index + 1], tt))
            print("{}(=,T{},_,{})".format(idx + 1, tt, total[index - 3]))
            print_str.append("{}(=,T{},_,{})".format(idx + 1, tt, total[index - 3]))
            idx += 2
            tt += 1

def get_print():
    return print_str
