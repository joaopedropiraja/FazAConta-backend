import uvicorn

from fazaconta_backend.shared.infra.config.settings import Settings
from fazaconta_backend.shared.infra.http.app import MyAPIApp

my_api_app = MyAPIApp()
app = my_api_app.app

if __name__ == "__main__":
    uvicorn.run(
        "fazaconta_backend.main:app",
        host=Settings().HOST,
        port=Settings().PORT,
        reload=True,
    )
    # uvicorn.run(app, host="0.0.0.0", port=8000)
