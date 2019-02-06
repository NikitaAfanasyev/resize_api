import requests
import unittest


class TestStringMethods(unittest.TestCase):

    def test_resizeWrongQuery(self):
        data={'height': 120 , 'imageName': 'lol.png'}
        r = requests.post("http://127.0.0.1:5000/resize", json=data)
        print(r.status_code, r.reason)
        self.assertEqual(r.status_code, 400)

    def test_uploadFile(self):
        f = open('test2.jpg', 'rb')
        files = {'file': f}
        r = requests.post('http://127.0.0.1:5000/imageUpload', files=files)
        f.close()
        print(r.status_code, r.reason)
        self.assertEqual(r.status_code, 200)

    def test_resizeGoodQuery(self):
        data={'height': 120 , 'width':300, 'imageName': 'test2.jpg'}
        r = requests.post("http://127.0.0.1:5000/resize", json=data)
        print(r.status_code, r.reason)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('jobID' in str(r.content))

    def test_getStatus(self):
        r = requests.get('http://127.0.0.1:5000/getStatus?jobID=1')
        print(r.status_code, r.reason)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('status' in str(r.content))

    
        

if __name__ == '__main__':
    unittest.main()
