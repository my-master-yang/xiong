<<<<<<< HEAD
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
=======
# xiong
20180723 -->2018730
# xiong
20180723 --->2018730 git add .     git commit -m "xiong"  git push     (push  分三步,1 用git add . 添加到工作状态树,2本次提交描述,3上传)
 
 下载:pull clone git@github.com:my-master-yang/xiong
 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8/1+drGU09A7rWiwv/IAoIFpXheX3zCMJjAGCm8clMkg/UXHWHHIzXg+yrVQBzhJjWtcvRF+MrDk6C1ZzBSNa3l9vSgbwEjuJyjF0XQAcV51PAYQjNI19L7GwLvi7f4BIlLc6CTMXyrUAqgf2d/rqgD1356Eous74ebd4D4phP95WT9Ff2s7k519scHnLiIoxQ5NiRl9a853z1AsXyZ7+yPUyBWD9XMOwNC8zjJtVb4Bdi0yAiDO2AfkfKL6s0gZEgU8+hp7Mp3GOjnf/hcA6BHZmxdEdBAT0LWFKHYc3IxTiBH/X7dUgg08XwQtqQa5dCs4+tCpXthm+Ko4K9FuV 3079362259@qq.com
~               
>>>>>>> 28ecf0be2c11a614f10bc36436d2ed80ad9e9065
