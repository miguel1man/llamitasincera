import subprocess

api_llamita = subprocess.Popen(["python", "api/api.py"])

api_llamita.wait()

print("All APIs stopped")
