""""
    语法分析
"""
# 产生式
analyse = {"right": [], "left": []}
# 终结符
terSymList = []
suTerSymList = []  # 不含 $
# 非终结符
nonTerList = []
# first, follow 集
firstDict = {}
followDict = {}
leftList = []  # 产生式左部list
rightList = []  # 产生式右部list
llTableList = []  # LL1 分析表
procedureStr = ""  # 源程序
analyseStack = []  # 分析栈
isError = False
print_str = []


# 读取文法中的非终结符，终结符，进行分类
def get_grammar():
    global analyse, nonTerList, suTerSymList, terSymList
    for line in open("Grammar.txt"):
        line = line.strip('\n')
        analyse['left'].append(line[0])  # 文法左侧
        analyse['right'].append(line[3:])  # 文法右侧

        if line[0] not in nonTerList:
            nonTerList.append(line[0])
        for single in line[3:]:  # 非终结符
            if not ('A' <= single <= "Z"):
                if single not in terSymList:
                    terSymList.append(single)
                    if single != '$':
                        suTerSymList.append(single)
    terSymList.append('#')
    suTerSymList.append('#')


# 求 First 集合
def get_firstDict(nonTer):
    cnt, flag = 0, 0
    for (left, right) in zip(leftList, rightList):
        if nonTer == left:  # 当前的非终结符与当前推导式匹配
            if left not in firstDict:
                firstDict[nonTer] = set()  # 建立 first 集合
            if right[0] in terSymList:  # 如果是终结符，直接加入
                firstDict[nonTer].add(right[0])
            else:
                for signal_right in right:
                    if signal_right in terSymList:  # 是终结符结束
                        firstDict[nonTer].add(signal_right)
                        break
                    get_firstDict(signal_right)
                    for ch in firstDict[signal_right]:
                        if ch == '$':
                            flag = 1
                        else:
                            firstDict[nonTer].add(ch)
                    if flag == 0:  # 当前元素不存在 $, 直接结束
                        break
                    else:
                        cnt += 1
                        flag = 0
                    break
                if cnt == len(right):
                    firstDict[nonTer].add('$')  # 当前右部所有 first(x) 都有 $, 加入 $


def get_followDict(nonTer):
    for (left, right) in zip(leftList, rightList):
        pos, rightLen = -1, len(right)
        for idx, single_right in enumerate(right):
            if single_right == nonTer:
                pos = idx
                if nonTer not in followDict:
                    followDict[nonTer] = set()
                break
        if pos != -1 and pos < rightLen - 1:  # 非终结符在右侧且不为最后一个
            nxt = right[pos + 1]
            if nxt in terSymList:  # 终结符直接加入
                followDict[nonTer].add(nxt)
            else:
                flag = 0  # first 集中是否有 $
                for ch in firstDict[nxt]:
                    if ch != '$':
                        followDict[nonTer].add(ch)
                    else:
                        flag = 1
                if flag == 1 and left != nonTer:  # follow(left) 加入 follow(right) 中
                    get_followDict(left)
                    for ch in followDict[left]:
                        followDict[nonTer].add(ch)
        elif pos != -1 and pos == rightLen - 1 and left != nonTer:
            get_followDict(left)
            for ch in followDict[left]:
                followDict[nonTer].add(ch)


# LL1 分析表
def get_table():
    global llTableList
    tableList = [["Empty" for i in range(len(suTerSymList))] for _ in range(len(nonTerList))]

    for (left, right) in zip(leftList, rightList):
        if right[0] in terSymList:  # 终结符，处理
            if right[0] != '$':
                # 非空终结符，将产生式右部添加到分析表对应位置
                tableList[nonTerList.index(left)][suTerSymList.index(right[0])] = right
            if right[0] == '$':
                # 对于产生式右部为空的情况，将 follow 集合中的终结符添加到对应位置
                for follow in followDict[left]:
                    tableList[nonTerList.index(left)][suTerSymList.index(follow)] = right
        else:  # 非终结符
            # 将产生式右部 first 集合中的终结符添加到对应位置
            for first in firstDict[right[0]]:
                tableList[nonTerList.index(left)][suTerSymList.index(first)] = right
                # 对于产生式右部包含空串的情况，将 follow 集合中的终结符添加到对应位置
            if '$' in firstDict[right[0]]:
                for follow in followDict[left]:
                    tableList[nonTerList.index(left)][suTerSymList.index(follow)] = right
    llTableList = tableList


