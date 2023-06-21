from faker import Faker
from kafka import KafkaProducer
import json, time
import random
import string

device_os = ["IOS", "Android", "Windows", "Linux"]
timestamp = [1677635068577, 1676942837, 1677549864335]
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
            "app_key": "fdd9ceb708fc45a039ec85c3d9e6b4b2e6a6982d",
            "device_id": "ee426f9b987bf444",
            "device_os": "Android",
            "device_model_name": "Samsung SM-G973F",
            "screenX": 1080,
            "screenY": 2168,
            "vc_appear_events": [
                {
                "vc_class_name": "LoginActivity",
                "selector_events": [],
                "multi_touches": [],
                "type": "activity"
                },
                {
                "vc_class_name": "z",
                "selector_events": [],
                "multi_touches": [],
                "type": "fragment"
                },
                {
                "vc_class_name": "SupportRequestManagerFragment",
                "selector_events": [],
                "multi_touches": [],
                "type": "fragment"
                },
                {
                "vc_class_name": "HomeActivity",
                "selector_events": [
                    {
                    "vc_class_name": "HomeActivity",
                    "selector_name": "com.vnptit.innovation.vnfaceremote:id/btn_check_in",
                    "time": 1677490503299,
                    "type": "clicked",
                    "view_frame": {
                        "height": 168,
                        "width": 978,
                        "x": 51,
                        "y": 1649
                    },
                    "instance_class_name": "MaterialButton"
                    }
                ],
                "multi_touches": [
                    {
                    "time": 1677490503297,
                    "touches": [
                        {
                        "id": 0,
                        "x": 348,
                        "y": 1722
                        }
                    ],
                    "type": "touch"
                    }
                ],
                "type": "activity"
                },
                {
                "vc_class_name": "SplashActivity",
                "selector_events": [],
                "multi_touches": [],
                "type": "activity"
                },
                {
                "vc_class_name": "VnptPortraitActivity",
                "selector_events": [
                    {
                    "vc_class_name": "VnptPortraitActivity",
                    "selector_name": "com.vnptit.innovation.vnfaceremote:id/viewCover",
                    "time": 1677490504634,
                    "type": "clicked",
                    "view_frame": {
                        "height": 2042,
                        "width": 1080,
                        "x": 0,
                        "y": 112
                    },
                    "instance_class_name": "View"
                    },
                    {
                    "vc_class_name": "VnptPortraitActivity",
                    "selector_name": "com.vnptit.innovation.vnfaceremote:id/viewCover",
                    "time": 1677490511997,
                    "type": "long_pressed",
                    "view_frame": {
                        "height": 2042,
                        "width": 1080,
                        "x": 0,
                        "y": 112
                    },
                    "instance_class_name": "View"
                    }
                ],
                "multi_touches": [
                    {
                    "time": 1677490504634,
                    "touches": [
                        {
                        "id": 0,
                        "x": 271,
                        "y": 1608
                        }
                    ],
                    "type": "touch"
                    },
                    {
                    "time": 1677490511994,
                    "touches": [
                        {
                        "id": 0,
                        "x": 266,
                        "y": 1644
                        }
                    ],
                    "type": "touch"
                    }
                ],
                "type": "activity"
                },
                {
                "vc_class_name": "HistoryActivity",
                "selector_events": [],
                "multi_touches": [],
                "type": "activity"
                },
                {
                "vc_class_name": "m",
                "selector_events": [],
                "multi_touches": [],
                "type": "fragment"
                },
                {
                "vc_class_name": "v",
                "selector_events": [],
                "multi_touches": [],
                "type": "fragment"
                }
            ],
            "screen_size": "Large",
            "_id": str(id)
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
    topic = "ux_data_heatmap_mobile_events63dc729ad09feb313fae7a85"
    time_sleep = 1
    producer.generate_ux_data(index, topic, time_sleep)