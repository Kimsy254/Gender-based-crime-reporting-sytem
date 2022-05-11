from django.urls import path
from users import views

app_name = 'users'

urlpatterns =[
    path('signup/',views.SignUp,name="signup"),
    path('signup/member_signup/',views.MemberSignUp,name="MemberSignUp"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('member/<int:pk>/',views.MemberDetailView.as_view(),name="member_detail"), 
    path('update/member/<int:pk>/',views.MemberUpdateView,name="member_update"),
    path('change_password/',views.change_password,name="change_password"),
]
