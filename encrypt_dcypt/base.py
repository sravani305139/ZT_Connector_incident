import base64
encoded = base64.b64encode(('data to be encoded').encode('utf-8'))
data = base64.b64decode(encoded.decode("utf-8"))
print(encoded)
print(data)
