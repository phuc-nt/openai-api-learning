from dotenv import load_dotenv
import openai
import os
import json
import requests

# Tải và cấu hình API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_current_weather(latitude, longitude):
    """
    Gọi API thời tiết và trả về kết quả.
    """
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {'latitude': latitude,
              'longitude': longitude, 'current_weather': 'true'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['current_weather']
    else:
        print(f'Lỗi khi lấy dữ liệu thời tiết: {response.status_code}')
        return None


def parse_json_content(content):
    """
    Phân tích nội dung JSON và xử lý lỗi.
    """
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Không thể phân tích dữ liệu JSON.")
        return None


def call_model_with_function(user_query, model="gpt-3.5-turbo-1106"):
    """
    Gọi OpenAI API với truy vấn người dùng và xử lý kết quả.
    """
    # Gọi API chat.completions
    response = openai.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Bạn là 1 trợ lý am hiểu về json và thời tiết. Nếu được hỏi liên quan tới thời tiết của 1 thành phố, hãy trả về json với 2 key latitude và longitude, chứa giá trị là kinh độ và vĩ độ của thành phố đó, và kèm theo string `get_current_weather` để biết rằng cần gọi tiếp function nội bộ"},
            {"role": "user", "content": user_query}
        ]
    )

    # Lấy nội dung tin nhắn từ phản hồi
    message_content = response.choices[0].message.content
    data = parse_json_content(message_content)

    if data and "get_current_weather" in message_content:
        return get_current_weather(data['latitude'], data['longitude'])
    else:
        return message_content


def get_human_readable_response(weather_data, user_query, model="gpt-3.5-turbo"):
    """
    Gọi OpenAI API để tạo phản hồi dễ đọc từ dữ liệu thời tiết.
    """
    weather_json = json.dumps(
        weather_data) if weather_data else "Không có dữ liệu thời tiết."

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Bạn là 1 trợ lý am hiểu về json và thời tiết. Từ 1 đoạn json, bạn có thể diễn giải được theo ngôn ngữ giao tiếp tự nhiên"},
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": weather_json}, 
        ]
    )
    return response.choices[0].message.content


# Sử dụng
user_query = "Thời tiết ở Da Lat đang như thế nào?"
weather_data = call_model_with_function(user_query)
human_response = get_human_readable_response(weather_data, user_query)
print(human_response)
