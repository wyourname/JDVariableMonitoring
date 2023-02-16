"""
Base modules
cron: 1 1 1 1 1
new Env('tg基础模块')
"""
import asyncio

import yaml


def read_config(option):
    try:

        with open('./config.yaml', 'r', encoding="utf-8") as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return data[option]
    except Exception as e:
        print(e)


# 这两处代码有些重复，也可以合并☝☟
async def write_config(key, value):
    with open("./config.yaml", "r", encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
        if key not in data:
            data[key] = value
        if key in data:
            data[key] = value
            # print(data['auth_token'])
    with open("./config.yaml", "w", encoding="utf-8") as f1:
        f1.write(yaml.dump(data, default_flow_style=False))
        print("Config updated")


async def read_varname(env_name):
    envpath = read_config("env_path")
    with open(envpath, encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
        for key in data.keys():
            for i in data[key]:
                for key1, value1 in i.items():
                    # print(key, value)
                    if env_name in value1:
                        print(key, key1)
                        return key1


# if __name__ == '__main__':
#     asyncio.run(read_varname("jd_completeInfoActivity_activityUrl"))
