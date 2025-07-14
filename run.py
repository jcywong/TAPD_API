#!/usr/bin/env python3
"""
TAPD API 后端服务启动脚本
"""

import uvicorn
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    print("🚀 启动 TAPD API 后端服务...")
    print("📖 API 文档地址: http://localhost:8000/docs")
    print("🔍 健康检查: http://localhost:8000/health")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 