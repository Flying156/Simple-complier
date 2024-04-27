total = []
# 寄存器数量
registerNum = 2
# 当前寄存器存储的变量
register = ['' for i in range(registerNum)]
# 寄存器使用的数量
top = 0
res = []


# 得到当前变量的寄存器位置
def get(ch):
    for i in range(registerNum):
        if ch == register[i]:
            return i
    return -1


# 判断哪个变量最晚使用
def use(x, ch):
    for i in range(x, len(total)):
        if ch == total[i][2] or ch == total[i][4]:
            return i
    return len(total)


# 分配寄存器
def find(x):
    global top
    if top < registerNum:
        top += 1
        return top - 1
    ans, t = -1, -1
    for i in range(registerNum): # 比较哪个变量最晚使用
        pos = use(x, register[i])
        if pos > t:
            t = pos
            ans = i
    return ans


def code_generation(tmp):
    global total, res
    total = tmp
    for i in range(len(total)):
        pos = get(total[i][2])
        if pos == -1:  # 当前的变量没有占用任何寄存器
            pos = find(i) # 查找寄存器
            if pos < len(register) and use(pos, register[pos]) < len(total):  # 如果当前的寄存器合法
                print(f"ST R{pos}, {register[pos]}")
                res.append(f"ST R{pos}, {register[pos]}")
                register[pos] = ''
            print(f"LD R{pos}, {total[i][2]}")
            res.append(f"LD R{pos}, {total[i][2]}")
        op = total[i][3]
        tmp = ""
        if op == '+':
            tmp += "ADD"
        elif op == "*":
            tmp += "MUL"
        elif op == "/":
            tmp += "DIV"
        elif op == "-":
            tmp += "SUB"
        tmp += f" R{pos}, "
        g = get(total[i][4]) # 判断变量是否在寄存器中
        if g == -1:
            tmp += total[i][4]
        else:
            tmp += f"R{g}"
        res.append(tmp)
        print(tmp)
        register[pos] = total[i][0]
    return res
