"""
Author: Fang Shihao, An Xin
version: 1.7
Date: 2024-6-2
"""
import tkinter as tk  # 导入 tkinter 模块，用于创建图形用户界面
from tkinter import filedialog, messagebox  # 从 tkinter 模块导入文件对话框和消息框
import networkx as nx  # 导入 networkx 模块，用于创建和操作复杂网络
import matplotlib.pyplot as plt  # 导入 matplotlib 模块，用于绘制图形
from collections import Counter, defaultdict  # 从 collections 模块导入 Counter 类和 defaultdict 类
import re  # 导入正则表达式模块
import random  # 导入随机模块
from string import punctuation  # 导入 string 模块中的标点符号
import msvcrt  # 导入 msvcrt 模块，用于检测键盘输入
from random import randint  # 从 random 模块导入 randint 函数
import time  # 导入时间模块
import threading

# 定义全局变量，用于存储有向图
MyGraph = defaultdict(list)  # 使用 defaultdict 创建一个字典，值为列表
graph = nx.DiGraph()  # 创建一个有向图对象

# 定义随机游走结束标志
randomWalkStopFlag = 0

# 定义函数，用于加载文件并处理
def load_file():
    file_path = filedialog.askopenfilename()  # 打开文件选择对话框，让用户选择文件
    file_entry.delete(0, tk.END)  # 清空文件路径输入框
    file_entry.insert(0, file_path)  # 将选择的文件路径插入到输入框中
    process_file(file_path)  # 调用 process_file 函数处理文件内容

# 定义函数，用于处理文件内容并生成有向图
def process_file(file_path):
    global graph  # 声明使用全局变量 graph
    with open(file_path, 'r', encoding='utf-8') as f:  # 打开文件，指定编码为 utf-8
        l = f.readline().lower()  # 读取文件的第一行
        transtab = str.maketrans(punctuation, ' ' * len(punctuation))  # 创建翻译表，将标点符号替换为空格
        Pre = ''  # 初始化前一个单词为空字符串
        while l != '':  # 循环读取文件的每一行，直到文件结束
            l = l.translate(transtab)  # 将当前行的标点符号替换为空格
            l = l.split()  # 将当前行按空格分割成单词列表
            for i in l:  # 遍历单词列表中的每个单词
                if MyGraph[i]:  # 如果单词已在图中
                    pass
                if Pre != '':  # 如果前一个单词不为空
                    MyGraph[Pre].append(i)  # 将当前单词添加到前一个单词的邻接列表中
                Pre = i  # 更新前一个单词为当前单词
            l = f.readline().lower()  # 读取文件的下一行
        for i in MyGraph.keys():  # 遍历图中的每个节点
            MyGraph[i] = dict(Counter(MyGraph[i]))  # 统计每个节点的邻接节点的出现次数
        VisSet = set()  # 创建一个空集合，用于记录访问过的节点
        for i in MyGraph.keys():  # 遍历图中的每个节点
            VisiteNode(i, VisSet)  # 调用 VisiteNode 函数访问节点及其邻接节点

# 定义函数，用于访问节点及其邻接节点，并在图中添加边
def VisiteNode(node, vis_set):
    Stack = [node]  # 初始化栈，存储待访问的节点
    while Stack:  # 当栈不为空时
        m = Stack.pop()  # 弹出栈顶节点
        w = MyGraph[m].keys()  # 获取该节点的邻接节点
        for i in w:  # 遍历邻接节点
            graph.add_edge(m, i, weight=MyGraph[m][i])  # 在图中添加边，并设置权重为邻接节点的出现次数
            if i not in vis_set:  # 如果邻接节点未被访问过
                vis_set.add(i)  # 将邻接节点加入已访问集合
                Stack.append(i)  # 将邻接节点压入栈中

# 定义函数，用于显示生成的有向图
def show_graph():
    pos = nx.spring_layout(graph)  # 计算图的布局
    nx.draw(graph, pos, with_labels=True, node_color='orange', node_size=700, font_size=10)  # 绘制图形
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()  # 显示图形

# 定义函数，用于保存生成的有向图到指定路径
def save_graph():
    save_path = path_entry.get()  # 获取保存路径
    pos = nx.spring_layout(graph)  # 计算图布局
    nx.draw(graph, pos, with_labels=True, node_color='orange', node_size=700, font_size=10)  # 绘制图形
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.savefig(save_path)  # 保存图形到指定路径
    plt.close()  # 关闭图形窗口

