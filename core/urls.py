from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # basic links------------------------------------------------------------------------------------
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('register/', views.registerView, name="reg-form"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('createcv/', views.createCv, name="createcv"),
    path('cv-detail/<id>', views.viewPDF, name="cv-detail"),
    path('cv-detail1/<id>', views.viewPDF1, name="cv-detail1"),
    path('cv-detail2/<id>', views.viewPDF2, name="cv-detail2"),
    path('cv-detail3/<id>', views.viewPDF3, name="cv-detail3"),
    path('cv-detail4/<id>', views.viewPDF4, name="cv-detail4"),
    path('cv-detail5/<id>', views.viewPDF5, name="cv-detail5"),
    path('cv-detail6/<id>', views.viewPDF6, name="cv-detail6"),
    path('cv-detail7/<id>', views.viewPDF7, name="cv-detail7"),
    path('s-t/<id>', views.selectPDF, name="s-t"),
    path('cv-edit/', views.editCv, name="cv-edit"),
    path('cv-download/<id>', views.GeneratePdf.as_view(),name="cv-download"), 



    # delete links-------------------------------------------------------------------------------- 
    path('cv-edit/deleteprofile/', views.deleteProfile, name="profile-delete"),
    path('cv-edit/eduview/delete_academic/', views.deleteAcademic, name="delete_academic"),
    path('cv-edit/expview/delete_experiance/', views.deleteExp, name="delete_exp"),
    path('cv-edit/skillview/delete_skill/', views.deleteSkill, name="delete_skill"),
    path('cv-edit/linkview/delete_link/', views.deleteLink, name="delete_link"),
    path('cv-edit/hobbyview/delete/hobby/', views.deleteHobby, name="delete_hobby"),
    path('cv-edit/langview/delete/lang/', views.deletelang, name="delete_lang"),
    path('cv-edit/ecaview/delete/eca/', views.deleteeca, name="delete_eca"),
    path('cv-edit/refview/delete/ref/', views.deleteref, name="delete_ref"),



    #update links-----------------------------------------------------------------------------  
    path('cv-edit/refview/update_ref/', views.updateref, name="update_ref"),
    path('cv-edit/ecaview/update_eca/', views.updateeca, name="update_eca"),
    path('cv-edit/langview/update_lang/', views.updatelang, name="update_lang"),
    path('cv-edit/hobbyview/update_hobby/', views.updatehobby, name="update_hobby"),
    path('cv-edit/linkview/update_link/', views.updatelink, name="update_link"),
    path('cv-edit/skillview/update_skill/', views.updateskill, name="update_skill"),
    path('cv-edit/expview/update_experiance/', views.updateexp, name="update_exp"),
    path('cv-edit/eduview/update_academic/', views.updateAcademic, name="update_academic"),
    path('cv-edit/updateprofile/', views.updateProfile, name="profile-update"),


    # save links-----------------------------------------------------------------------------
    path('profile-save/', views.uploadProfile, name="profile-save"),
    path('skill-save/', views.saveSkill, name="skill-save"),
    path('edu-save/', views.saveEducation, name="edu-save"),
    path('exp-save/', views.saveExperiance, name="exp-save"),
    path('ref-save/', views.saveReferee, name="ref-save"),
    path('link-save/', views.saveLink, name="link-save"),
    path('hobby-save/', views.saveHobby, name="hobby-save"),
    path('lang-save/', views.saveLang, name="lang-save"),
    path('eca-save/', views.saveEca, name="eca-save"),

    # fetch links-----------------------------------------------------------------------------
    path('cv-edit/fetchprofile/', views.fetchProfile, name="fetchprofile"),
    path('cv-edit/eduview/academic/', views.fetchAcademic, name="fetchacademic"),
    path('cv-edit/expview/experiance/', views.fetchexp, name="fetchexp"),
    path('cv-edit/skillview/skill/', views.fetchskill, name="fetchskill"),
    path('cv-edit/linkview/link/', views.fetchlink, name="fetchlink"),
    path('cv-edit/hobbyview/hobby/', views.fetchHobby, name="fetchhobby"),
    path('cv-edit/langview/lang/', views.fetchlang, name="fetchlang"),
    path('cv-edit/ecaview/eca/', views.fetcheca, name="fetcheca"),
    path('cv-edit/refview/ref/', views.fetchref, name="fetchref"),



    # views links-----------------------------------------------------------------------------
    path('cv-edit/eduview/', views.educationView, name="edu-view"),
    path('cv-edit/expview/', views.experianceView, name="exp-view"),
    path('cv-edit/skillview/', views.skillView, name="skill-view"),
    path('cv-edit/linkview/', views.linkView, name="link-view"),
    path('cv-edit/hobbyview/', views.hobbyView, name="hobby-view"),
    path('cv-edit/langview/', views.langView, name="lang-view"),
    path('cv-edit/ecaview/', views.ecaView, name="eca-view"),
    path('cv-edit/refview/', views.refView, name="ref-view"),

]
