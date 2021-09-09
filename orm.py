'''ORM Model'''
from flask import Flask, render_template, request, redirect, jsonify
import connexion
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sqlacodegen

#connection for swagger
app = connexion.App(__name__, specification_dir='./')

#connection to database with old code
engine = create_engine('mysql+pymysql://root:asdf@localhost/practice')

#connection to database with new code
#engine = create_engine('sqlacodegen mysql+oursql://root:asdf@localhost/practice')
Session = sessionmaker(bind=engine)
session = Session()

#base for all class
Base = declarative_base()


class Student(Base):
    '''create table student'''
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    clasid = Column(Integer(), ForeignKey("class.id"), unique=False, nullable=False)
    creon = (String(45))
    updon = (String(45))


class Class(Base):
    '''create table student'''
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    clsrep = (String(45))
    creon = (String(45))
    updon = (String(45))





#engine = create_engine('mysql://root:asdf@localhost/practice')
#app.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/practice'
#app.app.config()
#engine.execute("CREATE DATABASE dbname")
#engine.execute("USE dbname")



#Base = declarative_base()




#Base.metadata.create_all(engine)

@app.route("/insert/student", methods=['POST'])
def insert1():
    '''inserting data'''
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        clasid= request.form.get('class_id')
        creon = request.form.get('created_on')
        updon = request.form.get('updated_on')
        temp = Student(id=id,name=name,clasid=clasid,creon=creon,updon=updon)
        session.add(temp)
        session.commit()

        return_var = {"status": True, "msg": "success"}
    except Exception as ex:
        print("error while inserting data is ", ex)
        return_var = {"status": False}

    return jsonify(return_var)



@app.route("/insert/class", methods=['POST'])
def insert2():
    """insert method"""
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        clsrep = request.form.get('class_id')
        creon = request.form.get('created_on')
        updon = request.form.get('updated_on')
        temp = Class(id=id, name=name, clsrep=clsrep, creon=creon, updon=updon)
        session.add(temp)
        session.commit()


        session.commit()
        return_var = {"status": True, "msg": "success"}
    except Exception as ex:
        print("error while inserting data is ", ex)
        return_var = {"status": False}

    return jsonify(return_var)


@app.route("/read/student", methods=['GET'])
def read1():
    """reading data"""
    try:
        stu = session.query(Student).all()
        stu_dic = {}
        for j in stu:
            stu_dic[str(j)] = {"id":j.id,"name":j.name,"class_id":j.clasid, "created_on": str(j.creon), "updated_on": str(j.updon)}
        return_var = {"status":True, "data":json.dumps(stu_dic)}
    except Exception as ex:
        print("error while reading data is ", ex)
        return_var = {"status":False}
    return jsonify(return_var)


@app.route("/read/class", methods=['GET'])
def read2():
    """reading data"""
    try:
        cls = session.query(Class).all()
        cls_dic = {}
        for j in cls:
            cls_dic[str(j)] = {"id":j.id,"name":j.name,"class_leader":str(j.clsrep), "created_on": str(j.creon), "updated_on": str(j.updon)}
        return_var = {"status":True, "data":json.dumps(cls_dic)}
    except Exception as ex:
        print("error while reading data is ", ex)
        return_var = {"status":False}
    return jsonify(return_var)


app.add_api("swagger.yaml")

if __name__ == '__main__':
    app.run(debug=True)
