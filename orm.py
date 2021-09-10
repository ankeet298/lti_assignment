'''Sqlalchemy ORM Model'''
import json
import time
import connexion
from flask import request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#connection for swagger
app = connexion.App(__name__, specification_dir='./')

#connection to database
engine = create_engine('mysql+pymysql://root:asdf@localhost/practice')
Session = sessionmaker(bind=engine)
session = Session()

#base for all class
Base = declarative_base()

#table details
#pylint: disable=too-few-public-methods
class Student(Base):
    '''Student table'''
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True) #pylint: disable=invalid-name
    name = Column(String(45))
    clasid = Column(Integer(), ForeignKey("class.id"), unique=False, nullable=False)
    creon = Column(String(45))
    updon = Column(String(45))

#pylint: disable=too-few-public-methods
class Class(Base):
    '''Class table'''
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True) #pylint: disable=invalid-name
    name = Column(String(45))
    clsrep = Column(String(45))
    creon = Column(String(45))
    updon = Column(String(45))

@app.route("/create/student", methods=['POST'])
def insert1():
    '''inserting data in student'''
    try:
        # pylint: disable=invalid-name, redefined-builtin
        id = request.form.get('id')
        name = request.form.get('name')
        clasid= request.form.get('class_id')
        creon = time.ctime(time.time())
        temp = Student(id=id,name=name,clasid=clasid,creon=creon)
        session.add(temp)
        session.commit()

        return_var = {"status": True, "msg": "success"}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while inserting data is ", ex)

        return_var = {"status": False}

    return jsonify(return_var)

@app.route("/create/class", methods=['POST'])
def insert2():
    """insert data in class"""
    try:
        # pylint: disable=invalid-name, redefined-builtin
        id = request.form.get('id')
        name = request.form.get('name')
        clsrep = request.form.get('class_leader')
        creon = time.ctime(time.time())
        temp = Class(id=id, name=name, clsrep=clsrep, creon=creon)
        session.add(temp)
        session.commit()

        return_var = {"status": True, "msg": "success"}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while inserting data is ", ex)

        return_var = {"status": False}

    return jsonify(return_var)

@app.route("/read/student", methods=['GET'])
def read1():
    """reading data from student"""
    try:
        stu = session.query(Student).all()
        stu_dic = {}
        for j in stu:
            stu_dic[str(j)] = {"id":j.id,
                               "name":j.name,
                               "class_id":j.clasid,
                               "created_on":j.creon,
                               "updated_on":j.updon}

        return_var = {"status":True, "data":json.dumps(stu_dic)}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while reading data is ", ex)

        return_var = {"status":False}

    return jsonify(return_var)

@app.route("/read/class", methods=['GET'])
def read2():
    """reading data from class"""
    try:
        cls = session.query(Class).all()
        cls_dic = {}
        for j in cls:
            cls_dic[str(j)] = {"id":j.id,
                               "name":j.name,
                               "class_leader":j.clsrep,
                               "created_on":j.creon,
                               "updated_on":j.updon}

        return_var = {"status":True, "data":json.dumps(cls_dic)}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while reading data is ", ex)

        return_var = {"status":False}

    return jsonify(return_var)

@app.route("/update/student", methods=['PUT'])
def update1():
    """Student table update"""
    try:
        # pylint: disable=invalid-name, redefined-builtin
        id = request.form.get('id')
        entry = session.query(Student).filter(Student.id==id).first()
        entry.name = request.form.get('name')
        entry.clasid = request.form.get('class_id')
        entry.updon = time.ctime(time.time())
        session.commit()

        return_var = {"status":True,"msg":"success"}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while updating data is ", ex)

        return_var = {"status": False}

    return jsonify(return_var)

@app.route("/update/class", methods=['PUT'])
def update2():
    """Class table update"""
    try:
        # pylint: disable=invalid-name, redefined-builtin
        id = request.form.get('id')
        entry = session.query(Class).filter(Class.id==id).first()
        entry.name = request.form.get('name')
        entry.clsrep = request.form.get('class_leader')
        entry.updon = time.ctime(time.time())
        session.commit()

        return_var = {"status":True,"msg":"success"}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while updating data is ", ex)

        return_var = {"status": False}

    return jsonify(return_var)

@app.route("/delete/student", methods=['DELETE'])
def delete1():
    """delete data from student"""
    try:
        # pylint: disable=invalid-name, redefined-builtin
        id = request.form.get('id')
        entry = session.query(Student).filter(Student.id == id).first()
        session.delete(entry)
        session.commit()

        return_var = {"status": True, "msg": "success"}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while deleting data is ", ex)

        return_var = {"status": False}

    return jsonify(return_var)

@app.route("/delete/class", methods=['DELETE'])
def delete2():
    """delete data from class"""
    try:
        # pylint: disable=invalid-name, redefined-builtin
        id = request.form.get('id')
        entry = session.query(Class).filter(Class.id == id).first()
        session.delete(entry)
        session.commit()

        return_var = {"status": True, "msg": "success"}
    # pylint:disable=broad-except
    except Exception as ex:
        print("error while deleting data is ", ex)

        return_var = {"status": False}

    return jsonify(return_var)

#yaml file adding
app.add_api("swagger.yaml")

if __name__ == '__main__':
    app.run(debug=True)
