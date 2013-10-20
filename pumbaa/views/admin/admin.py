'''
Created on Oct 19, 2013

@author: boatkrap
'''

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pumbaa import models

@view_config(route_name='admin.index', 
             permission='admin', 
             renderer='/admin/index.mako')
def index(request):
    return dict()