from typing import Optional
from fastapi import Query
import requests
from app.util import cookie
import config


entry_type_map = {
    "bug": "缺陷",
    "bug_remark": "缺陷备注",
    "story": "需求",
    "task": "任务"
}

def get_common_info(
    entry_type: Optional[str] = Query(description="评论类型（如bug|bug_remark|story|tasks，多类型用|分隔）"),
    entry_id: Optional[int] = Query(..., description="评论所依附的业务对象实体id"),
    workspace_id: int = Query(..., description="项目ID，必填"),
):
    """
    查询评论列表
    """
    common_get_info_url = f"{config.TAPD_API_CONFIG['base_url']}/aggregation/workitem_aggregation/common_get_info"
    cookies = cookie.load_cookies_from_file()

    # 构建 请求体
    data = {
        "workspace_id": workspace_id,
        "entity_id": entry_id,
        "entity_type": entry_type,
        "api_controller_prefix": "",
        "enable_description": "true",
        "is_detail": 1,
        "blacklist_fields": [],
        "identifier": "app_for_editor,app_for_obj_more,app_for_obj_dialog_dropdown,app_for_obj_detail_panel,app_for_obj_detail_bottom_card,app_for_obj_attachment,app_for_obj_copy_link,app_for_obj_additional_panel",
        "installed_app_entity": {
            "obj_id": entry_id,
            "obj_type": entry_type,
            "obj_name": entry_type_map[entry_type] if entry_type in entry_type_map else ""
        },
        "has_edit_rule_fields": [],
        "is_archived": 0,
        "is_assistant_exec_log": 1,
        "app_id": "",
        "dsc_token": cookies["dsc-token"] if 'dsc-token' in cookies.keys() else ""
    }

    # 发送请求
    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    try:
        response = requests.post(
            common_get_info_url,
            headers=headers,
            json=data
        )

    
        if response.status_code == 200:
            result = response.json()

            return {
                "msg": "success",
                "result": result,
            }
        else:
            result = response.text
            return {
                "msg": "error",
                "error": result
            }
    except Exception as e:
        return {
            "msg": "error",
            "error": str(e)
        }