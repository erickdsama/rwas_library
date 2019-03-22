from rwas import RWAS

rwas_service = RWAS() # class call
read = rwas_service.read()
print(read)
mensajes = read.parse_to_json()
# rwas_service.send(message="Hello world from mexico", remote_jid="5216562724890@s.whatsapp.net")
print(mensajes)