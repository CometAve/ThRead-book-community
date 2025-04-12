from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from . models import User
from . forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

# Create your views here.
@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect("books:index")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("books:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)

@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect("books:index")

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned_data에서 선택된 관심 장르 추출
            selected_genres = form.cleaned_data.get('interested_genres', [])
            # 변환된 문자열을 User 객체의 interested_genres 필드에 할당
            user.interested_genres = ','.join(selected_genres)
            # User 객체 저장
            user.save()
            auth_login(request, user)
            return redirect("books:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)

@login_required
@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned_data에서 선택된 관심 장르 추출
            selected_genres = form.cleaned_data.get('interested_genres', [])
            # 변환된 문자열을 User 객체의 interested_genres 필드에 할당
            user.interested_genres = ','.join(selected_genres)
            # User 객체 저장
            user.save()
            return redirect("books:index")
    else:
        # 현재 User 객체의 interested_genres 문자열 확인
        current_genres = []
        if request.user.interested_genres:
            # 쉼표로 분리하여 Category 이름 리스트 만들기
            current_genres = request.user.interested_genres.split(',')
        
        # 폼 생성 및 initial 값 설정
        form = CustomUserChangeForm(instance=request.user, initial={'interested_genres': current_genres})
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)

@login_required
@require_POST
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("books:index")

@login_required
@require_http_methods(["GET", "POST"])
def change_password(request, user_pk):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("books:index")
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


@login_required
@require_http_methods(["GET"])
def profile(request, username):
    if request.user.username != username:
        return redirect("books:index")
    
    user = request.user
    # 관심 장르 처리
    genre_list = []
    if user.interested_genres:
        genre_list = [genre.strip() for genre in user.interested_genres.split(',') if genre.strip()]
    
    context = {
        "profile_user": user,
        "genre_list": genre_list,
    }
    return render(request, "accounts/profile.html", context)
