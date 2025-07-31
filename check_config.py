#!/usr/bin/env python3
"""
配置验证脚本 - 检查DeepSeek环境是否正确配置
"""

import os
import sys
from dotenv import load_dotenv, find_dotenv

def check_deepseek_config():
    """检查DeepSeek配置"""
    print("🔍 DeepSeek配置检查")
    print("=" * 40)
    
    # 加载环境变量
    load_dotenv(find_dotenv())
    
    # 检查DeepSeek API Key
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    if deepseek_key:
        print(f"✅ DEEPSEEK_API_KEY: 已配置 (长度: {len(deepseek_key)})")
        if not deepseek_key.startswith('sk-'):
            print("⚠️  警告: API Key格式可能不正确，应以'sk-'开头")
    else:
        print("❌ DEEPSEEK_API_KEY: 未配置")
        print("💡 请在.env文件中添加: DEEPSEEK_API_KEY=sk-xxx")
        return False
    
    # 检查代理配置
    http_proxy = os.getenv('HTTP_PROXY')
    https_proxy = os.getenv('HTTPS_PROXY')
    if http_proxy or https_proxy:
        print(f"🌐 代理配置: HTTP={http_proxy}, HTTPS={https_proxy}")
    else:
        print("🔗 代理配置: 未设置 (如果网络正常可忽略)")
    
    return True

def check_bge_model():
    """检查BGE模型配置"""
    print("\n🤖 BGE模型配置检查")
    print("=" * 40)
    
    bge_path = os.getenv('BGE_MODEL_PATH')
    if bge_path:
        print(f"📁 BGE_MODEL_PATH: {bge_path}")
        if os.path.exists(bge_path):
            print("✅ 本地模型路径存在")
        else:
            print("⚠️  本地路径不存在，将使用在线模型")
    else:
        print("📥 BGE_MODEL_PATH: 未设置，将使用在线模型BAAI/bge-small-zh-v1.5")
    
    return True

def check_qdrant_config():
    """检查Qdrant配置"""
    print("\n🗄️ Qdrant配置检查")
    print("=" * 40)
    
    qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
    qdrant_port = os.getenv('QDRANT_PORT', '6333')
    
    print(f"🏠 QDRANT_HOST: {qdrant_host}")
    print(f"🚪 QDRANT_PORT: {qdrant_port}")
    
    # 尝试连接Qdrant (可选)
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(host=qdrant_host, port=int(qdrant_port))
        info = client.get_cluster_info()
        print("✅ Qdrant连接成功")
    except ImportError:
        print("⚠️  qdrant-client未安装，跳过连接测试")
    except Exception as e:
        print(f"⚠️  Qdrant连接失败: {e}")
        print("💡 请确保Qdrant服务正在运行")
    
    return True

def test_deepseek_api():
    """测试DeepSeek API调用"""
    print("\n🧪 DeepSeek API测试")
    print("=" * 40)
    
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "你好，请回复'API测试成功'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API调用成功: {result}")
        return True
        
    except ImportError:
        print("⚠️  openai库未安装，跳过API测试")
        return True
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        print("💡 请检查API Key是否正确，网络是否正常")
        return False

def main():
    """主函数"""
    print("🚀 LLM面试模拟系统 - 配置检查工具")
    print("🇨🇳 基于DeepSeek + BGE + Qdrant技术栈")
    print("=" * 60)
    
    all_good = True
    
    # 检查各项配置
    all_good &= check_deepseek_config()
    all_good &= check_bge_model()
    all_good &= check_qdrant_config()
    all_good &= test_deepseek_api()
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 恭喜！所有配置检查通过")
        print("✨ 可以开始使用面试模拟系统了")
        print("\n📚 使用指南:")
        print("   1. 入门学习: Learn-Agent-Enhanced.ipynb")
        print("   2. 基础面试: v1-Create-Custom-Agent-Enhanced.ipynb")
        print("   3. JD面试: v2-Create-Custom-Agent-Enhanced.ipynb")
        print("   4. CV面试: v3-Create-Custom-Agent-Enhanced.ipynb")
    else:
        print("⚠️  配置存在问题，请根据上述提示进行修复")
        sys.exit(1)

if __name__ == "__main__":
    main()
