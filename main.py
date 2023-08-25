import subprocess

api_llamita = subprocess.Popen(["python3", "api/api.py"])

api_llamita.wait()

print("All APIs stopped")
