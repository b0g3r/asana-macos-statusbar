from rumps import rumps

from asana_api import AsanaClient


rumps.debug_mode(True)


class AsanaMacosStatusbar(rumps.App):
    """
    FIXME: write doc
    """


macos_app = AsanaMacosStatusbar("", title="")


def get_task_name_updater(asana_client: AsanaClient):
    def updater(timer_obj):
        macos_app.title = 'Fetch task'
        macos_app.title = asana_client.get_task_name()

    return updater
