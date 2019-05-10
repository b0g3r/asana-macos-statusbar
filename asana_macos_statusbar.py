from asana import Client
import rumps

from asana_api import AsanaClient
from macos import macos_app, get_task_name_updater

token = ''
section_id = ''
client = AsanaClient(token, section_id='1122582230576767')


rumps.Timer(get_task_name_updater(client), 60).start()
macos_app.run()