from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils.translation import gettext_lazy as _

from app_account.decorators import checking_profile_employer, checking_profile_applicant

from .utils import set_if_not_none, true_if_not_none, set_if_value
from .forms import QuestionnaireCreateForm, QuestionnaireUpdateForm, QuestionnaireDeleteForm, VacancyCreateForm, \
    VacancyUpdateForm, VacancyDeleteForm, FilterVacancyForm
from .models import Questionnaire, Vacancy
from .decorators import checking_my_questionnaire, checking_my_questionnaire_edit, checking_my_limit_questionnaire, \
    checking_my_vacancy_edit, checking_my_vacancy


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_applicant, name='dispatch')
class MyQuestionnaireListView(ListView):
    """Список анкет пользователя"""
    model = Questionnaire
    # paginate_by = 10

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(user=self.request.user).exclude(status='deleted').order_by('-public_date')
        return queryset


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_applicant, name='dispatch')
@method_decorator(checking_my_limit_questionnaire, name='dispatch')
class QuestionnaireCreateView(CreateView):
    """Создание анкеты пользователя"""
    model = Questionnaire
    form_class = QuestionnaireCreateForm
    success_url = reverse_lazy('my_questionnaire_list')

    def form_valid(self, form):
        """привязываем анкету к авторизованному пользователю"""
        forms = form.save(commit=False)
        forms.user = self.request.user
        forms.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        last_model = Questionnaire.objects.filter(user=self.request.user)
        if last_model.exists():
            form.fields['region'].choices = [(last_model[0].region.id, last_model[0].region)]
            self.initial['region'] = last_model[0].region
            form.fields['city'].choices = [(last_model[0].city.id, last_model[0].city)]
            self.initial['city'] = last_model[0].city
        return form


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_applicant, name='dispatch')
@method_decorator(checking_my_questionnaire_edit, name='dispatch')
class QuestionnaireUpdateView(UpdateView):
    """Редактирование анкеты пользователя"""
    model = Questionnaire
    form_class = QuestionnaireUpdateForm
    success_url = reverse_lazy('my_questionnaire_list')

    def form_valid(self, form):
        forms = form.save(commit=False)
        forms.status = 'inspection'
        forms.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        last_model = Questionnaire.objects.filter(user=self.request.user)
        if len(last_model) > 1:
            form.fields['region'].choices = [(last_model[0].region.id, last_model[0].region)]
            self.initial['region'] = last_model[0].region
            form.fields['city'].choices = [(last_model[0].city.id, last_model[0].city)]
            self.initial['city'] = last_model[0].city
        return form


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_applicant, name='dispatch')
@method_decorator(checking_my_questionnaire_edit, name='dispatch')
class QuestionnaireDeleteView(UpdateView):
    """Удаление анкеты пользователя (изменение статуса)"""
    model = Questionnaire
    form_class = QuestionnaireDeleteForm

    def form_valid(self, form):
        forms = form.save(commit=False)
        forms.status = 'deleted'
        forms.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class QuestionnaireDetailView(DetailView):
    """Переходим на вакансию и отмечаем как просмотренная"""
    model = Questionnaire

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        obj.count_see.add(self.request.user)
        return obj


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_applicant, name='dispatch')
@method_decorator(checking_my_questionnaire, name='dispatch')
class MyQuestionnaireDetailView(DetailView):
    """Переходим на свою вакансию"""
    model = Questionnaire
    template_name = 'app_profile/my_questionnaire_detail.html'


def questionnaire_activate_removed(request):
    """Ajax функция _ отвечает за добавление и снятие анкеты с публикации"""
    if request.method == 'POST':
        questionnaire_id = request.POST['ajax-questionnaire-id']
        questionnaire = Questionnaire.objects.filter(pk=int(questionnaire_id), user=request.user)
        status = 'defined'
        print(22)
        if questionnaire.exists():
            questionnaire = questionnaire[0]
            if questionnaire.status == 'active' or questionnaire.status == 'removed':
                if questionnaire.status == 'active':
                    questionnaire.status = 'removed'
                elif questionnaire.status == 'removed':
                    questionnaire.status = 'active'
                status = questionnaire.status
                questionnaire.save()
        return JsonResponse({'status': status})


# Раздел для Работодателя


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_employer, name='dispatch')
class MyVacancyListView(ListView):
    """Список вакансий пользователя"""
    model = Vacancy

    def get_queryset(self):
        queryset = Vacancy.objects.filter(user=self.request.user).exclude(status='deleted').order_by('-public_date')
        return queryset


