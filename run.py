from app import app, db
import pymysql

pymysql.install_as_MySQLdb()
# db.drop_all()
# db.create_all()
print(f"\n{db.engine.url.database} database used\n".upper())

app.run(host="0.0.0.0", debug=True)
