from langchain.schema import Document

# 위젯 정보를 LangChain Document로 변환 (메타데이터 포함)
def widget_to_document(widget):
    return Document(
        page_content=f"{widget['name']} {widget['description']}",
        metadata={
            "widget_id": widget["id"],
            "category": widget["category"],
            "component_name": widget["component_name"],
            "thumbnail_url": widget["thumbnail_url"]
        }
    ) 