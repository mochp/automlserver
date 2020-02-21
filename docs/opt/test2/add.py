from tasks import add
import time

for i in range(1000):
    if i%100==0:
        print(i,end=";")
    result = add.delay(4, 4)
