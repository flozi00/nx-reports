from server.documents.pdf_utils import write_pdf
import json
from pathlib import Path
from server.utils.statics import *
from server.utils.timing import timeit
from tabulate import tabulate


@timeit
def read_clients(clients, local_path, client):
    for c in clients:
        if c.endswith("/"):
            c = c.replace("/", "")
            try:
                Path(local_path + c).mkdir(parents=True, exist_ok=True)
                client.download_async(
                    f"{c}/Details.json", f"{local_path + c}/Details.json"
                )
            except:
                pass

    client.download_sync(f"Mitarbeiter.md", f"{local_path}/Mitarbeiter.md")


@timeit
def writedetails(path, data, client, local_path):
    local_path = local_path + "Details.json"
    upload_path = f"./{path}/Details.json"
    myfile = open(local_path, "w+")
    myfile.write(json.dumps(json.loads(data)))
    myfile.close()
    client.upload_sync(upload_path, local_path)


@timeit
def writefile(
    meta,
    client,
    local_path,
    signature,
):
    local_dir = local_path
    Path(local_dir).mkdir(parents=True, exist_ok=True)

    now1 = meta.get("AuftragsDatum")
    customer_name = meta.get("Kunde")
    report_text = meta.get("Bericht")
    times_str = meta.get("Zeiten")
    times_str = tabulate(
        times_str, headers=["Datum", "Monteur", "Zeit"], tablefmt="html"
    )

    local_path = local_path + now1 + ".json"
    upload_path = f"./{customer_name}/{now1}.json"
    report_text += "\n" * 3

    filedata = json.dumps(meta, indent=4)

    Path(local_dir).mkdir(parents=True, exist_ok=True)
    myfile = open(local_path, "w+", encoding="utf-8")
    myfile.write(filedata)
    myfile.close()
    client.upload_sync(upload_path, local_path)

    write_pdf(
        local_path=local_path,
        local_dir=local_dir,
        client=client,
        upload_path=upload_path,
        meta=meta,
        data=report_text,
        timestable=times_str,
        signature=signature,
    )
