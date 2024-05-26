import sys

import questionary
import asyncio
from DrissionPage import WebPage


async def listen(choice: int):
    if choice == 0:
        page.listen.start("https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/listNotifications")
        page.get("https://ys.mihoyo.com/cloud/#/")
    elif choice == 1:
        page.listen.start("https://cg-hkrpg-api.mihoyo.com/hkrpg_cn/cg/gamer/api/listNotifications")
        page.get("https://sr.mihoyo.com/cloud/#/")

    for packet in page.listen.steps():
        result = "X-Rpc-App_id" in packet.request.headers
        print(f"> {packet.url} -> {result}")

        if result:
            return packet.request.headers


if __name__ == '__main__':
    r = questionary.select(
        "请选择你的游戏类型：",
        choices=[
            questionary.Choice("云·原神", 0),
            questionary.Choice("云·星穹铁道", 1)
        ]
    ).ask()

    page = WebPage()

    loop = asyncio.get_event_loop()
    task = loop.create_task(listen(r))

    print("请完成登录并等待...")

    loop.run_until_complete(task)

    headers = task.result()

    if headers is None:
        print("未完成登录，请重启程序后重试。")
        questionary.press_any_key_to_continue().ask()
        sys.exit(-1)

    # 筛选关键 Headers
    print("X-Rpc-Combo_token: " + headers["x-rpc-combo_token"])
    print("X-RPC-Sys_version: " + headers["x-rpc-sys_version"])
    print("X-Rpc-Device_id: " + headers["x-rpc-device_id"])
    print("X-Rpc-Device_model: " + headers["x-rpc-device_model"])
    print("X-Rpc-Device_name: " + headers["x-rpc-device_name"])

    # 阻塞
    questionary.press_any_key_to_continue().ask()
