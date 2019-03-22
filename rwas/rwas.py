# coding=utf-8
import json
import time

from subprocess import check_output, CalledProcessError
from .columns import COLUMN


class WHO:
    FROM_ME = "key_from_me == 1"
    OTHERS = "key_from_me != 1"
    ALL = ""


class TYPE:
    GPS = 1
    IMAGE = 2
    TEXT = 3


class RWAS:
    """Rest WhatsApp Application Service

    Class to read and write messgaes directly to an android device [Sqlite3 is needed]

    Args:
        emulator (str): ID from your Android device, can be an Android phone or a Emulator with Sqlite3 installed.

    Note:
        if you only use one Device is not necesary pass the 'emulator' arg, It will be detected automatically
    """

    def __init__(self, emulator=None):
        self.emulator = emulator

    def rwas_check_output(self, last_id=None, who=None):
        if last_id is None:
            query_str = " WHERE {}".format(who) if (who != WHO.ALL) else ""
        else:
            query_str = " AND {}".format(who) if (who != WHO.ALL) else ""
            query_str = "WHERE _id>{} {}".format(last_id, query_str)
        if self.emulator is None:
            return check_output(
                "adb shell 'sqlite3 /data/data/com.whatsapp/databases/msgstore.db \"select * from messages {};\"'".format(
                    query_str), shell=True)
        else:
            return check_output(
                "adb -s {} shell 'sqlite3 /data/data/com.whatsapp/databases/msgstore.db \"select * from messages {};\"'".format(
                    self.emulator, query_str), shell=True)

    def read(self, last_id=None, who=WHO.OTHERS):
        """ Method to read the messages from the database of whatsapp
        
        Args:
            last_id (int): The last _id that do u want
            who (WHO): Whos the message emitter          

        Note:
            if you don't pass tha last_id param, returns all messages

        Returns:
            DATA if successful, None otherwise. 
        """
        try:
            return self.DATA(self.rwas_check_output(last_id=last_id, who=who))
        except CalledProcessError as e:
            return None

    def send(self, message=None, location=None, remote_jid=None):
        build_message = self.BuildMessage(message=message, location=None, remote_jid=remote_jid)
        print(build_message.chat_string)
        try:
            print(check_output("adb shell pkill com.whatsapp", shell=True))
            print(check_output("adb shell chmod 777 /data/data/com.whatsapp/databases/msgstore.db", shell=True))
            print(check_output(build_message.chat_string, shell=True))
            print(check_output(build_message.list_string, shell=True))
            print(check_output(build_message.update_string, shell=True))
            print(check_output("adb shell am start -n com.whatsapp/.Main", shell=True))
        except CalledProcessError as e:
            print(e)

    class DATA:
        _dumped = None

        def __init__(self, dumped=None):
            self._dumped = dumped

        def __repr__(self):
            return "data {}, length={}".format(self.__class__.__name__, len(self._parse_to_array()))

        def _parse_to_array(self):
            fields = []
            rows = self._dumped.split("|\n")
            del rows[-1]
            for row in rows:
                elements = row.split("|")
                fields.append(elements)
            return fields

        def parse_to_dict(self, **kwargs):
            array = self._parse_to_array()
            messages = []
            for row in array:
                data = {
                    "_id": row[COLUMN.id],
                    "message": row[COLUMN.message],
                    "latitude": row[COLUMN.latitude],
                    "longitude": row[COLUMN.longitude],
                    "med_du": row[COLUMN.media_duration],
                    "key_remote_jid": row[COLUMN.key_remote_jid],
                }
                messages.append(data)
            data = {
                "messages": messages
            }
            return data

        def parse_to_json(self):
            """ Convert the data to JSON object
                Returns:
                    A Json object of the data fetched
            """
            return json.dumps(self.parse_to_dict(), ensure_ascii=False)

    class BuildMessage:

        def __init__(self, message=None, location=None, remote_jid=None):
            self.location = location
            self.message = message
            self.remote_jid = remote_jid

        @property
        def chat_string(self):
            """str: Chat string query to insert """
            l1 = int(round(time.time() * 1000))
            l2 = int(l1 / 1000)
            k = "-1150867590"
            return """adb shell "sqlite3 /data/data/com.whatsapp/databases/msgstore.db \\"INSERT INTO messages (key_remote_jid, key_from_me, key_id, status, needs_push, data, timestamp, MEDIA_URL, media_mime_type, media_wa_type, MEDIA_SIZE, media_name , latitude, longitude, thumb_image, remote_resource, received_timestamp, send_timestamp, receipt_server_timestamp, receipt_device_timestamp, raw_data, media_hash, recipient_count, media_duration, origin) VALUES ('{}', 1,'{}-{}', 0,0, '{}',{},'','', 0, 0,'', 0.0,0.0,'','',{}, -1, -1, -1,0 ,'',0,0,0);\\""
            """.format(self.remote_jid, l2, k, self.message, l1, l1)

        @property
        def list_string(self):
            """str: List chat query to insert """
            return """ adb shell "sqlite3 /data/data/com.whatsapp/databases/msgstore.db \\"insert into chat_list (key_remote_jid) select '{0}' where not exists (select 1 from chat_list where key_remote_jid='{0}');\\"" """.format(
                self.remote_jid)

        @property
        def update_string(self):
            """str: List chat query to update based on list insert """
            return """ adb shell "sqlite3 /data/data/com.whatsapp/databases/msgstore.db \\"update chat_list set message_table_id = (select max(messages._id) from messages) where chat_list.key_remote_jid='{}';\\"" """.format(
                self.remote_jid)
