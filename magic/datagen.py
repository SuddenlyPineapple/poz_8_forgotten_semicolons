import json
from pprint import pprint
import requests
import random
import googlemaps
from faker import Faker
fake = Faker('pl_PL')


class Generate:
    def __init__(self):
        self.pack_id = 0
        self.x = 52.010440
        self.y = 21.129723
        self.gmaps = googlemaps.Client(
            key='AIzaSyCkF7rIDbq8WFxWv8i09_dpeTkf1ueXwRA')


    def gen_product_name(self):
        return 'product name'

    def gen_route(self):
        data = fake.address().split('\n')
        addres = data[0]
        f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={self.gmaps}'

    def gen_packs(self, user_id):
        number = random.randint(1, 6)
        packs = {}
        for i in range(number):
            packs[self.pack_id] = {
                'user_id': user_id,
                'product': self.gen_product_name(),
                'route': self.gen_route(),
            }
            self.pack_id += 1

    def gen_users(self, number):
        users = {}
        for i in range(number):
            users[i] = {
                'name': fake.name(),
                'pack': self.gen_packs(i),
            }


# data = fake.address().split('\n')
# addres = data[0]
# code = data[1].split(' ')[0]
# city = data[1].split(' ')[1]
# print(addres, ' ', code, ' ', city)

# with open('data.json', 'w') as file:
#     users = {}
#     packs = {}
#     users.update(packs)
#     json.dump(users, file)


# x_plus = random.randint(0, 1)
# y_plus = random.randint(0, 1)
# x_value = random.uniform(0, 100)
# # if x_plus:
# print(x_plus, y_plus, x_value/100)


data = fake.address().replace('\n', ' ')
address = data
key='AIzaSyCkF7rIDbq8WFxWv8i09_dpeTkf1ueXwRA'
link = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}'

x = requests.get(link)
data = x.json()
pprint(data['results'][0]['geometry'])

