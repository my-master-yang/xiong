# netsec0.2

> requirement: Ubuntu & python3.6

开发环境部署方法：
1. 安装`python3.6`和`pip`，配置软件源
2. 安装`pipenv`：`pip install pipenv --user`，`--user`是安装在用户目录下，是官方推荐的方式，如果安装后找不到`pipenv`，请将`pipenv`的目录添加到系统路径中
3. `sudo apt install python3-dev libmysqlclient-dev`
4. 安装依赖`pipenv install`
5. 安装其他库使用`pipenv install XXX`
6. 修改`/etc/hosts`文件，添加 `192.168.89.11  controller`

目录结构：
```
- netsec
    - apps
        - courses # 课程
        - examination # 考试
        - experiment # 实验
        - openstack_netsec # OpenStack相关
        - users # 用户
    - extra_apps
    - media
    - netsec
    - static
    - templates
```
