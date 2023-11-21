import os
from app import app

if __name__ == '__main__':
    host = os.environ.get('HOST', 'localhost')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
