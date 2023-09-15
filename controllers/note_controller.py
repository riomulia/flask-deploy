from models.note_model import Note, NoteSchema
from models.person_model import Person, PersonSchema
from config import db

# GET /notes
# [
#     { 
#         "note_id": 1
#         "content": "aaa"
#         "person": {lname: "...", fname:"...", "person_id": "..."}
#     }
# ]
def read_all():
    notes = Note.query.join(Person).all()

    note_schema = NoteSchema(many=True)
    results = note_schema.dump(notes)

    return results

def create(person_id, note):
    #1. find person dengan id person_id
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    #2. if person not extst abort
    if person is None:
        abort (404, f"Person with id {person_id} is not found")

    #3. if person exists, add new note to person
    content = note.get('content')
    new_note = Note(content = content, person_id = person.person_id)

    person.notes.append(new_note)

    person.save()

    note_schema = NoteSchema()
    result = note_schema.dump(new_note)

    return result

# PUT /people/{person_id}
def read_one(person_id, note_id):
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
            .filter(Note.note_id == note_id)
            # .filter(Person.person_id == person_id)
            .one_or_none()
    ) 
    if note is None:
        abort(
            404,
            f"Note with id {note_id} owned by person with id {person_id} is not found"
        )
    else:
        note_schema = NoteSchema()
        result = note_schema.dump(note)
        return result
    
    print(note, "<<<<<<<")

# PUT /people/{person_id}
def update(person_id, note_id, note):
    found_note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
            .filter(Note.note_id == note_id)
            # .filter(Person.person_id == person_id)
            .one_or_none()
    )

    if found_note is None:
        abort(404, f"note with id {note_id} own by person {person_id} is not found")
    
    # found_note.content = note.get('content')

    print(note, "<<<<<<<")

    content = note.get('content')
    found_note.update(content)

    note_schema = NoteSchema()
    result = note_schema.dump(found_note)

    return result
