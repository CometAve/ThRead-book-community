document.addEventListener('DOMContentLoaded', function() {
  const searchForm = document.getElementById('searchForm');
  const searchInput = document.getElementById('searchInput');
  const searchButton = document.getElementById('searchButton');
  const bookList = document.getElementById('bookList');
  const resultCount = document.getElementById('resultCount');
  const searchResultMessage = document.getElementById('searchResultMessage');
  
  // 검색 폼 제출 이벤트 처리
  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    
    if (query) {
      performSearch(query);
    }
  });
  
  // 검색 결과 없을 때 리셋 버튼 처리 (동적 추가된 경우)
  document.addEventListener('click', function(e) {
    if (e.target && (e.target.id === 'resetSearchBtn' || e.target.closest('#resetSearchBtn'))) {
      e.preventDefault();
      window.location.href = indexUrl;
    }
  });
  
  // 검색 실행 함수
  function performSearch(query) {
    // AJAX 요청 생성
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `${indexUrl}?query=${encodeURIComponent(query)}`, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onload = function() {
      if (xhr.status >= 200 && xhr.status < 300) {
        const response = JSON.parse(xhr.responseText);
        updateBookList(response.books, query);
        
        // URL 히스토리 업데이트 (페이지 새로고침 없이 URL 변경)
        const url = new URL(window.location.href);
        url.searchParams.set('query', query);
        window.history.pushState({}, '', url);
      } else {
        console.error('검색 중 오류가 발생했습니다.');
      }
    };
    
    xhr.onerror = function() {
      console.error('네트워크 오류가 발생했습니다.');
    };
    
    xhr.send();
  }
  
  // 도서 목록 업데이트 함수
  function updateBookList(books, query) {
    // 검색 결과 메시지 표시
    searchResultMessage.classList.remove('d-none');
    resultCount.textContent = books.length;
    
    // 도서 목록 영역 참조
    const container = document.querySelector('.container');
    const existingBookList = document.getElementById('bookList');
    const existingEmptyResult = container.querySelector('.empty-result');
    
    // 이전 결과 초기화
    if (existingEmptyResult) {
      container.removeChild(existingEmptyResult);
    }
    
    if (books.length === 0) {
      // 검색 결과가 없을 경우
      if (existingBookList) {
        // 기존 도서 목록이 있다면 숨김
        existingBookList.style.display = 'none';
      }
      
      // 템플릿에서 검색 결과 없음 메시지 생성
      const emptyTemplate = document.getElementById('empty-result-template');
      const emptyNode = document.importNode(emptyTemplate.content, true);
      
      // 검색어 설정
      const heading = emptyNode.querySelector('.alert-heading');
      heading.textContent = `"${query}"에 대한 검색 결과가 없습니다`;
      
      // 모든 도서 보기 버튼에 정확한 링크 설정
      const resetBtn = emptyNode.querySelector('#resetSearchBtn');
      resetBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = indexUrl;
      });
      
      // 클래스 추가하여 나중에 식별 가능하게 함
      const emptyResultDiv = document.createElement('div');
      emptyResultDiv.className = 'empty-result';
      emptyResultDiv.appendChild(emptyNode);
      
      // 검색 결과 메시지 다음에 삽입
      const searchResultMessage = document.getElementById('searchResultMessage');
      container.insertBefore(emptyResultDiv, searchResultMessage.nextSibling);
      
      // 새 도서 등록 버튼 숨김 (이미 있는 경우)
      const addBookBtn = container.querySelector('.d-flex.justify-content-center.mt-5');
      if (addBookBtn) {
        addBookBtn.style.display = 'none';
      }
    } else {
      // 검색 결과가 있을 경우
      
      // 새 도서 목록 생성
      let bookListElement;
      if (existingBookList) {
        // 기존 도서 목록이 있으면 재사용
        bookListElement = existingBookList;
        bookListElement.style.display = 'flex';
        bookListElement.style.flexWrap = 'wrap';
        bookListElement.innerHTML = '';
      } else {
        // 없으면 새로 생성
        bookListElement = document.createElement('div');
        bookListElement.id = 'bookList';
        bookListElement.className = 'row row-cols-1 row-cols-md-3 g-4';
        container.insertBefore(bookListElement, searchResultMessage.nextSibling);
      }
      
      // 도서 카드 추가
      books.forEach(function(book) {
        const bookCard = createBookCard(book);
        bookListElement.appendChild(bookCard);
      });
      
      // 도서 등록 버튼 표시
      const addBookBtn = container.querySelector('.d-flex.justify-content-center.mt-5');
      if (addBookBtn) {
        addBookBtn.style.display = 'flex';
      }
    }
  }
  
  // 도서 카드 생성 함수
  function createBookCard(book) {
    const template = document.getElementById('book-card-template');
    const cardNode = document.importNode(template.content, true);
    
    // 카드 데이터 채우기
    const cardTitle = cardNode.querySelector('.card-title');
    const authorName = cardNode.querySelector('.author-name');
    const coverContainer = cardNode.querySelector('.cover-container');
    const cardText = cardNode.querySelector('.card-text');
    const reviewRank = cardNode.querySelector('.review-rank');
    const detailLink = cardNode.querySelector('.detail-link');
    
    cardTitle.textContent = book.title;
    authorName.textContent = book.author;
    cardText.textContent = book.description;
    reviewRank.textContent = book.customer_review_rank;
    detailLink.href = book.detail_url;
    
    // 커버 이미지 처리
    if (book.cover_image) {
      const coverImg = cardNode.querySelector('.card-img-top');
      coverImg.src = book.cover_image;
      coverImg.alt = book.title;
    } else {
      const noImageTemplate = document.getElementById('no-image-template');
      const noImageNode = document.importNode(noImageTemplate.content, true);
      coverContainer.parentNode.replaceChild(noImageNode, coverContainer);
    }
    
    // 별점 설정
    const ratingDiv = cardNode.querySelector('.rating');
    for (let i = 1; i <= 5; i++) {
      const star = document.createElement('small');
      if (i <= book.customer_review_rank || i <= (book.customer_review_rank + 0.5)) {
        star.className = 'text-warning';
        star.textContent = '★';
      } else {
        star.className = 'text-secondary';
        star.textContent = '☆';
      }
      ratingDiv.appendChild(star);
    }
    
    return cardNode;
  }
  
  // 동적으로 추가된 초기화 버튼을 위한 함수
  function addResetButton() {
    // 기존 입력 그룹 선택
    const inputGroup = document.querySelector('.input-group');
    
    // 이미 초기화 버튼이 있는지 확인
    if (!document.getElementById('resetButton') && searchInput.value.trim()) {
      // 초기화 버튼 생성
      const resetBtn = document.createElement('a');
      resetBtn.id = 'resetButton';
      resetBtn.className = 'btn btn-outline-secondary ms-2';
      resetBtn.innerHTML = '<i class="bi bi-x-circle"></i> 초기화';
      resetBtn.href = indexUrl;
      
      // 입력 그룹에 버튼 추가
      inputGroup.appendChild(resetBtn);
    }
  }
  
  // 검색 후 초기화 버튼 추가
  if (searchInput.value.trim()) {
    addResetButton();
  }
});