import models

data=models.API.select().where(models.API.user=="amir")
for item in data:
    print(item.name)
    