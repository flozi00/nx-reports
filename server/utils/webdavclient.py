from webdav3.client import Client
from server.utils.timing import timeit


@timeit
def get_client(url, user, pas):
    options = {
        "webdav_hostname": f"{url}/remote.php/dav/files/{user}/",
        "webdav_login": user,
        "webdav_password": pas,
    }
    client = Client(options)

    return client


@timeit
def list_files(client):
    clients = client.list("./")[1:]

    filtered = []
    for c in clients:
        if c.count("-") > 1:
            filtered.append(c)

    return filtered


@timeit
def list_reports(client, customer):
    clients = client.list("./" + customer)[1:]

    filtered = []
    for c in clients:
        if c.endswith(".json") and c.count("-") > 1:
            filtered.append(c)

    return filtered
