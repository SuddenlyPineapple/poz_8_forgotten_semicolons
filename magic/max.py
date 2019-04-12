import yaml


def mock():
    with open("mock.db") as file:
        try:
            db = yaml.load(file)
        except yaml.YAMLError as e:
            print('database exception', e)
    print(db)


if __name__ == '__main__':
    mock()
