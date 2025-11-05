from flask import Flask
from flask_cors import CORS
import config
from routes.convert import convert_bp
from routes.merge import merge_bp
from routes.split import split_bp
from pathlib import Path

def create_app():
    app = Flask(__name__)
    CORS(app)  # permite requisições de qualquer origem (ajuste em produção)

    # garante que pastas existem
    Path(config.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(config.TEMP_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

    # registra rotas sem prefixo para ficar simples
    app.register_blueprint(convert_bp)  # rota fica /convert
    app.register_blueprint(merge_bp)    # rota fica /merge
    app.register_blueprint(split_bp)    # rota fica /split

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
