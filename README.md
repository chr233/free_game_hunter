# Free Game Hunter

> 使用asf自动添加steam上的免费游戏

## 使用方法

1. 将`example.config.toml`重命名为`config.toml`

2. 编辑`config.toml`设置`asf`和`bot`信息

3. 确保`data.db`存在,他用来保存数据

4. 运行`pip3 install -r requirements.txt`

5. 运行`python3 run.py`

## 其他说明

steam每小时最多添加50个sub,本脚本每次添加的上限为40
建议设置成定时任务,定期执行脚本
