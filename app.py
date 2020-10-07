from flask import Blueprint, jsonify, request,render_template,Flask
app = Flask(__name__, template_folder='views')
from models import TableBuilder

table_builder = TableBuilder()

@app.route("/serverside_table")
def serverside_table():
    return render_template("serverside_table.html")

@app.route("/tables/serverside_table", methods=['GET'])
def serverside_table_content():
    data = table_builder.collect_data_serverside(request)
    return jsonify(data)
