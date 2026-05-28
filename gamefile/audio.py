"""
마이크 입력 처리 모듈 (데시벨 및 연속 소리 감지 반영)
"""

import numpy as np

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except (ImportError, OSError):
    SOUNDDEVICE_AVAILABLE = False

class AudioManager:
    """마이크 입력을 관리하고 실제 데시벨(dB)을 계산하는 클래스"""

    def __init__(self, threshold_db: float = 85.0):
        self.threshold = threshold_db
        self.mic_db = 0.0
        self._stream = None

    def _audio_callback(self, indata, frames, time, status):
        """sounddevice 콜백: 실시간으로 RMS를 구하고 이를 데시벨(dB)로 변환"""
        rms = np.sqrt(np.mean(indata**2)) if len(indata) > 0 else 0.0
        
        if rms > 0:
            # 음압 레벨(dB) 근사치 계산 (기준값 1e-5)
            db = 20 * np.log10(rms / 1e-5)
            # 마이크 감도 및 환경에 따른 스케일링 보정
            self.mic_db = min(max(db, 0.0), 120.0) 
        else:
            self.mic_db = 0.0

    def start(self):
        """오디오 스트림 시작"""
        if SOUNDDEVICE_AVAILABLE:
            # 연속적인 데이터 흐름을 위해 적절한 blocksize 설정
            self._stream = sd.InputStream(callback=self._audio_callback, blocksize=1024)
            self._stream.start()

    def stop(self):
        """오디오 스트림 정지 및 종료"""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def is_shouting(self) -> bool:
        """현재 데시벨이 설정된 dB 임계값(85dB)을 초과하는지 반환"""
        return self.mic_db > self.threshold

    def get_volume(self) -> float:
        """현재 마이크 데시벨(dB) 반환"""
        return self.mic_db