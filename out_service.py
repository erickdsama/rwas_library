import time
from threading import Thread

from rwas import RWAS


class OutService(Thread):

    def __init__(self):
        self.rwas = RWAS()
        super(OutService, self).__init__()

    def validate(self, message=None):
        return message

    def out_request(self, message):
        pass

    def run(self):
        while True:
            messages = self.rwas.read().parse_to_dict()
            for message in messages.get("messages"):
                print(message.get("message"))

                if self.validate(message=message):
                    self.out_request(message)

            time.sleep(5)
