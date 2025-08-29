from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def root():
        # simple JSON response
        return {"status": "ok"}

    return app
