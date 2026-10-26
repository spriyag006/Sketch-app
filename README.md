# Photo to Sketch

Turn any photo into a pencil sketch right in your browser.

**Live demo:** https://sketch-app-qx4v.onrender.com

> The app is hosted on Render's free plan, so it sleeps after inactivity. The first load can take about 50 seconds to wake up.

## How it works

1. Upload a photo.
2. Tap **Convert**.
3. The server turns the photo into a sketch using OpenCV.
4. Preview the result and tap **Download** to save it as a PNG.

The sketch effect is made by converting the image to grayscale, inverting it, blurring the inverted image, and blending it back with the original using a color dodge.

## Tech stack

- **Backend:** Python, FastAPI, Uvicorn
- **Image processing:** OpenCV, Pillow, NumPy
- **Frontend:** plain HTML, CSS and JavaScript
- **Hosting:** Render

## Project structure

```
.
├── main.py            # FastAPI app and /sketch endpoint
├── sketcher.py        # OpenCV sketch function
├── requirements.txt   # Python dependencies
└── static/
    └── index.html     # Web page
```

## Run locally

```bash
git clone https://github.com/spriyag006/Sketch-app.git
cd Sketch-app
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

## Deploy on Render

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

## API

**POST** `/sketch`

- Body: `multipart/form-data` with a `file` field (the image)
- Response: the sketch as a `image/png`

Example:

```bash
curl -X POST -F "file=@photo.jpg" https://sketch-app-qx4v.onrender.com/sketch --output sketch.png
```

