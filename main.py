import subprocess

api_1 = subprocess.Popen(["python3", "api/api_upload_files.py"])
api_2 = subprocess.Popen(["python3", "api/api_chat_llama.py"])

api_1.wait()
api_2.wait()

print("All APIs stopped")
