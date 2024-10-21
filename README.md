# Uzinfocom Task

Bul proyekt Flask-ke tiykarlanǵan autentifikaciya sisteması bolıp, paydalanıwshılar dizimnen ótiw hám júyege kiriw ushın bir mártelik parolden (OTP) paydalanadı. Ol paydalanıwshılardı telefon nomeri hám OTP kodları járdeminde qáwipsiz dizimnen ótiw hám júyege kiriw mexanizmlerin usınıs etedi.

## Imkaniyatlar
 - OTP tastıyıqlaw járdeminde dizimnen ótiw
 - OTP tastıyıqlaw járdeminde júyege kiriw
 - JWT járdeminde tokenge tiykarlanǵan qáwipsizlik
 - OTP eskiriwi hám qayta paydalanıwǵa jol qoymaw
 - SMS xabarlardı Redis járdeminde nawbetke qoyıw

## Ózgeriwshiler `.env`
 - `SECRET_KEY`: Flask ushın jasırın gilt sóz
 - `DATABASE_URL`: Maǵlıwmatlar bazası ushın URL
 - `ESKIZ_EMAIL`: Eskiz ushın email
 - `ESKIZ_PASSWORD`: Eskis ushın jasırın parol

## Paydalanılǵan texnologiyalar
 - **Flask**: Web framework
 - **Flask-JWT-Extended**: JWT token menen islesiw
 - **SQLAlchemy**: Databazanı basqarıw ushın ORM
 - **Redis**: SMS xabarlardı waqtınshalıq saqlaw ushın
 - **PostgreSQL**: Maǵlıwmatlar bazası

