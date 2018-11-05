# Config file

import os
from app import app

#db path
DATABASE = str(os.path.join(app.root_path, 'db/bakery.db'))
print DATABASE

# Use Flask web forms wrapper
WTF_CSRF_ENABLED = True

# Token used to validate web forms with Flask form wrapper
SECRET_KEY = ':Kj;4uc84$&cn4Wx48w48&^%C\QJEC]SETUC'