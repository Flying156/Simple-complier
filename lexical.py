""""
    词法分析
"""
# 标识符
flagWordList = [chr(i) for i in range(97, 101)]
# 常数
constantWordList = [chr(i) for i in range(48, 57)]
# 关键词
keyWordList = ["while", "if", "else", "return", "void", "main", "printf", "int", "scanf", "for"]

# 运算符
operatorWordList = ["+", "-", "*", "/", "=", ">", "<", "==", "!="]

# 界符
delimiterWordList = [";", "{", "}", "(", ")"]
total = []

print_str = []


# 处理注释
def process_sentence(sentence):
    if sentence == "":
        return
    total.append(sentence)


# 不处理消除注释
def preProcess(line):
    if line.find("//") != -1:
        return False
    elif line.find("/*") != -1:
        return False
    return True


# 对每一行进行处理
def process_line(line):
    a = ""
    i = 0
    if not preProcess(line): # 如果该行是注释，不处理
        return
    while i < len(line):
        c = line[i]
        if c in "+-*/<>!=":  # 如果当前是运算符
            process_sentence(a)  # 打印字符
            a = ""
            if i + 1 < len(line) and line[i + 1] == '=':  # 判断是否有 == 或 !=
                total.append(f"{line[i]}=")
                i += 1
            else:
                total.append(c)
        elif c in "(){},;":  # 如果当前是界符
            process_sentence(a)
            a = ""
            total.append(c)  # 加入到元组中，方便后续处理
        else:
            a += c
        i += 1
    process_sentence(a)


# 词法分析
def lexical_analysis(lines):
    tmp = lines.split("\n")  # 处理读入的字符串，方便后续分析
    for t in tmp:
        for line in t.split(" "):
            process_line(line)
    print(total)
    print("*" * 50 + "\n" + "词法分析结果：" + "\n")  # 按类型打印
    print("字符".center(10) + "属性 ".center(10))
    print_str.append("词法分析结果：\n" + "字符".center(10) + "属性 ".center(10))
    for single in total:
        if single in keyWordList:
            print(single.center(10) + "关键字".center(10))
            print_str.append(single.center(10) + "关键字".center(10))
        elif single in flagWordList:
            print(single.center(10) + "标识符".center(10))
            print_str.append(single.center(10) + "标识符".center(10))
        elif single in constantWordList:
            print(single.center(10) + "常数  ".center(10))
            print_str.append(single.center(10) + "常数  ".center(10))
        elif single in operatorWordList:
            print(single.center(10) + "运算符".center(10))
            print_str.append(single.center(10) + "运算符".center(10))
        elif single in delimiterWordList:
            print(single.center(10) + "界符  ".center(10))
            print_str.append(single.center(10) + "界符  ".center(10))
    print("*" * 50)
    return total

def get_print():
    return print_str
