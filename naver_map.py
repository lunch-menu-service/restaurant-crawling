import time
import requests

NAVER_MAP_URL = "https://pcmap.place.naver.com/restaurant/list"

def _get_response_from_api(
    query: str | None = None,
    x: float | None = None,
    y: float | None = None
) -> requests.Response:
    params = {}
    if query is not None:
        params["query"] = query
    if x is not None and y is not None:
        params["clientX"] = str(x)
        params["clientY"] = str(y)
    return requests.get(
        url=NAVER_MAP_URL,
        params=params
    )

def is_available_restaurant(
    query: str | None = None,
    x: float | None = None,
    y: float | None = None
):
    for _ in range(5):
        resp = _get_response_from_api(query, x, y)
        if resp.status_code == 200:
            return "조건에 맞는 업체가 없습니다." not in resp.content.decode()
        time.sleep(1)
    return False

if __name__ == "__main__":
    restaurant_name = "조조칼국수"
    restaurant_position_x = 127.056678
    restaurant_position_y = 37.545243

    # test with query and client position
    is_available = is_available_restaurant(
        query=restaurant_name,
        x=restaurant_position_x,
        y=restaurant_position_y
    )
    if is_available:
        print(f"{restaurant_name} 업체는 현재 영업 중입니다.")
    else:
        print(f"{restaurant_name} 업체는 없습니다.")
