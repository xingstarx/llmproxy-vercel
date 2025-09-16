#!/usr/bin/env python3
"""
测试多模态功能的脚本
"""
import requests
import json
import base64

def test_multimodal_gemini():
    """测试Gemini多模态功能"""
    
    # 测试用的base64编码图片（一个简单的红色方块）
    test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    # 构造多模态消息
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请描述这张图片"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{test_image_base64}"
                    }
                }
            ]
        }
    ]
    
    payload = {
        "model": "gemini-1.5-flash",
        "messages": messages,
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_GEMINI_API_KEY"  # 需要替换为实际的API密钥
    }
    
    print("测试多模态请求...")
    print("Payload:", json.dumps(payload, indent=2, ensure_ascii=False))
    
    # 这里只是打印请求，实际测试时需要有效的API密钥
    print("\n发送到: http://localhost:3000/gemini/chat/completions")
    print("Headers:", headers)
    
    return payload

def test_text_only_gemini():
    """测试纯文本功能（确保向后兼容）"""
    
    messages = [
        {
            "role": "user", 
            "content": "你好，请介绍一下自己"
        }
    ]
    
    payload = {
        "model": "gemini-1.5-flash",
        "messages": messages,
        "stream": False,
        "temperature": 0.7
    }
    
    print("\n测试纯文本请求...")
    print("Payload:", json.dumps(payload, indent=2, ensure_ascii=False))
    
    return payload

if __name__ == "__main__":
    print("=== Gemini 多模态代理测试 ===")
    
    print("\n1. 测试多模态功能:")
    test_multimodal_gemini()
    
    print("\n2. 测试纯文本功能（向后兼容）:")
    test_text_only_gemini()
    
    print("\n=== 测试完成 ===")
    print("\n使用说明:")
    print("1. 最便宜的多模态模型: gemini-1.5-flash")
    print("2. 支持格式: 文本 + 图片（base64或URL）")
    print("3. 价格: ~$0.075/1M tokens (输入), $0.30/1M tokens (输出)")
    print("4. 用法与OpenAI API完全兼容")