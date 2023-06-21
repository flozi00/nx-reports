import os
from server.main import app

app.launch(
    server_name="0.0.0.0",
    server_port=8080,
    auth=(os.environ.get("Nextcloud_user"), os.environ.get("Nextcloud_pw")),
)
