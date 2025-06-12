from flask import Blueprint, request, jsonify
from services.widget_service import search_widgets

widget_bp = Blueprint('widgets', __name__, url_prefix='/api/widgets')

@widget_bp.route('/search', methods=['POST'])
def widget_search():
    data = request.get_json()
    query = data.get('query', '')
    results = search_widgets(query)
    return jsonify({'status': 'success', 'data': results}) 