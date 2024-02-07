from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Member, Child
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():

    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 1:
    #         flash('Note too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id= current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added!', category='success')


    return render_template("home.html", user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)

#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#             return jsonify({})
        
@views.route('/add-member', methods=['GET','POST'])
def add_member():
    if request.method == 'POST':
        print("yes") #finish registering the member
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        age_range = request.form.get('ageRange')
        marital_status = request.form.get('maritalStatus')
        address = request.form.get('address')
        phone_number = request.form.get('phoneNumber')
        email = request.form.get('email')
        former_church_name = request.form.get('formerChurchName')
        former_church_address = request.form.get('formerChurchAddress')
        prior_ministry = request.form.get('priorMinistry')
        current_ministry = request.form.get('currentMinistry')
        comments = request.form.get('comments')        

        member = Member.query.filter_by(email=email).first()
        print('the member has been found here:')
        # print(member.first_name)
        if member:
            flash('The email address already exists. Please use another email address.', category='error')
        else:
            children_data = []
            for key in request.form.keys():
                if key.startswith('childFirstName') and len(key)>14:
                    child_id = int(key[14:])
                    child_first_name = request.form.get(f'childFirstName{child_id}')
                    child_last_name = request.form.get(f'childLastName{child_id}')
                    child_birthDate = request.form.get(f'childBirthday{child_id}')
                    children_data.append({'first_name':child_first_name, 'last_name':child_last_name, 'birthdate':child_birthDate})
            new_member = Member(first_name=first_name, last_name=last_name, age_range=age_range,marital_status=marital_status,address=address,phone_number=phone_number,email=email,former_church_name=former_church_name, former_church_address=former_church_address, prior_ministry=prior_ministry, current_ministry=current_ministry, comments=comments)

            for child_data in children_data:
                new_child = Child(first_name=child_data['first_name'], last_name=child_data['last_name'], birthDate=datetime.strptime(child_data['birthdate'], '%Y-%m-%d'),)
                new_member.children.append(new_child)
            db.session.add(new_member)
            db.session.commit()
            flash('The member has been added successfully!', category='success')
    return (render_template("add_member.html", user = current_user))

@views.route('/view-members', methods=['GET'])
def view_members():
    members = Member.query.all()

    members_data = []

    for member in members:
        member_data = {
            'id': member.id,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'age_range': member.age_range,
            'marital_status': member.marital_status,
            'address': member.address,
            'children': []

        }
        if member.children:
            for child in member.children:
                child_data = {
                    'id': child.id,
                    'child_first_name': child.first_name,
                    'child_last_name' : child.last_name,
                    'child_birthdate': child.birthDate.strftime('%Y-%m-%d'),
                }
                member_data['children'].append(child_data)

        members_data.append(member_data)
        print(members_data)
    return jsonify(members_data)

@views.route('/render-view-members')
def render_view_members():
    return render_template("view_members.html", user=current_user)
            