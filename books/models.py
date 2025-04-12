from django.db import models


# 카테고리 이름을 담는 튜플 리스트 정의
CATEGORY_CHOICES = [
    ('소설/시/희곡', '소설/시/희곡'),
    ('경제/경영', '경제/경영'),
    ('자기계발', '자기계발'),
    ('인문/교양', '인문/교양'),
    ('과학', '과학'),
    ('취미/실용', '취미/실용'),
    ('어린이/청소년', '어린이/청소년'),
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    customer_review_rank = models.IntegerField()
    author = models.CharField(max_length=15)
    author_profile_img = models.ImageField(upload_to="author_profiles/", blank=True)
    author_info = models.TextField()
    author_works = models.CharField(max_length=50)
    cover_image = models.ImageField(blank=True)
    audio_file = models.FileField(upload_to="tts/", blank=True, null=True)
