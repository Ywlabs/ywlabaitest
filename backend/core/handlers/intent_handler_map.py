from core.handlers.employee_info_handler import handle_employee_info
from core.handlers.sales_status_handler import handle_sales_status

# intent별 후처리 핸들러 매핑
INTENT_HANDLER_MAP = {
    "employee_info": handle_employee_info,
    "sales_status": handle_sales_status,
    # 추가 intent는 여기에 등록
} 