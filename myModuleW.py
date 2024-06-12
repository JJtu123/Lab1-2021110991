"""
version: 1.2
Author: Fang Shihao, An Xin
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

# 定义函数，用于查询最短路径，并显示路径和路径长度
def query_path(word1, word2):
    if word1 not in graph:  # 如果第一个单词不在图中
        return "No " + word1 + " in the graph!"  # 返回错误信息
    if word2 not in graph:  # 如果第二个单词不在图中
        return "No " + word2 + " in the graph!"  # 返回错误信息
    if word1 and word2:  # 如果输入了两个单词
        try:
            path = nx.shortest_path(graph, source=word1, target=word2, weight='weight')  # 查询最短路径
            path_length = nx.shortest_path_length(graph, source=word1, target=word2, weight='weight')  # 计算路径长度
            return "The shortest path is: " + str(path) + ", and the shortest path length is " + str(path_length)
        except nx.NetworkXNoPath:
            return "No path from " + word1 + " to " + word2 + "!"  # 如果无路径，返回错误信息

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
