# IMPORT APP MODULE
from app import app

# IMPORT IMPORTANT MODULES FROM FLASK
from flask import (
    jsonify,
    request
)

# GET THE CODE STATUS DETAIL
from app.data.code import code_status

import pandas as pd

from uuid import uuid4

# CONTROLLERS
from app.control import (
    jwt_required, 
    jwt_verify, 
    generate_id, 
    generate_token,
    add_to_database,
    remove_from_database,
    unwrap_csv
)

# DATABASE INSTANCES
from app.model.database import Audience, Checkout

@app.route("/codes", methods=["GET"])
def get_code():
    """
    Request this when the app localstorage does not have this data
    """
    return jsonify({"status": "0", "code": code_status})

@app.route("/login", methods=["POST"])
def login():
    """
    Login by scanning QR Code printed by OO team
    only us can have this

    Request:
    {authentication: "QR CODE SCANNED DATA"}

    Response:
    - token: jwt issued by the server (make sure to store this on clientside)
    """
    login_hex = request.json.get("authentication")
    if not login_hex:
        return jsonify({"code": "1", "type": "user"})

    qr_code_password = app.config["QRCODE_PASSWORD"]

    if login_hex != qr_code_password:
        return jsonify({"code": "3"})
    
    jwt_token = generate_token({"id": generate_id()})

    return jsonify({"code": "0", "token": jwt_token})

@app.route("/upload", methods=["POST"])
def upload():
    """
    Upload the file
    for the audiences database

    This will be used in SERVER side only
    """
    upload_old_file = False
    file = request.files["data"]
    stream_data = file.stream
    
    website_ticket = "https://tedxruppticket.web.app/"

    df = pd.read_csv(stream_data)
    name = df["name"].values

    if "id" in df.columns:
        _id = df["id"].values
        _name = df["name"].values
        
        audiences = []
        for i in range(len(_id)):
            audiences.append(Audience(_id[i], _name[i]))
        add_to_database(audiences, multiple=True)

        return jsonify({"data": "added"})

    tickets = df["Ticket"].values
    ticket_num = df["Ticket"].values.sum()
    
    _name = []
    for i, n in enumerate(tickets):
        for j in range(n):
            print()
            _name.append(name[i])

    _id = [str(uuid4()).upper()[:7] for i in range(ticket_num)]

    if "id" in df.columns:
        upload_old_file = True
        _id = df["id"].values

    audiences = []
    _tickets = []
    for i in range(len(_id)):
        audiences.append(Audience(_id[i], _name[i]))
        _tickets.append(website_ticket + f"{_id[i]}")
    add_to_database(audiences, multiple=True)

    output_dataframe = pd.DataFrame(data={
        "id": _id,
        "name": _name,
        "ticket_url": _tickets
    })

    output_dataframe.to_csv("./files/CircleAudiences.csv")
    data_obj = output_dataframe.set_index("id").to_dict()

    return {"code": "0", "data": data_obj}

@app.route("/scan", methods=["POST"])
@jwt_required
def scan_ticket():
    """
    Scan the ticket get the ID and check with database and server

    Request:
    // data
    - {ticketNumber: "SCANNED DATA"}
    // header
    - {Authentication: "JWT TOKEN"}

    Response:
    - audience name if code number is 0
    - if code is 1, no name error
    """
    ticket_num = request.json.get("ticketNumber")

    audience = Audience.query.filter(Audience.id == ticket_num).first()
    checkout = Checkout.query.filter(Checkout.audience_id == ticket_num).first()
    if not audience:
        return jsonify({"code": "1", "type": "ticket not found"})

    if checkout:
        return jsonify({"code": "1", "type": "ticket already redeemed", "name": audience.name})

    checkout_object = Checkout(audience.id)
    add_to_database(checkout_object)

    return jsonify({"code": "0", "type": "checkout successful", "name": audience.name})

@app.route("/audiences", methods=["GET"])
@jwt_required
def list_all_audience():
    """
    List all users

    Request:
    // header
    - {Authentication: "JWT TOKEN"}

    Response:
    - data
    eg - 
    {
    "data": [
        {
            "name": "BURNS MARKS",
            "redeem": false
        },
        {
            "name": "BYRD HEWITT",
            "redeem": true
        }
        ]
    }
    """
    data = []
    checkouts = Checkout.query.all()
    for checkout in checkouts:
        audience_id = checkout.audience_id
        audience = Audience.query.filter(Audience.id == audience_id).first()

        checkout_time = checkout.date.strftime("%I:%M:%S")

        data.append([audience.name, checkout_time])

    return jsonify({"data": data})
