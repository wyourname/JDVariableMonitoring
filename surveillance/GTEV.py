"""
Get the environment variable from the warehouse.
cron: 1 1 1 1 *
author: xxxx
new Env('Tg变量生成')
"""
import os
import asyncio
import re
import aiofiles as aiofiles
import yaml
import asy
import pathlib

envpath = asy.read_config('env_path')


# 获取当前目录下的文件名,程序的起点
async def get_file_name():
    if os.path.exists('./config.yaml'):
        repo_path = asy.read_config('repositories_path')
        for repo in repo_path:
            await asyncio.create_task(cope_filepath(repo))
    else:
        await create_config()


async def cope_filepath(repo_path):
    filenames = os.listdir(repo_path)
    path_dir = os.getcwd()
    path_name = os.path.basename(repo_path)
    print(path_name)
    if path_name == "仓库文件夹":
        print("请前往config.yaml 修改仓库文件夹路径如：/ql/data/repo/KR...")
    else:
        print("当前路径为：", path_dir)
        if os.path.exists(envpath):
            print("文件已存在")
        else:
            print(f"{envpath}文件不存在，创建")
            pathlib.Path("varname.yaml").touch(exist_ok=True)
        for filename in filenames:
            if filename.endswith('.py') or filename.endswith('.ts') or filename.endswith('.js'):
                await asyncio.create_task(read_file_env(path_name, filename, f"{repo_path}/{filename}"))


async def read_file_env(folder, filename, open_path):
    # print(filename)
    async with aiofiles.open(open_path, mode='r', encoding='utf-8') as f:
        contents = await f.read()
        # print(contents)
        part_text = re.compile(r'export (.*?)=')
        res = part_text.findall(contents)
        if res is not None and len(res) > 0:
            await add_data(folder, filename, res)


# 此处用异步报错，未解决
async def add_data(repo, filename, env):
    with open(envpath, mode='r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
        if data is None:
            data = {repo: []}
            data[repo].append({filename: env})
            await update_data(data)
        if repo not in data:
            data[repo] = []
            data[repo].append({filename: env})
            await update_data(data)
        else:
            if {filename: env} not in data[repo]:
                data[repo].append({filename: env})
                await update_data(data)
            # print(data)
            else:
                print("变量已存在")


async def update_data(data):
    async with aiofiles.open(envpath, mode='w', encoding='utf-8') as f:
        await f.write(yaml.dump(data, default_flow_style=False))
        print("变量更新成功")


# important to call this function
async def create_config():
    desire_caps = {
        "host": "http://青龙ip:端口号",
        "client_id": "xxx",
        "client_secret": "xxx",
        "auth_token": "xxx",
        "api_hash": "xxx",
        "api_id": "xxx",
        "env_path": "./varname.yaml",
        "log_channel_id": "-xxxxx",
        "sur_channel_id": ["-xxxxx", "-xxxxx"],
        "repositories_path": ["/ql/data/repo/仓库文件夹1", "/ql/data/repo/仓库文件夹2"]
    }
    async with aiofiles.open('./config.yaml', mode='w', encoding='utf-8') as f:
        await f.write(yaml.dump(desire_caps, default_flow_style=False, allow_unicode=True))
        print("config.yaml 文件创建成功,请前往文件填写配置,再次运行")


if __name__ == '__main__':
    asyncio.run(get_file_name())
