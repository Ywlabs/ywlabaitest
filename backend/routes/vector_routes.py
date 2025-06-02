from flask import Blueprint, jsonify
from services.vector_service import initialize_vector_store, validate_vector_store

vector_bp = Blueprint('vector', __name__)

@vector_bp.route('/api/vector/update', methods=['POST'])
def update_vectors():
    """벡터 스토어 수동 갱신"""
    try:
        # 벡터 스토어 상태 검증 및 복구
        validate_result = validate_vector_store()
        
        # 벡터 스토어 초기화
        init_result = initialize_vector_store()
        
        return jsonify({
            'status': 'success',
            'validate_result': validate_result,
            'init_result': init_result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 