import json
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.util.cookie import get_cookies
from config import TAPD_API_CONFIG

url = f"{TAPD_API_CONFIG['base_url']}/aggregation/workitem_aggregation/get_info"
cookies = get_cookies()  

response = requests.post(
    url=url, 
    cookies=cookies,
    headers={"User-Agent": TAPD_API_CONFIG["user_agent"]},
    data={"workspace_id":"58581237","entity_id":"1158581237001024453","entity_type":"bug","api_controller_prefix":"","enable_description":"true","is_detail":1,"blacklist_fields":[],"identifier":"app_for_editor,app_for_obj_more,app_for_obj_dialog_dropdown,app_for_obj_detail_panel,app_for_obj_detail_bottom_card,app_for_obj_attachment,app_for_obj_copy_link,app_for_obj_additional_panel","installed_app_entity":{"obj_id":"1158581237001024453","obj_type":"bug","obj_name":"缺陷"},"has_edit_rule_fields":[],"is_archived":0,"is_assistant_exec_log":1,"dsc_token":"R5bqAR7M2X4OO1wI"}
)

print("状态码:", response.status_code)
try:
    data = response.json()
    print("响应内容(JSON):", json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print("响应内容(非JSON):", response.text)