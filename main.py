from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

def read_json_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON")

# Rota para obter informações do arquivo JSON
@app.get("/")
def get_aovivo_info():
    data = read_json_file('ao_vivo.json')
    return data

# Início do servidor com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
