from flask import Blueprint, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import traceback
import time

from . import logger, operator
from .handlers.global_values import *
from .database import db_session
from .database import __all_models as al
from .webforms.registerform import RegisterForm
from .webforms.loginform import LoginForm
from .webforms.headerform import HeaderForm
from .webforms.companyform import CompanyForm
from .webforms.lkform import LkForm
from .webforms.lkpasform import LkPasForm
from .webforms.reviewform import ReviewForm
from .webforms.appointmentform import AppointmentForm
from .webforms.company_appointmentform import CompanyAppointmentForm
from .webforms.company_appointment_badform import CompanyAppointmentBadForm
from .webforms.employersform import EmployersForm

module = Blueprint('statics_page', __name__, url_prefix='/static')


@module.route('/', methods=['GET', 'POST'])
def index():
    try:
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        if headerform.validate_on_submit():
            if headerform.type_app.data != 0:
                list_orgs = session.query(al.organization.Organization).filter(
                    al.organization.Organization.type_app_id == headerform.type_app.data).all()
            else:
                list_orgs = session.query(al.organization.Organization).all()
            orgs = []
            sort_orgs = {}
            for org in list_orgs:
                if headerform.search.data in org.name:
                    list_review = session.query(al.review.Review).filter(al.review.Review.org_id == org.id).all()
                    count = 0
                    for rev in list_review:
                        count += rev.stars
                    if len(list_review) == 0:
                        rating = 0
                    else:
                        rating = int(count / len(list_review))
                    if rating not in sort_orgs:
                        sort_orgs[rating] = []
                    x = {
                        "id": org.id,
                        "name": org.name,
                        "about": org.name,
                        "email": org.email,
                        "phone_number": org.phone_number,
                        "address": org.address,
                        "image_path": org.image_path if org.image_path else "images/categories/category-1.jpg",
                        "review": len(list_review),
                        'rating': rating,
                    }
                    sort_orgs[rating].append(x)
            key_sorted = sorted(list(sort_orgs.keys()), reverse=True)
            for i in key_sorted:
                orgs += sort_orgs[i]
            return render_template('index.html',
                                   title="Главная",
                                   is_organization=is_organization,
                                   h_form=headerform,
                                   is_rating=True,
                                   is_reviews=False,
                                   is_all=False,
                                   orgs=orgs)

        list_orgs = session.query(al.organization.Organization).all()
        orgs = []
        sort_orgs = {}
        for org in list_orgs:
            list_review = session.query(al.review.Review).filter(al.review.Review.org_id == org.id).all()
            count = 0
            for rev in list_review:
                count += rev.stars
            if len(list_review) == 0:
                rating = 0
            else:
                rating = int(count / len(list_review))
            if rating not in sort_orgs:
                sort_orgs[rating] = []
            x = {
                "id": org.id,
                "name": org.name,
                "about": org.name,
                "email": org.email,
                "phone_number": org.phone_number,
                "address": org.address,
                "image_path": org.image_path if org.image_path else "images/categories/category-1.jpg",
                "review": len(list_review),
                'rating': rating,
            }
            sort_orgs[rating].append(x)
        key_sorted = sorted(list(sort_orgs.keys()), reverse=True)
        for i in key_sorted:
            orgs += sort_orgs[i]
        return render_template('index.html',
                               title="Главная",
                               h_form=headerform,
                               is_organization=is_organization,
                               is_rating=True,
                               is_reviews=False,
                               is_all=False,
                               orgs=orgs)
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='static method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/<string:sort_param>', methods=['GET', 'POST'])
def index_sorted(sort_param):
    try:
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        if sort_param == "sort_reviews":
            list_orgs = session.query(al.organization.Organization).all()
            orgs = []
            sort_orgs = {}
            for org in list_orgs:
                list_review = session.query(al.review.Review).filter(al.review.Review.org_id == org.id).all()
                count = 0
                for rev in list_review:
                    count += rev.stars
                if len(list_review) == 0:
                    rating = 0
                else:
                    rating = int(count / len(list_review))
                if len(list_review) not in sort_orgs:
                    sort_orgs[len(list_review)] = []
                x = {
                    "id": org.id,
                    "name": org.name,
                    "about": org.name,
                    "email": org.email,
                    "phone_number": org.phone_number,
                    "address": org.address,
                    "image_path": org.image_path if org.image_path else "images/categories/category-1.jpg",
                    "review": len(list_review),
                    "rating": rating,
                }
                sort_orgs[len(list_review)].append(x)
            key_sorted = sorted(list(sort_orgs.keys()), reverse=True)
            for i in key_sorted:
                orgs += sort_orgs[i]
            return render_template('index.html',
                                   title="Главная",
                                   is_organization=is_organization,
                                   h_form=headerform,
                                   is_rating=False,
                                   is_reviews=True,
                                   is_all=False,
                                   orgs=orgs)
        elif sort_param == "sort_rating":
            list_orgs = session.query(al.organization.Organization).all()
            orgs = []
            sort_orgs = {}
            for org in list_orgs:
                list_review = session.query(al.review.Review).filter(al.review.Review.org_id == org.id).all()
                count = 0
                for rev in list_review:
                    count += rev.stars
                if len(list_review) == 0:
                    rating = 0
                else:
                    rating = int(count / len(list_review))
                if rating not in sort_orgs:
                    sort_orgs[rating] = []
                x = {
                    "id": org.id,
                    "name": org.name,
                    "about": org.name,
                    "email": org.email,
                    "phone_number": org.phone_number,
                    "address": org.address,
                    "image_path": org.image_path if org.image_path else "images/categories/category-1.jpg",
                    "review": len(list_review),
                    'rating': rating,
                }
                sort_orgs[rating].append(x)
            key_sorted = sorted(list(sort_orgs.keys()), reverse=True)
            for i in key_sorted:
                orgs += sort_orgs[i]
            return render_template('index.html',
                                   title="Главная",
                                   is_organization=is_organization,
                                   h_form=headerform,
                                   is_rating=True,
                                   is_reviews=False,
                                   is_all=False,
                                   orgs=orgs)
        else:
            list_orgs = session.query(al.organization.Organization).all()
            orgs = []
            for org in list_orgs:
                list_review = session.query(al.review.Review).filter(al.review.Review.org_id == org.id).all()
                count = 0
                for rev in list_review:
                    count += rev.stars
                if len(list_review) == 0:
                    rating = 0
                else:
                    rating = int(count / len(list_review))
                x = {
                    "id": org.id,
                    "name": org.name,
                    "about": org.name,
                    "email": org.email,
                    "phone_number": org.phone_number,
                    "address": org.address,
                    "image_path": org.image_path if org.image_path else "images/categories/category-1.jpg",
                    "review": len(list_review),
                    "rating": rating
                }
                orgs.append(x)
            return render_template('index.html',
                                   title="Главная",
                                   is_organization=is_organization,
                                   h_form=headerform,
                                   is_rating=False,
                                   is_reviews=False,
                                   is_all=True,
                                   orgs=orgs)
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='static method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegisterForm()
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('registration.html',
                                       title="Регистрация",
                                       is_organization=is_organization,
                                       form=form,
                                       h_form=headerform,
                                       message="*Пароли не совпадают")
            if session.query(al.users.Users).filter(al.users.Users.email == form.email.data).first():
                return render_template('registration.html',
                                       title='Регистрация',
                                       is_organization=is_organization,
                                       form=form,
                                       h_form=headerform,
                                       message="*Email адрес занят")
            if session.query(al.users.Users).filter(al.users.Users.phone_number == form.phone_number.data).first():
                return render_template('registration.html',
                                       title='Регистрация',
                                       is_organization=is_organization,
                                       form=form,
                                       h_form=headerform,
                                       message="*Номер телефона занят")
            new_user = al.users.Users(
                first_name=form.first_name.data,
                second_name=form.second_name.data,
                email=form.email.data,
                password=form.password.data,
                phone_number=form.phone_number.data,
                is_admin=False
            )
            session.add(new_user)
            session.commit()
            return redirect('/static/login')
        return render_template("registration.html", title="Регистрация", h_form=headerform, form=form,
                               is_organization=is_organization)
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        if form.validate_on_submit():
            user = session.query(al.users.Users).filter(al.users.Users.email == form.email.data,
                                                        al.users.Users.password == form.password.data).first()
            if user:
                login_user(user, remember=form.remember_me.data)
                return redirect("/static")
            return render_template('login.html',
                                   is_organization=is_organization,
                                   title="Вход",
                                   h_form=headerform,
                                   message="*Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html',
                               h_form=headerform,
                               is_organization=is_organization,
                               title="Вход",
                               form=form)
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/login method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/register_company', methods=['GET', 'POST'])
@login_required
def register_company():
    try:
        form = CompanyForm()
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list.copy()
        groups_list.pop(0)
        form.type_app.choices = groups_list.copy()
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        if form.validate_on_submit():
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.name == form.name.data).first():
                return render_template('registration.html',
                                       title="Регистрация компании",
                                       is_organization=is_organization,
                                       h_form=headerform,
                                       form=form,
                                       message="*Имя уже занято")
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.email == form.email.data).first():
                return render_template('registration.html',
                                       title="Регистрация компании",
                                       is_organization=is_organization,
                                       h_form=headerform,
                                       form=form,
                                       message="*Почта уже занята")
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.phone_number == form.phone_number.data).first():
                return render_template('registration.html',
                                       title="Регистрация компании",
                                       is_organization=is_organization,
                                       h_form=headerform,
                                       form=form,
                                       message="*Телефон уже занят")
            logger.debug(current_user.id)
            new_organization = al.organization.Organization(
                name=form.name.data,
                about=form.about.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                address=form.address.data,
                type_app_id=form.type_app.data,
                owner_id=current_user.id
            )
            session.add(new_organization)
            session.commit()
            return redirect('/static')

        return render_template("registrationcompany.html", title="Регистрация компании", h_form=headerform, form=form,
                               is_organization=is_organization)
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register_company method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/lk', methods=['GET', 'POST'])
@login_required
def lk():
    try:
        form = LkForm()
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list.copy()
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        if form.validate_on_submit():
            if session.query(al.users.Users).filter(al.users.Users.email == form.email.data,
                                                    al.users.Users.id != current_user.id).first():
                return render_template('account-profile.html',
                                       title='Регистрация',
                                       is_organization=is_organization,
                                       form=form,
                                       h_form=headerform,
                                       message="*Email адрес занят")
            if session.query(al.users.Users).filter(al.users.Users.phone_number == form.phone_number.data,
                                                    al.users.Users.id != current_user.id).first():
                return render_template('account-profile.html',
                                       title='Регистрация',
                                       is_organization=is_organization,
                                       form=form,
                                       h_form=headerform,
                                       message="*Номер телефона занят")
            cur_user = session.query(al.users.Users).filter(al.users.Users.id == current_user.id).first()
            cur_user.first_name = form.first_name.data
            cur_user.second_name = form.second_name.data
            cur_user.email = form.email.data
            cur_user.phone_number = form.phone_number.data
            cur_user.image_path = secure_filename(form.avatar.data.filename)
            form.avatar.data.save('web/static/uploads/' + secure_filename(form.avatar.data.filename))
            session.commit()
            return redirect('/static/lk')

        user_info = session.query(al.users.Users).filter(al.users.Users.id == current_user.id).first()
        form.first_name.data = user_info.first_name
        form.second_name.data = user_info.second_name
        form.email.data = user_info.email
        form.phone_number.data = user_info.phone_number

        return render_template("account-profile.html",
                               h_form=headerform,
                               is_organization=is_organization,
                               title="Личный кабинет",
                               form=form
                               )
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register_company method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/lk_pas', methods=['GET', 'POST'])
@login_required
def lk_pas():
    try:
        form = LkPasForm()
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list.copy()
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        if form.validate_on_submit():
            if not session.query(al.users.Users).filter(al.users.Users.id == current_user.id,
                                                        al.users.Users.password == form.password_now.data).first():
                return render_template("account-password.html",
                                       h_form=headerform,
                                       is_organization=is_organization,
                                       title="Личный кабинет",
                                       form=form,
                                       message="*Неверный пароль")
            if form.password.data != form.password_again.data:
                return render_template("account-password.html",
                                       is_organization=is_organization,
                                       h_form=headerform,
                                       title="Личный кабинет",
                                       form=form,
                                       message="*Пароли не совпадают")
            cur_user = session.query(al.users.Users).filter(al.users.Users.id == current_user.id).first()
            cur_user.password = form.password.data
            session.commit()
            return redirect('/static/lk_pas')
        return render_template("account-password.html",
                               h_form=headerform,
                               is_organization=is_organization,
                               title="Личный кабинет",
                               form=form
                               )
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register_company method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        logout_user()
        return redirect('/static')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register_company method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization/<int:org_id>', methods=['GET', 'POST'])
