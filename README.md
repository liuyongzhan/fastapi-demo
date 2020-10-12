### fastapi with peewee
#### version: v1.0.0


##### run app

```shell script
mkdir /data
cd /data
python3 -m venv fastapi_peewee
cd  fastapi_peewee
source bin/activate
(fastapi_peewee) git clone https://xxx.com/root/fastapi_peewee.git
(fastapi_peewee) cd fastapi_peewee
(fastapi_peewee) pip install -r requirements.txt
(fastapi_peewee) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-config=logging_config.ini
```


##### run celery

```shell script
(fastapi_peewee) celery -A app.celery_app worker -Q fastapi_default -l DEBUG
(fastapi_peewee) celery  -A app.celery_app worker -Q fastapi_long -l DEBUG
(fastapi_peewee) celery -A app.celery_app beat -l DEBUG
```

##### run test

```shell script
(fastapi_peewee) pytest

```

##### database init

```shell script
mysql> create database fastapi_demo charset utf8;
mysql> grant all on fastapi_demo.* to 'liuyz'@'%' identified by 'Zhian@2019';
```

##### database migrate

<https://github.com/aachurin/peewee_migrations>


##### run in docker
###### build image
```shell script
docker build -t fastapi_peewee_img -f dockerfile_web .
```
###### run image
```shell script
docker run -d --name fastapi_pwweww_demo --network host fastapi_peewee_img
```
