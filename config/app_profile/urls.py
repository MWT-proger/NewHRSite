from django.urls import path
from . import views

urlpatterns = [
    path('my_questionnaire/', views.MyQuestionnaireListView.as_view(), name='my_questionnaire_list'),
    path('create_questionnaire/', views.QuestionnaireCreateView.as_view(), name='questionnaire_create'),
    path('edit_questionnaire/<uuid:slug>/', views.QuestionnaireUpdateView.as_view(), name='questionnaire_edit'),
    path('detail_questionnaire/<uuid:slug>/', views.QuestionnaireDetailView.as_view(), name='questionnaire_detail'),
    path('delete_questionnaire/<uuid:slug>/', views.QuestionnaireDeleteView.as_view(), name='questionnaire_delete'),
    path('detail_questionnaire_my/<uuid:slug>/', views.MyQuestionnaireDetailView.as_view(), name='my_questionnaire_detail'),

    path('ajax/questionnaire_activate_removed/', views.questionnaire_activate_removed,
         name="ajax_questionnaire_activate_removed"),


    path('my_vacancy/', views.MyVacancyListView.as_view(), name='my_vacancy_list'),
    path('create_vacancy/', views.VacancyCreateView.as_view(), name='vacancy_create'),
    path('edit_vacancy/<uuid:slug>/', views.VacancyUpdateView.as_view(), name='vacancy_edit'),
    path('detail_vacancy/<uuid:slug>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('delete_vacancy/<uuid:slug>/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('detail_vacancy_my/<uuid:slug>/', views.MyVacancyDetailView.as_view(), name='my_vacancy_detail'),

    path('ajax/vacancy_activate_removed/', views.vacancy_activate_removed,
         name="ajax_vacancy_activate_removed"),


    path('all_vacancy/', views.AllVacancyListView.as_view(), name='all_vacancy_list'),
    path('recommended_vacancy/', views.RecommendedVacancyListView.as_view(), name='recommended_vacancy_list'),
    path('all_questionnaire/', views.AllQuestionnaireListView.as_view(), name='all_questionnaire_list'),

    path('demo_vacancy/', views.DemoVacancyListView.as_view(), name='demo_vacancy_list'),
]