# 定义函数，用于查询桥接词，并显示查询结果
def query_bridge_words():
    word1 = word1_bridge_entry.get().lower()  # 获取输入的第一个单词
    word2 = word2_bridge_entry.get().lower()  # 获取输入的第二个单词
    Bridge = []  # 初始化桥接词列表
    if word1 not in MyGraph.keys() or word2 not in MyGraph.keys():  # 如果输入单词不在图中
        word1 = '\"' + word1 + '\"'
        word2 = '\"' + word2 + '\"'
        result = "No " + word1 + " or " + word2 + " in the graph!"
    else:
        for i in MyGraph[word1].keys():  # 遍历第一个单词的邻接节点
            if MyGraph[i].get(word2) is not None:  # 如果邻接节点与第二个单词有边
                Bridge.append('\"' + i + '\"')  # 将邻接节点加入桥接词列表
        word1 = '\"' + word1 + '\"'
        word2 = '\"' + word2 + '\"'
        if Bridge:  # 如果找到桥接词
            result = "The bridge words from " + word1 + " to " + word2 + " are: " + ','.join(Bridge)
        else:  # 如果未找到桥接词
            result = "No bridge words from " + word1 + " to " + word2 + "!"
    messagebox.showinfo("Bridge Words", result)  # 显示结果

# 定义函数，用于根据桥接词生成新文本，并显示生成结果
def generate_new_text():
    t = new_text_entry.get().lower()  # 获取输入的新文本
    t = re.findall(r'\b\w+\b', t)  # 使用正则表达式提取所有单词
    sp = dict()  # 初始化字典，用于存储已查找的桥接词
    ans = []  # 初始化结果列表
    Pre = ''  # 初始化前一个单词为空字符串
    for i in t:  # 遍历输入的新文本中的每个单词
        if Pre != '':  # 如果前一个单词不为空
            if sp.get((Pre, i)) is not None:  # 如果已查找过该单词对的桥接词
                n = len(sp[(Pre, i)])  # 获取桥接词数量
                pos = randint(0, n - 1)  # 随机选择一个桥接词
                ans.append(sp[(Pre, i)][pos])  # 将桥接词添加到结果列表中
            else:
                Bridge = []  # 初始化桥接词列表
                if Pre not in MyGraph.keys() or i not in MyGraph.keys():  # 如果单词不在图中
                    sp[(Pre, i)] = Bridge
                else:
                    for j in MyGraph[Pre].keys():  # 遍历前一个单词的邻接节点
                        if MyGraph[j].get(i) is not None:  # 如果邻接节点与当前单词有边
                            Bridge.append(j)  # 将邻接节点加入桥接词列表
                    sp[(Pre, i)] = Bridge
                n = len(sp[(Pre, i)])  # 获取桥接词数量
                if n != 0:  # 如果有桥接词
                    pos = randint(0, n - 1)  # 随机选择一个桥接词
                    ans.append(sp[(Pre, i)][pos])  # 将桥接词添加到结果列表中
        ans.append(i)  # 将当前单词添加到结果列表中
        Pre = i  # 更新前一个单词为当前单词
    generated_text = ' '.join(ans)  # 生成新的文本
    messagebox.showinfo("Generated Text", generated_text)  # 显示生成的文本

# 定义函数，用于查询最短路径，并显示路径和路径长度
def query_path():
    word1 = word1_minpath_entry.get().lower()  # 获取输入的第一个单词
    word2 = word2_minpath_entry.get().lower()  # 获取输入的第二个单词
    if word1 not in graph:  # 如果第一个单词不在图中
        messagebox.showinfo("Error", f"No {word1} in the graph!")  # 显示错误信息
        return
    if word2 not in graph:  # 如果第二个单词不在图中
        messagebox.showinfo("Error", f"No {word2} in the graph!")  # 显示错误信息
        return
    if word1 and word2:  # 如果输入了两个单词
        try:
            path = nx.shortest_path(graph, source=word1, target=word2, weight='weight')  # 查询最短路径
            path_length = nx.shortest_path_length(graph, source=word1, target=word2, weight='weight')  # 计算路径长度
            print("The shortest path length is " + str(path_length))
            highlight_path(path, path_length)  # 突出显示最短路径
        except nx.NetworkXNoPath:
            messagebox.showinfo("Result", f"No path from {word1} to {word2}!")  # 如果无路径，显示错误信息

