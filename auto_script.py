import os
import datetime
import urllib
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bem.settings')

import django
django.setup()

from django.core.files import File
from windows.models import *

LEVEL = ['Newbie', 'Junior', 'Senior', 'Expert', 'Supervisor', 'Lead', 'Producer', 'Designer']
TEAM = ['World At Arms', 'City Mania', 'Modern Combat 5', 'Asphalt 8', 'R&D', 'Cross']
MEMBERS = [
    {
        'username': 'hop.duongthanh', 'name': 'Duong Thanh Hop', 'city': 'Quang Ngai', 'level': 'Supervisor', 'team': 'Asphalt 8', 'phone': '01694122063', 'skype': 'hop.duongthanh', 'starting': '03042013', 'birth': '02011990'
    },
    {
        'username': 'tu.nguyenvan','name': 'Nguyen Van Tu', 'city': 'Binh Dinh', 'level': 'Producer', 'team': 'Cross', 'phone': '0935900105', 'skype': 'n_v_tu', 'starting': '30092009', 'birth': '08021987'
    },
    {
        'username': 'tien.hoangdanh','name': 'Hoang Danh Tien', 'city': 'Nghe An', 'level': 'Producer', 'team': 'Asphalt 8', 'phone': '0905574281', 'skype': 'tien.hd', 'starting': '14062010', 'birth': '25101981'
    },
    {
        'username': 'son.phamthanh','name': 'Pham Thanh Son', 'city': 'Ha Noi', 'level': 'Producer', 'team': 'City Mania', 'phone': '0969587684', 'skype': 'sonthpham', 'starting': '11072016', 'birth': '18041985'
    },
    {
        'username': 'duc.luuminh','name': 'Luu Minh Duc', 'city': 'Da Nang', 'level': 'Producer', 'team': 'Modern Combat 5', 'phone': '01626817882', 'skype': 'venom002312', 'starting': '01032016', 'birth': '23121993'
    },
    {
        'username': 'tam.nguyenhoang3','name': 'Nguyen Hoang Tam', 'city': 'Da Nang', 'level': 'Lead', 'team': 'Cross', 'phone': '0937190188', 'skype': 'nguyenhoangtam3', 'starting': '15082011', 'birth': '19011988'
    },
    {
        'username': 'tan.tudinh','name': 'Tu Dinh Tan', 'city': 'Quang Ngai', 'level': 'Lead', 'team': 'Cross', 'phone': '0972016316', 'skype': 'tdtanvn', 'starting': '08022011', 'birth': '20041988'
    },
    {
        'username': 'trung.ngothanh','name': 'Ngo Thanh Trung', 'city': 'Quang Nam', 'level': 'Supervisor', 'team': 'Modern Combat 5', 'phone': '0935211468', 'skype': 'trung.ngothanh@gameloft.com', 'starting': '28092010', 'birth': '29121988'
    },
    {
        'username': 'son.lequangquoc','name': 'Le Quang Quoc Son', 'city': 'Da Nang', 'level': 'Supervisor', 'team': 'City Mania', 'phone': '0932441828', 'skype': 'dungke2005', 'starting': '18082010', 'birth': '04011987'
    },
    {
        'username': 'binh.huynhvan','name': 'Huynh Van Binh', 'city': 'Da Nang', 'level': 'Supervisor', 'team': 'World At Arms', 'phone': '0905095104', 'skype': 'vanbinh07t', 'starting': '01072011', 'birth': '15111989'
    },
    {
        'username': 'son.lehong','name': 'Le Hong Son', 'city': 'Quang Nam', 'level': 'Expert', 'team': 'Cross', 'phone': '01657986814', 'skype': 'bunhinrom.nbk', 'starting': '10062014', 'birth': '18041992'
    },
    {
        'username': 'nam.tranhuu','name': 'Tran Huu Nam', 'city': 'Da Nang', 'level': 'Senior', 'team': 'City Mania', 'phone': '0905952586', 'skype': 'huunamnhs', 'starting': '29072010', 'birth': '25111986'
    },
    {
        'username': 'thanh.truongquang2','name': 'Truong Quang Thanh', 'city': 'Quang Nam', 'level': 'Senior', 'team': 'R&D', 'phone': '01656024017', 'skype': 'mrchjng', 'starting': '25022011', 'birth': '02021988'
    },
    {
        'username': 'trieu.trandinh','name': 'Tran Dinh Trieu', 'city': 'Hue', 'level': 'Senior', 'team': 'Modern Combat 5', 'phone': '01656024017', 'skype': 'dinhtrieu08t4', 'starting': '03042013', 'birth': '01011990'
    },
    {
        'username': 'nin.nguyendong','name': 'Nguyen Dong Nin', 'city': 'Hue', 'level': 'Senior', 'team': 'Asphalt 8', 'phone': '01675089837', 'skype': 'nguyendongnin', 'starting': '14102014', 'birth': '02091990'
    },
    {
        'username': 'hoang.truongquoc','name': 'Truong Quoc Hoang', 'city': 'Quang Binh', 'level': 'Senior', 'team': 'World At Arms', 'phone': '0943210767', 'skype': 'h7starlight', 'starting': '13012015', 'birth': '01101990'
    },
    {
        'username': 'an.nguyenlethien','name': 'Nguyen Le Thien An', 'city': 'Da Nang', 'level': 'Junior', 'team': 'Asphalt 8', 'phone': '01274447177', 'skype': 'thienan092', 'starting': '26032015', 'birth': '29081992'
    },
    {
        'username': 'bao.phanhuynh','name': 'Phan Huynh Bao', 'city': 'Da Nang', 'level': 'Junior', 'team': 'World At Arms', 'phone': '0983824818', 'skype': 'huynhbaoph', 'starting': '04112013', 'birth': '27121984'
    },
    {
        'username': 'vi.nguyenquochoang','name': 'Nguyen Quoc Hoang Vi', 'city': 'Quang Nam', 'level': 'Junior', 'team': 'Modern Combat 5', 'phone': '01644771901', 'skype': 'gameloft.vi.nguyenquochoang', 'starting': '12082013', 'birth': '28021985'
    },
    {
        'username': 'chung.levan2','name': 'Le Van Chung', 'city': 'Hue', 'level': 'Junior', 'team': 'Asphalt 8', 'phone': '01668676454', 'skype': 'chunglv_1', 'starting': '14102014', 'birth': '05111991'
    },
    {
        'username': 'tu.daoanh2','name': 'Dao Anh Tu', 'city': 'Dak Lak', 'level': 'Junior', 'team': 'Modern Combat 5', 'phone': '01685136239', 'skype': 'anhtu250393', 'starting': '21032016', 'birth': '25031993'
    },
    {
        'username': 'nghia.tukhac','name': 'Tu Khac Nghia', 'city': 'Phu Yen', 'level': 'Junior', 'team': 'City Mania', 'phone': '01288352874', 'skype': 'khacnghia1890', 'starting': '05042016', 'birth': '01081990'
    },
    {
        'username': 'viet.lethai','name': 'Le Thai Viet', 'city': 'Da Nang', 'level': 'Junior', 'team': 'World At Arms', 'phone': '01285883609', 'skype': 'vietle922', 'starting': '01032016', 'birth': '28071992'
    },
    {
        'username': 'huong.tieudinh','name': 'Tieu Dinh Huong', 'city': 'Da Nang', 'level': 'Newbie', 'team': 'R&D', 'phone': '01282115101', 'skype': 'tieudinhhuong@gmail.com', 'starting': '19092016', 'birth': '11061995'
    },
    {
        'username': 'cong.nguyentrong','name': 'Nguyen Trong Cong', 'city': 'Kon Tum', 'level': 'Junior', 'team': 'City Mania', 'phone': '090258940', 'skype': 'congtrong.ntc@gmail.com', 'starting': '19092016', 'birth': '28021995'
    },
    {
        'username': 'hau.nguyencong','name': 'Nguyen Cong Hau', 'city': 'Quang Nam', 'level': 'Newbie', 'team': 'City Mania', 'phone': '01658949152', 'skype': 'nguyenconghau188@gmail.com', 'starting': '19092016', 'birth': '18081993'
    },
    {
        'username': 'vu.nguyenchiemminh','name': 'Nguyen Chiem Minh Vu', 'city': 'Hue', 'level': 'Newbie', 'team': 'Modern Combat 5', 'phone': '0934359954', 'skype': 'minh_vu_03', 'starting': '14122016', 'birth': '15101992'
    },
    {
        'username': 'dung.dangthikim','name': 'Dang Thi Kim Dung', 'city': 'Da Nang', 'level': 'Newbie', 'team': 'World At Arms', 'phone': '01653408887', 'skype': 'nuinui160', 'starting': '14122016', 'birth': '26071994'
    },
    {
        'username': 'tri.nguyenthanhminh','name': 'Nguyen Thanh Minh Tri', 'city': 'Da Nang', 'level': 'Designer', 'team': 'City Mania', 'phone': '0935214119', 'skype': 'dreamer.zzzzz', 'starting': '20042010', 'birth': '10051990'
    },
    {
        'username': 'lan.nguyenthe2', 'name': 'Nguyen The Lan', 'city': 'Da Nang', 'level': 'Designer',
        'team': 'Asphalt 8', 'phone': '0905860087', 'skype': 'lannguyen2510', 'starting': '29092011',
        'birth': '25101987'
    },
    {
        'username': 'thuan.thachgia', 'name': 'Thach Gia Thuan', 'city': 'Da Nang', 'level': 'Designer',
        'team': 'Modern Combat 5', 'phone': '01266582909', 'skype': 'thach.thuan2', 'starting': '25082014',
        'birth': '16091991'
    },
    {
        'username': 'tung.buileson', 'name': 'Bui Le Son Tung', 'city': 'Da Nang', 'level': 'Newbie',
        'team': 'Asphalt 8', 'phone': '0905280693', 'skype': 'tungten28693', 'starting': '27022017',
        'birth': '28061993'
    },
    {
        'username': 'trung.trancao', 'name': 'Tran Cao Trung', 'city': 'Da Nang', 'level': 'Newbie',
        'team': 'World At Arms', 'phone': '0905729459', 'skype': 'caotrung4691@gmail.com', 'starting': '27022017',
        'birth': '04061991'
    },
    {
        'username': 'hue.buithikim', 'name': 'Bui Thi Kim Hue', 'city': 'Quang Binh', 'level': 'Junior',
        'team': 'City Mania', 'phone': '0982998160', 'skype': 'kimhue2010@live.com', 'starting': '20042010',
        'birth': '03021987'
    },
    {
        'username': 'ca.tranngoc', 'name': 'Tran Ngoc Ca', 'city': 'Quang Nam', 'level': 'Newbie',
        'team': 'Asphalt 8', 'phone': '0938946895', 'skype': 'tng_ca', 'starting': '19092016',
        'birth': '30031993'
    },
    {
        'username': 'thien.tatruongminh', 'name': 'Ta Truong Minh Thien', 'city': 'Khanh Hoa', 'level': 'Newbie',
        'team': 'Asphalt 8', 'phone': '0908880747', 'skype': 'thienttm88', 'starting': '17042017',
        'birth': '21061988'
    },
    {
        'username': 'anh.phanhung', 'name': 'Phan Hung Anh', 'city': 'Da Nang', 'level': 'Newbie',
        'team': 'Modern Combat 5', 'phone': '0935000425', 'skype': 'hunganhphan@gmail.com', 'starting': '27022017',
        'birth': '10061984'
    },
    {
        'username': 'tuan.lamvan', 'name': 'Lam Van Tuan', 'city': 'Da Nang', 'level': 'Newbie',
        'team': 'City Mania', 'phone': '01202301474', 'skype': 'tuan.lam93', 'starting': '22032017',
        'birth': '15101992'
    },
]

