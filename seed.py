import httpx

URL = "http://localhost:3000/api/medicines"
medicines = [
    {"name": "Panadol 500mg", "batchNo": "B001", "category": "Tablet", "price": 25.5, "quantity": 200, "expiryDate": "2029-12-31"},
    {"name": "Augmentin 625mg", "batchNo": "B002", "category": "Tablet", "price": 450, "quantity": 60, "expiryDate": "2028-06-30"},
    {"name": "Calpol Syrup", "batchNo": "B003", "category": "Syrup", "price": 180, "quantity": 40, "expiryDate": "2028-03-15"},
    {"name": "Brufen 400mg", "batchNo": "B004", "category": "Tablet", "price": 60, "quantity": 150, "expiryDate": "2029-09-20"},
    {"name": "Amoxil 500mg", "batchNo": "B005", "category": "Capsule", "price": 320, "quantity": 80, "expiryDate": "2028-11-10"},
    {"name": "Flagyl Syrup", "batchNo": "B006", "category": "Syrup", "price": 150, "quantity": 35, "expiryDate": "2027-12-01"},
    {"name": "Voltaren Injection", "batchNo": "B007", "category": "Injection", "price": 95, "quantity": 120, "expiryDate": "2028-08-25"},
    {"name": "Ceftriaxone 1g", "batchNo": "B008", "category": "Injection", "price": 210, "quantity": 5, "expiryDate": "2027-10-30"},
    {"name": "Omeprazole 20mg", "batchNo": "B009", "category": "Capsule", "price": 140, "quantity": 90, "expiryDate": "2029-04-18"},
    {"name": "Betnovate Cream", "batchNo": "B010", "category": "Ointment", "price": 130, "quantity": 45, "expiryDate": "2028-02-14"},
    {"name": "Disprin", "batchNo": "B011", "category": "Tablet", "price": 12, "quantity": 300, "expiryDate": "2030-01-31"},
    {"name": "Ventolin Syrup", "batchNo": "B012", "category": "Syrup", "price": 380, "quantity": 25, "expiryDate": "2028-07-07"},
]
for m in medicines:
    r = httpx.post(URL, json=m)
    print(r.status_code, m["name"])