from pathlib import Path
import os
import ssl

from flask import Flask
from routes.health import health_endpoint
from routes.weather import weather_endpoint

app = Flask(__name__)
app.register_blueprint(health_endpoint, url_prefix='/api')
app.register_blueprint(weather_endpoint, url_prefix='/weather')


if __name__ == '__main__':
    certs_dir = Path('certs')
    port = int(os.getenv('APP_PORT', 443))
    app.secret_key = os.urandom(24)
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain(f'{certs_dir}/localhost.crt', f'{certs_dir}/localhost.key')
    app.run(debug=True, host='0.0.0.0', port=port, ssl_context=ctx)
