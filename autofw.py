#coding=utf-8
import itchat,json,sys,time
from itchat.content import *

if len(sys.argv) == 2:
    forward_user_name = sys.argv[1]
else:
    forward_user_name = '啊哈'

def replace_html(s):
    s = s.replace('&quot;','"')
    s = s.replace('&amp;','&')
    s = s.replace('&lt;','<')
    s = s.replace('&gt;','>')
    s = s.replace('&nbsp;',' ')
    return s

def get_msg_time(longtime):
    #转换成localtime
    time_local = time.localtime(longtime)
    #转换成新的时间格式(2016-05-05 20:28:54)
    return time.strftime("%Y-%m-%d %H:%M:%S",time_local)


@itchat.msg_register([TEXT, SHARING])
def text_reply(msg):
    #print msg
    if msg['Type'] == TEXT:
        forward_user.send('%s: %s' % (msg['User'].NickName, msg['Text']))
        print ('[%s][%s][%s]' % (get_msg_time(msg['CreateTime']), msg['User'].NickName, msg['Text']))

    if msg['Type'] == SHARING:
        forward_user.send('%s: %s\n%s' % (msg['User'].NickName, msg['Text'], replace_html(msg['Url'])))
        print ('[%s][%s][%s][%s]' % (get_msg_time(msg['CreateTime']), msg['User'].NickName, msg['Text'], replace_html(msg['Url'])))

@itchat.msg_register([TEXT, SHARING],isGroupChat=True)
def group_reply_text(msg):
    #res_data=json.dumps(msg,ensure_ascii=False,encoding="gb2312")
    #print msg
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']
    
    groupname = msg['User']['NickName']

    if msg['Type'] == TEXT:
        content = msg['Content']
    elif msg['Type'] == SHARING:
        content = msg['Text']
    if msg['Type'] == TEXT:
        forward_user.send('[%s][%s]\n%s' % (groupname, username, msg['Content']))
        print ('[%s][%s][%s][%s]' % (get_msg_time(msg['CreateTime']), groupname, username, msg['Content']))
    elif msg['Type'] == SHARING:
        forward_user.send('[%s][%s]\n%s\n%s' % (groupname, username, msg['Text'], replace_html(msg['Url'])))
        print ('[%s][%s][%s][%s][%s]' % (get_msg_time(msg['CreateTime']), groupname, username, msg['Text'], replace_html(msg['Url'])))


# 使用热启动
itchat.auto_login(hotReload=True,enableCmdQR=2)

print forward_user_name

forward_user=itchat.search_friends(name=unicode(forward_user_name,'utf-8'))[0]

itchat.run()