def organization(org_id):
    try:
        form = ReviewForm()
        session = db_session.create_session()

        available_groups = session.query(al.type_appointment.TypeAppointment).all()
        groups_list = [(i.id, i.name) for i in available_groups]
        groups_list.insert(0, (0, "Все категории"))
        headerform = HeaderForm()
        headerform.type_app.choices = groups_list.copy()
        is_organization = False
        if current_user.is_authenticated:
            if session.query(al.organization.Organization).filter(
                    al.organization.Organization.owner_id == current_user.id).all():
                is_organization = True
            elif session.query(al.employees.Employees).filter(al.employees.Employees.user_id == current_user.id).all():
                is_organization = True

        stars_list = [(i, f"{i} stars") for i in range(1, 6)]
        form.stars.choices = stars_list.copy()

        if form.validate_on_submit():
            new_review = al.review.Review(
                user_comment=form.comment.data,
                stars=form.stars.data,
                user_id=current_user.id,
                org_id=org_id
            )
            session.add(new_review)
            session.commit()
            return redirect(f'/static/organization/{org_id}')

        org_info = session.query(al.organization.Organization).filter(
            al.organization.Organization.id == org_id
        ).first()
        org_name = org_info.name
        org_description = org_info.about
        org_address = org_info.address
        org_number = org_info.phone_number
        org_email = org_info.email
        if org_info.image_path:
            imgs = org_info.image_path.split(";")
        else:
            imgs = ["/static/images/products/product-16-1.jpg"] * 5

        list_review = session.query(al.review.Review).filter(al.review.Review.org_id == org_info.id).all()
        ls_rev = []
        count = 0
        for rev in list_review:
            user_com = session.query(al.users.Users).filter(al.users.Users.id == rev.user_id).first()
            x = {
                "img_path": "/static/uploads/" + user_com.image_path if user_com.image_path else "/static/images/avatars/avatar-1.jpg",
                "name": user_com.first_name + " " + user_com.second_name,
                "rating": rev.stars,
                "comment": rev.user_comment,
                "data_create": rev.data_create.strftime("%H:%M %d.%m.%Y")
            }
            ls_rev.append(x)
            count += rev.stars
        if len(list_review) == 0:
            sum_rating = 0
        else:
            sum_rating = int(count / len(list_review))

        count_review = len(list_review)

        logger.debug(ls_rev)
        return render_template("product.html",
                               h_form=headerform,
                               form=form,
                               is_organization=is_organization,
                               title="Карточка организации",
                               org_id=org_id,
                               org_name=org_name,
                               org_description=org_description,
                               org_address=org_address,
                               org_number=org_number,
                               org_email=org_email,
                               imgs=imgs,
                               sum_rating=sum_rating,
                               count_review=count_review,
                               list_review=ls_rev
                               )
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register_company method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/favorites', methods=['GET', 'POST'])
def favorites():
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            list_favorite = session.query(al.favorites.Favorites).filter(
                al.favorites.Favorites.user_id == current_user.id).all()
            list_org = []
            for fav in list_favorite:
                org_info = session.query(al.organization.Organization).filter(
                    al.organization.Organization.id == fav.org_id).first()
                x = {
                    "org_id": fav.org_id,
                    "name": org_info.name,
                }
                list_org.append(x)

            return render_template("favorite.html",
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Избранное",
                                   list_org=list_org
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register_company method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization/<int:org_id>/favorite', methods=['GET', 'POST'])
def organization_add_fav(org_id):
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()
            if session.query(al.favorites.Favorites).filter(al.favorites.Favorites.user_id == current_user.id,
                                                            al.favorites.Favorites.org_id == org_id).first():
                return redirect(f'/static/favorites')

            new_favorite = al.favorites.Favorites(
                user_id=current_user.id,
                org_id=org_id
            )
            session.add(new_favorite)
            session.commit()

            return redirect(f'/static/favorites')
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/{org_id}/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/remove_favorite/<int:org_id>', methods=['GET', 'POST'])
def organization_del_fav(org_id):
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()
            session.query(al.favorites.Favorites).filter(al.favorites.Favorites.user_id == current_user.id,
                                                         al.favorites.Favorites.org_id == org_id).delete()
            session.commit()
            return redirect(f'/static/favorites')
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/remove_favorite/{org_id} method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization/<int:org_id>/new_appointment', methods=['GET', 'POST'])
def new_appointment(org_id):
    try:
        if current_user.is_authenticated:
            form = AppointmentForm()
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            if form.validate_on_submit():
                new_appoint = al.appointment.Appointment(
                    user_comment=form.user_comment.data,
                    status="В обработке",
                    user_id=current_user.id,
                    org_id=org_id,
                )
                session.add(new_appoint)
                session.commit()
                return redirect(f'/static/organization/{org_id}')

            org_info = session.query(al.organization.Organization).filter(al.organization.Organization.id == org_id).first()
            return render_template("signup.html",
                                   org_name=org_info.name,
                                   form=form,
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Новая запись",
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/{org_id}/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/appointment', methods=['GET', 'POST'])
def appointment_user():
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            list_appointment = session.query(al.appointment.Appointment).filter(
                al.appointment.Appointment.user_id == current_user.id,
                al.appointment.Appointment.status != "Отменено",
                al.appointment.Appointment.status != "Завершено"
            ).all()
            list_apps = []
            for appoint in list_appointment:
                org_info = session.query(al.organization.Organization).filter(
                    al.organization.Organization.id == appoint.org_id).first()
                x = {
                    "org_id": appoint.org_id,
                    "name": org_info.name,
                    "user_comment": appoint.user_comment,
                    "org_comment": appoint.org_comment if appoint.org_comment else "",
                    "data_app": appoint.org_time + ' ' + appoint.org_data if appoint.org_data else "",
                    "status": appoint.status,
                }
                list_apps.append(x)

            return render_template("cart.html",
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Новая запись",
                                   list_apps=list_apps,
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/appointment_history', methods=['GET', 'POST'])
def appointment_user_history():
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            list_appointment = session.query(al.appointment.Appointment).filter(
                al.appointment.Appointment.user_id == current_user.id
            ).all()
            list_apps = []
            for appoint in list_appointment:
                org_info = session.query(al.organization.Organization).filter(
                    al.organization.Organization.id == appoint.org_id).first()
                x = {
                    "org_id": appoint.org_id,
                    "name": org_info.name,
                    "user_comment": appoint.user_comment,
                    "org_comment": appoint.org_comment if appoint.org_comment else "",
                    "data_app": appoint.org_time + ' ' + appoint.org_data if appoint.org_data else "",
                    "status": appoint.status,
                }
                list_apps.append(x)

            return render_template("carthistory.html",
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Новая запись",
                                   list_apps=list_apps,
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organizations', methods=['GET', 'POST'])
def organization_user():
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            list_organization = session.query(al.organization.Organization).filter(
                al.organization.Organization.owner_id == current_user.id
            ).all()
            list_orgs = []
            for org in list_organization:
                x = {
                    "org_id": org.id,
                    "name": org.name,
                    "is_admin": True,
                }
                list_orgs.append(x)

            list_organization = session.query(al.employees.Employees).filter(
                al.employees.Employees.user_id == current_user.id
            ).all()
            for org in list_organization:
                org_info = session.query(al.organization.Organization).filter(
                    al.organization.Organization.id == org.org_id
                ).first()
                x = {
                    "org_id": org_info.id,
                    "name": org_info.name,
                    "is_admin": False,
                }
                list_orgs.append(x)

            return render_template("company-organizations.html",
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Новая запись",
                                   list_orgs=list_orgs,
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization_lid/<int:org_id>/appointments', methods=['GET', 'POST'])
def organizations_lid_appointments(org_id):
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            list_appointment = session.query(al.appointment.Appointment).filter(
                al.appointment.Appointment.org_id == org_id,
                al.appointment.Appointment.status != "Отменено",
                al.appointment.Appointment.status != "Завершено"
            ).all()
            list_apps = []
            for appoint in list_appointment:
                user_info = session.query(al.users.Users).filter(
                    al.users.Users.id == appoint.user_id
                ).first()
                x = {
                    "user_name": user_info.first_name + ' ' + user_info.second_name,
                    "user_comment": appoint.user_comment,
                    "user_contact": user_info.phone_number + ", " + user_info.email,
                    "app_time": appoint.org_time + ' ' + appoint.org_data if appoint.org_data else "",
                    "app_id": appoint.id,
                    "is_not_use": True if appoint.status == "В обработке" else False
                }
                list_apps.append(x)

            return render_template("company-cart.html",
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Новая запись",
                                   org_id=org_id,
                                   list_apps=list_apps,
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization_lid/<int:org_id>/appointments_history', methods=['GET', 'POST'])
def organizations_lid_appointments_history(org_id):
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            list_appointment = session.query(al.appointment.Appointment).filter(
                al.appointment.Appointment.org_id == org_id,
            ).all()
            list_apps = []
            for appoint in list_appointment:
                user_info = session.query(al.users.Users).filter(
                    al.users.Users.id == appoint.user_id
                ).first()
                x = {
                    "user_name": user_info.first_name + ' ' + user_info.second_name,
                    "user_comment": appoint.user_comment,
                    "user_contact": user_info.phone_number + ", " + user_info.email,
                    "app_time": appoint.org_time + ' ' + appoint.org_data if appoint.org_data else "",
                    "status": appoint.status,
                }
                list_apps.append(x)

            return render_template("company-carthistory.html",
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="История записей",
                                   org_id=org_id,
                                   list_apps=list_apps,
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization_lid/<int:org_id>/appointment_success/<int:app_id>', methods=['GET', 'POST'])
def appointment_success(org_id, app_id):
    try:
        if current_user.is_authenticated:
            form = CompanyAppointmentForm()
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            if form.validate_on_submit():
                appoint = session.query(al.appointment.Appointment).filter(
                    al.appointment.Appointment.id == app_id
                ).first()
                appoint.org_data = form.org_data.data,
                appoint.org_time = form.org_time.data,
                appoint.org_comment = form.org_comment.data,
                appoint.status = "Подтверждено"
                appoint.org_user_id = current_user.id

                session.commit()
                return redirect(f'/static/organization_lid/{org_id}/appointments')

            return render_template("company-appointment-success.html",
                                   form=form,
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Подтверждение записи",
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/{org_id}/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization_lid/<int:org_id>/appointment_bad/<int:app_id>', methods=['GET', 'POST'])
def appointment_bad(org_id, app_id):
    try:
        if current_user.is_authenticated:
            form = CompanyAppointmentBadForm()
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            if form.validate_on_submit():
                appoint = session.query(al.appointment.Appointment).filter(
                    al.appointment.Appointment.id == app_id
                ).first()
                appoint.org_comment = form.org_comment.data,
                appoint.status = "Отменено"
                appoint.org_user_id = current_user.id

                session.commit()
                return redirect(f'/static/organization_lid/{org_id}/appointments')

            appoint = session.query(al.appointment.Appointment).filter(
                al.appointment.Appointment.id == app_id
            ).first()
            if appoint.org_data:
                form.org_data.data = appoint.org_data
            if appoint.org_time:
                form.org_time.data = appoint.org_time
            if appoint.org_comment:
                form.org_comment.data = appoint.org_comment

            return render_template("company-appointment-bad.html",
                                   form=form,
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Отмена записи",
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/{org_id}/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization_lid/<int:org_id>/appointment_end/<int:app_id>', methods=['GET', 'POST'])
def appointment_end(org_id, app_id):
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()
            appoint = session.query(al.appointment.Appointment).filter(
                al.appointment.Appointment.id == app_id
            ).first()
            appoint.status = "Завершено"
            appoint.org_user_id = current_user.id
            return redirect(f'/static/organization_lid/{org_id}/appointments')
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/{org_id}/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization_lid/<int:org_id>/employers', methods=['GET', 'POST'])
def organizations_lid_employers(org_id):
    try:
        if current_user.is_authenticated:
            form = EmployersForm()
            session = db_session.create_session()

            available_groups = session.query(al.type_appointment.TypeAppointment).all()
            groups_list = [(i.id, i.name) for i in available_groups]
            groups_list.insert(0, (0, "Все категории"))
            headerform = HeaderForm()
            headerform.type_app.choices = groups_list.copy()
            is_organization = False
            if current_user.is_authenticated:
                if session.query(al.organization.Organization).filter(
                        al.organization.Organization.owner_id == current_user.id).all():
                    is_organization = True
                elif session.query(al.employees.Employees).filter(
                        al.employees.Employees.user_id == current_user.id).all():
                    is_organization = True

            if form.validate_on_submit():
                user_info = session.query(al.users.Users).filter(
                    al.users.Users.email == form.email.data
                ).first()
                if user_info:
                    new_employers = al.employees.Employees(
                        user_id=user_info.id,
                        org_id=org_id
                    )
                    session.add(new_employers)
                    session.commit()
                return redirect(f'/static/organization_lid/{org_id}/employers')

            list_employers = session.query(al.employees.Employees).filter(
                al.employees.Employees.org_id == org_id
            ).all()
            list_empl = []
            for emp in list_employers:
                user_info = session.query(al.users.Users).filter(
                    al.users.Users.id == emp.user_id
                ).first()
                x = {
                    "img_path": "/static/uploads/" + user_info.image_path if user_info.image_path else "/static/images/avatars/avatar-1.jpg",
                    "user_name": user_info.first_name + ' ' + user_info.second_name,
                    "email": user_info.email,
                    "phone_number": user_info.phone_number,
                    "user_id": user_info.id,
                }
                list_empl.append(x)

            return render_template("company-employers.html",
                                   h_form=headerform,
                                   is_organization=is_organization,
                                   title="Сотрудники",
                                   org_id=org_id,
                                   list_empl=list_empl,
                                   form=form
                                   )
        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/organization_lid/<int:org_id>/employers_del/<int:user_id>', methods=['GET', 'POST'])
def organizations_lid_employers_del(org_id, user_id):
    try:
        if current_user.is_authenticated:
            session = db_session.create_session()

            session.query(al.employees.Employees).filter(
                al.employees.Employees.user_id == user_id,
                al.employees.Employees.org_id == org_id
            ).delete()
            session.commit()

            return redirect(f'/static/organization_lid/{org_id}/employers')

        return redirect(f'/static/login')
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/organization/favorite method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))
