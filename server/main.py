import base64
import logging
import json
import os
from pathlib import Path

from server.utils.statics import *
from server.documents.readandwrite import *
from server.utils.webdavclient import get_client, list_files, list_reports
import gradio as gr

client = get_client(
    os.environ.get("Nextcloud_server"), os.environ.get("Nextcloud_user"), os.environ.get("Nextcloud_pw")
)


def read_root():
    result = []
    local_path = f"./{client_folder}/"
    Path(local_path).mkdir(parents=True, exist_ok=True)

    clients = list_files(client)
    read_clients(clients, local_path, client)
    for c in clients:
        if c.endswith("/"):
            c = c.replace("/", "")
            try:
                result.append(c.replace("/", ""))
            except Exception as e:
                logging.error(str(e) + " at read folder")
    return result


def read_customer(customer: str):
    local_path = f"./{client_folder}/"
    Path(local_path).mkdir(parents=True, exist_ok=True)

    reports = list_reports(client, customer)

    result = [report.replace(".json", "") for report in reports]
    print(result)
    return gr.Dropdown.update(choices=result)


def read_report_details(customer: str, date: str):
    try:
        local_path = f"./{client_folder}/"
        Path(local_path).mkdir(parents=True, exist_ok=True)

        client.download_sync(
            f"./{customer}/{date}.json", f"{local_path}{customer}/{date}.json"
        )
        with open(f"{local_path}{customer}/{date}.json", "r") as f:
            data = f.read()
            data = json.loads(data)

        return (
            data.get("Zeiten"),
            data.get("Auftragsnummer"),
            data.get("Bericht"),
        )

    except Exception as e:
        print(e)
        return "login data invalid"


def write(customers, date_of, times_table, id_number, report_details, signature):
    local_path = f"./{client_folder}{customers}/"
    metas = {
        "Zeiten": times_table.values.tolist(),
        "Auftragsnummer": id_number,
        "Bericht": report_details,
        "AuftragsDatum": date_of,
        "Kunde": customers,
    }

    if signature is not None:
        with open(signature, "rb") as image_file:
            sign_data = base64.b64encode(image_file.read()).decode()
    else:
        sign_data = ""

    writefile(
        meta=metas,
        client=client,
        local_path=local_path,
        signature=sign_data,
    )

    return gr.Dropdown.update(choices=read_root())


customer_list = read_root()

app = gr.Blocks()
with app:
    customers = gr.Dropdown(
        choices=customer_list, label="Kundenliste", interactive=True
    )
    reports_dropdown = gr.Dropdown(interactive=True, label="Auftragsdatum")
    times_table = gr.Dataframe(
        headers=["Datum", "Monteur", "Zeit"],
        datatype=["date", "str", "number"],
        col_count=(3, "fixed"),
        interactive=True,
    )
    id_number = gr.Textbox(max_lines=1, interactive=True, label="Auftragsnummer")
    report_details = gr.Textbox(interactive=True, label="Bericht")
    signature = gr.Image(source="canvas", brush_radius=1, type="filepath")
    send_button = gr.Button("Speichern")
    customers.change(fn=read_customer, inputs=customers, outputs=reports_dropdown)
    reports_dropdown.change(
        fn=read_report_details,
        inputs=[customers, reports_dropdown],
        outputs=[times_table, id_number, report_details],
    )
    send_button.click(
        fn=write,
        inputs=[
            customers,
            reports_dropdown,
            times_table,
            id_number,
            report_details,
            signature,
        ],
        outputs=customers,
    )
