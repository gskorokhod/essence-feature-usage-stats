from web.table_generator.colour import RED, YELLOW, get_linear_gradient_value, GREEN, HOT_ORANGE


def generate_html_table(data):
    data, features = data
    html = '<html>'
    html += '<body>'
    html += '<table border=1 style="border-collapse: separate; border-spacing:0;">'

    # Create the table header row
    html += '<thead style="top:0; position:sticky;">'
    html += '<tr>'
    html += '<th style="left:0; position:sticky; background-color: white;">Essence file</th>'
    for column_name in features.keys():
        html += f'<th style="background-color: white; writing-mode: vertical-lr;">{column_name}</th>'
    html += '</tr>'
    html += '</thead>'

    # Create rows for data
    for row_name, columns in data.items():
        html += '<tr>'
        html += f'<th scope="row" style="left:0; position:sticky; background-color: white;">{row_name}</th>'
        for feature in features.keys():
            n_uses = columns.get(feature, 0)

            minn, maxn, avg = 0, features[feature]['max_in_file'], int(features[feature]['avg_in_file'])
            if n_uses == 0:
                bg_col = RED
            elif n_uses <= avg:
                bg_col = get_linear_gradient_value(n_uses, minn, avg, HOT_ORANGE, YELLOW)
            else:
                bg_col = get_linear_gradient_value(n_uses, avg, maxn, YELLOW, GREEN)

            html += f'<td bgcolor={bg_col}>{n_uses}</td>'
        html += '</tr>'

    html += '</table>'
    html += '</body>'
    html += '</html>'
    return html
