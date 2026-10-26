import io
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from sketcher import classic_sketch, dl_sketch

app = FastAPI(title="Photo to Sketch")


@app.post("/sketch")
async def sketch(file: UploadFile = File(...), mode: str = Form("hed")):
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    img.thumbnail((768, 768))  # keep CPU inference fast

    out = classic_sketch(img) if mode == "classic" else dl_sketch(img, mode)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


app.mount("/", StaticFiles(directory="static", html=True), name="static")