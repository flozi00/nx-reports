def generate_html(
    reportnumber,
    created,
    customername,
    customermail,
    bericht,
    totaltime,
    head_data,
    b64image,
    b64logo,
):
    myfile = open("report_template.html", "r+")
    raw_html = myfile.read()
    myfile.close()

    bericht_temp = bericht.split("\n")
    bericht = ""
    for x in bericht_temp:
        x = x.split("-->")
        bericht += f"""<tr class='item'>
					<td>{x[0]}</td>

					<td>{'' if len(x) < 2 else x[1]}</td>
				</tr>"""
    raw_html = raw_html.replace("{reportnumber}", reportnumber)
    raw_html = raw_html.replace("{created}", created)
    raw_html = raw_html.replace("{customername}", customername)
    raw_html = raw_html.replace("{customermail}", customermail)
    raw_html = raw_html.replace("{bericht}", bericht)
    raw_html = raw_html.replace("{totaltime}", totaltime)
    raw_html = raw_html.replace("{b64image}", b64image)
    raw_html = raw_html.replace("{b64logo}", b64logo)
    raw_html = raw_html.replace("{head_data}", head_data.replace("\n", "<br>"))

    return raw_html
