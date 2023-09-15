from flask import make_response, abort
from config import db
from models.person_model import Person, PersonSchema

# /api/people
def read_all():
    people = Person.query.all()
    person_schema = PersonSchema(many=True)
    return person_schema.dump(people)

def read_one(person_id):
    person = Person.query.get(person_id)

    print(person)

    if person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        person_schema = PersonSchema()
        update = schema.load(person_data, instance=updated_person, session=db.session)

        db.session.merge(update)
        db.session.commit()

        return person_schema.dump(person)

def update(person_id, person_data):

    # Ambil 1 data dari db yg punya id person
    updated_person = Person.query.get(person_id)

    if person_id is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        # person_data
        # lname = person_data.get('lname')
        # fname = person_data.get('fname')

        # Bisa Pakai Cara ini juga
        # updated_person.fname = person_data['fname']
        # updated_person.lname = person_data['lname']

        person_schema = PersonSchema()
        fname=person_data['fname']
        lname=person_data['lname']

        person_instance = Person(
            person_id=person_id,
            fname=fname,
            lname=lname,
            timestamp=updated_person.timestamp
        )

        # db.session.merge(person_instance)
        # db.session.commit()

        updated = person_instance.update()
        return person_schema.dump(updated)

def create(person_data):
    person_schema = PersonSchema()
    fname=person_data['fname']
    lname=person_data['lname']

    person_instance = Person(
        fname=fname,
        lname=lname
    )

    db.session.merge(person_instance)
    db.session.commit()
    return "success create"

def delete(person_id):

    deleted_person = Person.query.get(person_id)

    if deleted_person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        person_schema = PersonSchema()
        db.session.delete(deleted_person)
        db.session.commit()

        return "success delete"