import requests

resp = requests.get(
    "http://localhost:5001/api/ask-llama",
    params={"question": "¿Cuándo se independizó el Perú?"},
    stream=True,
)
for word in resp.iter_lines():
    print(word)
