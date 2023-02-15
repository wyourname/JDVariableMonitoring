import datetime
import re
from telethon import events, TelegramClient
import asy
from ql_invoke import Invoke

api_id = asy.read_config("api_id")
api_hash = asy.read_config("api_hash")
client = TelegramClient("session_name", api_id, api_hash)


# 获取消息
@client.on(events.NewMessage(chats=asy.read_config("sur_channel_id")))
async def get_the_message(event):
    val = event.message.message
    await judgment_variables(val)
    # 采用监听方式采集消息


async def judgment_variables(val):
    rule = re.compile(r'export (.*")')
    variables_list = rule.findall(val)
    part_text = re.compile(r'export (.*?)=')
    value_list = part_text.findall(val)
    script_file = await condition(value_list, variables_list)
    if script_file:
        task_info = await invoke.get_task_info(script_file)
        if await invoke.task_status(task_info['id']):
            await send_message("开始运行任务，没有任务结束提示，后期更新加上")
    else:
        print("没有发现变量可调用的脚本，可能是脚本库没有标注出来，自行手动添加即可，功能待完善")


async def send_message(message):
    await client.send_message(asy.read_config("log_channel_id"), message)


async def condition(cod1, cod2):
    if cod1 and cod2 is not None:
        script_file = await asy.read_varname(cod1[0])
        if script_file:
            if await invoke.save_config(variables=cod1, value=cod2):
                await send_message(f"已将 {cod2} 写入配置文件中")
                return script_file
            else:
                await send_message(f"{cod2} 配置文件更新失败")
                return None
        else:
            await send_message(f"未匹配到 {cod1} 可能是脚本库没有标注出来，自行手动添加即可")
            return None


if __name__ == '__main__':
    # 获取当前时间
    now = datetime.datetime.now()
    print("------开始运行！-------")
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"运行时间于：{now_time}")
    invoke = Invoke()
    with client:
        client.loop.run_until_complete(send_message(f"hello!您在{now_time}上线啦"))
        client.run_until_disconnected()
