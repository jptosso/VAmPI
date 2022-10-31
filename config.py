import os
import connexion
from flask_sqlalchemy import SQLAlchemy

'''
 Decide if you want to server a vulnerable version or not!
 DO NOTE: some functionalities will still be vulnerable even if the value is set to 0
          as it is a matter of bad practice. Such an example is the debug endpoint.
'''
vuln = int(os.getenv('vulnerable', 1))
# vuln=1
# token alive for how many seconds?
alive = int(os.getenv('tokentimetolive', 60))
# requests allowed per minute by IP
# 0 means disabled
rate_limit = os.getenv('ratelimit', None)

vuln_app = connexion.App(__name__, specification_dir='./openapi_specs')

if rate_limit:
    print("Setting rate limit to %s" % rate_limit)
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(
        vuln_app.app, 
        key_func=get_remote_address,
        default_limits=[rate_limit],
        storage_uri="memory://"
        )

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(vuln_app.root_path, 'database/database.db')
vuln_app.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
vuln_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

vuln_app.app.config['SECRET_KEY'] = 'random'
# start the db
db = SQLAlchemy(vuln_app.app)

vuln_app.add_api('openapi3.yml')


