import time
from fastapi import Response
import xml.etree.ElementTree as Et
from lxml import etree
import os
import logging

# 日志
logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.INFO)


# Command constants
COMMAND_NEWCOMER_TEXT = "谢谢关注！！！ \n 发送指令：\n   验证码:可以获取网页验证码，验证码时效为1个小时!"
COMMAND_HELP = "帮助"
COMMAND_GET_VERIFICATION_CODE = "验证码"

# WeChat help dictionary
WECHAT_HELP = {
    COMMAND_HELP: "调出帮助菜单",
    COMMAND_GET_VERIFICATION_CODE: "获取一个chatgpt的验证码，持续时间"
}


class WeChatOAHandler:
    def __init__(self, xml_data, code):
        self.parse_xml = Et.fromstring(xml_data)
        self.xml_data = etree.fromstring(xml_data)
        self.ToUserName = self.parse_xml.find('ToUserName').text
        self.FromUserName = self.parse_xml.find('FromUserName').text
        self.CreateTime = self.parse_xml.find('CreateTime').text
        self.MsgType = self.parse_xml.find('MsgType').text
        self.code = code

    def handle(self):
        if self.is_event_type():
            return self.send_msg(COMMAND_NEWCOMER_TEXT)

        if self.is_text_type():
            user_msg = self.get_user_msg()
            if self.is_get_verification_code(user_msg):
                logging.info("self.is_get_verification_code")
                return self.get_verification_code()
        # 没得说了 就回复这个    
        return self.send_msg("感谢关注~~~")

    def is_text_type(self):
        return self.MsgType == 'text'

    def get_user_msg(self):
        return self.xml_data[4].text

    def is_event_type(self):
        return self.MsgType == 'event'

    def is_get_verification_code(self, msg):
        return msg.startswith(COMMAND_GET_VERIFICATION_CODE)

    def get_verification_code(self):
        try:
            return self.send_msg(self.code)
        except:
            return self.send_msg("获取验证码失败...")

    def send_msg_type(self, content):
        current_time = int(time.time())
        message = f"""
            <xml>
            <ToUserName><![CDATA[{self.FromUserName}]]></ToUserName>
            <FromUserName><![CDATA[{self.ToUserName}]]></FromUserName>
            <CreateTime>{current_time}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{content}]]></Content>
            </xml>
        """
        return message

    def send_msg(self, content):
        try:
            message = self.send_msg_type(content)
            return Response(message, media_type="application/xml")
        except Exception:
            logging.info("send_msg Exception")
            return Response('success')
