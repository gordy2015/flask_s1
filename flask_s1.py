from flask import Flask,url_for,request,render_template,g,redirect
import json,os,sqlite3,datetime
from flask_sqlalchemy import SQLAlchemy
# from exts import db
from models import db,Appointment,Ptime,Service_type,Appoint_ser
from exts import randomnum
import config
from xml.etree import ElementTree
from urllib.request import urlopen
from wxconfig import Wxinfo

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
# with app.app_context():
#     db.create_all()
Wxcon = Wxinfo()

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'GET':
        echostr = request.args.get('echostr')
        ha = hasattr(Wxcon, 'appid')
        hs = hasattr(Wxcon, 'secret')
        if ha and hs:
            a = getattr(Wxcon, 'appid')
            s = getattr(Wxcon, 'secret')
            rh = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'.format(appid=a, secret=s)
            a = urlopen(rh).read().decode('utf-8')
            print(a)
        if echostr:
            return echostr
        else:
            return 'success'
    elif request.method == 'POST':
        data = request.get_data()
        xml = ElementTree.fromstring(data)
        print('data:%s; xml:%s'%(data,xml))  #type(request.data) : byte类型
        MsgType = xml.findtext('.//MsgType')
        ToUserName = xml.findtext('.//ToUserName')
        FromUserName = xml.findtext('.//FromUserName')
        CreateTime = xml.findtext('.//CreateTime')
        MsgId = xml.findtext('.//MsgId')
        print(MsgType)
        if MsgType == 'text':
            Content = xml.findtext('.//Content')
            print(ToUserName, FromUserName, CreateTime, MsgId, Content)
            if '你是谁' in Content:
                return render_template('wxinfo.html',
                                ToUserName=ToUserName,
                                FromUserName=FromUserName,
                                CreateTime=CreateTime,
                                Content='对，我就是你老板')
            if '收到不支持的消息类型' in Content:
                return render_template('wxinfo.html',
                                       ToUserName=ToUserName,
                                       FromUserName=FromUserName,
                                       CreateTime=CreateTime,
                                       Content='用文字表达，好吗')
            else:
                return render_template('wxinfo.html',
                                       ToUserName=ToUserName,
                                       FromUserName=FromUserName,
                                       CreateTime=CreateTime,
                                       Content=Content)
        elif MsgType == 'image':
            MediaId = xml.findtext('.//MediaId')
            print(MediaId)
            Content = '小样，不要斗图好吗，流量党伤不起'
            return render_template('wxinfo.html',
                                       ToUserName=ToUserName,
                                       FromUserName=FromUserName,
                                       CreateTime=CreateTime,
                                       Content=Content)
        elif MsgType == 'voice':
            MediaId = xml.findtext('.//MediaId')
            print(MediaId)
            Content = '小样，你发的是语音，哥睡觉时再听'
            return render_template('wxinfo.html',
                                   ToUserName=ToUserName,
                                   FromUserName=FromUserName,
                                   CreateTime=CreateTime,
                                   Content=Content)
        else:
            MediaId = xml.findtext('.//MediaId')
            print(MediaId)
            Content = '小样，别玩了，早点睡觉吧'
            return render_template('wxinfo.html',
                                   ToUserName=ToUserName,
                                   FromUserName=FromUserName,
                                   CreateTime=CreateTime,
                                   Content=Content)



@app.route('/appointment', methods=['GET','POST'])
def appointment():
    if request.method == 'GET':
        st = Service_type.query.filter().all()
        pt = Ptime.query.filter().all()
        today_date = datetime.date.today().strftime("%Y-%m-%d")
        wh = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={rurl}&response_type=code&scope={scope}&state=987#wechat_redirect'.format(appid=Wxcon.appid,rurl=Wxcon.url,scope='snsapi_base')
        # print(request.args)
        if request.args.get('code'):
            c = request.args.get('code')
            print('code is: %s' %c)
        else:
            print('no get code')
            return redirect(wh)
        return render_template('appointment.html',st=st,pt=pt, today_date=today_date)

