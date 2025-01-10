import app.views
from django.urls import path


urlpatterns = [
    path('<str:module>/', app.views.SysView.as_view()),
    path('notices/<str:module>/', app.views.NoticesView.as_view()),
    path('departments/<str:module>/', app.views.DepartmentsView.as_view()),
    path('doctors/<str:module>/', app.views.DoctorsView.as_view()),
    path('patients/<str:module>/', app.views.PatientsView.as_view()),
    path('registes/<str:module>/', app.views.RegisterLogsView.as_view()),
    path('beds/<str:module>/', app.views.BedsView.as_view()),
    path('inhospital/<str:module>/', app.views.HospitalizationLogsView.as_view()),
    path('managers/<str:module>/', app.views.ManagersView.as_view()),
    path('queue/<str:module>/', app.views.QueueLogsView.as_view()),
    path('prescripts/<str:module>/', app.views.PrescriptionView.as_view()),
    path('reports/<str:module>/', app.views.ReportsView.as_view()),
    path('medicine/<str:module>/', app.views.MedicineView.as_view()),
    path('inware/<str:module>/', app.views.MedicineInWareView.as_view()),
]
