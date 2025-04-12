import json
import requests
import os
import uuid
from pathlib import Path
from django.conf import settings
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI
from .models import Book

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)


def translate_to_english(korean_name):
    """GPT를 이용해 한국어 작가명을 영어로 번역"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 더 작고 빠른 모델 사용
            messages=[
                {"role": "system", "content": "당신은 한국어 작가명을 영어로 변환하는 전문가입니다. 오직 영어 이름만 출력하세요."},
                {"role": "user", "content": f"다음 작가 이름을 영어로 변환해주세요. 위키피디아에서 검색할 수 있는 정확한 영어 표기법으로 변환하세요. 출력은 영어 이름만 포함해야 합니다: {korean_name}"}
            ],
            max_tokens=100
        )
        english_name = response.choices[0].message.content.strip()
        # 따옴표나 기타 불필요한 문자 제거
        english_name = english_name.replace('"', '').replace("'", "")
        print(f"GPT 번역: '{korean_name}' -> '{english_name}'")
        return english_name
    except Exception as e:
        print(f"GPT 번역 오류: {e}")
        return None


def get_wikipedia_info(author_name):
    """한국어 작가명과 GPT 변환 영어 이름으로 위키피디아에서 작가 정보와 이미지 검색"""
    name_variants = [author_name.replace(' ', '_')]  # 기본 이름 (공백 -> 언더스코어)
    
    # 1. 한국어 위키피디아 API로 먼저 시도
    url_ko = f"https://ko.wikipedia.org/api/rest_v1/page/summary/{name_variants[0]}"
    try:
        response = requests.get(url_ko)
        if response.status_code == 200:
            data = response.json()
            author_info = data.get('extract', '')
            author_image = data.get('thumbnail', {}).get('source', '')
            if author_image:
                print(f"한국어 위키피디아에서 이미지 찾음: {author_image}")
                return author_info, author_image
    except Exception as e:
        print(f"한국어 위키피디아 검색 오류: {e}")

    # 2. GPT를 이용해 한국어 작가명을 영어로 변환
    english_name = translate_to_english(author_name)
    if english_name:
        # 영어 이름에서 공백을 언더스코어로 변경
        english_name_variant = english_name.replace(' ', '_')
        name_variants.append(english_name_variant)
        
        # 영어 위키피디아 시도
        url_en = f"https://en.wikipedia.org/api/rest_v1/page/summary/{english_name_variant}"
        try:
            response = requests.get(url_en)
            if response.status_code == 200:
                data = response.json()
                english_info = data.get('extract', '')
                english_image = data.get('thumbnail', {}).get('source', '')
                if english_image:
                    print(f"영어 위키피디아에서 이미지 찾음: {english_image}")
                    # 영문 정보가 있지만 한글 정보가 없는 경우 GPT를 이용해 번역 (선택 사항)
                    # 여기서는 간단히 영문 정보 사용
                    return english_info, english_image
        except Exception as e:
            print(f"영문 위키피디아 검색 오류: {e}")

    # 3. MediaWiki API 시도
    for name_variant in name_variants:
        image_url = try_mediawiki_api(name_variant)
        if image_url:
            print(f"MediaWiki API에서 이미지 찾음: {image_url}")
            return "", image_url

    # 모든 시도 실패
    print(f"작가 '{author_name}'의 이미지를 찾을 수 없습니다.")
    return '', ''


def try_mediawiki_api(author_name):
    """MediaWiki API를 사용하여 작가 이미지 검색"""
    # 한국어 위키피디아 시도
    url_ko = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": author_name,
        "prop": "pageimages",
        "format": "json",
        "piprop": "original|thumbnail",
        "pithumbsize": 500,
    }
    
    try:
        response = requests.get(url_ko, params=params)
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            for page_id, page_data in pages.items():
                if page_id == "-1":  # 페이지가 없는 경우
                    continue
                    
                # 원본 이미지 시도
                original = page_data.get("original", {})
                if original:
                    return original.get("source")
                
                # 썸네일 이미지 시도
                thumbnail = page_data.get("thumbnail", {})
                if thumbnail:
                    return thumbnail.get("source")
    except Exception as e:
        print(f"MediaWiki API 검색 오류: {e}")
    
    # 영문 위키피디아도 시도
    url_en = "https://en.wikipedia.org/w/api.php"
    try:
        response = requests.get(url_en, params=params)
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            for page_id, page_data in pages.items():
                if page_id == "-1":  # 페이지가 없는 경우
                    continue
                    
                # 원본 이미지 시도
                original = page_data.get("original", {})
                if original:
                    return original.get("source")
                
                # 썸네일 이미지 시도
                thumbnail = page_data.get("thumbnail", {})
                if thumbnail:
                    return thumbnail.get("source")
    except Exception as e:
        print(f"영문 MediaWiki API 검색 오류: {e}")
    
    return None


def process_wikipedia_info(book):
    """책 정보를 기반으로 위키피디아에서 작가 정보와 이미지 가져오기"""
    author_info, img_url = get_wikipedia_info(book.author)
    
    # 작가 정보가 없으면 기본 메시지 설정
    if not author_info:
        author_info = "위키피디아에서 정보를 찾을 수 없습니다."
    
    # 저장 전 book 객체에 pk가 없으면 저장
    if not book.pk:
        book.save()
    
    # 이미지 URL이 있으면 다운로드 및 저장
    if img_url:
        try:
            response_img = requests.get(img_url, stream=True)
            if response_img.status_code == 200:
                # 저장 디렉토리 생성
                output_dir = Path(settings.MEDIA_ROOT) / "author_profiles"
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # 고유한 파일명 생성
                safe_author_name = book.author.replace(' ', '_').replace(',', '').replace('.', '')
                file_name = f"author_{book.pk}_{safe_author_name}.jpg"
                
                # 직접 ImageField에 저장
                from django.core.files.base import ContentFile
                
                book.author_profile_img.save(
                    file_name, 
                    ContentFile(response_img.content), 
                    save=True
                )
                
                print(f"작가 이미지 저장 완료: {file_name}")
            else:
                print(f"이미지 다운로드 실패: HTTP {response_img.status_code}")
        except Exception as e:
            print(f"작가 이미지 저장 중 오류 발생: {e}")
    else:
        print(f"작가 '{book.author}'의 이미지 URL을 찾을 수 없음")
    
    return author_info


def generate_author_data(author_name, author_info, book_title):
    """Generate author information and works using OpenAI API, 반환 형식은 JSON이어야 함."""
    try:
        prompt = (
            f"다음 정보를 바탕으로 '{book_title}'를 쓴 작가 {author_name}의 정보를 JSON 형식으로 출력하세요.\n"
            f"작가 정보(텍스트)와 대표작 목록을 반환해야 합니다.\n"
            "반환 형식 예시:\n"
            "{\n"
            '  "author_info": "여기에 작가에 관한 간단한 소개를 작성",\n'
            '  "author_works": ["대표작1", "대표작2", "대표작3"]\n'
            "}\n\n"
            f"정보: {author_info}\n\n"
            "반드시 응답은 위에 보인 JSON 형식만 포함해야 하며, 다른 텍스트는 추가하지 마세요."
        )
        
        # response_format 파라미터를 추가하여 JSON 형식 강제
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 JSON 형식의 출력을 제공하는 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},  # JSON 응답 강제
            max_tokens=300
        )
        
        content = response.choices[0].message.content.strip()
        print("GPT 응답:", content)
        
        # JSON 파싱
        data = json.loads(content)
        
        # 디버깅 출력
        print("파싱된 데이터:", data)
        print("author_info 존재:", "author_info" in data)
        print("author_works 존재:", "author_works" in data)
        
        return {
            "author_info": data.get("author_info", "정보를 찾을 수 없습니다."),
            "author_works": data.get("author_works", ["작품 정보 없음"])
        }
    except Exception as e:
        print(f"Error generating author data: {e}")
        # 오류 발생 시 기본값 반환
        return {
            "author_info": f"{author_name}에 대한 정보를 가져오는 중 오류가 발생했습니다.",
            "author_works": ["정보 없음"]
        }


def generate_author_gpt_info(book, wiki_summary):
    """OpenAI를 사용하여 작가 정보와 작품 생성 - 기존 프로젝트 호환성 유지"""
    author_data = generate_author_data(book.author, wiki_summary, book.title)
    return author_data["author_info"], ", ".join(author_data["author_works"]) if isinstance(author_data["author_works"], list) else author_data["author_works"]


def generate_audio_script(book, wiki_summary):
    """도서 소개용 오디오 스크립트를 생성 (약 1분 이상 분량)"""
    author_data = {"author_info": book.author_info}
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=2040,  # 충분한 텍스트 분량 보장
            messages=[
                {"role": "system", "content": "당신은 도서 소개용 오디오 스크립트를 작성하는 전문가입니다."},
                {"role": "user", "content": (
                    f"다음 정보를 바탕으로 '{book.title}'라는 도서를 소개하는 오디오 스크립트를 작성해주세요.\n"
                    f"저자: {book.author}\n"
                    f"도서 설명: {book.description}\n"
                    f"저자 정보: {book.author_info}\n"
                    f"저자 대표작: {book.author_works}\n"
                    f"위키피디아 요약: {wiki_summary}\n\n"
                    "스크립트는 최소 1분 이상 분량(한국어 음성 기준)으로, 도서의 주요 내용, 특색, 그리고 도서가 주는 감동과 영향을 상세하게 서술해주세요. "
                    "자연스럽고 감성적인 어조로, 청취자가 도서에 대한 깊은 이해와 흥미를 느낄 수 있도록 충분한 정보를 포함해 작성해주시기 바랍니다."
                )}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating audio script: {e}")
        return f"'{book.title}' by {book.author}. {book.description[:100]}..."


def create_tts_audio(book, audio_script):
    """TTS를 사용하여 오디오 파일 생성"""
    try:
        # Ensure directory exists
        output_dir = Path(settings.MEDIA_ROOT) / "tts"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_name = f"tts_{book.pk}_{uuid.uuid4().hex[:8]}.mp3"
        output_path = output_dir / file_name
        
        # Create audio file
        tts = gTTS(text=audio_script, lang='ko')
        tts.save(str(output_path))
        return str(Path("tts") / file_name)
    except Exception as e:
        print("gTTS 음성 파일 생성 에러:", e)
        return None


def save_author_data_to_db(author_name, author_data):
    """작가 데이터를 DB에 저장"""
    try:
        author_record = Book.objects.create(
            author=author_name,
            author_info=author_data.get("author_info", ""),
            author_works=", ".join(author_data.get("author_works", ["정보 없음"])) if isinstance(author_data.get("author_works"), list) else author_data.get("author_works", "정보 없음")
        )
        return author_record
    except Exception as e:
        print(f"DB 저장 중 오류 발생: {e}")
        return None
