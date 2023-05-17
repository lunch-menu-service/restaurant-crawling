import requests

NAVER_MAP_URL = "https://pcmap.place.naver.com/restaurant/list"

def get_response_from_api(
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

if __name__ == "__main__":
    restaurant_name = "조조칼국수"
    restaurant_position_x = 127.056678
    restaurant_position_y = 37.545243

    # test with query and client position
    resp = get_response_from_api(
        query=restaurant_name,
        x=restaurant_position_x,
        y=restaurant_position_y
    )
    if "조건에 맞는 업체가 없습니다." in resp.content.decode():
        print(f"{restaurant_name} 업체는 없습니다.")
    else:
        print(f"{restaurant_name} 업체는 현재 영업 중입니다.")
