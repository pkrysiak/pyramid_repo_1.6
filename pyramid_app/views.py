from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from allegro.lib import allegro_api, NoItemException as AllegroNoItemEx
from nokaut.lib import nokaut_api, NoItemException as NokautNoItemEx
from forms import RegisterForm, LoginForm
from pyramid_simpleform import Form
from sqlalchemy import and_,desc
from .models import DBSession, User, UserSearch
from pyramid.security import remember, forget,authenticated_userid, NO_PERMISSION_REQUIRED

def get_user(request):
    user_id = authenticated_userid(request)
    if user_id is not None:
        return DBSession.query(User).filter(User.id == user_id).first()

@view_config(
    route_name='home',
    renderer='pyramid_app:templates/search_box.mako'
)
def my_view(request):
    return {}


@view_config(
    route_name = 'search',
    renderer = 'pyramid_app:templates/search.mako'
)
def res_view(request):
    search_phrase = request.GET.get('search_field')
    nokaut_key = request.registry.settings.get('nokaut.key')
    user = request.user

    try :
        all = allegro_api(search_phrase)
    except AllegroNoItemEx:
        all = (None, None)

    try:
        nok = nokaut_api(search_phrase, nokaut_key)
    except NokautNoItemEx:
        nok = (None, None)

    nok_price, nok_link = nok[1], nok[0]
    all_price, all_link = all[1], all[0]

    mode = None
    if all_price and nok_price:
        if all_price < nok_price:
            mode = 'allegro'
        elif all_price > nok_price:
            mode = 'nokaut'
    elif all_price:
        mode = 'allegro'
    elif nok_price:
        mode = 'nokaut'

    if user is not None:
        prev = DBSession.query(UserSearch)\
                        .filter(UserSearch.search_id == user.id)\
                        .filter(UserSearch.search_content == search_phrase).first()

        if prev is not None:
            prev.search_quantity += 1
            DBSession.flush()
            quantity = prev.search_quantity
            last_update = prev.last_update
        else:
            prev = UserSearch(
                search_id = user.id,
                search_content = search_phrase,
                all_link = all_link or '#',
                all_price = all_price or 0,
                nok_link = nok_link or '#',
                nok_price = nok_price or 0,
                search_quantity = 1
            )
            DBSession.add(prev)

    else:
        quantity, last_update = None, None


    return {
        'product_name' : search_phrase,
        'allegro_link' : all_link,
        'nokaut_link' : nok_link,
        'allegro_price' : all_price,
        'nokaut_price' : nok_price,
        'won' : mode,
        'search_quantity' : quantity,
        'last_update' : last_update
    }


@view_config(
    route_name = 'history',
    renderer = 'pyramid_app:templates/history.mako',
    permission = 'view'
)

def history_view(request):
    user_id =  authenticated_userid(request)
    user_hist = DBSession.query(UserSearch)\
                         .filter(UserSearch.search_id == user_id).all()

    return {
        'user_hist': user_hist
    }


@view_config(route_name = 'top_search',
             renderer = 'pyramid_app:templates/top.mako',
             permission = 'view')
def top_search_view(request):
    top_search = DBSession.query(UserSearch)\
                          .order_by(desc(UserSearch.search_quantity)).limit(3)

    return {
        'top_search' : top_search
    }


@view_config(
    route_name = 'login',
    renderer = 'pyramid_app:templates/login.mako',
    permission = NO_PERMISSION_REQUIRED
)
def login_view(request):

    form = Form(request, schema = LoginForm)

    if request.method == 'POST' and form.validate():
        user = DBSession.query(User)\
                        .filter(User.username == form.data['login'])\
                        .filter(User.password == form.data['password']).first()

        headers = remember(request, user.id)
        return HTTPFound(location = '/', headers = headers)
    else:
        return {
            'errors' : set(form.errors.values())
        }


@view_config(
    route_name = 'logout',
    renderer = 'pyramid_app:templates/base.mako'
)
def logut_view(request):
    headers = forget(request)
    return HTTPFound(
        location = '/', headers = headers
    )


@view_config(
    route_name = 'register',
    renderer = 'pyramid_app:templates/register.mako',
    permission = NO_PERMISSION_REQUIRED
)
def register_view(request):
    login = request.POST.get('login')

    form = Form(request,
                    schema = RegisterForm)

    if request.method == 'POST' and form.validate():
        new_user = User(
                        username = form.data['login'],
                        password = form.data['password'],
                        group = 'viewer'
        )
        DBSession.add(new_user)
        user_id = DBSession.query(User).\
                    filter(User.username == new_user.username).first().id
        headers = remember(request, user_id)

        return  HTTPFound('/', headers = headers)
    else:
        return {
            'errors' : set(form.errors.values())
        }

@view_config(
    route_name = 'jsonview',
    renderer = 'json'
)
def json_view(request):
    return res_view(request)


@view_config(
    route_name = 'user_list',
    renderer = 'pyramid_app:templates/user_list.mako'
)
def user_list_view(request):
    """ ZROBIONE TYLKO W CELU PODGLADU ..
    """
    users = DBSession.query(User).all()
    history = DBSession.query(UserSearch).all()

    return {
        'users': users,
        'history': history
    }