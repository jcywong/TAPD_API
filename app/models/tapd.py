from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# 1. 添加错误消息
class AddErrorMessageRequest(BaseModel):
    # TODO: 根据实际参数补充字段
    message: str = Field(..., description="错误消息内容")

class AddErrorMessageResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str

# 2. 添加故事消息
class AddStoryMessageRequest(BaseModel):
    message: str = Field(..., description="故事消息内容")

class AddStoryMessageResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str

# 3. 标记 Bug 通过
class MarkBugPassRequest(BaseModel):
    bug_id: str

class MarkBugPassResponse(BaseModel):
    success: bool
    message: str

# 4. 拒绝 Bug
class RejectBugRequest(BaseModel):
    bug_id: str
    reason: Optional[str] = None

class RejectBugResponse(BaseModel):
    success: bool
    message: str

# 5. 标记 Story 通过
class MarkStoryPassRequest(BaseModel):
    story_id: str

class MarkStoryPassResponse(BaseModel):
    success: bool
    message: str

# 6. 拒绝 Story
class RejectStoryRequest(BaseModel):
    story_id: str
    reason: Optional[str] = None

class RejectStoryResponse(BaseModel):
    success: bool
    message: str

# 7. 获取 Story 的 case id
class GetStoryCaseIdRequest(BaseModel):
    story_id: str

class GetStoryCaseIdResponse(BaseModel):
    success: bool
    case_id: Optional[str] = None
    message: str

# 8. 获取 bug 的 case id
class GetBugCaseIdRequest(BaseModel):
    bug_id: str

class GetBugCaseIdResponse(BaseModel):
    success: bool
    case_id: Optional[str] = None
    message: str

# 9. 获取 test plan 信息
class GetTestPlanInfoRequest(BaseModel):
    plan_id: str

class GetTestPlanInfoResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str

# 10. 获取 case 信息
class GetCaseInfoRequest(BaseModel):
    case_id: str

class GetCaseInfoResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str

# 11. 获取 entry 的评论
class GetEntryCommentsRequest(BaseModel):
    entry_id: str

class GetEntryCommentsResponse(BaseModel):
    success: bool
    comments: List[Dict[str, Any]] = []
    message: str

# 12. 获取 entry 的附件
class GetEntryAttachmentsRequest(BaseModel):
    entry_id: str

class GetEntryAttachmentsResponse(BaseModel):
    success: bool
    attachments: List[Dict[str, Any]] = []
    message: str

# 13. 下载附件
class DownloadAttachmentRequest(BaseModel):
    attachment_id: str

class DownloadAttachmentResponse(BaseModel):
    success: bool
    file_url: Optional[str] = None
    message: str 

class AddCommentRequest(BaseModel):
    description: str = Field(..., description="内容")
    author: str = Field(..., description="评论人")
    entry_type: str = Field(..., description="评论类型（如bug、bug_remark、story、task）")
    entry_id: int = Field(..., description="评论所依附的业务对象实体id")
    workspace_id: int = Field(..., description="项目ID")
    root_id: Optional[int] = Field(None, description="根评论ID")
    reply_id: Optional[int] = Field(None, description="评论回复ID")


class UpdateCommentRequest(BaseModel):
    description: str = Field(..., description="内容")
    entry_type: str = Field(..., description="评论类型（如bug、bug_remark、story、task）")
    id: int = Field(..., description="评论ID")
    workspace_id: int = Field(..., description="项目ID")
    change_creator: str = Field(..., description="修改人")


class UpdateBugRequest(BaseModel):
    id: int = Field(..., description="缺陷ID")
    workspace_id: int = Field(..., description="项目ID")
    field_type: str = Field(..., description="字段类型")
    field_value: str = Field(..., description="字段值")