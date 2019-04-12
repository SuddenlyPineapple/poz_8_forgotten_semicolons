import yaml
from pprint import pprint


def mock():
    db = None
    with open("mock.yml") as file:
        try:
            db = yaml.load(file)
        except yaml.YAMLError as e:
            print('database exception', e)
    print(db)


if __name__ == '__main__':
    mock()
