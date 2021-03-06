# -*- coding: utf-8 -*-
#V1.3版本，更加智能化，更好的基于jira所提供的api进行自动化提醒，可移植性更强,Project参数不需要了

from jira import JIRA
import smtplib,sys
import  json,urllib
import time,datetime,random

jira = JIRA('JIRA网址', basic_auth=('usr','password'))


appkey = "563d9910adfc08142399f0e5497cc482"                                 #笑话用接口
                                                                            # 项目名
Group = JIRA.group_members(jira,"ERP")
Groups = sorted(Group.items())                                              #将字典转为元组形式访问，字典无法直接调用第某个参数
Email_Address = [0 for i in range(len(Group))]                              #INIT这里是人数
Sleep_Time = 600                                                            #休眠时间

def Run_Task():
    title = "今日提醒"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(title)
    for i in range(len(Group)):
        k = 0
        iss = jira.search_issues('status in (待处理, Reopened, "in progress") AND assignee in ('+Groups[i][0]+")" )
        for j in iss:
            if(Email_Address[i] == 0):
                Email_Address[i] = j.fields.assignee.emailAddress

    for i in range(len(Group)):
        if (Email_Address[i] != 0):
            try:
                Send_Email(Groups[i][0])
            except  Exception as e:
                print (e,"发送到"+Groups[i][0]+"的邮件发送失败！")

