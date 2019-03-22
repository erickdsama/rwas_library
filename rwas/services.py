import time

from threading import Thread

from .rwas import RWAS


class InService(Thread):

    def __init__(self):
        self.rwas = RWAS()
        super(InService, self).__init__()

    def _get_messages(self):
        messages = self.in_meesages()
        for idx, message in enumerate(messages):
            if type(message) is not dict:
                raise self.InvalidMessage
            messages[idx]["message"] = self.extras_message(message.get("message"))
        return messages

    def in_meesages(self):
        return []

    def extras_message(self, message):
        return message

    def run(self):
        while True:
            messages = self._get_messages()
            for message in messages:
                self.rwas.send(message=message.get("message"), remote_jid=message.get("number"))
            time.sleep(5)
            break

    class InvalidMessage(Exception):
        pass


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
