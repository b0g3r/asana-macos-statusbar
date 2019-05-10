from rumps import rumps

from asana_api import AsanaClient


class AsanaMacosStatusbar(rumps.App):
    """
    FIXME: write doc
    """


macos_app = AsanaMacosStatusbar("", title="fetch task")


def get_task_name_updater(asana_client: AsanaClient):
    def updater(timer_obj):
        print('aaa')
        macos_app.title = 'fetch task'
        macos_app.title = asana_client.get_task_name()

    return updater
