import json, base64, time, hashlib


header_data = {
    'alg': 'HS256',
    'typ': 'JWT',
}

header = base64.b64encode(json.dumps(header_data).encode()).decode()

iat = int(time.time())
payload_data =  {
    'sub': 'root',
    'exp': iat + 60 * 60,
    'iat': iat,
    'nbf': iat,
    'name': 'caoruchen',
    'admin': True,
}

payload = base64.b64encode(json.dumps(payload_data).encode()).decode()

# from django.conf import settings
# secret = settings.SECRET_KEY
secret = 'django-insecure-c@c@$(1)zocl++2o7a&ml6b=co(7dv2!u!#n9d6+sde$y83u+j'

jwt_data = header + payload + secret
hs256 = hashlib.sha256()
hs256.update(jwt_data.encode('utf-8'))
signature = hs256.hexdigest()

jwt_token = f'{header}.{payload}.{signature}'
print(jwt_token)

# validating
header, payload, signature = jwt_token.split('.')
payload_data = json.loads(base64.b64decode(payload.encode()))

exp = payload_data.get('exp', None)
if exp is not None and int(exp) + iat < int(time.time()):
    print("token expired")
else:
    print("token valid")

new_token = header + payload + secret
hs256 = hashlib.sha256()
hs256.update(new_token.encode('utf-8'))
new_signature = hs256.hexdigest()

if new_signature == signature:
    print("token correct")
else:
    print("fake token")
