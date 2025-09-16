# 多模态图片识别 API 使用指南

本指南提供了使用 LLM 反向代理服务进行多模态图片识别的完整示例，包括 cURL 和 Next.js 的调用方法。

## 📋 基本信息

- **推荐模型**: `gemini-2.5-flash-lite` (最优性价比)
- **API 端点**: `https://your-domain.com/gemini/chat/completions`
- **免费额度**: 15 RPM / 250K TPM / 1,000 RPD
- **支持格式**: JPEG, PNG, WebP, HEIC, HEIF

## 🔧 cURL 调用示例

### 基础图片分析

```bash
curl --location 'https://llm.describepicture.cc/gemini/chat/completions' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_GEMINI_API_KEY' \
  --data '{
    "model": "gemini-2.5-flash-lite",
    "messages": [
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
              "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
              "detail": "auto"
            }
          }
        ]
      }
    ],
    "max_tokens": 1000,
    "temperature": 0.7
  }'
```

### 多张图片对比

```bash
curl --location 'https://llm.describepicture.cc/gemini/chat/completions' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_GEMINI_API_KEY' \
  --data '{
    "model": "gemini-2.5-flash-lite",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "请对比这两张图片的差异："
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,IMAGE1_BASE64_STRING"
            }
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,IMAGE2_BASE64_STRING"
            }
          }
        ]
      }
    ],
    "max_tokens": 1000,
    "temperature": 0.7
  }'
```

### 流式响应

```bash
curl --location 'https://llm.describepicture.cc/gemini/chat/completions' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_GEMINI_API_KEY' \
  --data '{
    "model": "gemini-2.5-flash-lite",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "请分析这张图片并提供详细的描述。"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,YOUR_IMAGE_BASE64"
            }
          }
        ]
      }
    ],
    "stream": true,
    "max_tokens": 1000
  }'
```

## ⚛️ Next.js 调用示例

### 1. 基础图片分析组件

```jsx
// components/ImageAnalyzer.jsx
import { useState } from 'react';

export default function ImageAnalyzer() {
  const [image, setImage] = useState(null);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  // 将文件转换为 base64
  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  };

  // 分析图片
  const analyzeImage = async () => {
    if (!image) return;

    setLoading(true);
    try {
      const base64Image = await fileToBase64(image);
      
      const response = await fetch('https://llm.describepicture.cc/gemini/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_GEMINI_API_KEY}`
        },
        body: JSON.stringify({
          model: "gemini-2.5-flash-lite",
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "text",
                  text: "请详细描述这张图片的内容，包括颜色、形状、物体等信息。"
                },
                {
                  type: "image_url",
                  image_url: {
                    url: base64Image,
                    detail: "auto"
                  }
                }
              ]
            }
          ],
          max_tokens: 1000,
          temperature: 0.7
        })
      });

      const data = await response.json();
      setAnalysis(data.choices[0].message.content);
    } catch (error) {
      console.error('分析失败:', error);
      setAnalysis('分析失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">图片分析工具</h2>
      
      <div className="mb-4">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      {image && (
        <div className="mb-4">
          <img
            src={URL.createObjectURL(image)}
            alt="预览"
            className="max-w-full h-auto rounded-lg shadow-md"
          />
        </div>
      )}

      <button
        onClick={analyzeImage}
        disabled={!image || loading}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
      >
        {loading ? '分析中...' : '分析图片'}
      </button>

      {analysis && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-semibold mb-2">分析结果:</h3>
          <p className="whitespace-pre-wrap">{analysis}</p>
        </div>
      )}
    </div>
  );
}
```

### 2. 流式响应组件

```jsx
// components/StreamingImageAnalyzer.jsx
import { useState } from 'react';

