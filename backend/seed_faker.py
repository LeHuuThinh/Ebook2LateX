import random
from faker import Faker
from app.database import SessionLocal
from app.models import User, Document

fake = Faker()

def seed_faker_data():
    db = SessionLocal()
    try:
        print("Đang tạo 50 người dùng...")
        users = []
        for _ in range(50):
            # Tạo User giả
            user = User(
                username_email=fake.unique.email(),
                password_hash=fake.password(length=12),
                full_name=fake.name(),
                role=random.choice(['Admin', 'Editor', 'Viewer'])
            )
            db.add(user)
            users.append(user)
        
        # Commit lần 1 để lấy ID của user
        db.commit()

        print("Đang tạo 2-5 tài liệu cho mỗi người dùng...")
        for user in users:
            num_docs = random.randint(2, 5)
            for _ in range(num_docs):
                doc = Document(
                    user_id=user.user_id,
                    file_name=f"{fake.word()}_{fake.date_this_year()}.pdf",
                    file_path_url=f"/uploads/{fake.file_name(extension='pdf')}",
                    status=random.choice(['Pending', 'Processed', 'Error'])
                )
                db.add(doc)
        
        db.commit()
        print("Đã tạo thành công 50 người dùng và các tài liệu liên quan!")
    except Exception as e:
        db.rollback()
        print(f"Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_faker_data()
