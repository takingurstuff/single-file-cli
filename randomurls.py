import random

random.seed("pingas")
urls = []
for i in range(50):
    id = random.randint(25, 40000)
    urls.append(f"https://bbs.quantclass.cn/thread/{id}")


urlsfile = "\n".join(urls)

with open("urls.txt", "w") as f:
    f.write(urlsfile)
    f.close()
