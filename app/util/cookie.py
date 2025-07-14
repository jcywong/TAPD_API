import json
import os
from datetime import datetime, timedelta
from PyCookieCloud import PyCookieCloud
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import COOKIECLOUD_CONFIG, CACHE_CONFIG


def save_cookies_to_file(cookies_dict, filename=None):
    """将 cookies 保存到文件"""
    if filename is None:
        filename = CACHE_CONFIG["cookie_file"]
    
    cookie_data = {
        "timestamp": datetime.now().isoformat(),
        "cookies": cookies_dict
    }
    
    # 确保目录存在
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cookie_data, f, ensure_ascii=False, indent=2)
    
    print(f"Cookies 已保存到 {filename}")


def load_cookies_from_file(filename=None):
    """从文件加载 cookies"""
    if filename is None:
        filename = CACHE_CONFIG["cookie_file"]
    
    try:
        if not os.path.exists(filename):
            print(f"Cookie 文件 {filename} 不存在")
            return None
        
        with open(filename, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
        
        # 检查缓存是否过期
        if CACHE_CONFIG.get("cache_expire_hours"):
            saved_time = datetime.fromisoformat(cookie_data.get("timestamp", "1970-01-01T00:00:00"))
            expire_time = datetime.now() - timedelta(hours=CACHE_CONFIG["cache_expire_hours"])
            
            if saved_time < expire_time:
                print(f"Cookie 缓存已过期（保存时间: {saved_time}）")
                # 如果缓存过期，则重新获取 cookies
                return refresh_cookies()
        
        print(f"从文件加载 cookies，保存时间: {cookie_data.get('timestamp', '未知')}")
        return cookie_data.get("cookies", {})
    
    except Exception as e:
        print(f"加载 cookies 时出错: {e}")
        return None


def get_cookies(use_cache=None, cache_file=None):
    """获取 cookies，可选择使用缓存"""
    if use_cache is None:
        use_cache = CACHE_CONFIG["use_cache"]
    
    if cache_file is None:
        cache_file = CACHE_CONFIG["cookie_file"]
    
    if use_cache:
        cached_cookies = load_cookies_from_file(cache_file)
        if cached_cookies:
            return cached_cookies
    
    # 从 CookieCloud 获取新的 cookies
    cookie_cloud = PyCookieCloud(
        COOKIECLOUD_CONFIG["server_url"],
        COOKIECLOUD_CONFIG["key"], 
        COOKIECLOUD_CONFIG["secret"]
    )
    
    the_key = cookie_cloud.get_the_key()
    if not the_key:
        print('Failed to get the key')
        return {}
    
    encrypted_data = cookie_cloud.get_encrypted_data()
    if not encrypted_data:
        print('Failed to get encrypted data')
        return {}
    
    decrypted_data = cookie_cloud.get_decrypted_data()
    if not decrypted_data:
        print('Failed to get decrypted data')
        return {}
    
    # 提取 requests 可用的 cookies 字典
    cookies_dict = {}
    for item in decrypted_data.get("tapd.cn", []):
        name = item.get("name")
        value = item.get("value")
        if name and value:
            cookies_dict[name] = value
    
    # 保存到文件
    if cookies_dict:
        save_cookies_to_file(cookies_dict, cache_file)
    
    return cookies_dict


def refresh_cookies(cache_file=None):
    """强制刷新 cookies"""
    return get_cookies(use_cache=False, cache_file=cache_file)

def dict_to_cookie_str(cookies: dict) -> str:
    return "; ".join([f"{k}={v}" for k, v in cookies.items()])


if __name__ == '__main__':
    cookies = get_cookies()
    print(f"获取到 {len(cookies)} 个 cookies")
    for name, value in cookies.items():
        print(f"{name}: {value[:20]}..." if len(value) > 20 else f"{name}: {value}")
