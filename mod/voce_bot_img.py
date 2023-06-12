from mod.connect_lolicon import *
from config import *


class ImageHandler:
    def __init__(self, data):
        self.data = data
        self.user_id = str(self.data.from_uid)
        self.created_at = self.data.created_at
        self.target_gid = self.data.target.gid
        self.msg = self.data.detail.content

    def handle(self):
        if self.is_msg_from_susan():
            msg = self.get_data_from_loli()
            return self.send_to_voce_bot(msg)
        return

    def is_msg_from_susan(self):
        return self.msg.startswith(" @21")
    
    def get_data_from_loli(self):
        get_url, get_title, get_tags = Lolicon(self.msg).get_image_from_lolicon()
        msg = f"### {get_title} \n  {get_tags};\n![](get_url)"
        return msg
        
    def send_to_voce_bot(self, message):
        headers = {'content-type': "text/markdown", 'x-api-key': Settings.VoceChat['bot']['key']}
        url = f"{Settings.VoceChat['url']}/api/bot/send_to_group/1"
        requests.post(url=url, headers=headers, data=message.encode('utf-8'))


if __name__ == "__main__":
    print("")
