# JDVariableMonitoring
目前在开发中，但还是希望大佬们能在脚本中以 export variale=value 这种方式提示变量
## 前提：原意是为了手机模块上变量监控的，因为手机没有docker容器但是我换了软路由其实也用不上开发的了但是手痒就顺手弄了下
## 准备工作：魔法工具自备！一个telegram的账号，以及关注你要监控的线报群获取其id,和自己输出日志的群id，用tg号创建一个application（百度即可）
### 开始：第一步 进入青龙面板创建你的应用，然后拉库命令:ql repo https://github.com/wangquanfugui233/JDVariableMonitoring.git
### 第二步:拉完库先运行一次GTEV.py,会生成一个config.yaml文件，去把config.yaml完善后再运行一次GTEV.py会帮你查找你要监控的库的变量
### 第三步:ssh 登录你的容器终端 cd /ql/data/repo//wangquanfugui233_JDVariableMonitoring/
### 第四步: pip install -r requirements.txt
### 第五步: cd  surveillance
### 第六步：python3 surveillance_tg.py 然后输入0086你的手机号 验证码
### 第七步：登录成功会有日志提示在你的log群的 看到提示就可以 CTRL C了 然后  nohup python3 -u surveillance_tg.py > surveillance.log 2>&1 &  挂起后台了

