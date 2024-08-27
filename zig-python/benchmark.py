import time
import requests
from urllib import request
import request_zig

url = "http://localhost"
n = 10000

start = time.time()
for i in range(n):
    req = request.urlopen(url)
    content = req.msg
end = time.time()
print("Only Python time: {}".format(end - start))

start = time.time()
for i in range(n):
    req = requests.get(url)
    content = req.text
end = time.time()
print("request Library time: {}".format(end - start))

start = time.time()
for i in range(n):
    req = request_zig.Request()
    content = req.get(url)
end = time.time()
print("Python/Zig time: {}".format(end - start))

