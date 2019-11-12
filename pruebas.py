# coding=utf-8
from rwas.services import InService, OutService


class PruebaEntrada(InService):

    def in_meesages(self):
        messages = [
            {
                "message": "hola proyecto",
                "number": "5216562724890@s.whatsapp.net"
            }
        ]
        return messages

    def extras_message(self, message):
        return "mensaje enviado desde RWAS: {}".format(message)


in_service = PruebaEntrada()
in_service.run()


class Salida(OutService):

    _co = "lklklk"

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
#print(sale._co)


