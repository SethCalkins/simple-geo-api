# locustfile.py

from locust import Locust, TaskSet, task

class WebsiteTasks(TaskSet):
    def on_start(self):
#        self.client.post("/login", {
##            "username": "test_user",
#            "password": ""
#        })
        pass
    
    @task
    def phonenumber(self):
        self.client.get('/api/phonenumber/8005892634?country=US')
        
    @task
    def zip(self):
        self.client.get('/api/location/US/78745')
        
#    @task
#    def about(self):
#        self.client.get("/about/")

class WebsiteUser(Locust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000