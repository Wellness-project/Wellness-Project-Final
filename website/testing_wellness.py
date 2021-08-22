"""
This file tests the Wellness Project:
* Response testing - if the HTML response status is 200
* Content testing - if it returns a HTML template
"""



try:
    from main import app
    import unittest

except Exception as e:
    print("Some modules are missing {}".format(e)) #would explain what is missing

class FlaskTest(unittest.TestCase):
    #checks if /mood is a response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/mood")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #checks to see if the content that is being returned is a html-utf-8 in the /mood.
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/mood")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
    if __name__=="__main__":
        unittest.main()

#
class FlaskTest2(unittest.TestCase):
    #checks if /external_resources is a response 200
    def test_index2(self):
        tester = app.test_client(self)
        response = tester.get("/external_resources")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    #checks to see if the content that is being returned is a html-utf-8 in the external_resources.
    def test_index_content2(self):
        tester = app.test_client(self)
        response = tester.get("/external_resources")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    if __name__=="__main__":
        unittest.main()


class FlaskTest3(unittest.TestCase):
    #checks if / is a response 200
    def test_index3(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    if __name__=="__main__":
        unittest.main() #returns a 302 error. This is because this page is meant to redirect to another host, so it will not show a 200.

    # #checks to see if the content that is being returned is a html-utf-8 in the /.
    def test_index_content3(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    if __name__=="__main__":
        unittest.main()
