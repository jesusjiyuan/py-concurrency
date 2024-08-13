import os.path

import uvicorn

from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
#产线禁用swagger
#app = FastAPI(docs_url=None,redoc_url=None)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def hello(token: str = Depends(oauth2_scheme)):
    return {"ret": 'hello',"token":token}

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    print(file)
    if not os.path.exists('uploaded_files'):
        os.mkdir('uploaded_files')
    with open(f"uploaded_files/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"uploaded_files/{filename}"
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


if __name__ == '__main__':
    uvicorn.run('fastapiserver:app', host='127.0.0.1', port=18005, reload=True)

