import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from sketcher import classic_sketch

app = FastAPI(title="Photo to Sketch")


@app.post("/sketch")
async def sketch(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    img.thumbnail((1024, 1024))
    out = classic_sketch(img)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


app.mount("/", StaticFiles(directory="static", html=True), name="static")