@method_decorator(login_required, name='dispatch')
class AllVacancyListView(ListView):
    """Список всех вакансий"""
    model = Vacancy
    template_name = 'app_profile/all_vacancy_list.html'
    paginate_by = 2

    def get_queryset(self):

        sort_params = {}

        set_if_value(sort_params, 'region__in', self.request.GET.getlist('regions'))
        set_if_value(sort_params, 'city__in', self.request.GET.getlist('citys'))
        set_if_value(sort_params, 'profession__in', self.request.GET.getlist('professions'))
        set_if_value(sort_params, 'work_mode__in', self.request.GET.getlist('work_modes'))

        set_if_value(sort_params, 'money__gte', self.request.GET.get('money_from'))
        set_if_value(sort_params, 'money__lte', self.request.GET.get('money_to'))

        true_if_not_none(sort_params, 'accommodation', self.request.GET.get('accommodation'))
        true_if_not_none(sort_params, 'food', self.request.GET.get('food'))
        true_if_not_none(sort_params, 'drive', self.request.GET.get('drive'))

        set_if_not_none(sort_params, 'status', 'active')

        print(sort_params)

        queryset = Vacancy.objects.filter(**sort_params).order_by('-public_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllVacancyListView, self).get_context_data(**kwargs)
        context['form'] = FilterVacancyForm(self.request.GET)
        return context


@method_decorator(login_required, name='dispatch')
class AllVacancyListView(ListView):
    """Список рекомендованных вакансий"""
    model = Vacancy
    template_name = 'app_profile/all_vacancy_list.html'
    paginate_by = 2

    def get_queryset(self):

        sort_params = {}

        set_if_value(sort_params, 'region__in', self.request.GET.getlist('regions'))
        set_if_value(sort_params, 'city__in', self.request.GET.getlist('citys'))
        set_if_value(sort_params, 'profession__in', self.request.GET.getlist('professions'))
        set_if_value(sort_params, 'work_mode__in', self.request.GET.getlist('work_modes'))

        set_if_value(sort_params, 'money__gte', self.request.GET.get('money_from'))
        set_if_value(sort_params, 'money__lte', self.request.GET.get('money_to'))

        true_if_not_none(sort_params, 'accommodation', self.request.GET.get('accommodation'))
        true_if_not_none(sort_params, 'food', self.request.GET.get('food'))
        true_if_not_none(sort_params, 'drive', self.request.GET.get('drive'))

        set_if_not_none(sort_params, 'status', 'active')

        print(sort_params)

        queryset = Vacancy.objects.filter(**sort_params).order_by('-public_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllVacancyListView, self).get_context_data(**kwargs)
        context['form'] = FilterVacancyForm(self.request.GET)
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_employer, name='dispatch')
class VacancyCreateView(CreateView):
    """Создание вакансии пользователя"""
    model = Vacancy
    form_class = VacancyCreateForm
    success_url = reverse_lazy('my_vacancy_list')

    def form_valid(self, form):
        """привязываем вакансию к авторизованному пользователю"""
        forms = form.save(commit=False)
        forms.user = self.request.user
        forms.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_employer, name='dispatch')
@method_decorator(checking_my_vacancy_edit, name='dispatch')
class VacancyUpdateView(UpdateView):
    """Редактирование вакансии пользователя"""
    model = Vacancy
    form_class = VacancyUpdateForm
    success_url = reverse_lazy('my_vacancy_list')

    def form_valid(self, form):
        forms = form.save(commit=False)
        forms.status = 'inspection'
        forms.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_employer, name='dispatch')
@method_decorator(checking_my_vacancy_edit, name='dispatch')
class VacancyDeleteView(UpdateView):
    """Удаление вакансиипользователя (изменение статуса)"""
    model = Vacancy
    form_class = VacancyDeleteForm

    def form_valid(self, form):
        forms = form.save(commit=False)
        forms.status = 'deleted'
        forms.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VacancyDetailView(DetailView):
    """Переходим на вакансию и отмечаем как просмотренная"""
    model = Vacancy

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        obj.count_see.add(self.request.user)
        return obj


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_employer, name='dispatch')
@method_decorator(checking_my_vacancy, name='dispatch')
class MyVacancyDetailView(DetailView):
    """Переходим на свою вакансию"""
    model = Vacancy
    template_name = 'app_profile/my_vacancy_detail.html'


def vacancy_activate_removed(request):
    """Ajax функция _ отвечает за добавление и снятие вакансии с публикации"""
    if request.method == 'POST':
        vacancy_id = request.POST['ajax-vacancy-id']
        vacancy = Vacancy.objects.filter(pk=int(vacancy_id), user=request.user)
        status = 'defined'
        print(22)
        if vacancy.exists():
            vacancy = vacancy[0]
            if vacancy.status == 'active' or vacancy.status == 'removed':
                if vacancy.status == 'active':
                    vacancy.status = 'removed'
                elif vacancy.status == 'removed':
                    vacancy.status = 'active'
                status = vacancy.status
                vacancy.save()
        return JsonResponse({'status': status})
