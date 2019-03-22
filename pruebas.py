# coding=utf-8

from in_service import InService
from out_service import OutService


class Entrada(InService):

    def in_meesages(self):
        messages = [
            # {
            #     "message": "hola como estas ?",
            #     "number": "5216562724890@s.whatsapp.net"
            # },
            # {
            #     "message": "bien y tú ?",
            #     "number": "5216562724890@s.whatsapp.net"
            # },
            # {
            #     "message": "bien también?",
            #     "number": "5216562724890@s.whatsapp.net"
            # }

        ]
        return messages

    def extras_message(self, message):
        return "mensaje enviado desde RWAS: {}".format(message)


class Salida(OutService):

    def out_request(self, message):
        print("como que voy a un servicio con mi mensaje", message)

    def validate(self, message=None):
        if message:
            message_str = message.get("message")
            if message_str == "hola":
                return message
        return None

# inse = Entrada()
# inse.run()
sale = Salida()
sale.run()