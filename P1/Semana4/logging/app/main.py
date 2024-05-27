from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

app = FastAPI()

# Configurando o logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LogMessage(BaseModel):
    message: str

@app.post("/log/")
async def log_message(log_message: LogMessage):
    """
    Rota para receber mensagens de log e registrar no arquivo 'app.log'.
    """
    try:
        # Registrando a mensagem de log
        logging.info(log_message.message)
        return JSONResponse(status_code=200, content={"message": "Log registrado com sucesso"})
    except Exception as e:
        logging.error(f"Erro ao registrar o log: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Erro ao registrar o log"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
