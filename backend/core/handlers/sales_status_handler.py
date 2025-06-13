import re

def handle_sales_status(user_message, meta, response):
    """
    연도 추출, 템플릿 치환 등 sales_status intent 후처리
    """
    template_vars = {}
    match = re.search(r'(20[0-9]{2})년', user_message)
    if match:
        year = int(match.group(1))
        template_vars['year'] = year
    response_text = response
    for var_name, var_value in template_vars.items():
        response_text = response_text.replace(f'{{{var_name}}}', str(var_value))
    return {
        'status': 'success',
        'data': {
            'response': response_text,
            'response_type': meta.get('response_type'),
            'route_code': meta.get('route_code'),
            'route_name': meta.get('route_name'),
            'route_path': meta.get('route_path'),
            'route_type': meta.get('route_type'),
            'response_params': template_vars
        }
    }, meta 