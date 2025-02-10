from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class DBTask(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    created_by: Optional[str] = None
    assignee_id: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class DBUser(BaseModel):
    id: str
    full_name: str
    skills: List[str]
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# create table public.profiles (
#   created_at timestamp with time zone not null default now(),
#   full_name text not null,
#   id uuid not null default auth.uid (),
#   avatar text null,
#   about text null,
#   skills text null,
#   role public.roles null default 'User'::roles,
#   status public.user_status null default 'Active'::user_status,
#   constraint profiles_pkey primary key (id),
#   constraint profiles_id_fkey foreign KEY (id) references auth.users (id) on update CASCADE on delete CASCADE
# ) TABLESPACE pg_default;
class DBProfile(BaseModel):
    id: str
    full_name: str
    avatar: Optional[str] = None
    about: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    role: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None


class DBProject(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
