# HuggingFace 임베딩 관련 함수/클래스는 이 파일에 구현하세요.

import logging
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

# 모델별 차원 정보 (384차원만 지원)
MODEL_DIMENSIONS = {
    "snunlp/KR-SBERT-V40K-klueNLI-augSTS": 384
}

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
                        result = np.zeros(self.dimension)
                        result[:len(emb)] = emb
                        emb = result
                    
                    reduced.append(emb.tolist())
                    
                except Exception as e:
                    logger.error(f"[HF] 임베딩 처리 중 오류 발생: {str(e)}")
                    # 오류 발생 시 0 벡터로 대체
                    reduced.append(np.zeros(self.dimension).tolist())
            
            return reduced
            
        except Exception as e:
            logger.error(f"[HF] 문서 임베딩 생성 중 오류 발생: {str(e)}")
            return []
            
    def embed_query(self, text: str) -> List[float]:
        """단일 쿼리의 임베딩 벡터 반환"""
        try:
            # 1. 입력 검증
            if not text or not text.strip():
                return np.zeros(self.dimension).tolist()
                
            # 2. 임베딩 생성
            embedding = self.model.encode(text, output_value='sentence_embedding')
            
            # 3. NaN/Inf 체크 및 대체
            if np.any(np.isnan(embedding)) or np.any(np.isinf(embedding)):
                logger.warning("[HF] 쿼리 임베딩에 NaN/Inf 값 포함, 0으로 대체")
                embedding = np.nan_to_num(embedding, nan=0.0, posinf=1.0, neginf=-1.0)
            
            # 4. 차원 변환 (768 -> 384)
            if len(embedding) == 768:
                # 768차원을 384차원으로 변환 (평균 풀링)
                embedding = embedding.reshape(2, 384).mean(axis=0)
            
            # 5. 차원 검증
            if len(embedding) != self.dimension:
                logger.warning(f"[HF] 임베딩 차원 불일치: {len(embedding)} != {self.dimension}, 0으로 채움")
                result = np.zeros(self.dimension)
                result[:len(embedding)] = embedding
                embedding = result
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"[HF] 쿼리 임베딩 생성 중 오류 발생: {str(e)}")
            return np.zeros(self.dimension).tolist()

def get_hf_embedding(model_name: str) -> EmbeddingWrapper:
    """
    [HuggingFace 임베딩 모델 반환]
    - 입력: 
        - model_name: 사용할 모델 이름 (필수)
    - 출력: 
        - 임베딩 모델 래퍼
    """
    global _embedding_models
    
    # 모델 이름이 없으면 에러
    if not model_name:
        raise ValueError("모델 이름은 필수입니다")
    
    # 이미 로드된 모델이 있으면 재사용
    if model_name in _embedding_models:
        return _embedding_models[model_name]
    
    try:
        logger.info(f"[HF] 임베딩 모델 로드 시작: {model_name}")
        
        # 모델 초기화 (SentenceTransformer 직접 사용)
        model = SentenceTransformer(model_name)
        
        # 래퍼로 감싸서 저장
        wrapper = EmbeddingWrapper(model, model_name)
        _embedding_models[model_name] = wrapper
        
        logger.info(f"[HF] 임베딩 모델 로드 완료: {model_name} (차원: {wrapper.dimension})")
        return wrapper
        
    except Exception as e:
        logger.error(f"[HF] 임베딩 모델 초기화 실패: {str(e)}")
        raise

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