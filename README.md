# OneDrive网盘的轮子
##### 可能会比现有的轮子要新要圆？

配套
- 纯 api 服务器 *(todo)*
- CLI 命令行式程序 *(todo)*
- Chrome 扩展 *(todo)*
- 网站管理后台（管理OneDrive账号）
- 网站前端（文件选择器） *(todo)*

基于
- python 3.7
    - click
    - diskcache
    - 更多库请看[requirements.txt](requirements.txt)
- vue
    - vue-cli
    - element-ui 

使用
- chrome扩展将会在Google Chrome扩展商店上架 *(todo)*
- 启动网页服务器：
    - `python3 main.py server --port 23333 --password 123`
    - port 端口
    - password 管理后台的登录密码，**sha256加密后存放**    
- 命令行 所有命令：
    - 列出一些信息
        - `pyonedrive info`
        - 关于一些pyonedrive的运作数据，例如存储数据的目录和这个目录的容量信息等等
    - 本地账号的相关操作
        - 命令行不提供添加OneDrive账号功能，因为使用网页方式添加更加方便
        - 假设有 A 和 B 两个账号，没有设置默认账号
        - 列出所有账号的别名
            - `pyondrive cli accounts`
            - 输出[ A, B ]
        - 将别名为A的账号设置为默认账号 `pyonedrive cli --select A default`
        - [什么是默认账号？](#默认账号)
        - 再次列出所有账号
            - `pyonedrive cli accounts`
            - 输出[ *A, B ]
            - 带星号的是默认账号
        - 删除账号
            - `pyonedrive cli --select A`
            - 确认删除后就删了
    - OneDrive文件级操作
        - 将默认账号的目录定位到/ABC目录，*会影响相同账号的后续命令
            - `pyonedrive cli cd /ABC`
        - 将B账号的目录定位到/ABC目录，*会影响相同账号的后续命令
            - `pyonedrive cli cd /ABC`
        - 列出 /ABC 目录的所有内容 *受 cd 命令影响
            - `pyonedrive cli ls` 
    - `python3 main.py cli upload ./文本.txt` 将本地文件【文本.txt】上传到默认账号的 /ABC 目录，受 cd 命令影响
    - `python3 main.py cli upload ./文本.txt /` 将本地文件【文本.txt】上传到默认账号的 / 根目录，忽略 cd命令的影响
    - 有没有默认账号的区别：以下的命令可以少写一个账号别名参数 --select  / -s 
    - 假设有两个账号分别为A和B，A为默认账号，用上传文件操作举例：
    - `python3 main.py cli upload ./视频.mp4` 将本地的视频.mp4上传到A的根目录，因为A为默认账号，可以忽略--select选择账号参数
    - `python3 main.py cli --select B upload ./视频.mp4 /` 将本地的视频.mp4文件上传到B账号的OneDrive根目录
    
# 默认账号
将一个账号设置为默认账号后，可以快速操作这个账号

用一堆命令来举例：

先查看账号A的[目录A1]、[目录A2]的文件夹内容

再查看账号B的[目录B1]文件夹内容

- 没有默认账号的情况下：
    - `python3 main.py --select A cd /目录A1`
    - `python3 mian.py --select A ls`
    - `python3 main.py --select A cd /目录A2`
    - `python3 mian.py --select A ls`
    - `python3 main.py --select B cd /目录B1`
    - `python3 main.py --select B ls`
- 将账号A设置为默认账号的情况下：
    - `python3 main.py --select A default`
    - `python3 main.py cd /目录A1`
    - `python3 mian.py ls`
    - `python3 main.py cd /目录A2`
    - `python3 mian.py ls`
    - `python3 main.py --select B cd /目录B1`
    - `python3 main.py --select B ls`
        
省了很多次输入 -s / --select 参数，效果显著