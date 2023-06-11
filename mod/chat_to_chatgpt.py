


class Chatbot:
    def __init__(self, codes):
        self.codes = codes

    async def chat(self, item):
        current_time = int(datetime.now().timestamp())
        logging.info(f"{item['messages']['code']}提问：{item['messages']['content'][-1]['content']}")
        for code in self.codes:
            if code.code == item["messages"]["code"] and code.expire_time > current_time:
                ans = send_msg_to_openai(item["messages"]["content"])
                return {"content": ans}
        return "false"
