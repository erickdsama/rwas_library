import json


class Config:
    def __init__(self, **entries):
        self.__dict__.update(entries)


with open('../rwas_config.json') as json_data_file:
    data = json.load(json_data_file)
    print(data)
    # data = {"a": "a"}
    config = Config(**data)

    print(config.emulators)