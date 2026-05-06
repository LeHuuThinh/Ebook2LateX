import json
import os
from app.database import SessionLocal
from app.models import User, Document, FormulaEntry

def seed_from_json():
    db = SessionLocal()
    try:
        # Nếu chưa có documents nào, tạo giả 1 user và 1 document để test
        doc = db.query(Document).first()
        if not doc:
            print("Không tìm thấy Document nào để gán Formula. Đang tạo tạm...")
            dummy_user = User(username_email="dummy_json@test.com", password_hash="dummy")
            db.add(dummy_user)
            db.commit()
            
            doc = Document(user_id=dummy_user.user_id, file_name="math_formulas.pdf", file_path_url="/dummy/math.pdf")
            db.add(doc)
            db.commit()

        json_path = os.path.join(os.path.dirname(__file__), "data.json")
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("Đang nhập dữ liệu FormulaEntry từ data.json...")
        for item in data:
            formula = FormulaEntry(
                document_id=doc.id,
                latex_content=item.get("latex_content"),
                order_index=item.get("order_index"),
                raw_image_path=item.get("raw_image_path")
            )
            db.add(formula)
            
        db.commit()
        print(f"Đã nạp thành công {len(data)} công thức vào Document: {doc.file_name}!")
        
    except Exception as e:
        db.rollback()
        print(f"Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_from_json()
