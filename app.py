from config import vuln_app
from flask_limiter.util import get_remote_address

# start the app with port 5000 and debug on!
if __name__ == '__main__':
    vuln_app.run(host='0.0.0.0', port=5000, debug=True)
