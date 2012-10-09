#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *

from tastypie.api import Api
from db.api import SmallMoleculeResource,CellResource,DataSetResource

smallmolecule_resource = SmallMoleculeResource()
v1_api = Api(api_name='v1') 
v1_api.register(SmallMoleculeResource())
v1_api.register(CellResource())
v1_api.register(DataSetResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from hmslincs_server.views import *

urlpatterns = patterns('',

    # Login / logout.
    # Note: the name "login_url" name is set to the request by the registered hmslincs.context_procesor.login_url_with_redirect
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'db/login.html'}),
    url(r'^logout/$', logout_page, name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # url(r'^???/', include('???.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^db/$', 'db.views.main', name="home"),
    url(r'^db/sm/$','db.views.smallMoleculeIndex', name="listSmallMolecules" ),
    url(r'^db/sm/(?P<sm_id>\d+)/$', 'db.views.smallMoleculeDetail', name="sm_detail"),
    url(r'^db/cells/$','db.views.cellIndex', name="listCells"),
    url(r'^db/cells/(?P<facility_id>\d+)/$', 'db.views.cellDetail', name="cell_detail"),
    url(r'^db/proteins/$','db.views.proteinIndex', name="listProteins"),
    url(r'^db/proteins/(?P<lincs_id>\d+)/$', 'db.views.proteinDetail', name="protein_detail"),
    url(r'^db/libraries/$','db.views.libraryIndex', name="listLibraries"),
    url(r'^db/libraries/(?P<short_name>[^/]+)/$', 'db.views.libraryDetail', name="library_detail"),
    url(r'^db/screen/$','db.views.screenIndex', name="listScreens"),
    url(r'^db/screen/(?P<facility_id>\d+)/$', 'db.views.screenDetailMain', name="screen_detail"),
    url(r'^db/screen/(?P<facility_id>\d+)/main$', 'db.views.screenDetailMain', name="screen_detail_main"),
    url(r'^db/screen/(?P<facility_id>\d+)/cells$', 'db.views.screenDetailCells', name="screen_detail_cells"),
    url(r'^db/screen/(?P<facility_id>\d+)/proteins$', 'db.views.screenDetailProteins', name="screen_detail_proteins"),
    url(r'^db/screen/(?P<facility_id>\d+)/results$', 'db.views.screenDetailResults', name="screen_detail_results"),
    url(r'^db/study/$','db.views.studyIndex', name="listStudies"),
    #url(r'^db/search/', include('haystack.urls'), name="haystackSearch"),
    
    (r'^db/api/', include(v1_api.urls)),
)
