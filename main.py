import subprocess

api_chat_llama = subprocess.Popen(["python3", "api/api_chat_llama.py"])
api_upload_files = subprocess.Popen(["python3", "api/api_upload_files.py"])
api_similar_embeddings = subprocess.Popen(["python3", "api/api_similar_embeddings.py"])

api_chat_llama.wait()
api_upload_files.wait()
api_similar_embeddings.wait()

print("All APIs stopped")
