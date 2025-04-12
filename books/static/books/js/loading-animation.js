document.addEventListener('DOMContentLoaded', function() {
  console.log('Loading animation script loaded');
  
  const form = document.getElementById('book-form');
  console.log('Form element:', form);
  
  const loadingOverlay = document.getElementById('loading-overlay');
  console.log('Loading overlay element:', loadingOverlay);
  
  const loadingProgress = document.getElementById('loading-progress');
  const loadingMessage = document.getElementById('loading-message');
  
  const messages = [
    "작가 정보를 검색하고 있습니다...",
    "작가 프로필을 생성 중입니다...",
    "책 내용을 분석하고 있습니다...",
    "음성 설명을 생성하고 있습니다...",
    "거의 완료되었습니다..."
  ];
  
  if (form) {
    console.log('Form found, attaching submit event listener');
    form.addEventListener('submit', function(e) {
      console.log('Form submitted');
      
      // 폼 유효성 검사
      const title = document.getElementById('id_title')?.value.trim();
      const author = document.getElementById('id_author')?.value.trim();
      const description = document.getElementById('id_description')?.value.trim();
      
      console.log('Form values:', { title, author, description });
      
      if (!title || !author || !description) {
        console.log('Form validation failed: empty required fields');
        // 필수 필드가 비어있으면 기본 HTML 유효성 검사에 맡김
        return;
      }
      
      // 로딩 화면 표시
      if (loadingOverlay) {
        console.log('Showing loading overlay');
        loadingOverlay.classList.remove('d-none');
      } else {
        console.error('Loading overlay element not found');
      }
      
      // 진행 상황 애니메이션 시작
      let progress = 0;
      let messageIndex = 0;
      
      const updateProgress = setInterval(function() {
        progress += 2;
        if (progress > 100) {
          clearInterval(updateProgress);
        } else {
          if (loadingProgress) {
            loadingProgress.style.width = progress + '%';
          }
          
          // 진행 상황에 따라 메시지 업데이트
          if (progress % 20 === 0 && messageIndex < messages.length && loadingMessage) {
            loadingMessage.textContent = messages[messageIndex];
            messageIndex++;
          }
        }
      }, 200);
      
      // 폼 제출은 계속 진행
    });
  } else {
    console.error('Form element with ID "book-form" not found');
  }
});