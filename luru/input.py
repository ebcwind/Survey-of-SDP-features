# 导入tkinter和pandas库
import tkinter as tk
import tkinter.messagebox
import pandas as pd
import os
from ComBoPicker import Combopicker  # 导入自定义下拉多选框


paperName = pd.read_csv('papername.csv')
classifier = pd.read_csv('classifier.csv')
datasets = pd.read_csv('datasets.csv')
featureSelection = pd.read_csv('FS.csv')
metrics = pd.read_csv('metrics.csv')
performance = pd.read_csv('performance.csv')

# 创建一个空的dataframe，列名为你提供的属性
if os.path.exists("pName_metrics.csv"):
    df_pName_metrics = pd.read_csv("pName_metrics.csv")
else:
    df_pName_metrics = pd.DataFrame(columns=['ID', 'mID'])

if os.path.exists("pName_datasets.csv"):
    df_pName_datasets = pd.read_csv("pName_datasets.csv")
else:
    df_pName_datasets = pd.DataFrame(columns=["ID", "dID"])

if os.path.exists("pName_FS.csv"):
    df_pName_FS = pd.read_csv("pName_FS.csv")
else:
    df_pName_FS = pd.DataFrame(columns=["ID", "fID"])

if os.path.exists("pName_classifier.csv"):
    df_pName_classifier = pd.read_csv("pName_classifier.csv")
else:
    df_pName_classifier = pd.DataFrame(columns=["ID", "tID"])

if os.path.exists("pName_performance.csv"):
    df_pName_performance = pd.read_csv("pName_performance.csv")
else:
    df_pName_performance = pd.DataFrame(columns=["ID", "pID"])




# 提取选项
paperNameOption = paperName.iloc[:, 1].astype("string")
metricsOption = metrics.iloc[:, 1].astype("string").sort_values()
metricsetsOption = list(set(metrics.iloc[:, 2].astype("string")))
metricsetsOption.sort()
fsOption = featureSelection.iloc[:, 1].astype("string").sort_values()
datasetsOption = datasets.iloc[:, 1].astype("string").sort_values()
classifierOption = classifier.iloc[:, 1].astype("string").sort_values()
performanceOption = performance.iloc[:, 1].astype("string").sort_values()

# 创建一个窗口
window = tk.Tk()
window.geometry("600x800")
window.title("数据录入程序")


# 创建一个标签，提示用户输入论文名字
tk.Label(window, text="请输入论文名字：", bg="lightyellow").pack(side='top', fill="x")
# 创建一个下拉菜单，让用户选择论文名字
option1 = tk.StringVar()
option1.set("")
for i in range(len(paperNameOption)):
    paperNameOption[i] = str(i+1) + "+" + paperNameOption[i]
menu2 = tk.OptionMenu(window, option1, *paperNameOption)
menu2.pack()

# 创建一个标签，提示用户选择预测方式
tk.Label(window, text="请选择特征选择方法：", bg="lightyellow").pack(fill="x")

# 创建一个下拉菜单，让用户选择特征选择方式，可以根据你的dataframe数据修改选项
F2 = tk.Frame(window)
F2.pack(expand=False, fill="both", padx=10, pady=10)
Combo2 = Combopicker(F2, values=fsOption)
Combo2.pack()

# 以此类推，创建其他属性的标签和下拉菜单
tk.Label(window, text="请选择软件特征：", bg="lightyellow").pack(fill="x")
F3 = tk.Frame(window)
F3.pack(expand=False, fill="both", padx=10, pady=10)
Combo3 = Combopicker(F3, values=metricsOption)
Combo3.pack()

F31 = tk.Frame(window)
F31.pack(expand=False, fill="both", padx=10, pady=10)
Combo31 = Combopicker(F31, values=metricsetsOption)
Combo31.pack()

tk.Label(window, text="请选择数据集名称：", bg="lightyellow").pack(fill="x")
F4 = tk.Frame(window)
F4.pack(expand=False, fill="both", padx=10, pady=10)
Combo4 = Combopicker(F4, values=datasetsOption)
Combo4.pack()

tk.Label(window, text="请选择分类器：", bg="lightyellow").pack(fill="x")
F5 = tk.Frame(window)
F5.pack(expand=False, fill="both", padx=10, pady=10)
Combo5 = Combopicker(F5, values=classifierOption)
Combo5.pack()

