#!/bin/bash

# 多模态功能测试脚本 (curl版本)

echo "=== Gemini 多模态代理 cURL 测试 ==="
echo

# 测试用的小图片 (1x1像素红色方块)
TEST_IMAGE="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

echo "1. 测试多模态功能 (文本 + 图片):"
echo "curl --location 'https://your-project.vercel.app/gemini/chat/completions' \\"
echo "  --header 'Content-Type: application/json' \\"
echo "  --header 'Authorization: Bearer YOUR_GEMINI_API_KEY' \\"
echo "  --data '{"
echo "    \"model\": \"gemini-1.5-flash\","
echo "    \"messages\": ["
echo "      {"
echo "        \"role\": \"user\","
echo "        \"content\": ["
echo "          {"
echo "            \"type\": \"text\","
echo "            \"text\": \"请描述这张图片\""
echo "          },"
echo "          {"
echo "            \"type\": \"image_url\","
echo "            \"image_url\": {"
echo "              \"url\": \"data:image/png;base64,$TEST_IMAGE\""
echo "            }"
echo "          }"
echo "        ]"
echo "      }"
echo "    ],"
echo "    \"stream\": false,"
echo "    \"max_tokens\": 1000"
echo "  }'"
echo

echo "2. 测试纯文本功能 (向后兼容):"
echo "curl --location 'https://your-project.vercel.app/gemini/chat/completions' \\"
echo "  --header 'Content-Type: application/json' \\"
echo "  --header 'Authorization: Bearer YOUR_GEMINI_API_KEY' \\"
echo "  --data '{"
echo "    \"model\": \"gemini-1.5-flash\","
echo "    \"messages\": ["
echo "      {"
echo "        \"role\": \"user\","
echo "        \"content\": \"你好，请介绍一下自己\""
echo "      }"
echo "    ],"
echo "    \"stream\": false"
echo "  }'"
echo

echo "=== 使用说明 ==="
echo "1. 替换 'your-project.vercel.app' 为你的实际部署地址"
echo "2. 替换 'YOUR_GEMINI_API_KEY' 为你的 Gemini API 密钥"
echo "3. gemini-1.5-flash 是最便宜的多模态模型"
echo "4. 支持 base64 编码图片和图片 URL"
echo "5. 完全兼容 OpenAI API 格式"