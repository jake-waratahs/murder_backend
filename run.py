import sys
from application import app

if len(sys.argv) > 1 and sys.argv[1] == "prod":
    app.run()
else:
    app.run(debug=True)