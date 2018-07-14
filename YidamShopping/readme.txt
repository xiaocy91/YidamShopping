
亿达购物商城环境搭建


1、安装python
python-2.7.11.msi安装到E:\Program Files\python2.7; 添加环境变量E:\Program Files\python2.7到path中；

2、安装第三方库pip
E:\zhengliYidam\pip-9.0.1\pip-9.0.1>python setup.py install


3、在Eclipse中安装pydev插件
启动Eclipse, 点击Help->Install New Software，点Add 按钮。  Name中填:Pydev,  Location中填http://pydev.org/updates。  只选PyDev选项。


4、eclipse配置python路径
window-prefereces-pydev-Interpreter-python interpreter配置python.exe路径；


5、打开pydev窗口
window-perspective-open perspective-other-PyDev打开pydev的窗口


6、安装第三方库Django
E:\zhengliYidam\Django-1.9.13\Django-1.9.13>python setup.py install


7、创建Django项目
创建django项目，new-other-PyDev-PyDev Django Project

问题：此时提示Django not found，重新配置下python.exe，即window-prefereces-pydev-Interpreter-python interpreter配置python.exe路径


8、安装mysql
8.1、安装mysql第三方库，双击MySQL-python-1.2.5.win32-py2.7.exe


8.2、初始化操作步骤
8.2.1、创建名为yidam的utf-8数据库


8.2.2、初始化数据库

python manage.py makemigrations


python manage.py migrate


8.2.3、加载初始化admin数据
python manage.py loaddata user.json




9、安装python图片处理PIL/Pillow
解决Python图片处理模块pillow使用，安装PIL-1.1.7.win32-py2.7.exe
说明：PIL（Python Imaging Library）是Python常用的图像处理库，而Pillow是PIL的一个友好Fork



10、运行Django项目
运行manage.py，参数为runserver  0.0.0.0:8080


11、部署阿里云
部署在阿里云上，启动项目的方法 

11.1、查看ip
[root@iZ2ze23w0nyvm3rd82zgqlZ ~]# ifconfig
eth0      Link encap:Ethernet  HWaddr 00:16:3E:0A:BD:B8  
          inet addr:172.17.176.77  Bcast:172.17.191.255  Mask:255.255.240.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:856 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1049 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:134007 (130.8 KiB)  TX bytes:151741 (148.1 KiB)

[root@iZ2ze23w0nyvm3rd82zgqlZ YidamShopping]# cd YidamShopping/

11.2、将ip添加到settings中
root@iZ2ze23w0nyvm3rd82zgqlZ YidamShopping]# vi settings.py
ALLOWED_HOSTS = [u'39.106.26.41',u'127.0.0.1',u"172.17.176.77"]

11.3、启动ip和端口
[root@iZ2ze23w0nyvm3rd82zgqlZ YidamShopping]# python manage.py runserver 172.17.176.77:8080
0 errors found
June 30, 2018 - 16:35:46
Django version 1.6.11, using settings 'YidamShopping.settings'
Starting development server at http://172.17.176.77:8080/
Quit the server with CONTROL-C.

11.4、启动数据库
[root@iZ2ze23w0nyvm3rd82zgqlZ ~]# msyql status
-bash: msyql: command not found
[root@iZ2ze23w0nyvm3rd82zgqlZ ~]# service mysqld status
mysqld is stopped
[root@iZ2ze23w0nyvm3rd82zgqlZ ~]# service mysqld start
Starting mysqld:  [  OK  ]

11.5、初始化数据库中admin用户
11.5.1、在fixtures下添加一个user.json文件
[
  {
    "model": "user_center.Userinfo",
    "pk": 1,
    "fields": {
      "Account": "admin",
      "Password": "admin",
      "Phone": "123",
      "Nickname": "xiao",
      "Headphoto": "123",
      "Email": "2122"
    }
  }
]
11.5.2、在settings.py中添加FIXTURE_DIRS= (os.path.join(BASE_DIR, 'fixtures',).replace('\\', '/'),)
11.5.3、执行命令loaddata来初始化数据
E:\DjangoEclipseSpance\YidamShopping>python manage.py loaddata user
Installed 1 object(s) from 1 fixture(s)



