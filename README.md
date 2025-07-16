# TAPD_API

基于 FastAPI 的 TAPD 自动化接口服务，支持 cookies 管理、评论、工作项等多种 TAPD 相关操作，适合自动化集成和二次开发。

## 目录结构

```
TAPD_API/
├── app/
│   ├── api/                        # API 路由模块
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── comments.py     # 评论相关接口
│   │           ├── bugs.py         # bug相关接口
│   │           ├── stories.py      # story相关接口
│   │           ├── tcases.py       # tcases相关接口
│   │           ├── common.py       # 通用接口
│   │           └── ...             # 其他业务接口
│   ├── models/                     
│   │       └── tapd.py/            # Pydantic 数据模型
│   ├── util/
│   │   └── cookie.py               # Cookie 管理工具
│   └── main.py                     # FastAPI 主应用入口
├── config.py                       # 主配置文件
├── config.example.py               # 配置文件模板
├── requirements.txt                # Python 依赖列表
├── Dockerfile                      # Docker 镜像构建文件
├── run.py                          # 启动脚本
├── README.md                       # 项目说明文档
└── ...                             # 其他文件
```

## 环境要求

- Python 3.9+
- pip

## 安装依赖

```bash
pip install -r requirements.txt
```

## 本地运行

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或使用 run.py：

```bash
python run.py
```

## Docker 部署

1. 构建镜像

   ```bash
   docker build -t tapd-api .
   ```

2. 运行容器

   ```bash
   docker run -d -p 8000:8000 --name tapd-api tapd-api
   ```

## 配置说明

请参考  `config.example.py`，配置 TAPD 相关参数于`config.py`、CookieCloud 等信息。

## 主要功能

- TAPD cookies 自动获取与缓存
- 工作项信息查询
- 评论的增删改查
- 附件下载
- story页面信息的获取及修改
- bug页面信息的获取及修改

## API 文档

启动服务后访问：

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 后期功能
- [] cookie生成

## 贡献与反馈

如有问题或建议，欢迎提 issue 或 PR。

---

**温馨提示：**  
请勿将包含敏感信息的 `config.py`、`cookies.json` 等文件提交到公共仓库。 