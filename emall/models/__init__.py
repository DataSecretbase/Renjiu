from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime,date

#Other app models
import base.models as base


from .goods import *
from .order import *
from .coupons import *
#from .datasettings import league_model as m_set
