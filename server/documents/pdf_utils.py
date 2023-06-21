from server.documents.report_util import generate_html
from server.documents.email_util import sendmail
import pdfkit
import os, platform
from datetime import datetime
import logging
import json
import time
import base64
import requests


def write_pdf(
    local_path, local_dir, client, upload_path, meta, data, timestable, signature
):
    now = str(round(time.time() * 1000))
    try:
        with open(local_dir + "Details.json") as f:
            customer_data = json.loads(f.read())
        report_data = meta

    except Exception as e:
        print(e)
        customer_data = {}
        report_data = meta

    try:
        logo_bytes = requests.get(os.environ.get("logo_url")).content
    except:
        logo_bytes = bytes()
    b64logo = base64.b64encode(logo_bytes).decode()  # encode to base64 (bytes)

    head_data = os.environ.get("head_data", "").replace(",", "\n")

    official_data = generate_html(
        report_data.get("Auftragsnummer", ""),
        datetime.now().strftime("%d %B, %Y - %H:%M"),
        customer_data.get("Name", ""),
        customer_data.get("E-mail", ""),
        data,
        timestable,
        head_data,
        signature,
        b64logo,
    )
    myfile = open(local_path + now + ".html", "w+")
    myfile.write(official_data)
    myfile.close()

    try:
        if platform.system() == "Windows":
            pdfkit_config = pdfkit.configuration(
                wkhtmltopdf=os.environ.get(
                    "WKHTMLTOPDF_PATH",
                    f"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe",
                )
            )
        else:
            pdfkit_config = pdfkit.configuration()

        pdfkit.from_string(
            official_data,
            local_path + now + ".pdf",
            configuration=pdfkit_config,
            options={"encoding": "UTF-8", "enable-local-file-access": True},
        )

        client.upload_sync(upload_path + now + ".pdf", local_path + now + ".pdf")
        if signature != "":
            text = f"""
Sehr geehrter Kunde, Vielen Dank für Ihren Auftrag! Wir haben gern für Sie gearbeitet.
Im Anhang finden sie ihre Kopie des Berichts für den Einsatz des heutigen Tages.
Wir danken Ihnen für Ihr Vertrauen und die gute Zusammenarbeit. Wir freuen uns über Ihre Weiterempfehlung.
                
{data}
                
                
Mit freundlichen Grüßen

{head_data}
"""
            sendmail(
                path=local_path + now + ".pdf",
                receiver_email=customer_data.get("E-mail", ""),
                text=text,
                subject="Bericht zur Auftragsnummer: "
                + report_data.get("Auftragsnummer", ""),
            )
        os.remove(local_path + now + ".pdf")
        os.remove(local_path + now + ".html")

    except Exception as e:
        logging.error(e)
