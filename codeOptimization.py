"""
    中间代码优化
"""

print_str = []


# DAG 树节点
class Node:
    def __init__(self):
        self.val = []
        self.left, self.right = -1, -1
        self.op = ""

    left, right = -1, -1
    val = []
    op = ""


total = []
ans = [['' for i in range(200)] for j in range(200)]  # 用于存储优化后的中间代码
tree = [Node() for i in range(200)]  # DAG 树
st = [False for _ in range(200)]  # 判断节点是否多余
res = []  # 优化后算式
num = 0  # 记录DAG树节点的数量
expressions = []  # 存储原始表达式的列表


# DAG树的节点值列表中查找变量是否存在
def find_var(x, ch):
    for t in tree[x].val:
        if ch == t:
            return True
    return False


# 向DAG树中添加一个节点
def add_node(ch):
    global num
    for i in range(0, num):
        if ch == tree[i].op or find_var(i, ch):
            return i
    tree[num].op = ch
    num += 1
    return num


# 向DAG树中添加一个运算符节点
def add_operator(ch, op, left, right):
    global num
    for i in range(num - 1, -1, -1):
        if tree[i].op == op and tree[i].left == left and tree[i].right == right:
            tree[i].val.append(ch)
            return
    tree[num].val.append(ch)
    tree[num].op = op
    tree[num].left = left
    tree[num].right = right
    num += 1


# 深度优先搜索DAG树，标记多余的节点，排除叶子节点
def dfs(idx):
    if tree[idx].left != -1 and tree[idx].right != -1:
        st[idx] = True
        dfs(tree[idx].left)
        dfs(tree[idx].right)


# 在表达式中查找下一个赋值语句
def find(idx):
    for i in range(idx, len(total)):
        if total[i] == "=" and total[i + 2] in "+-*/":
            return i
    return -1


def get_message(idx):
    message = ""
    if idx != -1:
        message = "{}{}{}{}{}".format(total[idx - 1], total[idx], total[idx + 1], total[idx + 2], total[idx + 3])
    return message


# 代码优化
def optimization(tmp):
    global total, expressions, res
    total = tmp
    idx = 0
    # 表达式最左
    tmp_val = []
    print("*" * 50)
    print("优化以前:")
    print_str.append("优化以前:")
    while idx != -1:
        idx = find(idx + 1)
        if idx == -1:
            break
        temp = get_message(idx)
        print(temp.center(15))
        expressions.append(temp)
        add_operator(temp[0], temp[3], add_node(temp[2]), add_node(temp[4]))
        tmp_val.append(temp[0])
        print_str.append(temp)
    for i in range(0, num):  #
        if tree[i].left != -1 and tree[i].right != -1:  # 如果不是叶子节点，需要进行重构
            ans[i][0] = tree[i].val[0]
            ans[i][1] = "="
            ll = tree[tree[i].left]
            rr = tree[tree[i].right]
            ans[i][2] = ll.val[0] if len(ll.val) > 0 else ll.op
            ans[i][3] = tree[i].op
            ans[i][4] = rr.val[0] if len(rr.val) > 0 else rr.op

    for tmp in tmp_val:
        for i in range(num - 1, -1, -1):
            if ans[i][0] == tmp:
                dfs(i)
                break
    print("\n优化后:")
    print_str.append("优化后:")
    for i in range(num):
        if st[i]:
            str1 = "{}{}{}{}{}".format(ans[i][0], ans[i][1], ans[i][2], ans[i][3], ans[i][4])
            res.append(str1)
            print_str.append(str1)
            print(str1.center(15))
    if len(res) == 0:
        print("无法继续优化！")
        return expressions
    return res


def get_print():
    return print_str
