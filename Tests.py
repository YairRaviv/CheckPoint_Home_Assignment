import asyncio
import math
import time
from unittest import TestCase
import unittest
import requests
from threading import Thread




class TestDiGraph(TestCase):

    def Test(self):
        # ===========================================================> Test 1 <===================================================================

        requests.post("http://localhost/api/v1/events" , data="Avanan is a leading Enterprise Solution for Cloud Email and Collaboration Security")
        time.sleep(25)
        response = requests.get("http://localhost/api/v1/stats?interval=30").json()
        self.assertEqual(response['checkpoint'] , 0)
        self.assertEqual(response['avanan'], 1)
        self.assertEqual(response['email'], 1)
        self.assertEqual(response['security'], 1)
        time.sleep(6)
        response = requests.get("http://localhost/api/v1/stats?interval=30").json()
        self.assertEqual(response['checkpoint'], 0)
        self.assertEqual(response['avanan'], 0)
        self.assertEqual(response['email'], 0)
        self.assertEqual(response['security'], 0)

        # ===========================================================> Test 2 <===================================================================

        start = time.time()
        for i in range (0,10):
            requests.post("http://localhost/api/v1/events", data="checkpoinT")
        end = time.time()

        tmp_time = str(math.floor((end-start)+5))
        req = "http://localhost/api/v1/stats?interval="+tmp_time
        response = requests.get(req).json()
        self.assertEqual(response['checkpoint'], 10)
        self.assertEqual(response['avanan'], 0)
        self.assertEqual(response['email'], 0)
        self.assertEqual(response['security'], 0)
        time.sleep(int(tmp_time))
        response = requests.get(req).json()
        self.assertEqual(response['checkpoint'], 0)
        self.assertEqual(response['avanan'], 0)
        self.assertEqual(response['email'], 0)
        self.assertEqual(response['security'], 0)

        # ===========================================================> Test 3 <===================================================================

        start = time.time()
        for i in range(0,20):
            requests.post("http://localhost/api/v1/events", data="checkpoint is a cyber security provider , AVANAN , EMail")
        end = time.time()

        tmp_time = str(math.floor((end - start) + 5))
        req = "http://localhost/api/v1/stats?interval=" + tmp_time
        response = requests.get(req).json()
        self.assertEqual(response['checkpoint'], 20)
        self.assertEqual(response['avanan'], 20)
        self.assertEqual(response['email'], 20)
        self.assertEqual(response['security'], 20)
        time.sleep(int(tmp_time))
        response = requests.get(req).json()
        self.assertEqual(response['checkpoint'], 0)
        self.assertEqual(response['avanan'], 0)
        self.assertEqual(response['email'], 0)
        self.assertEqual(response['security'], 0)
        # ===========================================================> Test 4 <===================================================================

        thread_1 = Thread(target=post_function, args=("checkpoint",))
        thread_2 = Thread(target=post_function, args=("avanan",))
        thread_3 = Thread(target=post_function, args=("email",))
        thread_4 = Thread(target=post_function, args=("security",))

        start_time = time.time()
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()

        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()
        end_time = time.time()

        tmp_time = str(math.floor((end_time - start_time) + 5))
        req = "http://localhost/api/v1/stats?interval=" + tmp_time
        response = requests.get(req).json()
        self.assertEqual(response['checkpoint'], 5)
        self.assertEqual(response['avanan'], 5)
        self.assertEqual(response['email'], 5)
        self.assertEqual(response['security'], 5)
        time.sleep(int(tmp_time))
        response = requests.get(req).json()
        self.assertEqual(response['checkpoint'], 0)
        self.assertEqual(response['avanan'], 0)
        self.assertEqual(response['email'], 0)
        self.assertEqual(response['security'], 0)



def post_function(sentence):
    for i in range (0,5):
        requests.post("http://localhost/api/v1/events", data=sentence)



if __name__ == '__main__':
    asyncio.run(unittest.main())
