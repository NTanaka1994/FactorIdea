import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import numpy as np
import os,sys
from tkinter import filedialog
import learn

root=tk.Tk()

#ファイルを開く
def Button1Click(event):
    #print("OK")
    file={}
    file[".csv"]="csv"
    file[".xlsx"]="Excel"
    fTyp = [("csvファイル", "*.csv"),("Excelファイル", "*.xlsx")]
    iFile = os.path.abspath(os.path.dirname(__file__))
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    root,ext=os.path.splitext(iFilePath)
    Filekind.delete(0,tk.END)
    Filekind.insert(tk.END,file[ext])
    EditBox1.delete(0,tk.END)
    EditBox1.insert(tk.END,iFilePath)
    if Filekind.get()=="csv":
        df=pd.read_csv(EditBox1.get(),encoding="shift-jis")
        PullDown2["values"]=list(df.columns)
        PullDown2.current(0)
        PullDown3["values"]=list(df.columns)
        PullDown3.current(0)
        col=[]
        col.append(list(df.columns))
        tab=[]
        tab=df.values
        table["columns"]=np.arange(len(df.columns))
        table["show"]="headings"
        for i in range(len(df.columns)):
            table.column(i)
        for i in range(len(df.columns)):
            table.heading(i,text=col[0][i])
        for i in range(len(tab)):
            table.insert( "", "end", tag=0, values=tab[i])
    elif Filekind.get()=="Excel":
        df=pd.read_excel(EditBox1.get(),sheet_name=Sheetname.get())
        PullDown2["values"]=list(df.columns)
        PullDown2.current(0)
        PullDown3["values"]=list(df.columns)
        PullDown3.current(0)
        col=[]
        col.append(list(df.columns))
        tab=[]
        tab=df.values
        table["columns"]=np.arange(len(df.columns))
        table["show"]="headings"
        for i in range(len(df.columns)):
            table.column(i)
        for i in range(len(df.columns)):
            table.heading(i,text=col[0][i])
        for i in range(len(tab)):
            table.insert( "", "end", tag=0, values=tab[i])
        
        
#ダミー変数を作成
def Button2Click(event):
    EditBox2.insert(tk.END,PullDown3.get()+",")
    root.update()

#分析開始
def Button3Click(event):
    print(Filekind.get())
    if Filekind.get()=="csv":
        #print("OK")
        df=pd.read_csv(EditBox1.get(),encoding="shift-jis")
        #ダミー変数作成
        if EditBox2.get()!="":
            text=EditBox2.get()
            text2=text[:-1]
            dummie=text2.split(",")
            df=pd.get_dummies(df,columns=dummie)
        label=PullDown2.get()
        if PullDown4.get()=="カテゴリ":
            acc=learn.classification(df,label,EditBox3.get())
            label4["text"]="予測精度平均="+str(100*acc)+"%\n保存完了"
        elif PullDown4.get()=="数値":
            acc=learn.regression(df,label,EditBox3.get())
            label4["text"]="予測精度平均="+str(100*(1-acc))+"%\n保存完了"
    elif Filekind.get()=="Excel":
        df=pd.read_excel(EditBox1.get(),sheet_name=Sheetname.get())
        #ダミー変数作成
        if EditBox2.get()!="":
            text=EditBox2.get()
            text2=text[:-1]
            dummie=text2.split(",")
            df=pd.get_dummies(df,columns=dummie)
        label=PullDown2.get()
        if PullDown4.get()=="カテゴリ":
            acc=learn.classification(df,label,EditBox3.get())
            label4["text"]="予測精度平均="+str(100*acc)+"%\n保存完了"
        elif PullDown4.get()=="数値":
            acc=learn.regression(df,label,EditBox3.get())
            label4["text"]="予測精度平均="+str(100*(1-acc))+"%\n保存完了"
                        
#保存先フォルダ指定
def Button4Click(event):
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    EditBox3.delete(0,tk.END)
    EditBox3.insert(tk.END,iDirPath)

#Sheet名を入れる
Sheetname=tk.Entry(width=50)
Sheetname.insert(tk.END,"Excelファイルの場合シート名を入力してください")
Sheetname.pack()
    
#ファイルのパスを入れる
EditBox1=tk.Entry(width=50)
EditBox1.insert(tk.END,"ファイルのパス")
EditBox1.pack()

#データ参照をするボタン
Button1=tk.Button(text="データの参照")
Button1.bind("<Button-1>",Button1Click)
Button1.pack()


#ファイルの種類の選択
Filekind=tk.Entry(width=50)
Filekind.insert(tk.END,"ファイルの種類")
Filekind.pack()

#表の形式を表示

table=ttk.Treeview(root)
table.pack()

#ラベル1
label1=ttk.Label(root,text="分析目的項目を選んでください")
label1.pack()

#分析対象
PullDown2=ttk.Combobox(root,state="readonly")
PullDown2.pack()

#ラベル2
label2=ttk.Label(root,text="表の中で数値でない項目を選んでください")
label2.pack()

#カテゴリ変数選択用
PullDown3=ttk.Combobox(root,state="readonly")
PullDown3.pack()

#ダミー変数を選択
Button2=tk.Button(text="カテゴリ項目の選択")
Button2.bind("<Button-1>",Button2Click)
Button2.pack()

#ダミー変数を入れる
EditBox2=tk.Entry(width=50)
EditBox2.pack()

#ラベル3
label3=ttk.Label(root,text="分析目的の項目の種類を選んでください")
label3.pack()

#目的変数の種類
PullDown4=ttk.Combobox(root,state="readonly")
PullDown4["values"]=("数値","カテゴリ")
PullDown4.pack()

#保存先
Button4=tk.Button(text="保存先の指定")
Button4.bind("<Button-1>",Button4Click)
Button4.pack()

#ファイルのパスを入れる
EditBox3=tk.Entry(width=50)
EditBox3.insert(tk.END,"保存先フォルダのパス")
EditBox3.pack()

#分析開始
Button3=tk.Button(text="分析開始")
Button3.bind("<Button-1>",Button3Click)
Button3.pack()

#ラベル4
label4=tk.Label(text="")
label4.pack()

#root.mainloop()
