import threading
import time
import random



def f(*args, **kwargs):
  n = args[0]
  time.sleep(random.random()/9)
  print(f"I am {n}")




max_threads = 20
s = list(range(1,453))


threads = []


st = time.monotonic()
while s:
  x = s.pop(0)
  p = threading.Thread(target=f, args=(x,), kwargs={'kw1': 1, 'kw2': '2'})
  p.start()
  threads.append(p)
  if len(threads) >= max_threads:
    t = threads.pop(0)
    t.join()

while threads:
    t = threads.pop(0)
    t.join()
  

print(f"{time.monotonic() - st}")

