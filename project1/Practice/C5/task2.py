import requests
import json

r = requests.get('https://baconipsum.com/api/?type=meat-and-filler')
r = json.loads(r.content)
print(r)
print(r[0])
print(r[-1])
for a, b in enumerate(r):
    print(f'Текст номер {a+1}: {b[:20]}')
