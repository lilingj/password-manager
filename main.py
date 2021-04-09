import os
from typing import List

import myrsa
import mypw

def get_verify_input() -> bool:
    print("警告!请确认你的输入[y, n]:")
    return get_opt(["y", "n"]) == "y"

def get_opt(opts: List[str]):
    print("请输入: ")
    while True:
        inp = input()
        if inp in opts:
            return inp
        print("输入有误，请重新输入: ")

def print_menu(opts: List[str]):
    print("┏-------------------------------------------------------------┓")
    for i in range(len(opts)):
        print("┣━", str(i + 1) + ":", opts[i])
    print("┗-------------------------------------------------------------┛")

def save():
    if pws == []:
        return
    else:
        try:
            os.rename("pwdb.pkl", "pwdb.pkl.bak")
        except:
            pass
        for pw in pws:
            pw.encrypt(rsa_obj)
        mypw.store_mypws(pws)

def main_menu():
    print_menu(
        [
            "默认载入公私钥和数据(public.key private.key pwdb.pkl)",
            "生成公私钥, 重置数据",
            "退出",
        ]
    )

    opt = int(get_opt(list(map(str,range(1, 4)))))
    
    mp = {
        1: lambda: mypw.load_mypws(),
        2: lambda: get_verify_input(),
        3: lambda: False,
    }

    data = mp[opt]()
    if data == False:
        save()
        return
    elif data == True:
        pass
    else:
        global pws
        pws = data
        show_all()
        for pw in pws:
            pw.decrypt(rsa_obj)
    
    sec_menu()

def sec_menu():
    while True:
        print_menu(
            [
                "存储记录",
                "查看记录",
                "检索记录",
                "删除记录",
                "保存并退出"
            ]
        )

        opt = int(get_opt(list(map(str,range(1, 6)))))
        
        mp = {
            1: lambda: new_pw_menu(),
            2: lambda: show_all(),
            3: lambda: search_menu(),
            4: lambda: del_pw_menu(),
            5: lambda: False,
        }

        if mp[opt]() == False:
            save()
            return

def new_pw_menu():
    print("[如果password为空, 将自动生成密码]")
    url      = input("请输入url:      ")
    username = input("请输入username: ")
    password = input("请输入password: ")
    note     = input("请输入note:     ")
    if get_verify_input():
        new_pw = mypw.MyPW(url, username, password, note)
        if new_pw.password == "":
            new_pw.gen_pw()
        pws.append(new_pw)
        print(str(new_pw))
    else:
        new_pw_menu()

def del_pw_menu():
    show_all()
    while True:
        try:
            idx = int(input("请问要删除哪条记录(输入-1返回上一级): "))
            if idx == -1:
                return
            if 0 <= idx < len(pws):
                print("即将删除的记录: ")
                print(str(pws[idx]))
                if get_verify_input():
                    del pws[idx]
                return
            else:
                raise Exception("just print prompt and continue")
        except:
            print("非法输入!")
    
    

def search_menu():
    keyword = input("请输入关键字: ")
    for pw in pws:
        for s in [pw.url, pw.username, pw.password, pw.note]:
            if keyword in s:
                print(str(pw))
    print("检索完毕!全部结果已经打出")


def show_all():
    print("┏----┬--------------------┬--------------------┬--------------------┬--------------------┓")
    print("|id  |url                 | username           | password           | note               |")
    print("├----+--------------------+--------------------+--------------------+--------------------┤")
    for i in range(len(pws)):
        print(pws[i].format_str(i))
    print("┗----┴--------------------┴--------------------┴--------------------┴--------------------┛")


rsa_obj = myrsa.RsaObj()
pws = []

main_menu()