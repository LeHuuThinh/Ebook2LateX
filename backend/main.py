# Goi thu vien FastAPI

from fastapi import FastAPI

# Tao doi tuong app tu class FastAPI

app = FastAPI()

# Tao decorator cho app.get(“/”) 

@app.get("/")

# khi nguoi dung truy cap vao web root, goi ham sau

def read_root():

    return {"message": "Chao mung ban den voi Ebook2LateX!"}

# Bài tập 10a: Nhận một số qua thanh địa chỉ (Path parameter) và nhân với 10
@app.get("/multiply/{number}")
def multiply_by_10(number: float):
    return {"result": number * 10}

# Bài tập 10b: Nhận nhãn hiệu và kích thước (Query parameters) qua thanh địa chỉ
@app.get("/shoes")
def buy_shoes(brand: str, size: int):
    return {"message": f"Bạn muốn mua giày {brand} kích thước {size} đúng không?"}
