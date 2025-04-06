import requests

def rc4_decrypt(data, key):
    s = list(range(256))
    j = 0
    key = [ord(c) for c in key]
    
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    
    i = j = 0
    result = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        t = (s[i] + s[j]) % 256
        result.append(byte ^ s[t])
    
    return bytes(result)

url="http://fetch.tasks.2025.ctf.cs.msu.ru/flag"
session = requests.Session()
session.max_redirects = 10000  
session.allow_redirects = True  

response = session.get(url, stream=True, timeout=10)

key = response.headers.get("X-Flag-Key")
   
encrypted_data = response.raw.read()
decrypted_data = rc4_decrypt(encrypted_data, key)


flag = decrypted_data.decode("utf-8")

print("Flag:", flag)
    
