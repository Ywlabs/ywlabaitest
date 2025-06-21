# HuggingFace 임베딩 관련 함수/클래스는 이 파일에 구현하세요.

import logging
import time
import threading
import os
import shutil
from typing import List, Union, Dict
from sentence_transformers import SentenceTransformer
from config import get_config
import numpy as np

# 로거 설정
logger = logging.getLogger(__name__)

# 설정 로드
config = get_config()

# 전역 변수로 모델 저장
_embedding_models = {}
_model_locks = {}  # 모델별 락 추가

# 모델별 차원 정보 (384차원만 지원)
MODEL_DIMENSIONS = {
    "snunlp/KR-SBERT-V40K-klueNLI-augSTS": 384
}

# 모델 로딩 설정
MODEL_LOAD_TIMEOUT = 300  # 5분 타임아웃
MODEL_LOAD_RETRIES = 3    # 3회 재시도

def reduce_dimension(embedding: List[float], target_dim: int = 384) -> List[float]:
    """
    [임베딩 차원 축소]
    - 입력: 
        - embedding: 원본 임베딩 벡터
        - target_dim: 목표 차원
    - 출력: 
        - 차원이 축소된 임베딩 벡터
    """
    try:
        # 1. 입력 검증
        if not embedding or len(embedding) == 0:
            raise ValueError("빈 임베딩 벡터")
            
        # 2. 이미 목표 차원이면 그대로 반환
        if len(embedding) <= target_dim:
            return embedding
            
        # 3. numpy 배열로 변환
        embedding_array = np.array(embedding).reshape(1, -1)
        
        # 4. 정규화 (0-1 범위로)
        min_val = np.min(embedding_array)
        max_val = np.max(embedding_array)
        if max_val > min_val:
            embedding_array = (embedding_array - min_val) / (max_val - min_val)
        
        # 5. 차원 축소
        mean = np.mean(embedding_array, axis=0)
        centered = embedding_array - mean
        
        # 6. 공분산 행렬 계산
        cov = np.cov(centered.T)
        
        # 7. 고유값 분해
        eigenvals, eigenvecs = np.linalg.eigh(cov)
        
        # 8. 고유값 정렬
        idx = eigenvals.argsort()[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]
        
        # 9. 차원 축소
        reduced = np.dot(centered, eigenvecs[:, :target_dim])
        
        # 10. 결과 검증
        if np.any(np.isnan(reduced)) or np.any(np.isinf(reduced)):
            # NaN/Inf가 있으면 원본 벡터를 0으로 채워서 반환
            logger.warning("[HF] 차원 축소 결과에 NaN/Inf 값 포함, 원본 벡터 사용")
            result = np.zeros(target_dim)
            result[:len(embedding)] = embedding
            return result.tolist()
            
        return reduced[0].tolist()
        
    except Exception as e:
        logger.error(f"[HF] 차원 축소 중 오류 발생: {str(e)}")
        # 오류 발생 시 원본 벡터를 0으로 채워서 반환
        result = np.zeros(target_dim)
        result[:len(embedding)] = embedding
        return result.tolist()

class EmbeddingWrapper:
    """임베딩 모델 래퍼 클래스"""
    def __init__(self, model: SentenceTransformer, model_name: str):
        self.model = model
        self.model_name = model_name
        self.dimension = MODEL_DIMENSIONS.get(model_name)
        if self.dimension is None:
            raise ValueError(f"지원하지 않는 모델입니다: {model_name}")
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """문서 리스트의 임베딩 벡터 반환"""
        try:
            # 1. 입력 검증
            if not texts:
                return []
                
            # 2. 빈 문자열 필터링
            valid_texts = [text for text in texts if text and text.strip()]
            if not valid_texts:
                return []
                
            # 3. 임베딩 생성
            embeddings = self.model.encode(valid_texts, output_value='sentence_embedding')
            
            # 4. 차원 축소 및 검증
            reduced = []
            for emb in embeddings:
                try:
                    # 4-1. NaN/Inf 체크 및 대체
                    if np.any(np.isnan(emb)) or np.any(np.isinf(emb)):
                        logger.warning("[HF] 임베딩에 NaN/Inf 값 포함, 0으로 대체")
                        emb = np.nan_to_num(emb, nan=0.0, posinf=1.0, neginf=-1.0)
                    
                    # 4-2. 차원 변환 (768 -> 384)
                    if len(emb) == 768:
                        # 768차원을 384차원으로 변환 (평균 풀링)
                        emb = emb.reshape(2, 384).mean(axis=0)
                    
                    # 4-3. 차원 검증
                    if len(emb) != self.dimension:
                        logger.warning(f"[HF] 임베딩 차원 불일치: {len(emb)} != {self.dimension}, 0으로 채움")
                        result = np.zeros(self.dimension or 384)
                        result[:len(emb)] = emb
                        emb = result
                    
                    reduced.append(emb.tolist())
                    
                except Exception as e:
                    logger.error(f"[HF] 임베딩 처리 중 오류 발생: {str(e)}")
                    # 오류 발생 시 0 벡터로 대체
                    reduced.append(np.zeros(self.dimension or 384).tolist())
            
            return reduced
            
        except Exception as e:
            logger.error(f"[HF] 문서 임베딩 생성 중 오류 발생: {str(e)}")
            return []
            
    def embed_query(self, text: str) -> List[float]:
        """단일 쿼리의 임베딩 벡터 반환"""
        try:
            # 1. 입력 검증
            if not text or not text.strip():
                return np.zeros(self.dimension or 384).tolist()
                
            # 2. 임베딩 생성
            embedding = self.model.encode(text, output_value='sentence_embedding')
            
            # 3. NaN/Inf 체크 및 대체
            if np.any(np.isnan(embedding)) or np.any(np.isinf(embedding)):
                logger.warning("[HF] 쿼리 임베딩에 NaN/Inf 값 포함, 0으로 대체")
                embedding = np.nan_to_num(embedding, nan=0.0, posinf=1.0, neginf=-1.0)
            
            # 4. 차원 변환 (768 -> 384)
            if len(embedding) == 768:
                # 768차원을 384차원으로 변환 (평균 풀링)
                reshaped = embedding.reshape(2, 384)
                embedding = np.mean(reshaped, axis=0)
            
            # 5. 차원 검증
            if len(embedding) != self.dimension:
                logger.warning(f"[HF] 임베딩 차원 불일치: {len(embedding)} != {self.dimension}, 0으로 채움")
                result = np.zeros(self.dimension or 384)
                result[:len(embedding)] = embedding
                embedding = result
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"[HF] 쿼리 임베딩 생성 중 오류 발생: {str(e)}")
            return np.zeros(self.dimension or 384).tolist()

