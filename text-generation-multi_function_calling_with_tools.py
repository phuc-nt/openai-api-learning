import asyncio
import aiohttp
from dotenv import load_dotenv
import openai
import os
import json

# Tải cấu hình và thiết lập API key từ biến môi trường
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def get_current_weather(session, latitude, longitude):
    # Hàm lấy dữ liệu thời tiết từ API theo vĩ độ và kinh độ
    url = f'https://api.open-meteo.com/v1/forecast?latitude={
        latitude}&longitude={longitude}&current_weather=true'
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data['current_weather']
        else:
            print(f'Lỗi khi lấy dữ liệu thời tiết: {response.status}')
            return None


async def call_model_and_fetch_weather(user_query, model="gpt-3.5-turbo-1106"):
    # Hàm gửi truy vấn đến mô hình OpenAI và xử lý phản hồi
    messages = [
        # Tin nhắn hệ thống mô tả nhiệm vụ của trợ lý ảo
        {"role": "system", "content": "Bạn là 1 trợ lý am hiểu về json và thời tiết..."},
        # Tin nhắn từ người dùng
        {"role": "user", "content": user_query}
    ]

    # Định nghĩa các công cụ (tools) mà mô hình có thể sử dụng
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "string", "description": "Latitude of the location"},
                        "longitude": {"type": "string", "description": "Longitude of the location"},
                    },
                    "required": ["latitude", "longitude"],
                },
            },
        }
    ]

    async with aiohttp.ClientSession() as session:
        # Gửi truy vấn đến mô hình và nhận phản hồi
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        # Lấy phản hồi và danh sách tool_calls từ phản hồi của mô hình
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Xử lý từng tool_call
        if tool_calls:
            # Thêm phản hồi của trợ lý vào tin nhắn
            messages.append({
                "tool_calls": tool_calls,
                "role": "assistant",
            })
            for tool_call in tool_calls:
                tool_call_id = tool_call.id
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == 'get_current_weather':
                    latitude = function_args["latitude"]
                    longitude = function_args["longitude"]
                    weather_data = await get_current_weather(session, latitude, longitude)

                    response_content = json.dumps(
                        weather_data) if weather_data else "Không thể lấy dữ liệu thời tiết."
                    messages.append({
                        "tool_call_id": tool_call_id,
                        "role": "tool",
                        "name": function_name,
                        "content": response_content,
                    })

            # Gửi tất cả phản hồi đã thu thập về cho mô hình để nhận phản hồi cuối cùng
            second_response = openai.chat.completions.create(
                model=model,
                messages=messages,
            )
            return second_response.choices[0].message.content


async def main():
    # Truy vấn ví dụ
    user_query = "Thời tiết ở Hồ Chí Minh và Tokyo đang như thế nào?"
    # Gọi hàm và in kết quả
    human_response = await call_model_and_fetch_weather(user_query)
    print(human_response)

if __name__ == "__main__":
    asyncio.run(main())
