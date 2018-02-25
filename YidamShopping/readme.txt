
初始化操作步骤
1、创建名为yidam的utf-8数据库


2、初始化数据库

python manage.py makemigrations


python manage.py migrate


3、加载初始化admin数据
python manage.py loaddata user.json