export default function StreamingImageAnalyzer() {
  const [image, setImage] = useState(null);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const analyzeImageStream = async () => {
    if (!image) return;

    setLoading(true);
    setAnalysis('');
    
    try {
      const base64Image = await fileToBase64(image);
      
      const response = await fetch('https://llm.describepicture.cc/gemini/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_GEMINI_API_KEY}`
        },
        body: JSON.stringify({
          model: "gemini-2.5-flash-lite",
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "text",
                  text: "请分析这张图片并提供详细的描述。"
                },
                {
                  type: "image_url",
                  image_url: {
                    url: base64Image
                  }
                }
              ]
            }
          ],
          stream: true,
          max_tokens: 1000
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') return;
            
            try {
              const parsed = JSON.parse(data);
              const content = parsed.choices[0]?.delta?.content;
              if (content) {
                setAnalysis(prev => prev + content);
              }
            } catch (e) {
              // 忽略解析错误
            }
          }
        }
      }
    } catch (error) {
      console.error('分析失败:', error);
      setAnalysis('分析失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">流式图片分析</h2>
      
      <div className="mb-4">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
        />
      </div>

      {image && (
        <div className="mb-4">
          <img
            src={URL.createObjectURL(image)}
            alt="预览"
            className="max-w-full h-auto rounded-lg shadow-md"
          />
        </div>
      )}

      <button
        onClick={analyzeImageStream}
        disabled={!image || loading}
        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
      >
        {loading ? '分析中...' : '开始流式分析'}
      </button>

      {analysis && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-semibold mb-2">实时分析结果:</h3>
          <p className="whitespace-pre-wrap">{analysis}</p>
          {loading && <span className="animate-pulse">▋</span>}
        </div>
      )}
    </div>
  );
}
```

### 3. API 路由示例 (Next.js App Router)

```javascript
// app/api/analyze-image/route.js
import { NextResponse } from 'next/server';

export async function POST(request) {
  try {
    const { image, prompt = "请描述这张图片" } = await request.json();
    
    const response = await fetch('https://llm.describepicture.cc/gemini/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.GEMINI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gemini-2.5-flash-lite",
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: prompt
              },
              {
                type: "image_url",
                image_url: {
                  url: image, // base64 格式: data:image/jpeg;base64,xxx
                  detail: "auto"
                }
              }
            ]
          }
        ],
        max_tokens: 1000,
        temperature: 0.7
      })
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error?.message || '分析失败');
    }

    return NextResponse.json({
      success: true,
      analysis: data.choices[0].message.content
    });

  } catch (error) {
    console.error('API 错误:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}
```

## 🔑 环境变量配置

### Next.js 环境变量

```bash
# .env.local
NEXT_PUBLIC_GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # 服务端使用
```

## 📊 支持的模型对比

| 模型 | RPM | TPM | RPD | 推荐场景 |
|------|-----|-----|-----|----------|
| **gemini-2.5-flash-lite** | 15 | 250K | 1,000 | 🏆 **最佳选择** - 日常多模态应用 |
| gemini-2.5-flash | 10 | 250K | 250 | 高质量分析 |
| gemini-2.0-flash | 15 | 1M | 200 | 长文本+图片处理 |
| gemini-2.0-flash-lite | 30 | 1M | 200 | 高并发场景 |

## ⚠️ 注意事项

1. **API 密钥安全**: 
   - 前端使用时注意 API 密钥安全
   - 建议通过后端 API 路由调用

2. **图片大小限制**:
   - 建议图片大小 < 4MB
   - 支持的格式: JPEG, PNG, WebP, HEIC, HEIF

3. **错误处理**:
   - 实现适当的错误处理和重试机制
   - 监控 API 使用量避免超出限制

4. **性能优化**:
   - 图片压缩可以提高响应速度
   - 使用流式响应提升用户体验

## 🚀 快速开始

1. 克隆项目并部署到 Vercel
2. 获取 Gemini API 密钥
3. 配置环境变量
4. 使用上述示例代码开始开发

更多详细信息请参考项目 README 文档。