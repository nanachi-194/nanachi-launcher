import TkEasyGUI as eg
import os
import sys
import logging

#ログ確認
logging.basicConfig(
    filename="log_file.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="UTF-8"
)
logging.info("アプリ起動")
debug_log=[]

# exe一覧取得関数
def get_exe_list():
    if not os.path.isdir("apps"):
        return ["appsフォルダがありません"]
    return [f for f in os.listdir("apps") if f.endswith(".exe")]

#ログ追加関数
def app_log(messege):
    debug_log.append(messege)
    window["-debug-"].update(values=debug_log)

#設定
List_box_style_1 = {
    "size": (20, 10),
    "key": "-LIST-",
    "font": ("けいふぉんと", 16),
    "enable_events": True
}

List_box_style_2 = {
    "values": [""],
    "key": "-debug-",
    "size": (20,10),
    "font": ("けいふぉんと", 16),
}

# レイアウト
layout = [
    [eg.Text("起動したいアプリを選択または入力してください",font=("けいふぉんと", 16))],
    [eg.Input(key="-INPUT-",font=("けいふぉんと", 16)), eg.Button("起動",font=("Arial", 10))],
    [eg.Button("更新"), eg.Button("終了")],
    [eg.Text("exe一覧", font=("けいふぉんと",14))],
    [eg.Listbox(get_exe_list(),**List_box_style_1)],
    [eg.Text("ログ一覧",font=("けいふぉんと",14))],
    [eg.Listbox(**List_box_style_2)]
]

window = eg.Window("アプリランチャー", layout)

while True:
    event, values = window.read()

    if event == eg.WINDOW_CLOSED:
        break

    # 一覧更新
    if event == "更新":
        window["-LIST-"].update(get_exe_list())
        app_log("一覧を更新しました")

    # リストから選択
    if event == "-LIST-":
        if values["-LIST-"]:
            window["-INPUT-"].update(values["-LIST-"][0])

    # 起動ボタン
    if event == "起動":
        filename = values["-INPUT-"]

        if not filename.endswith(".exe"):
            app_log("exeファイルを入力してください")
            continue

        path = f'apps\\{filename}'

        if not os.path.isfile(path):
            app_log("ファイルが存在しません")
            continue

        result = os.system(f'"{path}"')

        if result == 0:
            app_log("起動成功")
        else:
            app_log("起動失敗")

    # 終了
    if event == "終了":
        confirm = eg.popup_yes_no("アプリを終了しますか？")
        if confirm == "Yes":
            sys.exit(0)

window.close()