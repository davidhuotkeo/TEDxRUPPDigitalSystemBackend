from app import app, db
import pymysql

pymysql.install_as_MySQLdb()
# db.drop_all()
db.create_all()

app.run(host="0.0.0.0", debug=True)
