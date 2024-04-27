import lexical
import middleCode
import grammatical
import codeOptimization
from tkinter import *
from tkinter import filedialog
import targetGeneration

produce_str = "" # 用于语法分析程序串
text_str = "" # 文件中的数据
total = []  # 词法分析得到的字符表
expressions = [] # 中间代码优化后的运算式
# 文法对应关键字字典
keyWordDict = {"while": "t", "if": "w", "else": "u", "return": "s", "void": "z",
               "main": "y", "printf": "r", "int": "x",
               "scanf": "f"}



class GUI:
    def __init__(self, root):
        self.initGUI(root)

    def show_msg(self):
        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            self.result_text.insert(INSERT, content)
            self.result_text.see(END)

        self.root.after(100, self.show_msg)

    # 初始化界面
    def initGUI(self, root):
        global text_str
        self.root = root
        self.root.title("简单编译系统")
        self.root.geometry("1280x960")
        self.root.resizeable = False

        self.display_label = Label(root, text="词法分析结果", width=12, height=5, font=("黑体", 10))
        self.display_label.place(x=410, y=380)

        self.display_label = Label(root, text="语法分析结果", width=12, height=5, font=("黑体", 10))
        self.display_label.place(x=550, y=865)

        self.display_label = Label(root, text="中间代码生成", width=12, height=5, font=("黑体", 10))
        self.display_label.place(x=760, y=380)

        self.display_label = Label(root, text="中间代码优化", width=12, height=5, font=("黑体", 10))
        self.display_label.place(x=1110, y=170)

        self.display_label = Label(root, text="目标代码生成", width=12, height=5, font=("黑体", 10))
        self.display_label.place(x=1110, y=400)
        # 按钮区域
        self.file_button = Button(root, text="导入文件", command=self.read_file)
        self.file_button.place(x=10, y=400)

        self.lexical_button = Button(root, text="词法分析", command=lambda: self.run_lexical(text_str))
        self.lexical_button.place(x=120, y=400)

        self.grammatical_button = Button(root, text="语法分析", command=lambda: self.run_grammatical(produce_str))
        self.grammatical_button.place(x=10, y=450)

        self.middle_button = Button(root, text="中间代码生成", command=lambda: self.run_middleCode(total))
        self.middle_button.place(x=120, y=450)

        self.optim_button = Button(root, text="中间代码优化", command=lambda: self.run_codeOptim(total))
        self.optim_button.place(x=10, y=500)

        self.target_button = Button(root, text="目标代码生成", command=lambda: self.run_target(expressions))
        self.target_button.place(x=120, y=500)
        # 文本框区域
        self.file_text = Text(root, width=30, height=30, undo=True)
        self.file_text.place(x=0, y=0)

        self.lexical_text = Text(root, width=30, height=30, undo=True)
        self.lexical_text.place(x=350, y=0)

        self.grammatical_text = Text(root, width=300, height=25, undo=True)
        self.grammatical_text.place(x=0, y=550)

        self.middle_text = Text(root, width=30, height=30, undo=True)
        self.middle_text.place(x=700, y=0)

        self.optim_text = Text(root, width=30, height=13, undo=True)
        self.optim_text.place(x=1050, y=0)

        self.target_text = Text(root, width=30, height=13, undo=True)
        self.target_text.place(x=1050, y=240)

        root.mainloop()
    # 目标代码生成
    def run_target(self, expression):
        print('*' * 50)
        print("目标代码生成:")
        sentence = targetGeneration.code_generation(expression)
        for tmp in sentence:
            self.target_text.insert(INSERT, tmp + "\n")

    # 中间代码生成
    def run_middleCode(self, total):
        print('*' * 50)
        print("中间代码生成:")
        middleCode.generate_code(total)
        for tmp in middleCode.get_print():
            self.middle_text.insert(INSERT, tmp + "\n")


    # 中间代码优化
    def run_codeOptim(self, total):
        global expressions
        print('*'*50)
        print("中间代码优化:")
        expressions = codeOptimization.optimization(total)
        for tmp in codeOptimization.get_print():
            self.optim_text.insert(INSERT, tmp +"\n")
    # 读取文件
    def read_file(self):
        global text_str
        filename = filedialog.askopenfilename(title='导入文件', filetypes=[('c', '*.c')])
        with open(filename) as file:
            text_str = file.read()
        file.close()
        self.file_text.insert(INSERT, text_str)

    # 词法分析
    def run_lexical(self, text_str):
        global produce_str, total
        total = lexical.lexical_analysis(text_str)
        print(total)
        procedureStr = ""
        for single in total:
            if single in keyWordDict:
                procedureStr += keyWordDict[single]
            else:
                procedureStr += single
        print(procedureStr)
        produce_str = procedureStr
        for tmp in lexical.get_print():
            self.lexical_text.insert(INSERT, tmp + "\n")
    # 语法分析
    def run_grammatical(self, str):
        print('*' * 50)
        print("语法分析:")
        grammatical.code_grammar(str)
        for tmp in grammatical.get_print():
            self.grammatical_text.insert(INSERT, tmp)


# 开始运行
if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
