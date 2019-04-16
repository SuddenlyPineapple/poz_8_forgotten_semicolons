# allepaczka

## Project setup
```
cd magic
conda env create
conda activate allegro
pip install -r requirements.txt
```
In different terminals type:
```
make run-back
make run-front
```

## Getting Running it in Different Mode - For Development

### Run Python server

Install Python Requirements - all are in requirements.txt file then:
```
python3 server.py mock.yml 0.0.0.0 6060
```
### Run npm development server with hot reloading:
In folder front type:
```
npm run serve
```

### API_Requests
```
/paczka_info?id=p0
/paczka_stan?id=p0
/paczki?user=u0
```

## Działanie (PL)

Kurier ma spisane paczki, na dany dzień. 

1. Kurier przyjeżdzą po paczkę. Rozpoznaje paczkę po pdf-ie który jest naklejony na paczkę.
2. Skanuje kod kreskowy na pdfie
3. Paczka zapala się na zielono w jego menu
4. User zaczyna mieć możliwość śledzenia go
5. Kiedy paczka dojeżdża, kierowca skanuje to po raz drugi i paczka jest usuwana 

## Screenshots

![Main Screen](https://imagizer.imageshack.com/img921/3783/GVvO9j.jpg)

![Package Screen](https://imagizer.imageshack.com/img923/97/GTj00v.jpg)

![Mobile Menu](https://imagizer.imageshack.com/img924/8789/yrlaPH.jpg)

## Authors

- Daniel Cieśliński
- Wojciech Kasperski
- Max Adamski
- Jakob Wolitzki
