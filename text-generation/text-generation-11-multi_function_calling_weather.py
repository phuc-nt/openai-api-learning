import asyncio
import aiohttp
from dotenv import load_dotenv
import openai
import os
import json

# Tải và cấu hình API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def get_current_weather(session, latitude, longitude):
    """
    Gọi API thời tiết một cách bất đồng bộ và trả về kết quả.
    """
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data['current_weather']
        else:
            print(f'Lỗi khi lấy dữ liệu thời tiết: {response.status}')
            return None


async def fetch_weather_data(locations):
    """
    Lấy dữ liệu thời tiết cho nhiều địa điểm một cách bất đồng bộ.

    Args:
        locations (dict): Một dictionary với key là tên thành phố và giá trị là một
                          dict chứa vĩ độ, kinh độ và hành động cần thực hiện.

    Returns:
        dict: Dictionary với key là tên thành phố và giá trị là dữ liệu thời tiết.
    """
    async with aiohttp.ClientSession() as session:
        tasks = {city: get_current_weather(session, loc['latitude'], loc['longitude'])
                 for city, loc in locations.items() if loc.get('action') == 'get_current_weather'}
        weather_results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), weather_results))

def parse_json_content(content):
    """
    Phân tích nội dung JSON và xử lý lỗi.
    """
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Không thể phân tích dữ liệu JSON.")
        return None


async def call_model_with_function(user_query, model="gpt-3.5-turbo-1106"):
    """
    Gọi OpenAI API với truy vấn người dùng và xử lý kết quả.
    """
    # Gọi API chat.completions
    response = openai.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Bạn là 1 trợ lý am hiểu về json và thời tiết. Nếu được hỏi liên quan tới thời tiết của 1 hoặc nhiều thành phố, hãy trả về json với 2 key latitude và longitude cho mỗi thành phố, chứa giá trị là kinh độ và vĩ độ của thành phố đó, và kèm theo string `get_current_weather` để biết rằng cần gọi tiếp function nội bộ"},
            {"role": "user", "content": user_query}
        ]
    )
    
    # Lấy nội dung tin nhắn từ phản hồi
    message_content = response.choices[0].message.content
    locations = parse_json_content(message_content)
    
    # Kiểm tra output
    # print("Thông tin locations: ", locations)
    
    weather_data = await fetch_weather_data(locations)
    
    # Chuyển đổi dữ liệu thời tiết thành JSON để gửi lại cho mô hình
    weather_json = json.dumps(weather_data)
    
    # Kiểm tra output
    # print("Thông tin weather json: ", weather_json)
    
    # Gọi OpenAI API với dữ liệu thời tiết
    return await get_human_readable_response(weather_json, user_query, model)


async def get_human_readable_response(weather_json, user_query, model="gpt-3.5-turbo"):
    """
    Gọi OpenAI API để tạo phản hồi dễ đọc từ dữ liệu thời tiết.
    """
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
async def main():
    user_query = "Thời tiết ở Paris, TP.HCM và Tokyo đang như thế nào?"
    human_response = await call_model_with_function(user_query)
    print(human_response)

if __name__ == "__main__":
    asyncio.run(main())
