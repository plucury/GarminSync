# GarminSync

## HowTO
0. 一台可以正确连接到[https://connect.garmin.com](https://connect.garmin.com)的电脑
1. 克隆代码
	`git clone https://github.com/plucury/GarminSync.git`
2. 安装依赖
	`cd GarminSync`
    `pip3 install -r requirements.txt `
3. 设置密码，目录内新建`.env`文件
	```
	CN_USERNAME="" // 中国站用户名
	CN_PASSWORD="" // 中国站密码
	GLOBAL_USERNAME="" // 国际站用户名
	GLOBAL_PASSWORD="" // 国际站密码
	```
4. 执行代码
    `python3 main.py --size=10 # size为每次回溯多少条activity记录，默认10条`