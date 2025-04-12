/**
 * FAKER 도서 페이지 전용 YouTube 배경 영상 기능
 * - YouTube API를 활용한 배경 영상 재생
 * - 영상 제어(음소거, 재생/정지, 자막, 전체화면) 기능
 */

// 전역 변수 선언
var player;
var isMuted = true;
var isPlaying = true;
var captionsOn = false;
var navBar = null;
var contentContainer = null;
var isFullscreenMode = false;

// YouTube API 로드
function loadYouTubeAPI() {
  var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

// YouTube API가 준비되면 실행
function onYouTubeIframeAPIReady() {
  player = new YT.Player('youtubePlayer', {
    videoId: 'yUWjUX78SzI', // FAKER 영상 ID
    playerVars: {
      'autoplay': 1,
      'mute': 1,
      'controls': 0,
      'showinfo': 0,
      'rel': 0,
      'loop': 1,
      'playlist': 'yUWjUX78SzI',
      'cc_load_policy': 0,
      'iv_load_policy': 3,
      'disablekb': 1,
      'modestbranding': 1,
      'playsinline': 1,
      'fs': 0,
      'enablejsapi': 1
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

// 플레이어 준비되면 실행
function onPlayerReady(event) {
  // 자막 초기 비활성화
  try {
    player.unloadModule('captions');
  } catch(e) {
    console.log('자막 비활성화 시도:', e);
  }
  
  // 요소 캐싱 (성능 향상)
  navBar = document.querySelector('nav.navbar');
  contentContainer = document.querySelector('.container.py-5');
  
  // 컨트롤 버튼 이벤트 리스너 설정
  setupControls();
}

// 플레이어 상태 변경 시 호출
function onPlayerStateChange(event) {
  if (event.data === YT.PlayerState.ENDED) {
    player.playVideo();
  }
}

// 컨트롤 버튼 설정
function setupControls() {
  // 소리 켜기/끄기
  document.getElementById('toggleMute').addEventListener('click', function() {
    if (isMuted) {
      player.unMute();
      this.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
    } else {
      player.mute();
      this.innerHTML = '<i class="bi bi-volume-mute-fill"></i>';
    }
    isMuted = !isMuted;
  });
  
  // 재생/일시정지
  document.getElementById('togglePlay').addEventListener('click', function() {
    if (isPlaying) {
      player.pauseVideo();
      this.innerHTML = '<i class="bi bi-play-fill"></i>';
    } else {
      player.playVideo();
      this.innerHTML = '<i class="bi bi-pause-fill"></i>';
    }
    isPlaying = !isPlaying;
  });
  
  // 자막 켜기/끄기
  document.getElementById('toggleCaptions').addEventListener('click', function() {
    if (captionsOn) {
      try {
        player.unloadModule('captions');
        this.style.color = '#00ffaa';
      } catch(e) {
        console.log('자막 끄기 오류:', e);
      }
    } else {
      try {
        player.loadModule('captions');
        this.style.color = '#ffcc00';
      } catch(e) {
        console.log('자막 켜기 오류:', e);
      }
    }
    captionsOn = !captionsOn;
  });
  
  // 전체 화면 모드
  document.getElementById('toggleFullContentBtn').addEventListener('click', toggleFullscreenMode);
  
  // 전체 화면 모드 종료 버튼
  document.getElementById('exitFullModeBtn').querySelector('button').addEventListener('click', toggleFullscreenMode);
  
  // ESC 키 누르면 전체 화면 모드 종료
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && isFullscreenMode) {
      toggleFullscreenMode();
    }
  });
}

// 전체 화면 모드 토글 함수
function toggleFullscreenMode() {
  if (isFullscreenMode) {
    // 일반 모드로 돌아가기
    if (navBar) navBar.style.display = '';
    if (contentContainer) contentContainer.style.display = '';
    document.getElementById('exitFullModeBtn').style.display = 'none';
    document.getElementById('toggleFullContentBtn').innerHTML = '<i class="bi bi-arrows-fullscreen"></i>';
  } else {
    // 전체 화면 모드로 전환
    if (navBar) navBar.style.display = 'none';
    if (contentContainer) contentContainer.style.display = 'none';
    document.getElementById('exitFullModeBtn').style.display = 'block';
    document.getElementById('toggleFullContentBtn').innerHTML = '<i class="bi bi-fullscreen-exit"></i>';
  }
  
  isFullscreenMode = !isFullscreenMode;
}

// 페이지 로드 시 YouTube API 로드
document.addEventListener('DOMContentLoaded', function() {
  loadYouTubeAPI();
});