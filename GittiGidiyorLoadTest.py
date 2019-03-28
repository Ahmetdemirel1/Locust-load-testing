from locust import HttpLocust, TaskSet, task, seq_task
from bs4 import BeautifulSoup
import random



list = []



class GittiGidiyor(TaskSet):

    @task
    def home(self):
        self.client.get("https://www.gittigidiyor.com/")


    @task
    def search(self):
        search_key_list = ['telefon', 'bilgisayar']
        search_key = random.choice(search_key_list)
        response = self.client.get("https://www.gittigidiyor.com/arama/?k=" + search_key + "")

        pq = BeautifulSoup(response.content, "html.parser")
        for link in pq.find_all("ul", attrs={"class": "catalog-view clearfix products-container"}):
            list.append(link.li.a["href"])

        global product_link
        product_link = random.choice(list)
        print("href :" + product_link)


    @task
    def product_page(self):
        response = self.client.get("https:" + product_link)

        pq = BeautifulSoup(response.text)
        global productId, productNumber
        productId = pq.find('input', attrs={'name': 'id'}).get('value')
        productNumber = pq.find('input', attrs={'name': 'adet'}).get('value')



    @task
    def add_to_cart(self):
        self.client.post("https://www.gittigidiyor.com/sepete-ekle", {"id": productId, "adet": productNumber})

        response = self.client.get("https://www.gittigidiyor.com/sepetim/")
        pq = BeautifulSoup(response.text)
        price = pq.find('a', attrs={'class': 'title-link'})
        print("sepet:" + price.h2.text)





class LoginUser(HttpLocust):
    task_set = GittiGidiyor
    min_wait = 5000
    max_wait = 9000