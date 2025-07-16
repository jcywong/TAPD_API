from fastapi import APIRouter, Query
import requests

from app.api.v1.endpoints.common import EntryTypeEnum, download_attachment, get_attacments, get_info
from app.models.tapd import UpdateTaskDescriptionRequest, UpdateTaskRequest, UpdateTaskStatusRequest
from app.util import cookie
import config

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def get_task_infos(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询任务信息
    """
    return get_info(
        workspace_id=workspace_id,
        entry_id=entity_id,
        entry_type=EntryTypeEnum.task
    )

@router.put("/")
def update_task(task: UpdateTaskRequest):
    """
    更新任务
    """
    cookies = cookie.load_cookies_from_file()
    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    if task.field_type == "status":
        # 更新状态
        change_task_status_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/workflow/change_task_status"
        change_task_status_data = {
            "workspace_id": str(task.workspace_id),
            "data": {
                "auto_complete_effort": "no",
                "new_status": task.field_value, 
                "Task": {
                    "task_id": str(task.id)
                },
                "from": ""
            },
            "dsc_token": cookies.get("dsc_token", "") if cookies else ""
        }

        try:
            response = requests.post(
                change_task_status_url,
                headers=headers,
                json=change_task_status_data
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
                        "message": f"change_task_status_error: {result}"
                    }
                }
        except Exception as e:
            return {
                "meta": {
                    "code": 500,
                    "message": f"change_task_status_error: {str(e)}"
                }
            }
    else:
        # 更新其他字段  
        inline_update_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/inline_edit/task_update"
        inline_update_data = {
            "workspace_id": task.workspace_id,
            "id": task.id,
            "dsc_token": cookies.get("dsc_token", "") if cookies else "",
            "field": task.field_type,
            "value": task.field_value
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
                        "meta": result["meta"],
                    }
                return {
                    "meta": result["meta"],
                    "result": result["data"]
                }
        except Exception as e:
            return {
                "meta": {
                    "code": 500,
                    "message": f"change_task_status_error: {str(e)}"
                }
            }


@router.get("/status_dict")
def get_task_status_dict(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询任务状态字典
    """
    infos = get_task_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }
    
    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["workspace_configs"]["workflow_infos"]["task"]["status_map"]
    }   

@router.get("/status")
def get_task_status(workspace_id: int, entity_id: int):
    """
    查询任务状态
    """
    infos = get_task_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }
    
    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["Task"]["status"]
    }

@router.put("/status")
def update_task_status(body: UpdateTaskStatusRequest):
    """
    更新任务状态
    """
    task = UpdateTaskRequest(
        workspace_id=body.workspace_id,
        id=body.id,
        field_type="status",
        field_value=body.status
    )
    return update_task(task)

@router.get("/description")
def get_task_description(workspace_id: int, entity_id: int):
    """
    查询任务描述
    """
    infos = get_task_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }
    
    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["Task"]["description"]
    }

@router.put("/description")
def update_task_description(body: UpdateTaskDescriptionRequest):
    """
    更新任务描述
    """
    task = UpdateTaskRequest(
        workspace_id=body.workspace_id,
        id=body.id,
        field_type="description",
        field_value=body.description
    )
    return update_task(task)

@router.get("/attachments")
def get_task_attachments(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询任务附件信息
    """
    return get_attacments(workspace_id, EntryTypeEnum.task, entity_id)

@router.get("/attachment/download")
def download_task_attachment(
    workspace_id: int = Query(..., description="项目ID"),
    attachment_id: int = Query(..., description="附件ID"),
    ):
    """
    下载任务附件
    """
    return download_attachment(workspace_id, EntryTypeEnum.task, attachment_id)