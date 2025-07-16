import json
from fastapi import APIRouter, Query
from typing import Optional, List

import requests

from app.api.v1.endpoints.common import EntryTypeEnum, get_info
from app.util import cookie
import config
from app.models.tapd import AddCommentRequest, UpdateCommentRequest
router = APIRouter(prefix="/comments", tags=["comments"])



@router.get("/")
def get_comments(
    workspace_id: int = Query(..., description="项目ID"),
    entry_type: EntryTypeEnum = Query(description="评论类型（如bug|story|task）"),
    entry_id: int = Query(..., description="评论所依附的业务对象实体id"),
    ):
    """
    查询评论列表
    """
    result = get_info(
        entry_type=entry_type,
        entry_id=entry_id,
        workspace_id=workspace_id
    )

    if str(result["meta"]["code"]) != "0":
        return {
            "meta": result["meta"],
        }

    try:
        comments = result["result"]["get_info_ret"]["data"]["comment_list"]["comments"]
        return {
            "meta": result["meta"],
            "result": comments
        }
    except Exception as e:
        return {
            "meta": {
                "code": 500,
                "message": f"get_comments_error: {str(e)}"
            }
        }


@router.post("/")
def add_comment(body: AddCommentRequest):
    """
    添加评论
    """
    add_comment_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/comments/add_comment"
    cookies = cookie.load_cookies_from_file()

    data = {
        "workspace_id": body.workspace_id,
        "entity_id": body.entry_id,
        "entity_type": body.entry_type,
        "description": body.description,
        "description_type": 1,
        "root_id": body.root_id,
        "reply_id": body.reply_id,
        "dsc_token": cookies["dsc-token"] if cookies and "dsc-token" in cookies else ""
    }

    headers = {
        "User-Agent": config.TAPD_API_CONFIG["user_agent"],
        "Cookie": cookie.dict_to_cookie_str(cookies) if cookies else "",
    }

    try:
        response = requests.post(
            add_comment_url,
            headers=headers,
            json=data
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
                    "message": f"add_comment_error: {result}"
                }
            }
    except Exception as e:
        return {
            "meta": {
                "code": 500,
                "message": f"add_comment_error: {str(e)}"
            }
        }   


# @router.put("/")
# def update_comment(body: UpdateCommentRequest):
    # """
    # 编辑评论
    # """
    # edit_comment_url = f"{config.TAPD_API_CONFIG['base_url']}/entity/comments/edit_comment"
    # cookies = cookie.load_cookies_from_file()

    # data = {
    #     "id": body.id,
    #     "workspace_id": body.workspace_id,
    #     "entity_type": body.entry_type,
    #     "description": body.description,
    #     "description_type": 1,
    #     "markdown_description": "",
    #     "dsc_token": "KNmB2HQtBGkb1vz"
    # }

    # headers = {
    #     "User-Agent": config.TAPD_API_CONFIG["user_agent"],
    #     "Cookie": dict_to_cookie_str(cookies) if cookies else "",
    # }

    # try:
    #     response = requests.put(
    #         edit_comment_url,
    #         headers=headers,
    #         json=data
    #     )

    #     if response.status_code == 200:
    #         result = response.json()
    #         return {
    #             "msg": "success",
    #             "result": result
    #         }
    #     else:
    #         result = response.text
    #         return {
    #             "msg": "error",
    #             "error": result
    #         }
    # except Exception as e:
    #     return {
    #         "msg": "error",
    #         "error": str(e)
    #     }
