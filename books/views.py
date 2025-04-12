from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm
from .utils import (
    process_wikipedia_info,
    generate_author_gpt_info,
    generate_audio_script,
    create_tts_audio,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.http import JsonResponse
from django.db.models import Q
import re

# Create your views here.
@require_http_methods(["GET", "POST"])
def index(request):
    books = Book.objects.all()
    
    # 검색어 처리
    original_query = request.GET.get('query', '')
    if original_query:
        # 원본 검색어 저장
        original_search_query = original_query
        
        # 공백을 제거한 검색어 생성
        no_space_query = original_query.replace(' ', '')
        
        # 검색어에서 공백을 유연하게 처리하기 위한 정규식 패턴 생성
        # 예: "노인과 바다" -> "노인\s*과\s*바다"
        # 이렇게 하면 "노인과바다", "노인 과 바다" 등도 검색 가능
        flexible_query = ''
        for char in original_query:
            if char == ' ':
                continue
            flexible_query += char + r'\s*'
        flexible_query = flexible_query.rstrip(r'\s*')
        
        # 다양한 검색 조건을 OR 조건으로 결합
        books = books.filter(
            Q(title__icontains=original_query) | 
            Q(author__icontains=original_query) | 
            Q(description__icontains=original_query) | 
            Q(author_info__icontains=original_query) |
            # 공백 제거 검색 추가
            Q(title__iregex=flexible_query) |
            Q(author__iregex=flexible_query) |
            # 완전한 공백 제거 검색도 추가 (정규식 없이)
            Q(title__icontains=no_space_query) |
            Q(author__icontains=no_space_query)
        ).distinct()  # 중복 결과 제거
    
    # AJAX 요청인 경우 JSON 응답 반환
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        book_list = []
        for book in books:
            book_data = {
                'id': book.pk,
                'title': book.title,
                'author': book.author,
                'description': book.description[:100] + '...' if len(book.description) > 100 else book.description,
                'cover_image': book.cover_image.url if book.cover_image else None,
                'customer_review_rank': float(book.customer_review_rank),
                'detail_url': f'/books/{book.pk}/'
            }
            book_list.append(book_data)
        
        return JsonResponse({'books': book_list})
    
    context = {
        "books": books,
    }
    return render(request, "books/index.html", context)

@require_http_methods(["GET", "POST"])
@login_required
def create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)

            wiki_summary = process_wikipedia_info(book)

            author_info, author_works = generate_author_gpt_info(
                book, wiki_summary
            )
            book.author_info = author_info
            book.author_works = author_works
            book.save()

            audio_script = generate_audio_script(book, wiki_summary)

            audio_file_path = create_tts_audio(book, audio_script)
            if audio_file_path:
                book.audio_file = audio_file_path
                book.save()

            return redirect("books:detail", book.pk)
    else:
        form = BookForm()
    context = {"form": form}
    return render(request, "books/create.html", context)

@require_safe
def detail(request, pk):
    book = Book.objects.get(pk=pk)
    context = {
        "book": book,
    }
    return render(request, "books/detail.html", context)

@require_http_methods(["GET", "POST"])
@login_required
def update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books:detail", pk)
    else:
        form = BookForm(instance=book)
    context = {
        "form": form,
        "book": book,
    }
    return render(request, "books/update.html", context)

@require_POST
@login_required
def delete(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect("books:index")


