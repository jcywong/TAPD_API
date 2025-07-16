from fastapi import APIRouter, Query
import requests

from app.api.v1.endpoints.common import EntryTypeEnum, download_attachment, get_attacments, get_info
from app.models.tapd import UpdateStoryDescriptionRequest, UpdateStoryRequest, UpdateStoryStatusRequest
from app.util import cookie
import config

router = APIRouter(prefix="/stories", tags=["stories"])

@router.get("/")
def get_story_infos(
    workspace_id: int = Query(..., description="项目ID"),
    entry_id: int = Query(..., description="实体ID"),
    ):
    """
    查询需求信息
    """
    return get_info(
        workspace_id=workspace_id,
        entry_id=entry_id,
        entry_type=EntryTypeEnum.story
    )


@router.put("/")
def update_story(story: UpdateStoryRequest):
    """
    更新需求
    """
    cookies = cookie.load_cookies_from_file()
    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    if story.field_type == "status":
        # 更新状态
        # 获取当前状态


        current_status = get_story_status(story.workspace_id, story.id)
        if str(current_status["meta"]["code"]) != "0":
            return {
                "meta": current_status["meta"],
            }
        
        current_status = current_status["result"]

        # 更新状态
        change_story_status_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/workflow/change_story_status"
        change_story_status_data = {
                "workspace_id": story.workspace_id,
                "data": {
                    "type": "storieslist",
                    "new_status": story.field_value,
                    "change_type": "",
                    "Story": {
                        "current_status": current_status,
                        "story_id": story.id,
                        "close_task": False,
                        "complete_effort": False
                    },
                    "branch": {},
                    "Comment": {
                        "description": "",
                        "markdown_description": "",
                        "description_type": 1
                    },
                    "is_editor_or_markdown": 1,
                    "STATUS_planning-developing": {
                        "remarks": "",
                        "owner": ""
                    }
                },
                "dsc_token": cookies["dsc-token"] if cookies and 'dsc-token' in cookies else ""
            }

        try:
            response = requests.post(
                change_story_status_url,
                headers=headers,
                json=change_story_status_data
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
                        "message": f"change_story_status_error: {result}"
                    }
                }
        except Exception as e:
            return {
                "meta": {
                    "code": 500,
                    "message": f"change_story_status_error: {str(e)}"
                }
            }
    else:
        # 更新其他字段
        inline_update_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/inline_edit/story_update"

        inline_update_data = {
            "workspace_id": story.workspace_id,
            "id": story.id,
            "dec_token": cookies["dsc-token"] if cookies and 'dsc-token' in cookies else "",
            "field": story.field_type,
            "value": story.field_value
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
def get_story_status_dict(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询需求状态字典
    """
    infos = get_story_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }

    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["workspace_configs"]["workflow_infos"]["story"]["status_map"][str(workspace_id)]
    }


@router.get("/status")
def get_story_status(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询需求状态
    """
    infos = get_story_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }

    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["Story"]["status"]
    }


@router.put("/status")
def update_story_status(body: UpdateStoryStatusRequest):
    """
    更新需求状态
    """
    story = UpdateStoryRequest(
        workspace_id=body.workspace_id,
        id=body.id,
        field_type="status",
        field_value=body.status
    )
    return update_story(story)

@router.get("/description")
def get_story_description(
    workspace_id: int = Query(..., description="项目ID"),
    entity_id: int = Query(..., description="实体ID"),
    ):
    """
    查询需求描述
    """
    infos = get_story_infos(workspace_id, entity_id)
    if str(infos["meta"]["code"]) != "0":
        return {
            "meta": infos["meta"],
        }
    return {
        "meta": infos["meta"],
        "result": infos["result"]["get_info_ret"]["data"]["Story"]["description"]
    }

@router.put("/description")
def update_story_description(body: UpdateStoryDescriptionRequest):
    """
    更新需求描述
    """
    story = UpdateStoryRequest(
        workspace_id=body.workspace_id,
        id=body.id,
        field_type="description",
        field_value=body.description
    )
    return update_story(story)


@router.get("/attachments")
def get_story_attachments(workspace_id: int, entity_id: int):
    """
    查询需求附件
    """
    return get_attacments(workspace_id, EntryTypeEnum.story, entity_id)


@router.get("/attachment/download")
def download_story_attachment(workspace_id: int, attachment_id: int):
    """
    下载需求附件
    """
    return download_attachment(workspace_id, EntryTypeEnum.story, attachment_id)