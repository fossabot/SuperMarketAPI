

from app import create_app



def test_class_BrandList():
    with create_app(db_url="sqlite:///testing_data.db").test_client() as c:
        response = c.get("/brand")
        json_response = response.get_json()
        print(json_response.status_code)




test_class_BrandList()