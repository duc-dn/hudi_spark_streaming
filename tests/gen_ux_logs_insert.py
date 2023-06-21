from faker import Faker
from kafka import KafkaProducer
import json, time
import random
import string

device_os = ["IOS", "Android", "Windows", "Linux"]
timestamp = [1676687547526, 1677549864335, 1677482471687]

class Producer:
    def __init__(self):
        pass 

    def init_producer(self):
        producer = KafkaProducer(
            bootstrap_servers=['broker:9092'],
            value_serializer=self.json_serializer
        )
        return producer

    def generate_dummy_data(self, id: int):
        return {
            "collection": "logs63dc75d7d09feb313fae7a8a",
            "query": "insert",
            "data": {
                "ts": 1677648822041,
                "reqts": 1677648823403,
                "d": {
                "id": str(id),
                "p": "Windows",
                "pv": "mw10"
                },
                "l": {
                "cc": "Unknown",
                "cty": "Unknown"
                },
                "v": "0:0",
                "t": {
                "events": "[{\"key\":\"[CLY]_action\",\"count\":1,\"segmentation\":{\"type\":\"click\",\"x\":1316,\"y\":142,\"width\":1460,\"height\":1919,\"view\":\"/\",\"domain\":\"console-smartbot.vnpt.vn\",\"segment\":\"Windows\"},\"timestamp\":1677648821650,\"hour\":12,\"dow\":3}]"
                },
                "q": "{\"events\":[{\"key\":\"[CLY]_action\",\"count\":1,\"segmentation\":{\"type\":\"click\",\"x\":1316,\"y\":142,\"width\":1460,\"height\":1919,\"view\":\"/\",\"domain\":\"console-smartbot.vnpt.vn\",\"segment\":\"Windows\"},\"timestamp\":1677648821650,\"hour\":12,\"dow\":3}],\"app_key\":\"eec32c3dc543547ae0028ca1ac092241f3013e0a\",\"device_id\":\"2eb4c2f5-c1bd-4baa-abe3-da543b8c8868\",\"sdk_name\":\"javascript_native_web\",\"sdk_version\":\"22.06.0\",\"t\":\"1\",\"timestamp\":\"1677648822041\",\"hour\":\"12\",\"dow\":\"3\"}",
                "s": {
                "version": "22.06.0",
                "name": "javascript_native_web"
                },
                "h": {
                "host": "smartux-dev.icenter.ai",
                "x-request-id": "3dbcb61af5e5a6d3a34921408cec470f",
                "x-real-ip": "127.0.0.1",
                "x-forwarded-for": "127.0.0.1",
                "x-forwarded-host": "smartux-dev.icenter.ai",
                "x-forwarded-port": "443",
                "x-forwarded-proto": "https",
                "x-forwarded-scheme": "https",
                "x-scheme": "https",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
                "sec-ch-ua-mobile": "?0",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "sec-ch-ua-platform": "\"Windows\"",
                "accept": "*/*",
                "origin": "https://console-smartbot.vnpt.vn",
                "sec-fetch-site": "cross-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://console-smartbot.vnpt.vn/",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9"
                },
                "m": "GET",
                "b": False,
                "c": False,
                "res": {},
                "p": False
            }
        }

    @staticmethod
    def id_generator(
            size=24, chars=string.ascii_lowercase + string.digits
    ):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def json_serializer(data):
        return json.dumps(data).encode('utf-8')

    def generate_ux_data(self, init_index: int, topic: str, time_sleep: int):
        producer = self.init_producer()
        i = init_index
        while True:
            i += 1
            data = self.generate_dummy_data(i)
            print("============================================================")
            print(data)
            producer.send(topic=topic, value=data)
            time.sleep(time_sleep)

if __name__ == '__main__':
    producer = Producer()

    index = 0
    topic = "ux_data_insert_logs_collection"
    time_sleep = 10
    producer.generate_ux_data(index, topic, time_sleep)