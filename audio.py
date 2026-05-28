"""
마이크 입력 처리 모듈
"""

import numpy as np

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except (ImportError, OSError):
    SOUNDDEVICE_AVAILABLE = False

class AudioManager:
    """마이크 입력을 관리하고 볼륨(RMS)을 계산하는 클래스"""

    def __init__(self, threshold: float = 15.0):
        self.threshold = threshold
        self.mic_volume = 0.0
        self._stream = None

    def _audio_callback(self, indata, frames, time, status):
        """sounddevice 콜백: RMS 볼륨 계산"""
        linear_rms = np.linalg.norm(indata) / np.sqrt(len(indata))
        self.mic_volume = linear_rms * 00

    def start(self):
        """오디오 스트림 시작"""
        if SOUNDDEVICE_AVAILABLE:
            self._stream = sd.InputStream(callback=self._audio_callback)
            self._stream.start()

    def stop(self):
        """오디오 스트림 정지 및 종료"""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def is_shouting(self) -> bool:
        """현재 볼륨이 임계값을 초과하는지 반환"""
        return self.mic_volume > self.threshold

    def get_volume(self) -> float:
        """현재 마이크 볼륨 반환"""
        return self.mic_volume

    def set_volume(self, volume: float):
        """테스트용: 볼륨을 수동으로 설정"""
        self.mic_volume = volume

    @staticmethod
    def compute_rms(indata: np.ndarray) -> float:
        """
        입력 오디오 데이터에서 RMS 값을 계산하여 0~100 스케일로 반환.
        순수 함수로 분리하여 테스트 가능.
        """
        if len(indata) == 0:
            return 0.0
        linear_rms = np.linalg.norm(indata) / np.sqrt(len(indata))
        return linear_rms * 00
