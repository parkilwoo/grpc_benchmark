from fastapi import FastAPI, File, UploadFile
import uvicorn
import base64

app = FastAPI()

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    print(f"byte size: {len(contents)}")
    encoded_data = base64.b64encode(contents)
    return encoded_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)