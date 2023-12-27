import sys
sys.path.insert(0, "..")
from flask import Flask, render_template, request
from opcua import Client

app = Flask(__name__)

def browse_nodes(node):
    nodes_list = []

    try:
        children = node.get_children()
        for child in children:
            display_name = child.get_display_name().Text
            try:
                value = child.get_value()
            except Exception:
                value = None  

            if (
                isinstance(value, (int, float, bool, str))  
            ):
                node_info = f"{display_name}: {value}"
                nodes_list.append(node_info)

            nodes_list.extend(browse_nodes(child))

    except Exception as e:
        nodes_list.append(f"Error accessing node: {e}")

    return nodes_list



@app.route('/process_form', methods=['POST'])
def process_form():
    server_URL = request.form.get('server_URL')
    content_find = request.form.get('content_find')
    try:
        local_client = Client(server_URL)
        local_client.connect()

        try:
            root_node = local_client.get_root_node()
            nodes_data = browse_nodes(root_node)
             
            return render_template('results.html', bulk_data=nodes_data, find_this=content_find)

        finally:
            local_client.disconnect()

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
