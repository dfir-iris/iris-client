objects_map = {
    "ioc_type": {
        "id": "type_id",
        "name": "type_name",
        "description": "type_description",
        "taxonomy": "type_taxonomy"
    },
    "tlp": {
        "id": "tlp_id",
        "name": "tlp_name",
        "color": "tlp_bscolor"
    },
    "ioc": {
        "id": "ioc_id",
        "_value": "ioc_value",
        "_description": "ioc_description",
        "_tags": "ioc_tags",
        "_tlp": "ioc_tlp_id",
        "_ioc_type": "ioc_type_id"
    },
    "customer": {
        "id": "customer_id",
        "name": "customer_name"
    },
    "analysis_status": {
        "id": "id",
        "name": "name"
    },
    "asset_type": {
        "id": "asset_id",
        "description": "asset_description",
        "name": "asset_name"
    },
    "asset": {
        "id": "asset_id",
        "_name": "asset_name",
        "_description": "asset_description",
        "_ip": "asset_ip",
        "tags": "asset_tags",
        "_domain": "asset_domain",
        "_compromised": "asset_compromised",
        "_additional_info": "asset_info",
        "analysis_status": "analysis_status_id",
        "ioc_links": "linked_ioc",
        "asset_type": "asset_type_id"
    },
    "notes_group": {
        "id": "group_id",
        "_title": "group_title"
    },
    "note": {
        "id": "note_id",
        "_title": "note_title",
        "_content": "note_content"
    },
    "event": {
        "id": "event_id",
        "_category": "event_category_id",
        "_color": "event_color",
        "_content": "event_content",
        "date": "event_date",
        "_date_wtz": "event_date_wtz",
        "_in_graph": "event_in_graph",
        "_in_summary": "event_in_summary",
        "_raw_content": "event_raw",
        "_source": "event_source",
        "_tags": "event_tag",
        "_title": "event_title",
        "_tz": "event_tz"
    },
    "event_category": {
        "id": "id",
        "_name": "name"
    },
    "case_task": {
        "id": "task_id",
        "_title": "task_title",
        "assignee": "task_assignee_id",
        "_description": "task_description",
        "open_date": "task_open_date",
        "close_date": "task_close_date",
        "last_update_date": "task_last_update",
        "status": "task_status",
        "tags": "task_tags"
    },
    "global_task": {
        "id": "task_id",
        "_title": "task_title",
        "assignee": "task_assignee_id",
        "_description": "task_description",
        "open_date": "task_open_date",
        "close_date": "task_close_date",
        "last_update_date": "task_last_update",
        "status": "task_status_id",
        "tags": "task_tags"
    },
    "task_status": {
        "id": "id",
        "_name": "status_name",
        "_description": "status_description",
        "_bscolor": "status_bscolor"
    },
    "user": {
        "id": "user_id",
        "login": "user_login",
        "name": "user_name",
        "active": "user_active"
    },
    "evidence": {
        "id": "id",
        "_description": "file_description",
        "_filename": "filename",
        "_hash": "file_hash",
        "_size": "file_size"
    }
}
