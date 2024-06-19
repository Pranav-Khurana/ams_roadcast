from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
manager_bp = Blueprint('manager', __name__)
staff_bp = Blueprint('staff', __name__)

from routes.auth_routes import *
from routes.manager_routes import *
from routes.staff_routes import *