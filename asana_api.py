from typing import Optional

from asana import Client


class AsanaClient(object):
    def __init__(
            self,
            token: str,
            project_id: Optional[str] = None,
            section_id: Optional[str] = None,
            tag_id: Optional[str] = None,
    ):
        self._client = Client.access_token(token)
        if project_id is not None:
            filter_func = lambda: self._client.tasks.find_by_project(project_id)
        elif section_id is not None:
            filter_func = lambda: self._client.tasks.find_by_section(section_id)
        elif tag_id is not None:
            filter_func = lambda: self._client.tasks.find_by_tag(tag_id)
        else:
            raise ValueError("You should set one of filter_props")
        self.filter_func = filter_func

    def get_task_name(self) -> str:
        tasks = list(self.filter_func())
        if tasks:
            return tasks[0]['name']
        else:
            return 'No task'

