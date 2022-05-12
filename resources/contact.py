from models.contact import ContactModel
from flask_restful import Resource, reqparse


class Contact(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # def get(self): #dont need this one for now, cause we have Resource "ContactsList" that returns whole list of Contacts
    #     pass

    def post(self):
        data = Contact.parser.parse_args()
        if ContactModel.find_contact_by_email(data["email"]):
            return {"message": "Contact with that email already exists"}, 400

        contact = ContactModel(
            data["first_name"], data["last_name"], data["email"], data["phone"])
        try:
            contact.save_to_db()
        except:
            return {"message": "An error occured inserting a contact."}, 500

        return {
            "message": contact.json()
        }

    def put(self):
        data = Contact.parser.parse_args()
        contact = ContactModel.find_contact_by_email(data["email"])

        if not contact:
            return {"message": "Contact with that email doesn't exist."}, 400

        contact.first_name = data["first_name"]
        contact.last_name = data["last_name"]
        # contact.email = data["email"]
        contact.phone_number = data["phone"]
        try:
            contact.save_to_db()
            return {"message": "Contact updated", "contact": contact.json()}, 200
        except:
            return {"message": "An error occured updating the contact."}, 500

    def delete(self):
        data = Contact.parser.parse_args()
        contact = ContactModel.find_contact_by_email(data["email"])
        if not contact:
            return {"message": "Contact with that email doesn't exist."}, 400

        try:
            contact.delete_from_db()
            return {"message": "Contact deleted"}, 200
        except:
            return {"message": "An error occured deleting the contact."}, 500


class ContactsList(Resource):
    def get(self):
        return {"contacts": [contact.json() for contact in ContactModel.find_all()]}