IMAGE_PATH = 'images/'

def AddTeam(name):
    t = Team.objects.get_or_create(name=name)[0]
    t.name = name
    t.save()
    return t

def AddLevel(level):
    l = Level.objects.get_or_create(level=level)[0]
    l.level = level
    l.save()
    return l

def AddDeveloper(user, data):
    try:
        d = Developer.objects.get(user=user)
    except Developer.DoesNotExist:
        d = Developer(user=user)
    d.name = data['name']
    d.city = data['city']
    d.team = AddTeam(data['team'])
    d.level = AddLevel(data['level'])
    d.phone = data['phone']
    d.skype = data['skype']
    d.start = datetime.datetime.strptime(data['starting'], "%d%m%Y").date()
    d.birth = datetime.datetime.strptime(data['birth'], "%d%m%Y").date()
    # d.image.save(
    #     data['username'] + '.png',
    #     File(open(urllib.urlretrieve(IMAGE_PATH + 'test.png')[0], 'rb'))
    # )
    d.save()

def AddUser(user):
    u = User.objects.get_or_create(username=user['username'])[0]
    u.set_password('gameloft')
    u.email = user['username'] + '@gameloft.com'
    u.first_name = user['name'][user['name'].rfind(' ') + 1:]
    u.last_name = user['name'][user['name'].find(' ')]
    u.is_staff = True
    if (user['level'] == 'Lead' or user['level'] == 'Supervisor' or user['level'] == 'Producer'):
        u.is_superuser = True
    u.save()
    AddDeveloper(u, user)

def CalculateScore():
    best_score = 0
    for bem in Bem.objects.all():
        bem.score = 0
        if bem.vote is not None:
            for dev in bem.vote.users.all():
                if dev.user.is_superuser:
                    bem.score += 1.0
                else:
                    bem.score += 0.5
                dev.vote_team = False
                dev.vote_count = 0
                dev.save()
        if best_score < bem.score:
            best_score = bem.score
        bem.save()
    for bem in Bem.objects.all():
        if bem.score == best_score:
            bem.is_best = True
        bem.expired = True
        bem.save()

if __name__ == '__main__':
    print 'Starting setup scripts...'
    # for user in MEMBERS:
    #     AddUser(user)
    CalculateScore()
    print 'Done!!!'