# 定义函数，用于突出显示最短路径，确保原图不受影响
def highlight_path(path, path_length):
    pos = nx.spring_layout(graph)  # 计算图布局
    plt.figure()    # 防止新生成的突出显示路径与原图重叠
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=10)  # 绘制原图
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    path_edges = list(zip(path[:-1], path[1:]))  # 获取路径边
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='red', node_size=700)  # 突出显示路径节点
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)  # 突出显示路径边
    plt.title(f"Shortest path from {path[0]} to {path[-1]} with length: {path_length}")  # 设置图标题
    plt.show()  # 显示图形

# 定义函数，用于进行随机游走
def RandomWalk():
    global randomWalkStopFlag
    randomWalkStopFlag = False
    now = ""
    words = []
    eds_set = set()  # 初始化集合，用于存储已访问的边
    while True:
        time.sleep(0.5)
        if randomWalkStopFlag != False:  # 用户未手动停止
            break
        if now == "":  # 如果当前单词为空
            kms = list(MyGraph.keys())  # 获取所有节点
            n = len(kms)
            pos = randint(0, n - 1)  # 随机选择一个节点
            words.append(kms[pos])  # 将节点添加到结果列表中
            now = kms[pos]  # 更新当前节点
        else:
            kms = list(MyGraph[now].keys())  # 获取当前节点的邻接节点
            n = len(kms)
            if n == 0:
                break
            pos = randint(0, n - 1)  # 随机选择一个邻接节点
            words.append(kms[pos])  # 将邻接节点添加到结果列表中
            if (now, kms[pos]) in eds_set:  # 如果边已被访问过
                break
            else:
                eds_set.add((now, kms[pos]))  # 将边加入已访问集合
            now = kms[pos]  # 更新当前节点
    ans = ' -> '.join(words)  # 生成随机游走结果
    messagebox.showinfo("随机游走结果", "最终游走结果：" + ans)

# 定义启动随机游走线程函数
def RandomWalkStart():
    threading.Thread(target=RandomWalk).start()

# 定义随机游走停止函数
def RandomWalkStop():
    global randomWalkStopFlag
    randomWalkStopFlag = True

# 创建主窗口
root = tk.Tk()
root.title("Lab 1: Directed Graph App")

# 创建输入文本文件路径标签和输入框
text_label = tk.Label(root, text="输入文本文件路径:")
text_label.pack(side="top")

file_entry = tk.Entry(root, width=50)
file_entry.pack(side="top")

browse_button = tk.Button(root, text="浏览", command=load_file)
browse_button.pack(side="top")

# 显示图结构按钮
show_button = tk.Button(root, text="显示图结构", command=show_graph)
show_button.pack(side="top")

# 输入保存图形路径标签和输入框
path_label = tk.Label(root, text="输入保存图形的路径:")
path_label.pack(side="top")

path_entry = tk.Entry(root, width=50)
path_entry.pack(side="top")

save_button = tk.Button(root, text="保存图形", command=save_graph)
save_button.pack(side="top")

# 输入单词以查询桥接词标签和输入框
query_bridge_label = tk.Label(root, text="输入两个单词以查询桥接词:")
query_bridge_label.pack(side="top")

word1_bridge_entry = tk.Entry(root, width=30)
word1_bridge_entry.pack(side="top")

word2_bridge_entry = tk.Entry(root, width=30)
word2_bridge_entry.pack(side="top")

# 查询桥接词按钮
query_button = tk.Button(root, text="查询桥接词", command=query_bridge_words)
query_button.pack(side="top")

# 输入单词以查询最短路径标签和输入框
query_minpath_label = tk.Label(root, text="输入两个单词以查询最短路径:");
query_minpath_label.pack(side="top")

word1_minpath_entry = tk.Entry(root, width=30)
word1_minpath_entry.pack(side="top")

word2_minpath_entry = tk.Entry(root, width=30)
word2_minpath_entry.pack(side="top")

# 查询最短路径按钮
path_query_button = tk.Button(root, text="查询最短路径", command=query_path)
path_query_button.pack(side="top")

# 输入新文本标签和输入框
new_text_label = tk.Label(root, text="输入新文本:")
new_text_label.pack(side="top")

new_text_entry = tk.Entry(root, width=50)
new_text_entry.pack(side="top")

# 生成新文本按钮
generate_text_button = tk.Button(root, text="生成新文本", command=generate_new_text)
generate_text_button.pack(side="top")

# 生成开始随机游走按钮
start_random_walk_button = tk.Button(root, text="开始随机游走", command=RandomWalkStart)
start_random_walk_button.pack(side="top")

# 生成结束随机游走按钮
stop_random_walk_button = tk.Button(root, text="结束随机游走", command=RandomWalkStop)
stop_random_walk_button.pack(side="top")

# 运行主循环
root.mainloop()
