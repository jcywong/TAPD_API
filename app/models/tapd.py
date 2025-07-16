from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.api.v1.endpoints.common import TaskStatusEnum


class AddCommentRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    entry_type: str = Field(..., description="评论类型（如bug、bug_remark、story、task）")
    entry_id: int = Field(..., description="评论所依附的业务对象实体id")
    description: str = Field(..., description="内容")
    root_id: Optional[int] = Field(None, description="评论回复ID")
    reply_id: Optional[int] = Field(None, description="评论回复ID")


class UpdateCommentRequest(BaseModel):
    description: str = Field(..., description="内容")
    entry_type: str = Field(..., description="评论类型（如bug、bug_remark、story、task）")
    id: int = Field(..., description="评论ID")
    workspace_id: int = Field(..., description="项目ID")
    change_creator: str = Field(..., description="修改人")


class UpdateBugRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="缺陷ID")
    field_type: str = Field(..., description="字段类型（如status）")
    field_value: str = Field(..., description="字段值")


class UpdateBugStatusRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="缺陷ID")
    status: str = Field(..., description="状态")


class UpdateBugDescriptionRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="缺陷ID")
    description: str = Field(..., description="描述")

class UpdateStoryRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="需求ID")
    field_type: str = Field(..., description="字段类型（如status）")
    field_value: str = Field(..., description="字段值")

class UpdateStoryStatusRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="需求ID")
    status: str = Field(..., description="状态")

class UpdateStoryDescriptionRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="需求ID")
    description: str = Field(..., description="描述")

class UpdateTaskRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="任务ID")
    field_type: str = Field(..., description="字段类型（如status）")
    field_value: str = Field(..., description="字段值")


class UpdateTaskStatusRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="任务ID")
    status: TaskStatusEnum = Field(..., description="状态（progressing/open/done）")

class UpdateTaskDescriptionRequest(BaseModel):
    workspace_id: int = Field(..., description="项目ID")
    id: int = Field(..., description="任务ID")
    description: str = Field(..., description="描述")