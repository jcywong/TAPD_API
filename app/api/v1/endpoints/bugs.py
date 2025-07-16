from fastapi import APIRouter, Query
import requests

from app.api.v1.endpoints.common import download_attachment, get_attacments, get_info
from app.models.tapd import UpdateBugDescriptionRequest, UpdateBugRequest, UpdateBugStatusRequest
from app.util import cookie
import config

router = APIRouter(prefix="/bugs", tags=["bugs"])

@router.get("/")
def get_bug_infos(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询缺陷信息
    """
    return get_info(
        workspace_id=workspace_id,
        entry_id=entity_id,
        entry_type="bug"
    )



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
        # 更新状态
        # 获取当前状态
        current_status = get_bug_status(bug.workspace_id, bug.id)
        if str(current_status["meta"]["code"]) != "0":
            return {
                "meta": current_status["meta"],
            }

        current_status = current_status["result"]

        # 更新状态
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
            "dsc_token": cookies["dsc-token"] if cookies and 'dsc-token' in cookies else ""
        }

        try:
            response = requests.post(
                change_bug_status_url,
                headers=headers,
                json=change_bug_status_data
            )

            if response.status_code == 200:
                result = response.json()
                if str(result["meta"]["code"]) != "0":
                    return {
                        "meta": result["meta"],
                    }

                return {
                    "meta": result["meta"],
                    "result": result["data"]
                }
            else:
                result = response.text
                return {
                    "meta": {
                        "code": response.status_code,
                        "message": f"change_bug_status_error: {result}"
                    }
                }
        except Exception as e:  
            return {
                "meta": {
                    "code": 500,
                    "message": f"change_bug_status_error: {str(e)}"
                }
            }
    else:
        # 更新其他字段
        inline_update_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/bugs/inline_update"

        inline_update_data = {
            "workspace_id": bug.workspace_id,
            "dec_token": cookies["dsc-token"] if cookies and 'dsc-token' in cookies else "",
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
                if str(result["meta"]["code"]) != "0":
                    return {
                        "meta": {
                            "code": result["meta"]["code"],
                            "message": f"inline_update_error: {result['meta']['message']}"
                        },
                    }

                return {
                    "meta": result["meta"],
                    "result": result["data"]
                }
            else:
                result = response.text
                return {
                    "meta": {
                        "code": response.status_code,
                        "message": f"inline_update_error: {result}"
                    }
                }
        except Exception as e:
            return {
                "meta": {
                    "code": 500,
                    "message": f"inline_update_error: {str(e)}"
                }
            }


@router.get("/status_dict")
def get_bug_status_dict(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询缺陷状态字典
    """
    infos = get_bug_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }

    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["workspace_configs"]["workflow_infos"]["bug"]["status_map"][str(workspace_id)]
    }


@router.get("/status")
def get_bug_status(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询缺陷状态
    """
    infos = get_bug_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }
    
    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["Bug"]["status"]
    }

@router.put("/status")
def update_bug_status(body: UpdateBugStatusRequest):
    """
    更新缺陷状态
    """
    bug = UpdateBugRequest(
        workspace_id=body.workspace_id,
        id=body.id,
        field_type="status",
        field_value=body.status
    )
    return update_bug(bug)

@router.get("/description")
def get_bug_description(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询缺陷描述
    """
    infos = get_bug_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }
    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["Bug"]["description"]
    }

@router.put("/description")
def update_bug_description(body: UpdateBugDescriptionRequest):
    """
    更新缺陷描述
    """
    bug = UpdateBugRequest(
        workspace_id=body.workspace_id,
        id=body.id,
        field_type="description",
        field_value=body.description
    )
    return update_bug(bug)


@router.get("/attachments")
def get_bug_attachments(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询缺陷附件信息
    """
    return get_attacments(workspace_id, "bug", entity_id)


@router.get("/attachment/download")
def download_bug_attachment(
    workspace_id: int = Query(..., description="项目ID"),
    attachment_id: int = Query(..., description="附件ID"),
    ):
    """
    下载缺陷附件
    """
    return download_attachment(workspace_id, "bug", attachment_id)