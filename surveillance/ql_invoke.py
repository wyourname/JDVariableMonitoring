"""
这是调用青龙的模块
cron: 1 1 1 1 1
new Env('tg-青龙对接模块')
"""
import asyncio
import re
import aiohttp
import asy


class Invoke:
    def __init__(self):
        self.url = asy.read_config("host")
        self.params = {
            "client_id": asy.read_config("client_id"),
            "client_secret": asy.read_config("client_secret")
        }
        # self.header = {"Authorization": asy.read_config("auth_token")}

    async def requests_method(self, requests_type, url, data=None, header=None):
        async with aiohttp.ClientSession() as session:
            if requests_type == "get":
                async with session.get(url=url, params=data, headers=header) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        if response.status == 401:
                            await self.init_file()
                        return None
            elif requests_type == "post":
                async with session.post(url=url, data=data, headers=header) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        if response.status == 401:
                            await self.init_file()
                        return None
            elif requests_type == "put":
                async with session.put(url=url, json=data, headers=header) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        if response.status == 401:
                            await self.init_file()
                        return None
            elif requests_type == "delete":
                async with session.delete(url=url, params=data, headers=header) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        if response.status == 401:
                            await self.init_file()
                        return None

    async def init_file(self):
        token_url = self.url + "/open/auth/token"
        token_result = await self.requests_method('get', url=token_url, data=self.params)
        if token_result:
            # data = {"auth_token": f"{token_result['data']['token_type']} {token_result['data']['token']}"}
            await asy.write_config("auth_token",
                                   f"{token_result['data']['token_type']} {token_result['data']['token']}")
            return f"{token_result['data']['token_type']} {token_result['data']['token']}"
        else:
            print("请检查你的host,client_id,client_secret是否正确")

    # 获取配置文件信息
    async def fetch_token(self):
        auth_token = asy.read_config("auth_token")
        # 如果auth_token存在Bearer格式，则直接返回
        if auth_token.startswith("Bearer "):
            # print(auth_token)
            return auth_token
        # 如果auth_token不存在，则获取token
        else:
            return await self.init_file()

    async def save_config(self, variables, value):
        content_url = self.url + "/open/configs/config.sh"
        token = await self.fetch_token()
        header = {"Authorization": token}
        config_content = await self.requests_method('get', content_url, header=header)
        if config_content:
            content = await self.regex(config_content['data'], variables, value)
            save_url = self.url + "/open/configs/save"
            data = {
                "name": "config.sh",
                "content": f"{content}"
            }
            result = await self.requests_method('post', url=save_url, data=data, header=header)
            if result:
                return True
        else:
            await self.save_config(variables, value)

    @staticmethod
    async def regex(data, variables=None, value=None):  # variables是变量值，value是变量名
        part_text = re.compile(r'export (.*?)=')
        result = part_text.findall(data)
        # 匹配等号后面的字符串
        for variable in variables:
            value_text = re.compile(f'export {variable}=(.*)')
            value_var = f'export {value[variables.index(variable)]}'
            if variable in result:
                data = value_text.sub(value_var, data)
                # print(data)
            else:
                data = f'{data} \n{value_var}'
        return data

    async def basics(self):
        token = await self.fetch_token()
        header = {"Authorization": token}
        return header

    async def get_task_info(self, script_name):
        header = await self.basics()
        scripts_url = self.url + "/open/crons"
        result = await self.requests_method('get', url=scripts_url, header=header)
        if result:
            return await self.find_task(result['data']['data'], script_name)
        else:
            await self.get_task_info(script_name)

    @staticmethod
    # 查找任务id
    async def find_task(data, script_name):
        rule = re.compile(r'/(.*)')
        # print(data[0]['children'])
        for task in data:
            # print(task)
            result = rule.findall(task['command'])
            if result[0] == script_name:
                return task

    async def task_status(self, task_id):
        header = await self.basics()
        status_url = self.url + f"/open/crons/{task_id}"
        result = await self.requests_method('get', url=status_url, header=header)
        if result['data']['status'] == 1:
            # print(result)
            await self.run_task(result['data']['id'])
            return result
        else:  # 如果状态不为1则等待任务执行完成返回false
            # print(f"{result['data']['name']} 任务运行中,请等待！")
            await asyncio.sleep(3)
            await self.task_status(task_id)

    async def run_task(self, task_id):
        header = await self.basics()
        run_url = self.url + "/open/crons/run"
        data = [task_id]
        result = await self.requests_method('put', url=run_url, data=data, header=header)
        if result:
            return True
        else:
            return False

    async def task_log(self, task_id):
        log_url = self.url + f"/open/crons/{task_id}/log"
        header = await self.basics()
        result = await self.requests_method('get', url=log_url, header=header)
        print(result)

#
# if __name__ == '__main__':
#     invoke = Invoke()
#     asyncio.run(invoke.task_log(418))
