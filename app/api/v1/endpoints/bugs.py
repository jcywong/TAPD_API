from fastapi import APIRouter, Query
import requests

from app.api.v1.endpoints.common import get_common_info
from app.models.tapd import UpdateBugRequest
from app.util import cookie
import config

router = APIRouter(prefix="/bugs", tags=["bugs"])

@router.get("/")
def get_bug_info(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    entity_type: str = Query("bug", description="实体类型"),
):
    """
    查询缺陷详情
    """
    get_info_url = f"{config.TAPD_API_CONFIG['base_url']}/aggregation/workitem_aggregation/get_info"
    cookies = cookie.load_cookies_from_file()

    data = {
        "workspace_id": workspace_id,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "api_controller_prefix": "",
        "enable_description": "true",
        "is_detail": 1,
        "blacklist_fields": [],
        "identifier": "app_for_editor,app_for_obj_more,app_for_obj_dialog_dropdown,app_for_obj_detail_panel,app_for_obj_detail_bottom_card,app_for_obj_attachment,app_for_obj_copy_link,app_for_obj_additional_panel",
        "installed_app_entity": {
            "obj_id": entity_id,
            "obj_type": entity_type,
            "obj_name": "缺陷"
        },
        "has_edit_rule_fields": [],
        "is_archived": 0,
        "is_assistant_exec_log": 1,
        "dsc_token": cookies["dsc-token"] if 'dsc-token' in cookies.keys() else ""
    }

    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    try:
        response = requests.post(
            get_info_url,
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            return {
                "msg": "success",
                "result": result
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
    

@router.put("/")
def update_bug(bug: UpdateBugRequest):
    """
    更新缺陷
    """

    cookies = cookie.load_cookies_from_file()
    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    if bug.field_type == "status":
        common_info = get_common_info(
            workspace_id=bug.workspace_id,
            entry_id=bug.id,
            entry_type="bug"
        )

        if common_info["msg"] != "success":
            return {
                "msg": "error",
                "error": common_info["error"]
            }

        current_status = common_info["result"]["data"]["get_info_ret"]["data"]["Bug"]["status"]



        change_bug_status_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/workflow/change_bug_status"
        change_bug_status_data = {
            "workspace_id": bug.workspace_id,
            "data": {
                "Bug": {
                    "current_status": current_status,
                    "id": bug.id,
                    "complete_effort": False
                },
                "new_status": bug.field_value,
                "Comment": {
                    "description": "",
                    "markdown_description": "",
                    "description_type": 1
                },
                "is_editor_or_markdown": 1,
                "branch": {},
                "STATUS_new-in_progress": {
                    "remarks": "",
                    "current_owner": "",
                    "de": ""
                }
            },
            "dsc_token": cookies["dsc-token"] if 'dsc-token' in cookies.keys() else ""
        }

        try:
            response = requests.post(
                change_bug_status_url,
                headers=headers,
                json=change_bug_status_data
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "msg": "success",
                    "result": result
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
    else:
        inline_update_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/bugs/inline_update"

        inline_update_data = {
            "workspace_id": bug.workspace_id,
            "dec_token": cookies["dsc-token"] if 'dsc-token' in cookies.keys() else "",
            "data": {
                "id": bug.id,
                "field": bug.field_type,
                "value": bug.field_value
            },
        }

        try:
            response = requests.post(
                inline_update_url,
                headers=headers,
                json=inline_update_data
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "msg": "success",
                    "result": result
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