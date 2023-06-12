import requests
import json


class Lolicon:
    def __init__(self, tag):
        self.tag = tag
        
    def get_image_from_lolicon(self):
        url = "https://api.lolicon.app/setu/v2"
        headers = {"Content-Type": "application/json"}
        data = {"tag": [self.process_tag()]}
        res = requests.post(url, headers=headers, data=json.dumps(data))
        if res.status_code == 200:
            res_text = json.loads(res.text)
            res_url = res_text["data"][0]["urls"]['original']
            res_title = res_text["data"][0]["title"]
            res_tags = ", ".join(res_text["data"][0]["tags"])
            return res_url, res_title, res_tags
        return False

    def process_tag(self):
        tag_list = []
        tag_data = self.tag[5:].replace("\n", "").split(",")
        first_tag, second_tag = [tag.split(" ") for tag in tag_data]
        tag_list.extend([tag for tag in first_tag if tag])
        tag_list.extend([tag for tag in second_tag if tag])
        return tag_list


