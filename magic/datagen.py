import json
import yaml
from pprint import pprint
import requests
import random
import googlemaps
from faker import Faker
from datetime import datetime

fake = Faker('pl_PL')


class Generate:
    def __init__(self):
        self.pack_id = 0
        self.x = 52.010440
        self.y = 21.129723
        self.key = 'AIzaSyCkF7rIDbq8WFxWv8i09_dpeTkf1ueXwRA'
        self.users = {}
        self.packs = {}
        self.product = [
            {
                'id': 'i0',
                'name': 'LEGO CITY 60206 Policyjny patrol',
                'url': 'https://allegro.pl/oferta/lego-city-60206-policyjny-patrol-7764308125',
                'img': 'https://3.allegroimg.com/original/014e4e/22bdd5c545d795a31cb134438823/LEGO-CITY-60206-Policyjny-patrol',
            },
            {
                'id': 'i1',
                'name': 'Zestaw z maszynką do golenia Gillette Mach3',
                'url': 'https://allegro.pl/oferta/zestaw-z-maszynka-do-golenia-gillette-mach3-zel-7968767514?bi_s=strk_specjalna_sg_pion&bi_c=Licytacje&',
                'img': 'https://6.allegroimg.com/original/0080d6/8c255ba24701b88b1c051fc8eb26/Zestaw-Gillette-X-mass-81675185/Zestaw-z-maszynka-do-golenia-Gillette-Mach3-zel',
            },
            {
                'id': 'i2',
                'name': 'MacBook Pro 15 Core i7',
                'url': 'https://allegro.pl/oferta/macbook-pro-15-core-i7-2-5ghz-16-512-gt750-2014-7795075067?reco_id=541adc33-5db9-11e9-8dea-246e96320fe8&sid=214dee23af5dacba6db9ec985d2421ccbc3b0218e9654c1f9eeca650c7d606e7',
                'img': 'https://d.allegroimg.com/original/03b22e/7e0fdf8d4abaafb957abd050e1cd/MacBook-Pro-15-Core-i7-2-5GHz-16-512-GT750-2014',
            },
            {
                'id': 'i3',
                'name': 'Statyw POLAROID 183cm',
                'url': 'https://allegro.pl/oferta/statyw-polaroid-183cm-t72-canon-nikon-sony-gratis-7845334847?reco_id=7ed34abb-5db9-11e9-89b2-000af7f61ef0&sid=214dee23af5dacba6db9ec985d2421ccbc3b0218e9654c1f9eeca650c7d606e7',
                'img': 'https://1.allegroimg.com/original/069079/c98a79374c9aa86c46666a2ba6a1/Statyw-POLAROID-183cm-T72-Canon-Nikon-Sony-GRATIS',
            },
            {
                'id': 'i4',
                'name': 'Smartfon Apple iPhone XS Max złoty 256 GB',
                'url': 'https://allegro.pl/oferta/iphone-xs-max-256-gb-nowy-7976779097?reco_id=94bfa021-5db9-11e9-9530-6c3be5c06da0&sid=214dee23af5dacba6db9ec985d2421ccbc3b0218e9654c1f9eeca650c7d606e7',
                'img': 'https://c.allegroimg.com/original/03594d/d73ca2324857b68cd12ca9afa1cc/IPHONE-XS-MAX-256-GB-NOWY',
            },
        ]

    def gen_product(self):
        return random.choice(self.product)

    def gen_route(self):
        route = []
        i = 0
        number = random.randint(2, 5)
        while i < number:
            try:
                location = {}
                fake_address = fake.address()
                full_name = fake_address.replace('\n', ' ')
                fake_address = fake_address.split('\n')
                address = fake_address[0]
                location['addr'] = address
                location['code'] = fake_address[1].split(' ')[0]
                location['city'] = fake_address[1].split(' ')[1]
                link = f'https://maps.googleapis.com/maps/api/geocode/json?address={full_name}&key={self.key}'
                x = requests.get(link)
                data = x.json()
                location['cord'] = [data['results'][0]['geometry']['location']['lat'],
                                    data['results'][0]['geometry']['location']['lng']]
                location['date'] = datetime.now()
                i += 1
                route.append(location)
            except:
                continue
        return route

    def gen_packs(self, user_id, number):
        for i in range(number):
            self.packs[f'p{self.pack_id}'] = {
                'user_id': user_id,
                'product': self.gen_product(),
                'route': self.gen_route(),
                'date_sent': datetime.now(),
                'curr_state': True,
                'curr_route': 0,
            }
            self.pack_id += 1

    def gen_users(self, number):
        for i in range(number):
            number_of_packs = random.randint(5, 5)
            self.users[f'u{i}'] = {
                'name': fake.name(),
                'pack': [f'p{self.pack_id + i}' for i in range(number_of_packs)]
            }
            self.gen_packs(i, number_of_packs)


def main():
    gen = Generate()
    gen.gen_users(1)
    base = {
        'users': gen.users,
        'packs': gen.packs
    }
    with open('data_dump.yml', 'w') as f:
        yaml.dump(base, f)


if __name__ == "__main__":
    main()
