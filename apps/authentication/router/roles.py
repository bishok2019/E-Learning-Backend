from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params
from base.route import StandardResponse
from base.utils.query_utils import generic_list_handler

from ..models import CustomPermission, CustomRole
from ..schema import RoleBaseSchema

router = APIRouter()


@router.get("/list")
def list_roles(
    search: str = "",
    is_active: bool = None,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
    # __: User = Depends(get_current_user),
):
    """List all Role records with pagination, search, and filters"""

    query = db.query(CustomRole)

    return generic_list_handler(
        query=query,
        schema=RoleBaseSchema,
        pagination=pagination,
        search=search,
        search_fields=[
            CustomRole.name,
            CustomRole.description,
        ],
        filters={
            CustomRole.is_active: is_active,
        },
    )