def Daily_Project_High():
    flag = False
    if  datetime.datetime.isoweekday(datetime.datetime.now()) <=5:
        flag = True
        nums = 0
    while flag:
        nums = nums+1
        print("  ● 提醒时间（高频率）：工作日的 8:40,10:30,11:30,14:10,15:30,17:30 )程序已执行"+str(nums)+"次")
        print("现在是："+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        year = datetime.date.today().year
        month = datetime.date.today().month
        day = datetime.date.today().day

        fst_remind = datetime.datetime(year, month, day, 8, 40, 00)
        snd_remind = datetime.datetime(year, month, day, 10, 30, 00)
        trd_remind = datetime.datetime(year, month, day, 11, 30, 00)
        fth_remind = datetime.datetime(year, month, day, 14, 10, 00)
        sth_remind = datetime.datetime(year, month, day, 15, 30, 00)
        sev_remind = datetime.datetime(year, month, day, 17, 30, 00)
        before_sleep = datetime.datetime.now()
        time.sleep(Sleep_Time)
        after_sleep = datetime.datetime.now()
        if (before_sleep - fst_remind).total_seconds() <= 0 and (after_sleep - fst_remind).total_seconds() >= 0:
            Run_Task()
        elif (before_sleep - snd_remind).total_seconds() <= 0 and (after_sleep - snd_remind).total_seconds() >= 0:
            Run_Task()
        elif (before_sleep - trd_remind).total_seconds() <= 0 and (after_sleep - trd_remind).total_seconds() >= 0:
            Run_Task()
        elif (before_sleep - fth_remind).total_seconds() <= 0 and (after_sleep - fth_remind).total_seconds() >= 0:
            Run_Task()
        elif (before_sleep - sth_remind).total_seconds() <= 0 and (after_sleep - sth_remind).total_seconds() >= 0:
            Run_Task()
        elif (before_sleep - sev_remind).total_seconds() <= 0 and (after_sleep - sev_remind).total_seconds() >= 0:
            Run_Task()
        if datetime.datetime.isoweekday(datetime.datetime.now()) >5:
            time.sleep(86400)                   #检测到此时是周六 自动休眠两天


def Daily_Project_Low():
    flag = False
    if  datetime.datetime.isoweekday(datetime.datetime.now()) <=5:
        flag = True
        nums = 0
    while flag:
        nums = nums+1
        print("  ● 提醒时间（低频率）：工作日的 8:40,11:00,14:30,17:00 程序已执行"+str(nums)+"次")
        print("现在是："+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        year = datetime.date.today().year
        month = datetime.date.today().month
        day = datetime.date.today().day

        fst_remind = datetime.datetime(year, month, day, 8, 40, 00)
        trd_remind = datetime.datetime(year, month, day, 11, 00, 00)
        fth_remind = datetime.datetime(year, month, day, 14, 30, 00)
        sev_remind = datetime.datetime(year, month, day, 17, 00, 00)

        before_sleep = datetime.datetime.now()
        time.sleep(Sleep_Time)
        after_sleep = datetime.datetime.now()
        if (before_sleep - fst_remind).total_seconds() <= 0 and (after_sleep - fst_remind).total_seconds() >= 0:  # 8:40
            Run_Task()
        elif (before_sleep - trd_remind).total_seconds() <= 0 and (
            after_sleep - trd_remind).total_seconds() >= 0:  # 11:30
            Run_Task()
        elif (before_sleep - fth_remind).total_seconds() <= 0 and (
            after_sleep - fth_remind).total_seconds() >= 0:  # 14:10
            Run_Task()
        elif (before_sleep - sev_remind).total_seconds() <= 0 and (
            after_sleep - sev_remind).total_seconds() >= 0:  # 17:30
            Run_Task()
        if datetime.datetime.isoweekday(datetime.datetime.now()) >5:
            time.sleep(86400)                   #检测到此时是周末 自动休眠两天

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def Send_Email(Name):
    iss = jira.search_issues('status in (待处理, Reopened, "in progress") AND assignee in (' + Name + ') ORDER BY summary ASC')
    k=0
    html =\
        """
        <html>
            <body>
                <style>
                    table {
                            border-radius: 5px 5px 3px 2px / 5px 5px 1px 3px;
                            
                        }
                        
                    table th,table td { font-size:11px; }
                </style>
                <table  id="issuetable" valign= "top" border=1 cellspacing=0>
                    <tr>
                        <th>关键字</th>
                        <th>主题</th>
                        <th>报告人</th>
                        <th>经办人</th>
                        <th>优先级</th>
                        <th>状态</th>
                        <th>创建日期</th>
                        <th>更新日期</th>
                    </tr>
        """
    for j in iss:
        k=k+1

        htmltemp = """<tr>
                      <td>"""+j.key+"""</td>
                      <td align = "center"><a href="http://132.37.3.100:9090/browse/"""+j.key+"""">"""+j.fields.summary+"""</a></td>
                      <td align="center">"""+j.fields.creator.displayName+"""</td>
                      <td align="center">"""+j.fields.assignee.displayName+"""</td>
                      <td align="center">"""+j.fields.priority.name+""" </td>
                      <td>"""+j.fields.status.name+"""</td>
                      <td>"""+j.fields.created[0:10]+"""</td>
                      <td>"""+j.fields.updated[0:10]+"""</td>

                    </tr>"""

        html =html + htmltemp
    html += """
                </table><HR style="FILTER: alpha(opacity=100,finishopacity=0,style=3)" width="100%" color=#987cb9 SIZE=3>
                <em align = "center">高强度工作挺久了，休息一下，喝口水，走一走</em>
                <div style="margin:10px auto"><img src="https://source.unsplash.com/random/800x600"></div>
                </body></html>
                """
    EmailAddress = j.fields.assignee.emailAddress
        #<br />"""+Joke(appkey,"GET")+""
    print(EmailAddress)
    _user = "usr"     #Email usrname like xxx@xx.com
    _pwd = "password" 
    _to = EmailAddress
    smtpserver = 'smtp.163.com'   #smtpsever
    msg = MIMEMultipart('alternative')
    msg["Subject"] = j.fields.assignee.displayName+'，你还有'+ str(k) +'个未完成任务，请及时处理【】'
    msg["From"]    = _user
    msg["To"]      = _to

    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    s = smtplib.SMTP()
    print("connect!")
    s.connect(smtpserver)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    print("successful")
    s.quit()

def Joke(Appkey,m = "GET"):
    url = "http://v.juhe.cn/joke/randJoke.php"
    params = {
        "type": "", #趣图或者文字
        "key": Appkey,
    }
    params = urllib.parse.urlencode(params)
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            Joke_Content = res["result"][0]["content"]
            # print(res["result"][0]["content"])
        else:
            Joke_Content = "笑话出现了点问题，明日再会！"

    return Joke_Content

if __name__ == '__main__':

#    Run_Task()
    if sys.argv[1] == "high":
        Daily_Project_High()
    else:
        Daily_Project_Low()