@app.route('/add_appointment', methods=['GET','POST'])
def add_appointment():
    if request.method == 'POST':
        ret = {'status': True, 'info': 'None', 'data': None}
        try:
            u = request.form.get('user')
            p = request.form.get('phone')
            a = request.form.get('address')
            n = request.form.get('note')
            s = request.form.getlist('service_type')
            t = request.form.get('time')
            ad = request.form.get('appointment_date')
            if u and p and a and s:
                print(u, p, a, n, s, t,ad,type(ad))
                inp = "user={u},phone={p},address={a},note={n},pt_id={t}".format(u=u,p=p,a=a,n=n,t=t)
                print(inp)
                l = ad.replace("-","")
                curr_date = datetime.date.today().strftime("%Y-%m-%d")
                if int(l) < int(curr_date.replace("-","")):
                    ret['status'] = False
                    ret['info'] = '选择的日期最早是今天{date}'.format(date=curr_date)
                    # q = Appointment.query.filter(Appointment.user == u, Appointment.phone == p,Appointment.address==a,
                    #                                    Appointment.note==n, Appointment.pt_id==t).all()
                    # if q:
                    #     ret['status'] = False
                    #     ret['info'] = '您已预约过了'
                else:
                    r_num = randomnum()
                    ins = Appointment(user=u,phone=p,address=a,note=n,pt_id=t, appoint_num=r_num, appoint_date=ad)
                    db.session.add(ins)
                    db.session.commit()
                    q = Appointment.query.filter(Appointment.user == u, Appointment.phone == p,Appointment.address==a,
                                                   Appointment.note==n, Appointment.pt_id==t).all()
                    for i in q:
                        aid = i.id
                    for i in s:
                        w = Appoint_ser(st_id=i,appoint_id=aid,appoint_num=r_num)
                        db.session.add(w)
                        db.session.commit()
                    ret['status'] = True
                    ret['info'] = '预约成功，您的预约号为{r_num}'.format(r_num=r_num)
            else:
                ret['status'] = False
                ret['info'] = '输入内容不能为空'
        except Exception as e:
            print('-----------ERROR: %s-------'%e)
            ret['status'] = False
            ret['info'] = 'request error'
        return json.dumps(ret)

@app.route('/check_appointment', methods=['GET','POST'])
def check_appointment():
    m = Appoint_ser.query.filter().all()
    appointment = Appointment.query.filter().all()
    return render_template('check_appointment.html',m=m,appointment=appointment)

@app.route('/user_check_appointment', methods=['GET','POST'])
def user_check_appointment():
    if request.method == 'GET':
        return render_template('user_check_appointment.html')
    elif request.method == 'POST':
        ret = {'status': True, 'info': 'None', 'data': None}
        try:
            p = request.form.get('phone')
            num = request.form.get('anumber')
            fresult = True
            if p:
                if len(p) != 11:
                    fresult = False
                    ret['info'] = '查询失败，请输入11位手机号码'
                else:
                    n = Appointment.query.filter(Appointment.phone == p).all()
                    print(n)
                    if n: #手机号码可以预约多个单，所以如果查询到的手机号码是预约了多个单需要列出这个手机号码所有的单
                        qr = []
                        tresult = []
                        for i in n:
                            u = i.user
                            nu = i.appoint_num
                            a = i.address
                            n = i.note
                            t = i.pt_appoint.appointment_time
                            ad = i.appoint_date
                            print(u,nu,a,n,t,ad)
                            q = Appoint_ser.query.filter(Appoint_ser.appoint_num == nu).all()
                            rnum = nu
                            for row in q:
                                s = row.st_a.name
                                qr.append(s)
                            presult = '您的预约编号是:{r_num},姓名:{user},电话:{phone},地址:{address},备注:{note},服务类型:{service_type},预约时间段:{appoint_date}'.format(
                                r_num=rnum, service_type=qr,user=u, phone=p, address=a, note=n, appoint_date=ad + ' ' + t)
                            # print('PRESULT:%s'%presult)
                            tresult.append(presult)

                    else:
                        fresult = False
                        ret['info'] = '查询失败，手机号码不存在'

            elif num:  #预约编号是唯一的
                if len(num) != 16:
                    fresult = False
                    ret['info'] = '查询失败，请输入16位预约编号'
                else:
                    n = Appointment.query.filter(Appointment.appoint_num == num).all()
                    if n:
                        qr = []
                        tresult = []
                        for i in n:
                            u = i.user
                            p = i.phone
                            a = i.address
                            n = i.note
                            t = i.pt_appoint.appointment_time
                            ad = i.appoint_date
                            q = Appoint_ser.query.filter(Appoint_ser.appoint_num==num).all()
                            rnum = num
                            for row in q:
                                s = row.st_a.name
                                qr.append(s)
                            presult = '您的预约编号是:{r_num},姓名:{user},电话:{phone},地址:{address},备注:{note},服务类型:{service_type},预约时间段:{appoint_date}'.format(
                                r_num=rnum, service_type=qr, user=u, phone=p, address=a, note=n,appoint_date=ad + ' ' + t)
                            tresult.append(presult)
                    else:
                        fresult = False
                        ret['info'] = '查询失败，预约编号不存在'
            else:
                fresult = False
                ret['info'] = '查询失败，请输入手机号码或者预约编号'

            if fresult:
                ret['status'] = True
                ret['info'] = tresult
            else:
                ret['status'] = False
        except Exception:
            print('-----------ERROR: %s-------'%e)
            ret['stus'] = False
            ret['info'] = '请求错误'
        return json.dumps(ret)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