tk.Label(window, text="请选择性能评估指标：", bg="lightyellow").pack(fill="x")
F6 = tk.Frame(window)
F6.pack(expand=False, fill="both", padx=10, pady=10)
Combo6 = Combopicker(F6, values=performanceOption)
Combo6.pack()

text = tk.Text(window, height=15)
text.pack()

def text_display(t1, t2, i):
    text.insert(f'{i}.end', t1)
    text.insert(f'{i}.end', ', ')
    text.insert(f'{i}.end', t2)
    text.insert(f'{i}.end', ' ')
def save_df():
    # 获取用户输入的数据
    text.delete('1.0', 'end')
    pN = option1.get().split("+")
    ID = paperName.loc[paperName.iloc[:, 1] == pN[1], "ID"].item()
    text.insert('1.0', 'ID, fID')
    if Combo2.current_value and Combo2.current_value[0] != '':
        for x in Combo2.current_value:
            fID = featureSelection.loc[featureSelection.iloc[:, 1] == x, "fID"].item()
            df_pName_FS.loc[len(df_pName_FS)] = ID, fID
            text_display(ID, fID, 1)
    text.insert('1.end', '\n')
    mIDs = []
    text.insert('2.0', 'ID, mID')
    if Combo31.current_value and Combo31.current_value[0] != '':
        for x in Combo31.current_value:
            mIDs = metrics.loc[metrics.iloc[:, 2] == x, "mID"]
            for i in mIDs:
                df_pName_metrics.loc[len(df_pName_metrics)] = ID, i
                text_display(ID, i, 2)
    if Combo3.current_value and Combo3.current_value[0] != '':
        for x in Combo3.current_value:
            mID = metrics.loc[metrics.iloc[:, 1] == x, "mID"].item()
            if mID not in mIDs:
                df_pName_metrics.loc[len(df_pName_metrics)] = ID, mID
                text_display(ID, mID, 3)
    text.insert('2.end', '\n\n')
    text.insert('4.0', 'ID, dID')
    if Combo4.current_value and Combo4.current_value[0] != '':
        for x in Combo4.current_value:
            dID = datasets.loc[datasets.iloc[:, 1] == x, "dID"].item()
            df_pName_datasets.loc[len(df_pName_datasets)] = ID, dID
            text_display(ID, dID, 4)
    text.insert('4.end', '\n')
    text.insert('5.0', 'ID, tID')
    if Combo5.current_value and Combo5.current_value[0] != '':
        for x in Combo5.current_value:
            tID = classifier.loc[classifier.iloc[:, 1] == x, "tID"].item()
            df_pName_classifier.loc[len(df_pName_classifier)] = ID, tID
            text_display(ID, tID, 5)
    text.insert('5.end', '\n')
    text.insert('6.0', 'ID, pID')
    if Combo6.current_value and Combo6.current_value[0] != '':
        for x in Combo6.current_value:
            pID = performance.loc[performance.iloc[:, 1] == x, "pID"].item()
            df_pName_performance.loc[len(df_pName_performance)] = ID, pID
            text_display(ID, pID, 6)

    option1.set("")
    Combo_all = [Combo2, Combo3, Combo4, Combo5, Combo6, Combo31]
    for Combo in Combo_all:
        Combo.dict_checkbutton = {}
        Combo.dict_checkbutton_var = {}
        Combo.dict_intvar_item = {}
        Combo.entry_var.set("")





def save_data():
    # 保存dataframe为csv格式，你可以修改文件名和路径
    df_pName_FS.to_csv("pName_FS.csv", index=False, encoding='utf-8')
    df_pName_metrics.to_csv("pName_metrics.csv", index=False, encoding='utf-8')
    df_pName_datasets.to_csv("pName_datasets.csv", index=False, encoding='utf-8')
    df_pName_classifier.to_csv("pName_classifier.csv", index=False, encoding='utf-8')
    df_pName_performance.to_csv("pName_performance.csv", index=False, encoding='utf-8')
    # 提示用户数据已保存
    tk.messagebox.showinfo("提示", "数据已保存")


# 创建一个按钮，绑定save_data函数
tk.Button(window, text="保存数据", command=save_df).pack()
tk.Button(window, text="写入CSV数据", command=save_data).pack()

# 运行窗口
window.mainloop()
