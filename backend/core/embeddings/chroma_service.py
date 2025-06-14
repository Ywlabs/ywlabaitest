from typing import List, Dict, Any

def add_documents_to_collection(collection_name: str, documents: List[Dict[str, Any]]) -> None:
    """
    문서를 ChromaDB 컬렉션에 추가
    - 2024-06-14 기준: response_handler 필드 추가
    """
    try:
        collection = get_collection(collection_name)
        
        for doc in documents:
            # 메타데이터 필드 구성
            metadata = {
                'pattern_id': doc.get('pattern_id'),
                'pattern': doc.get('pattern'),
                'pattern_text': doc.get('pattern_text'),
                'pattern_type': doc.get('pattern_type', 'static'),
                'priority': doc.get('priority', 0),
                'similarity_threshold': doc.get('similarity_threshold', 0.7),
                'domain': doc.get('domain'),
                'category': doc.get('category'),
                'response_handler': doc.get('response_handler'),  # response_handler 필드 추가
                'route_code': doc.get('route_code'),
                'route_name': doc.get('route_name'),
                'route_path': doc.get('route_path')
            }
            
            # 직원 정보가 있는 경우 추가
            if 'employee' in doc:
                metadata.update({
                    'employee_name': doc['employee'].get('name'),
                    'employee_position': doc['employee'].get('position'),
                    'employee_dept': doc['employee'].get('dept_nm'),
                    'employee_email': doc['employee'].get('email'),
                    'employee_phone': doc['employee'].get('phone')
                })
            
            # 문서 추가
            collection.add(
                documents=[doc['content']],
                metadatas=[metadata],
                ids=[str(doc['pattern_id'])]
            )
            
        logger.info(f"[ChromaDB] {len(documents)}개 문서 추가 완료")
        
    except Exception as e:
        logger.error(f"[ChromaDB] 문서 추가 중 오류 발생: {str(e)}")
        raise

def update_document_in_collection(collection_name: str, document: Dict[str, Any]) -> None:
    """
    ChromaDB 컬렉션의 문서 업데이트
    - 2024-06-14 기준: response_handler 필드 추가
    """
    try:
        collection = get_collection(collection_name)
        pattern_id = str(document['pattern_id'])
        
        # 메타데이터 필드 구성
        metadata = {
            'pattern_id': document.get('pattern_id'),
            'pattern': document.get('pattern'),
            'pattern_text': document.get('pattern_text'),
            'pattern_type': document.get('pattern_type', 'static'),
            'priority': document.get('priority', 0),
            'similarity_threshold': document.get('similarity_threshold', 0.7),
            'domain': document.get('domain'),
            'category': document.get('category'),
            'response_handler': document.get('response_handler'),  # response_handler 필드 추가
            'route_code': document.get('route_code'),
            'route_name': document.get('route_name'),
            'route_path': document.get('route_path')
        }
        
        # 직원 정보가 있는 경우 추가
        if 'employee' in document:
            metadata.update({
                'employee_name': document['employee'].get('name'),
                'employee_position': document['employee'].get('position'),
                'employee_dept': document['employee'].get('dept_nm'),
                'employee_email': document['employee'].get('email'),
                'employee_phone': document['employee'].get('phone')
            })
        
        # 문서 업데이트
        collection.update(
            ids=[pattern_id],
            documents=[document['content']],
            metadatas=[metadata]
        )
        
        logger.info(f"[ChromaDB] 문서 업데이트 완료: pattern_id={pattern_id}")
        
    except Exception as e:
        logger.error(f"[ChromaDB] 문서 업데이트 중 오류 발생: {str(e)}")
        raise 