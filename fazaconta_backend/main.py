import uvicorn

from fazaconta_backend.shared.infra.http.app import App


app = App.connect()

if __name__ == "__main__":
    uvicorn.run("fazaconta_backend.main:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
