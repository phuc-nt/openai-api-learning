import requests

def get_current_weather(latitude, longitude):
    """
    Lấy thông tin thời tiết hiện tại cho một vị trí cụ thể từ API open-meteo.com.

    Args:
        latitude (float): Vĩ độ của vị trí.
        longitude (float): Kinh độ của vị trí.

    Returns:
        dict: Dữ liệu thời tiết hiện tại.
    """
    
    # Endpoint của open-meteo.com cho thời tiết hiện tại
    url = 'https://api.open-meteo.com/v1/forecast'
    
    # Tham số cho lời gọi API
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': 'true'
    }
    
    # Thực hiện lời gọi API
    response = requests.get(url, params=params)
    
    # Kiểm tra nếu phản hồi thành công
    if response.status_code == 200:
        # Trả về dữ liệu thời tiết hiện tại
        return response.json()['current_weather']
    else:
        print(f'Lỗi khi lấy dữ liệu thời tiết: {response.status_code}')
        return None
