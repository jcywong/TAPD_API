from enum import Enum
from typing import Optional
from fastapi import Query, Response
import requests
from app.util import cookie
import config
from fastapi import APIRouter

router = APIRouter(prefix="/common", tags=["common"])

entry_type_map = {
    "bug": "缺陷",
    "story": "需求",
    "task": "任务"
}

class EntryTypeEnum(str, Enum):
    bug = "bug"
    story = "story"
    task = "task"

class TaskStatusEnum(str, Enum):
    progressing = "progressing"
    open = "open"
    done = "done"

@router.get("/")
def get_info(
    workspace_id: int = Query(..., description="项目ID"),
    entry_type: Optional[str] = Query(description="类型（如bug|story)"),
    entry_id: Optional[int] = Query(..., description="实体id"),
    ):
    """
    通用获取实体信息

    返回信息：
    1. get_tab_setting_ret: tab区域信息
    2. get_workitem_basic_info_ret: 激活 tab 区域信息
    3. installed_app_entrance_ret: 安装的 app 入口信息（腾讯会议）
    4. personal_copy_link_display_configs: 个人复制链接配置信息
    5. get_info_ret: 详细信息、基础信息、标签、附件、评论
    6. get_last_execute_detail_ret: 最近执行详情
    7. workspace：项目信息
    """
    common_get_info_url = f"{config.TAPD_API_CONFIG['base_url']}/aggregation/workitem_aggregation/common_get_info"
    get_info_url = f"{config.TAPD_API_CONFIG['base_url']}/aggregation/workitem_aggregation/get_info"
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
        "dsc_token": cookies["dsc-token"] if cookies and "dsc-token" in cookies else ""
    }
    # 发送请求
    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    try:
        common_get_info_response = requests.post(
            common_get_info_url,
            headers=headers,
            json=data
        )

    
        if common_get_info_response.status_code == 200:
            common_get_info_result = common_get_info_response.json()

            if str(common_get_info_result["meta"]["code"]) != "0":
                return {
                    "meta": common_get_info_result["meta"],
                }
            
            # 增加 get_info 请求
            try:
                get_info_response = requests.post(
                    get_info_url,
                    headers=headers,
                    json=data
                )

                if get_info_response.status_code == 200:
                    get_info_result = get_info_response.json()

                    if str(get_info_result["meta"]["code"]) != "0":
                        return {
                            "meta": get_info_result["meta"],
                        }

                    return {
                        "meta": get_info_result["meta"],
                        "result": {
                            **common_get_info_result["data"],
                            **get_info_result["data"]
                        }
                    }
                else:
                    get_info_result = get_info_response.text
                    return {
                        "meta": {
                            "code": get_info_response.status_code,
                            "message": f"get_info_error: {get_info_result}"
                        }
                    }
            except Exception as e:
                return {
                    "meta": {
                        "code": 500,
                        "message": f"get_info_error: {str(e)}"
                    }
                }
        else:
            result = common_get_info_response.text
            return {
                "meta": {
                    "code": common_get_info_response.status_code,
                    "message": f"common_get_info_error: {result}"
                }
            }
    except Exception as e:
        return {
            "meta": {
                "code": 500,
                "message": f"common_get_info_error: {str(e)}"
            }
        }


def get_attacments(
    workspace_id: int = Query(..., description="项目ID"),
    entity_type: str = Query(..., description="实体类型"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    获取附件
    """
    infos = get_info(workspace_id, entity_type, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }

    try:
        attachments = infos["result"]["get_info_ret"]["data"]["attachment_list"]["attachments"]
        return {
            "meta": infos["meta"],
            "result": attachments
        }
    except Exception as e:
        return {
            "meta": {
                "code": 500,
                "message": f"get_attacments_error: {str(e)}"
            }
        }

        
def download_attachment(
    workspace_id: int = Query(..., description="项目ID"),
    entity_type: str = Query(..., description="实体类型"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    下载需求附件
    """
    dowanload_url = f"https://www.tapd.cn/{workspace_id}/attachments/preview_attachments/{entity_id}/{entity_type}？"
    cookies = cookie.load_cookies_from_file()
    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    response = requests.get(
        dowanload_url,
        headers=headers,
        cookies=cookies
    )
    if response.status_code == 200:
        return Response(
            content=response.content,
            media_type=response.headers["Content-Type"]
        )
    else:
        return {
            "meta": {
                "code": response.status_code,
                "message": f"download_attachment_error: {response.text}"
            }
        }