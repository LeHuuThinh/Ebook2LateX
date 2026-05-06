from app.database import SessionLocal
from app.models import User, Document, FormulaEntry
from sqlalchemy.sql import func

def get_user_document_stats():
    """
    Yêu cầu 1: Thống kê báo cáo (Reporting)
    Danh sách tất cả các User, kèm theo số lượng tài liệu mà mỗi người đã tải lên.
    """
    db = SessionLocal()
    try:
        # Sử dụng outerjoin để đếm số tài liệu kể cả user chưa upload tài liệu nào (sẽ = 0)
        results = (
            db.query(User.username_email, User.full_name, func.count(Document.id).label('doc_count'))
            .outerjoin(Document, User.user_id == Document.user_id)
            .group_by(User.user_id)
            .all()
        )
        
        print("\n--- THỐNG KÊ SỐ LƯỢNG TÀI LIỆU CỦA NGƯỜI DÙNG ---")
        for username, full_name, doc_count in results:
            name_display = full_name if full_name else username
            print(f"Người dùng: {name_display} | Số lượng tài liệu: {doc_count}")
        print("-------------------------------------------------\n")
        
        return results
    finally:
        db.close()

def search_formulas(keyword: str):
    """
    Yêu cầu 2: Tìm kiếm công thức
    Tìm kiếm FormulaEntry có chứa từ khóa trong latex_content.
    """
    db = SessionLocal()
    try:
        # Sử dụng ilike để tìm kiếm (không phân biệt hoa thường)
        search_query = f"%{keyword}%"
        formulas = db.query(FormulaEntry).filter(FormulaEntry.latex_content.ilike(search_query)).all()
        
        print(f"--- KẾT QUẢ TÌM KIẾM CÔNG THỨC: '{keyword}' ---")
        if not formulas:
            print("Không tìm thấy công thức nào phù hợp.")
        for f in formulas:
            print(f"[ID: {f.id}] -> LaTeX: {f.latex_content}")
        print("-------------------------------------------------\n")
        
        return formulas
    finally:
        db.close()

if __name__ == "__main__":
    # Test Yêu cầu 1
    get_user_document_stats()
    
    # Test Yêu cầu 2 (thử tìm từ khóa sqrt, hoặc có thể thay đổi tùy ý)
    search_formulas("sqrt")
