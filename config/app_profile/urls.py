from django.urls import path
from . import views

urlpatterns = [
    path('my_questionnaire/', views.MyQuestionnaireListView.as_view(), name='my_questionnaire_list'),
    path('create_questionnaire/', views.QuestionnaireCreateView.as_view(), name='questionnaire_create'),
    path('edit_questionnaire/<int:pk>/', views.QuestionnaireUpdateView.as_view(), name='questionnaire_edit'),
    path('detail_questionnaire/<int:pk>/', views.QuestionnaireDetailView.as_view(), name='questionnaire_detail'),
    path('delete_questionnaire/<int:pk>/', views.QuestionnaireDeleteView.as_view(), name='questionnaire_delete'),
    path('detail_questionnaire_my/<int:pk>/', views.MyQuestionnaireDetailView.as_view(), name='my_questionnaire_detail'),

    path('ajax/questionnaire_activate_removed/', views.questionnaire_activate_removed,
         name="ajax_questionnaire_activate_removed"),


    path('my_vacancy/', views.MyVacancyListView.as_view(), name='my_vacancy_list'),
    path('create_vacancy/', views.VacancyCreateView.as_view(), name='vacancy_create'),
    path('edit_vacancy/<int:pk>/', views.VacancyUpdateView.as_view(), name='vacancy_edit'),
    path('detail_vacancy/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('delete_vacancy/<int:pk>/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('detail_vacancy_my/<int:pk>/', views.MyVacancyDetailView.as_view(), name='my_vacancy_detail'),

    path('ajax/vacancy_activate_removed/', views.vacancy_activate_removed,
         name="ajax_vacancy_activate_removed"),


    path('all_vacancy/', views.AllVacancyListView.as_view(), name='all_vacancy_list'),
]