def analysis():
    global analyseStack, procedureStr, isError
    sentence = procedureStr[::-1]  # 字符逆序分析
    analyseStack.append('#')
    analyseStack.append(nonTerList[0])
    print("LL(1)文法分析过程：\n" + "分析栈".center(30) + "剩余输入串".center(120) + "推导式".center(30))
    print_str.append("LL(1)文法分析过程：\n" + "分析栈".center(30) + "剩余输入串".center(120) + "推导式".center(30) + "\n")
    while len(sentence) > 0:
        out = ""
        # 将分析栈中的符号放入字符串，方便打印
        for ch in analyseStack:
            out += ch
        print(out.center(30), end="")
        tmp_str = ""
        tmp_str += out.center(30)

        out = sentence[::-1]
        print(out.center(120), end="")
        tmp_str += out.center(120)

        ch1 = analyseStack[len(analyseStack) - 1]
        ch2 = sentence[len(sentence) - 1]
        # 分析成功，接受文法
        if ch1 == ch2 and ch1 == '#':
            print("接受语法".center(40))
            print_str.append(tmp_str+"接受语法".center(40)+"\n")
            return
        # 符号匹配，弹出分析栈和输入层的符号
        if ch1 == ch2:
            analyseStack.pop()
            sentence = sentence[:-1]
            print("匹配".center(40))
            print_str.append(tmp_str+"匹配".center(40)+"\n")
        # 根据 LL(1) 分析表执行推到
        elif llTableList[nonTerList.index(ch1)][suTerSymList.index(ch2)] != "Empty":
            str1 = llTableList[nonTerList.index(ch1)][suTerSymList.index(ch2)]
            analyseStack.pop()
            if str1 != '$':
                tmp = str1[::-1]
                for ch in tmp:
                    analyseStack.append(ch)
            print(str1.center(40))
            print_str.append(tmp_str+str1.center(40)+"\n")
        else:
            print("错误".center(40)+"\n")
            print_str.append(tmp_str+"错误".center(40))
            isError = True
            return


def code_grammar(tmp):
    global rightList, leftList, llTableList, procedureStr
    step = 0
    procedureStr = tmp
    procedureStr += '#'

    get_grammar()
    print(analyse)
    print("非终结符".center(10) + f"{nonTerList}".center(200))
    print("终结符".center(10) + f"{terSymList}".center(200))
    print(f"终结符(不含$)".center(10) + f"{suTerSymList}".center(200))
    rightList, leftList = analyse["right"], analyse["left"]
    # 求 FIRST 集合
    print("非终结符".center(10) + "first集合".center(43))
    for nonTer in nonTerList:
        get_firstDict(nonTer)
        print(f"{nonTer}".center(10) + f"{firstDict[nonTer]}".center(50))
    print("非终结符".center(10) + "follow集合".center(43))
    for nonTer in nonTerList:
        if step == 0:
            followDict[nonTer] = set()
            followDict[nonTer].add("#")
            step += 1
        get_followDict(nonTer)
        print(f"{nonTer}".center(10) + f"{followDict[nonTer]}".center(50))
    get_table()
    for col, row in zip(nonTerList, llTableList):
        print(f"{col}:", end="")
        for elem in row:
            print(elem.center(12), end="")
        print("")
    analysis()  # 递归下降分析
    return isError


def get_print():
    return print_str
