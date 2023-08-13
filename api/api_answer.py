import requests

resp = requests.get(
    "http://localhost:5000/api/llamacpp",
    params={"question": "¿Cuál es la capital del Perú?"},
    stream=True,
)
for word in resp.iter_lines():
    print(word)
