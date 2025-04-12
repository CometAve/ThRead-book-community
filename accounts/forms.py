from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from books.models import Category, CATEGORY_CHOICES
from django.forms.widgets import CheckboxSelectMultiple


class CustomUserCreationForm(UserCreationForm):
    # MultipleChoiceField로 관심 장르 필드 추가
    interested_genres = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,  # 직접 CATEGORY_CHOICES 사용
        widget=CheckboxSelectMultiple,
        required=False,
        label='관심 장르'
    )
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'gender', 
            'age', 
            'weekly_reading_hours', 
            'yearly_reading_count', 
            'profile_image',
            'interested_genres',
            'password1', 
            'password2'
        )
        labels = {
            'username': '아이디',
            'first_name': '이름',
            'last_name': '성',
            'email': '이메일',
            'gender': '성별',
            'age': '나이',
            'weekly_reading_hours': '주간 평균 독서 시간',
            'yearly_reading_count': '연간 독서량',
            'profile_image': '프로필 사진',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 패스워드 필드의 레이블을 한글로 설정
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
        
        # 동적인 카테고리 로딩도 유지 (백업 방식으로)
        try:
            categories = Category.objects.all()
            if categories.exists():  # 카테고리가 존재하는 경우에만 업데이트
                choices = [(category.name, category.name) for category in categories]
                self.fields['interested_genres'].choices = choices
        except:
            # 예외 발생 시 기본 CATEGORY_CHOICES 유지
            pass
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # 선택한 관심 장르를 쉼표로 구분된 문자열로 변환하여 저장
        selected_genres = self.cleaned_data.get('interested_genres', [])
        user.interested_genres = ','.join(selected_genres)
        
        if commit:
            user.save()
        return user
        
class CustomUserChangeForm(UserChangeForm):
    # MultipleChoiceField로 관심 장르 필드 추가
    interested_genres = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,  # 직접 CATEGORY_CHOICES 사용
        widget=CheckboxSelectMultiple,
        required=False,
        label='관심 장르'
    )
    
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'first_name', 
            'last_name', 
            'email', 
            'gender', 
            'age', 
            'weekly_reading_hours', 
            'yearly_reading_count', 
            'profile_image',
            'interested_genres',
        )
        labels = {
            'username': '아이디',
            'first_name': '이름',
            'last_name': '성',
            'email': '이메일',
            'gender': '성별',
            'age': '나이',
            'weekly_reading_hours': '주간 평균 독서 시간',
            'yearly_reading_count': '연간 독서량',
            'profile_image': '프로필 사진',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'password' in self.fields:
            self.fields.pop('password')
            
        # 동적인 카테고리 로딩도 유지 (백업 방식으로)
        try:
            categories = Category.objects.all()
            if categories.exists():  # 카테고리가 존재하는 경우에만 업데이트
                choices = [(category.name, category.name) for category in categories]
                self.fields['interested_genres'].choices = choices
            
            # 사용자의 기존 관심 장르를 초기 선택값으로 설정
            if self.instance and hasattr(self.instance, 'interested_genres') and self.instance.interested_genres:
                user_genres = self.instance.interested_genres.split(',')
                self.initial['interested_genres'] = user_genres
        except:
            # 예외 발생 시 기본 CATEGORY_CHOICES 유지
            pass
            
    def save(self, commit=True):
        user = super().save(commit=False)
        # 선택한 관심 장르를 쉼표로 구분된 문자열로 변환하여 저장
        selected_genres = self.cleaned_data.get('interested_genres', [])
        user.interested_genres = ','.join(selected_genres)
        
        if commit:
            user.save()
        return user

