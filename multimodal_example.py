#!/usr/bin/env python3
"""
多模态使用示例 - 支持图片识别的完整示例
"""
from openai import OpenAI
import base64
import requests
from io import BytesIO

def encode_image_from_url(image_url: str) -> str:
    """从URL获取图片并转换为base64"""
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

def encode_image_from_file(image_path: str) -> str:
    """从本地文件读取图片并转换为base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 示例1: 使用base64编码的图片
def example_base64_image():
    """使用base64编码图片的示例"""
    
    client = OpenAI(
        api_key="your-gemini-api-key",  # 替换为你的Gemini API密钥
        base_url="https://your-project.vercel.app/gemini",  # 替换为你的部署地址
    )
    
    # 假设你有一张本地图片
    # base64_image = encode_image_from_file("path/to/your/image.jpg")
    
    # 或者从URL获取图片
    # base64_image = encode_image_from_url("https://example.com/image.jpg")
    
    # 这里使用一个测试用的小图片
    test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite",  # 最便宜的多模态模型
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请详细描述这张图片的内容，包括颜色、形状、物体等信息。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{test_image}",
                            "detail": "auto"  # 可选: low, high, auto
                        }
                    }
                ]
            }
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    print("图片分析结果:")
    print(response.choices[0].message.content)

# 示例2: 使用URL图片地址
def example_url_image():
    """直接使用图片URL的示例"""
    
    client = OpenAI(
        api_key="your-gemini-api-key",  # 替换为你的Gemini API密钥
        base_url="https://your-project.vercel.app/gemini",  # 替换为你的部署地址
    )
    
    # 使用你提供的图片URL
    image_url = "https://img.describepicture.cc/images/1757015053745_670714.webp"
    
    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite",  # 最便宜的多模态模型
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请详细描述这张图片的内容，包括颜色、形状、物体、场景等信息。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": "auto"  # 可选: low, high, auto
                        }
                    }
                ]
            }
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    print("URL图片分析结果:")
    print(response.choices[0].message.content)

# 示例3: 多张图片对比
def example_multiple_images():
    """多张图片对比分析的示例"""
    
    client = OpenAI(
        api_key="your-gemini-api-key",
        base_url="https://your-project.vercel.app/gemini",
    )
    
    # 两张测试图片
    image1 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image2 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwAEhAJ/wlseKgAAAABJRU5ErkJggg=="
    
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请对比这两张图片的差异："
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image1}"}
                    },
                    {
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/png;base64,{image2}"}
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    
    print("图片对比结果:")
    print(response.choices[0].message.content)

# 示例3: 流式响应
def example_streaming():
    """流式响应示例"""
    
    client = OpenAI(
        api_key="your-gemini-api-key",
        base_url="https://your-project.vercel.app/gemini",
    )
    
    test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    stream = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请分析这张图片并提供详细的描述。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{test_image}"}
                    }
                ]
            }
        ],
        stream=True,
        max_tokens=1000
    )
    
    print("流式响应:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()

# 示例4: 兼容性测试 - 纯文本
def example_text_only():
    """纯文本示例（确保向后兼容）"""
    
    client = OpenAI(
        api_key="your-gemini-api-key",
        base_url="https://your-project.vercel.app/gemini",
    )
    
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "user", "content": "你好！请介绍一下Gemini 1.5 Flash模型的特点。"}
        ],
        max_tokens=500
    )
    
    print("纯文本响应:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    print("=== Gemini 多模态代理使用示例 ===\n")
    
    print("注意: 运行前请替换API密钥和部署地址\n")
    
    print("支持的功能:")
    print("✅ 单张图片分析")
    print("✅ 多张图片对比") 
    print("✅ 流式响应")
    print("✅ 向后兼容纯文本")
    print("✅ base64和URL两种图片格式")
    print()
    
    print("最便宜的多模态模型: gemini-1.5-flash")
    print("价格: 输入 ~$0.075/1M tokens, 输出 ~$0.30/1M tokens")
    print()
    
    print("取消注释下面的函数调用来测试:")
    print("# example_text_only()")

    print("# example_base64_image()")
    # example_base64_image()

    print("# example_url_image()")
    # example_url_image()

    print("# example_multiple_images()")
    print("# example_streaming()")