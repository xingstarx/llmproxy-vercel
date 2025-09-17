#!/usr/bin/env python3
"""
测试URL图片功能
"""
from openai import OpenAI

def test_url_image():
    """测试使用URL图片地址的功能"""
    
    # 使用你的实际配置
    client = OpenAI(
        api_key="your-actual-gemini-api-key",  # 请替换为实际的API密钥
        base_url="https://your-actual-deployment.vercel.app/gemini",  # 请替换为实际的部署地址
    )
    
    # 使用你提供的图片URL
    image_url = "https://img.describepicture.cc/images/1757015053745_670714.webp"
    
    try:
        response = client.chat.completions.create(
            model="gemini-1.5-flash",  # 使用支持多模态的模型
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
                                "detail": "auto"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        print("✅ URL图片分析成功!")
        print("分析结果:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("\n请检查:")
        print("1. API密钥是否正确且有效")
        print("2. 部署地址是否正确")
        print("3. 网络连接是否正常")
        print("4. 图片URL是否可访问")

if __name__ == "__main__":
    print("=== 测试URL图片功能 ===\n")
    print("注意: 请先在代码中替换实际的API密钥和部署地址\n")
    
    # 取消注释下面这行来运行测试
    # test_url_image()
    
    print("请修改代码中的API密钥和部署地址，然后取消注释 test_url_image() 来运行测试")