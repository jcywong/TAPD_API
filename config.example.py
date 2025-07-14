# TAPD API 配置文件示例
# 请复制此文件为 config.py 并修改相应的配置

# CookieCloud 配置
COOKIECLOUD_CONFIG = {
    "server_url": "http://your-cookiecloud-server.com",  # 修改为您的 CookieCloud 服务器地址
    "key": "your-key",  # 修改为您的key
    "secret": "your-secret"   # 修改为您的secret
}

# TAPD API 配置
TAPD_API_CONFIG = {
    "base_url": "https://www.tapd.cn/api",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

# 缓存配置
CACHE_CONFIG = {
    "cookie_file": "cookies.json",
    "use_cache": True,
    "cache_expire_hours": 24  # cookie 缓存过期时间（小时）
}

# 请求配置
REQUEST_CONFIG = {
    "timeout": 30,  # 请求超时时间（秒）
    "retry_times": 3,  # 重试次数
    "retry_delay": 1  # 重试延迟（秒）
} 