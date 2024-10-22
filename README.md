# Uzinfocom Task

Bul proyekt Flask-ke tiykarlanǵan autentifikaciya sisteması bolıp, paydalanıwshılar dizimnen ótiw hám júyege kiriw ushın bir mártelik parolden (OTP) paydalanadı. Ol paydalanıwshılardı telefon nomeri hám OTP kodları járdeminde qáwipsiz dizimnen ótiw hám júyege kiriw mexanizmlerin usınıs etedi.

## Content:
 - [**Features**](#imkaniyatlar)
 - [**Environment variables**](#ózgeriwshiler-env)
 - [**Technologies used**](#paydalanılǵan-texnologiyalar)
 - [**Running the project**](#proyektti-iske-túsiriw)
   - [Virtual Environment](#virual-ortalıq)
   - [Installing libraries](#sırtqı-paketlerdi-ornatıw)
   - [Installing Gunicorn](#gunicorndı-ornatıw)
   - [Running](#proyektti-júrgiziw)
 - [**Documentation**]

## Imkaniyatlar
 - OTP tastıyıqlaw járdeminde dizimnen ótiw
 - OTP tastıyıqlaw járdeminde júyege kiriw
 - JWT járdeminde tokenge tiykarlanǵan qáwipsizlik
 - OTP eskiriwi hám qayta paydalanıwǵa jol qoymaw
 - SMS xabarlardı Redis járdeminde nawbetke qoyıw

## Ózgeriwshiler `.env`
 - `SECRET_KEY`: Flask ushın jasırın sóz
 - `DATABASE_URL`: Maǵlıwmatlar bazası ushın URL
 - `ESKIZ_EMAIL`: Eskiz ushın email
 - `ESKIZ_PASSWORD`: Eskis ushın jasırın parol

## Paydalanılǵan texnologiyalar
 - **Flask**: Web framework
 - **Flask-JWT-Extended**: JWT token menen islesiw
 - **SQLAlchemy**: Databazanı basqarıw ushın ORM
 - **Redis**: SMS xabarlardı waqtınshalıq saqlaw ushın
 - **PostgreSQL**: Maǵlıwmatlar bazası

---

# Proyektti iske túsiriw
## Virual Ortalıq
Virtual ortalıqtı jaratıw:
```shell
python -m venv venv
```
Virtual ortalıqtı aktivlestiriw
```shell
source venv/bin/activate

# Windows ushın
.\venv\Scripts\activate
```
## Sırtqı paketlerdi ornatıw
```shell
pip install -r requirements.txt
```
## Gunicorndı ornatıw:
```shell
pip install gunicorn
```
## Proyektti júrgiziw
```shell
gunicorn --bind 0.0.0.0:8080 app:app
```

---

# Documentaciya
API haqqında dokumentaciyanı (Swagger-UI) kóriw ushın `/apidocs/` endpointına shaqırıq etiń.