<h2>简介</h2>
鉴于系统较多，每个系统都需要账号密码，独立一套用户系统。
<h2>特性</h2>
支持Google动态口令

支持SSO，一次登录多站点登录
<h2>项目地址</h2>
GITHUB:<a href="https://github.com/SRELabs/passport">https://github.com/SRELabs/passport</a>
<h2>快速开始</h2>
<h3>安装</h3>
<pre class="lang:default decode:true ">cd /home/cloudsa/
mkdir passport.cloudsa.org
git clone git@github.com:SRELabs/passport.git passport.cloudsa.org</pre>
<h3>安装pip依赖</h3>
<pre class="lang:default decode:true">cd passport.cloudsa.org
pip install -r requirements.txt</pre>
<h3>修改配置文件</h3>
<pre class="lang:default decode:true">mv archer/settings.py.sample archer.setting.py</pre>
如果你使用sqlite3，数据库配置默认即可。如果想使用MySQL，那么请将配置文件中的mysql改为default即可。

vim archer/settings.py
<pre class="lang:default decode:true">DATABASES = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'archer_user',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'data/main.db'
    }
}</pre>
启用OTP动态口令
<pre class="lang:default decode:true">ARCHER_ENABLE_OTP = True # False关闭</pre>
<h3>初始化数据</h3>
<pre class="lang:default decode:true">python manage.py migrate</pre>
<h3>创建管理员账户</h3>
<pre class="lang:default decode:true "># python manage.py createsuperuser
Username (leave blank to use 'root'): cloudsa
Email address: admin@cloudsa.org
Password:
Password (again):
Superuser created successfully.</pre>
<h3>启动</h3>
<pre class="lang:default decode:true ">python manage.py runserver</pre>
<h2>更新日志</h2>
2017-05-13

&nbsp;

&nbsp;
