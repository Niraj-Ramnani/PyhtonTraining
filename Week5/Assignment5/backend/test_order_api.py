import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5000/api"

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    
    body = json.dumps(data).encode("utf-8") if data is not None else None
    try:
        with urllib.request.urlopen(req, data=body) as response:
            res_body = response.read().decode("utf-8")
            return response.status, json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        res_body = e.read().decode("utf-8")
        try:
            parsed = json.loads(res_body)
        except Exception:
            parsed = {"error": res_body}
        return e.code, parsed

def run_tests():
    print("=" * 60)
    print("Running POST /orders API Tests")
    print("=" * 60)

    payload = {
        "customer_id": 1,
        "restaurant_id": 1,
        "items": [
            {"food_item_id": 1, "quantity": 2},
            {"food_item_id": 2, "quantity": 1}
        ],
        "payment_information": {
            "payment_method": "upi"
        }
    }
    status, res = make_request("POST", "/orders", payload)
    print(f"\n[Test 1] Create valid order with UPI payment:")
    print(f"Status Code: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status == 201, f"Expected 201, got {status}"
    assert "order_id" in res, "Missing order_id"
    assert res["order_status"] == "pending", f"Expected pending status, got {res.get('order_status')}"
    assert res["payment"]["payment_method"] == "upi", "Payment method mismatch"
    assert res["payment"]["payment_status"] == "completed", "Payment status mismatch"
    print("--> Test 1 Passed!")

    invalid_cust_payload = {
        "customer_id": 99999,
        "restaurant_id": 1,
        "items": [{"food_item_id": 1, "quantity": 1}],
        "payment_method": "cash"
    }
    status, res = make_request("POST", "/orders", invalid_cust_payload)
    print(f"\n[Test 2] Invalid Customer ID:")
    print(f"Status Code: {status}, Error: {res.get('error')}")
    assert status == 400, f"Expected 400, got {status}"
    print("--> Test 2 Passed!")

    mismatched_payload = {
        "customer_id": 1,
        "restaurant_id": 2,
        "items": [{"food_item_id": 1, "quantity": 1}],
        "payment_method": "card"
    }
    status, res = make_request("POST", "/orders", mismatched_payload)
    print(f"\n[Test 3] Food item from wrong restaurant:")
    print(f"Status Code: {status}, Error: {res.get('error')}")
    assert status == 400, f"Expected 400, got {status}"
    print("--> Test 3 Passed!")

    invalid_payment_payload = {
        "customer_id": 1,
        "restaurant_id": 1,
        "items": [{"food_item_id": 1, "quantity": 1}],
        "payment_method": "bitcoin"
    }
    status, res = make_request("POST", "/orders", invalid_payment_payload)
    print(f"\n[Test 4] Invalid payment method:")
    print(f"Status Code: {status}, Error: {res.get('error')}")
    assert status == 400, f"Expected 400, got {status}"
    print("--> Test 4 Passed!")

    print("\n" + "=" * 60)
    print("ALL POST /orders API TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