def get_hf_embedding(model_name: str) -> EmbeddingWrapper:
    """
    [HuggingFace 임베딩 모델 반환]
    - 입력: 
        - model_name: 사용할 모델 이름 (필수)
    - 출력: 
        - 임베딩 모델 래퍼
    """
    global _embedding_models, _model_locks
    
    # 모델 이름이 없으면 에러
    if not model_name:
        raise ValueError("모델 이름은 필수입니다")
    
    # 이미 로드된 모델이 있으면 재사용
    if model_name in _embedding_models:
        return _embedding_models[model_name]
    
    # 모델별 락 생성
    if model_name not in _model_locks:
        _model_locks[model_name] = threading.Lock()
    
    # 락을 사용하여 동시 로딩 방지
    with _model_locks[model_name]:
        # 락 획득 후 다시 확인 (다른 스레드가 로드했을 수 있음)
        if model_name in _embedding_models:
            return _embedding_models[model_name]
        
        # 재시도 로직으로 모델 로딩
        last_error = None
        for attempt in range(MODEL_LOAD_RETRIES):
            try:
                logger.info(f"[HF] 임베딩 모델 로드 시작: {model_name} (시도 {attempt + 1}/{MODEL_LOAD_RETRIES})")
                
                # 타임아웃 설정으로 모델 초기화
                start_time = time.time()
                model = SentenceTransformer(model_name)
                load_time = time.time() - start_time
                
                # 래퍼로 감싸서 저장
                wrapper = EmbeddingWrapper(model, model_name)
                _embedding_models[model_name] = wrapper
                
                logger.info(f"[HF] 임베딩 모델 로드 완료: {model_name} (차원: {wrapper.dimension}, 로딩시간: {load_time:.2f}초)")
                return wrapper
                
            except Exception as e:
                last_error = e
                logger.warning(f"[HF] 임베딩 모델 로드 실패 (시도 {attempt + 1}/{MODEL_LOAD_RETRIES}): {str(e)}")
                
                if attempt < MODEL_LOAD_RETRIES - 1:
                    # 재시도 전 대기 (지수 백오프)
                    wait_time = 2 ** attempt
                    logger.info(f"[HF] {wait_time}초 후 재시도...")
                    time.sleep(wait_time)
        
        # 모든 재시도 실패
        logger.error(f"[HF] 임베딩 모델 초기화 최종 실패: {str(last_error)}")
        if last_error:
            raise last_error
        else:
            raise RuntimeError("임베딩 모델 초기화 실패")

def get_embeddings(texts: List[str], model_name: str) -> List[List[float]]:
    """
    [텍스트 리스트의 임베딩 벡터 반환]
    - 입력: 
        - texts: 변환할 텍스트 리스트
        - model_name: 사용할 모델 이름 (필수)
    - 출력: 
        - 임베딩 벡터 리스트
    """
    try:
        model = get_hf_embedding(model_name)
        return model.embed_documents(texts)
        
    except Exception as e:
        logger.error(f"[HF] 임베딩 생성 실패: {str(e)}")
        raise 

def clear_hf_cache():
    """
    [HuggingFace 캐시 디렉토리 정리]
    - filelock 문제 해결을 위해 캐시 정리
    """
    try:
        # HuggingFace 캐시 디렉토리 경로
        cache_dir = os.path.expanduser("~/.cache/huggingface")
        
        if os.path.exists(cache_dir):
            # .locks 디렉토리만 정리
            locks_dir = os.path.join(cache_dir, "hub", ".locks")
            if os.path.exists(locks_dir):
                logger.info(f"[HF] 캐시 락 파일 정리 시작: {locks_dir}")
                
                # 오래된 락 파일들 정리 (1시간 이상 된 파일)
                current_time = time.time()
                removed_count = 0
                
                for root, dirs, files in os.walk(locks_dir):
                    for file in files:
                        if file.endswith('.lock'):
                            file_path = os.path.join(root, file)
                            try:
                                # 파일 수정 시간 확인
                                mtime = os.path.getmtime(file_path)
                                if current_time - mtime > 3600:  # 1시간 이상
                                    os.remove(file_path)
                                    removed_count += 1
                            except Exception as e:
                                logger.warning(f"[HF] 락 파일 정리 중 오류: {file_path} - {str(e)}")
                
                logger.info(f"[HF] 캐시 락 파일 정리 완료: {removed_count}개 파일 제거")
                
    except Exception as e:
        logger.warning(f"[HF] 캐시 정리 중 오류 발생: {str(e)}") 