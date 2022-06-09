from pathlib import Path
import os
import ssl

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/health')
def health():
    return jsonify({'status': 'up'})


if __name__ == '__main__':
    certs_dir = Path('certs')
    port = int(os.getenv('APP_PORT', 443))
    app.secret_key = os.urandom(24)
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain(f'{certs_dir}/localhost.crt', f'{certs_dir}/localhost.key')
    app.run(debug=True, host='0.0.0.0', port=port, ssl_context=ctx)
