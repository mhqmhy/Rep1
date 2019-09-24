# -*- coding: utf-8 -*-
import requests
import json
import re

municipality1 = ["北京市", "上海市", "天津市", "重庆市"]
municipality0 = ["北京", "上海", "天津", "重庆"]
province0 = ["山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "广东", "海南", "四川", "贵州", "云南",
             "陕西", "甘肃", "青海", "台湾", "河北", "湖南"]
province1 = ["山西省", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省", "广东省", "海南省", "四川省",
              "贵州省", "云南省", "陕西省", "甘肃省", "青海省", "台湾省", "河北省", "湖南省"]

province2 = ["内蒙古自治区", "广西壮族自治区", "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区", "香港特别行政区", "澳门特别行政区"]
city_ = ["石家庄市", "唐山市","秦皇岛市","邯郸市","邢台市","保定市","张家口市","承德市","沧州市","廊坊市","衡水市",
		 "太原市", "大同市", "阳泉市", "长治市", "晋城市", "朔州市", "晋中市", "运城市", "忻州市", "临汾市", "吕梁市",
		 "沈阳市","大连市","鞍山市","抚顺市","本溪市","丹东市","锦州市","营口市","阜新市","辽阳市","盘锦市","铁岭市","朝阳市","葫芦岛市",
		 "长春市","吉林市","四平市","辽源市","通化市","白山市","松原市","白城市","延边朝鲜族自治州",
				"郑州市","开封市","洛阳市","平顶山市","安阳市","鹤壁市","新乡市","焦作市","濮阳市","许昌市","漯河市","三门峡市","南阳市","商丘市","信阳市","周口市","驻马店市","济源市",
				"南京市","无锡市","徐州市","常州市","苏州市","南通市","连云港市","淮安市","盐城市","扬州市","镇江市","泰州市","宿迁市",
				"杭州市","宁波市","温州市","嘉兴市","湖州市","绍兴市","金华市","衢州市","舟山市","台州市","丽水市",
				"合肥市","芜湖市","蚌埠市","淮南市","马鞍山市","淮北市","铜陵市","安庆市","黄山市","滁州市","阜阳市","宿州市","巢湖市","六安市","亳州市","池州市","宣城市",
				"福州市","厦门市","莆田市","三明市","泉州市","漳州市","南平市","龙岩市","宁德市",
				"南昌市","景德镇市","萍乡市","九江市","新余市","鹰潭市","赣州市","吉安市","宜春市","抚州市","上饶市",
				"济南市","青岛市","淄博市","枣庄市","东营市","烟台市","潍坊市","威海市","济宁市","泰安市","日照市","莱芜市","临沂市","德州市","聊城市","滨州市","菏泽市",
				"武汉市","黄石市","襄樊市","十堰市","荆州市","宜昌市","荆门市","鄂州市","孝感市","黄冈市","咸宁市","随州市","恩施州","仙桃市","潜江市","天门市","神农架林区",
				"长沙市","株洲市","湘潭市","衡阳市","邵阳市","岳阳市","常德市","张家界市","益阳市","郴州市","永州市","怀化市","娄底市","湘西州",
				"广州市","深圳市","珠海市","汕头市","韶关市","佛山市","江门市","湛江市","茂名市","肇庆市","惠州市","梅州市","汕尾市","河源市","阳江市","清远市","东莞市","中山市","潮州市","揭阳市","云浮市",
				"海口市","龙华区","秀英区","琼山区","美兰区","三亚市",
				"成都市","自贡市","攀枝花市","泸州市","德阳市","绵阳市","广元市","遂宁市","内江市","乐山市","南充市","宜宾市","广安市","达州市","眉山市","雅安市","巴中市","资阳市","阿坝州","甘孜州","凉山州",
				"贵阳市","六盘水市","遵义市","安顺市","铜仁地区","毕节地区","黔西南州","黔东南州","黔南州",
				"昆明市","大理市","曲靖市","玉溪市","昭通市","楚雄市","红河市","文山市","思茅市","西双版纳市","保山市","德宏市","丽江市","怒江市","迪庆市","临沧市",
				"西安市","铜川市","宝鸡市","咸阳市","渭南市","延安市","汉中市","榆林市","安康市","商洛市",
				"兰州市","嘉峪关市","金昌市","白银市","天水市","武威市","张掖市","平凉市","酒泉市","庆阳市","定西市","陇南市","临夏州","甘南州",
				"西宁市","海东地区","海北州","黄南州","海南州","果洛州","玉树州","海西州",
				"哈尔滨市","齐齐哈尔市","鸡西市","鹤岗市","双鸭山市","大庆市","伊春市","佳木斯市","七台河市","牡丹江市","黑河市","绥化市","大兴安岭地区",
				"呼和浩特市","包头市","乌海市","赤峰市","通辽市","鄂尔多斯市","呼伦贝尔市","巴彦淖尔市","乌兰察布市","兴安盟","锡林郭勒盟","阿拉善盟",
				"南宁市","柳州市","桂林市","梧州市","北海市","防城港市","钦州市","贵港市","玉林市","百色市","贺州市","河池市","来宾市","崇左市",
				"拉萨市","昌都市","山南市","日喀则市","那曲市","阿里市","林芝市",
				"银川市","石嘴山市","吴忠市","固原市","中卫市",
				"乌鲁木齐市","克拉玛依市","吐鲁番市","哈密市","和田地区","阿克苏地区","喀什地区","克孜勒苏柯尔克孜自治州","巴音郭楞蒙古自治州","昌吉回族自治州","博尔塔拉蒙古自治州","伊犁哈萨克自治州","塔城地区","阿勒泰地区","石河子市","阿拉尔市","图木舒克市","五家渠市",
				"台北市","高雄市","基隆市","台中市","台南市","新竹市","嘉义市","台北县","宜兰县","桃园县","新竹县","苗栗县","台中县","彰化县","南投县","云林县","嘉义县","台南县","高雄县","屏东县","澎湖县","台东县","花莲县",
				"中西区","东区","九龙城区","观塘区","南区","深水埗区","黄大仙区","湾仔区","油尖旺区","离岛区","葵青区","北区","西贡区","沙田区","屯门区","大埔区","荃湾区","元朗区" ]
direc = ["晋州市",
       "遵化市",
       "武安市",
       "南宫市",
       "涿州市",
       "泊头市",
       "霸州市",
       "深州市",
       "新乐市",
       "平泉市",
       "迁安市",
       "沙河市",
       "安国市",
       "任丘市",
       "三河市",
       "辛集市",
       "定州市",
       "河间市",
       "高碑店市",
       "黄骅市古交市",
       "潞城市",
       "高平市",
       "原平市",
       "孝义市",
       "介休市",
       "侯马市",
       "河津市",
       "汾阳市",
       "霍州市",
       "永济市满洲里市",
       "霍林郭勒市",
       "丰镇市",
       "乌兰浩特市",
       "二连浩特市",
       "牙克石市",
       "扎兰屯市",
       "根河市",
       "额尔古纳市",
       "阿尔山市",
       "锡林浩特市",
       "新民市",
       "瓦房店市",
       "庄河市",
       "海城市",
       "东港市",
       "凤城市",
       "凌海市",
       "北镇市",
       "大石桥市",
       "盖州市",
       "灯塔市",
       "调兵山市",
       "开原市",
       "凌源市",
       "北票市",
       "兴城市",
       "德惠市",
       "榆树市",
       "舒兰市",
       "桦甸市",
       "蛟河市",
       "磐石市",
       "公主岭市",
       "双辽市",
       "梅河口市",
       "集安市",
       "临江市",
       "大安市",
       "洮南市",
       "扶余市",
       "延吉市",
       "图们市",
       "敦化市",
       "龙井市",
       "珲春市",
       "和龙市",
       "尚志市",
       "五常市",
       "讷河市",
       "宁安市",
       "海林市",
       "穆棱市",
       "绥芬河市",
       "东宁市",
       "同江市",
       "富锦市",
       "抚远市",
       "铁力市",
       "密山市",
       "虎林市",
       "安达市",
       "肇东市",
       "海伦市",
       "北安市",
       "五大连池市",
       "江阴市",
       "宜兴市",
       "邳州市",
       "新沂市",
       "溧阳市",
       "张家港市",
       "常熟市",
       "太仓市",
       "昆山市",
       "如皋市",
       "海门市",
       "启东市",
       "东台市",
       "高邮市",
       "仪征市",
       "丹阳市",
       "扬中市",
       "句容市",
       "靖江市",
       "兴化市",
       "泰兴市",
       "建德市",
       "余姚市",
       "慈溪市",
       "瑞安市",
       "乐清市",
       "诸暨市",
       "嵊州市",
       "海宁市",
       "平湖市",
       "桐乡市",
       "兰溪市",
       "义乌市",
       "东阳市",
       "永康市",
       "江山市",
       "龙泉市",
       "临海市",
       "温岭市",
       "玉环市",
       "巢湖市",
       "桐城市",
       "界首市",
       "天长市",
       "明光市",
       "宁国市",
       "福清市",
       "石狮市",
       "晋江市",
       "南安市",
       "龙海市",
       "漳平市",
       "永安市",
       "邵武市",
       "建瓯市",
       "武夷山市",
       "福安市",
       "福鼎市",
       "瑞金市",
       "丰城市",
       "樟树市",
       "高安市",
       "井冈山市",
       "德兴市",
       "瑞昌市",
       "共青城市",
       "庐山市",
       "乐平市",
       "贵溪市",
       "胶州市",
       "平度市",
       "莱西市",
       "滕州市",
       "龙口市",
       "莱阳市",
       "莱州市",
       "招远市",
       "蓬莱市",
       "栖霞市",
       "海阳市",
       "青州市",
       "诸城市",
       "寿光市",
       "安丘市",
       "高密市",
       "昌邑市",
       "曲阜市",
       "邹城市",
       "新泰市",
       "肥城市",
       "乳山市",
       "荣成市",
       "乐陵市",
       "禹城市",
       "临清市",
       "新郑市",
       "新密市",
       "登封市",
       "荥阳市",
       "巩义市",
       "偃师市",
       "舞钢市",
       "汝州市",
       "林州市",
       "卫辉市",
       "辉县市",
       "沁阳市",
       "孟州市",
       "禹州市",
       "长葛市",
       "义马市",
       "灵宝市",
       "永城市",
       "项城市",
       "邓州市",
       "济源市",
       "大冶市",
       "丹江口市",
       "洪湖市",
       "石首市",
       "松滋市",
       "宜都市",
       "当阳市",
       "枝江市",
       "老河口市",
       "枣阳市",
       "宜城市",
       "钟祥市",
       "麻城市",
       "武穴市",
       "应城市",
       "安陆市",
       "汉川市",
       "赤壁市",
       "广水市",
       "恩施市",
       "利川市",
       "仙桃市",
       "潜江市",
       "天门市",
       "浏阳市",
       "宁乡市",
       "醴陵市",
       "湘乡市",
       "韶山市",
       "耒阳市",
       "常宁市",
       "武冈市",
       "临湘市",
       "汨罗市",
       "沅江市",
       "津市市",
       "冷水江市",
       "涟源市",
       "资兴市",
       "洪江市",
       "吉首市乐昌市",
       "南雄市",
       "吴川市",
       "廉江市",
       "雷州市",
       "四会市",
       "恩平市",
       "台山市",
       "开平市",
       "鹤山市",
       "化州市",
       "信宜市",
       "高州市",
       "兴宁市",
       "陆丰市",
       "阳春市",
       "英德市",
       "连州市",
       "普宁市",
       "罗定市",
       "岑溪市",
       "凭祥市",
       "合山市",
       "北流市",
       "靖西市",
       "东兴市",
       "桂平市",
       "五指山市",
       "琼海市",
       "文昌市",
       "万宁市",
       "东方市",
       "都江堰市",
       "彭州市",
       "邛崃市",
       "崇州市",
       "简阳市",
       "江油市",
       "广汉市",
       "什邡市",
       "绵竹市",
       "隆昌市",
       "峨眉山市",
       "阆中市",
       "万源市",
       "华蓥市",
       "西昌市",
       "康定市",
       "清镇市",
       "马尔康市清镇市",
       "赤水市",
       "仁怀市",
       "盘州市",
       "兴义市",
       "凯里市",
       "都匀市",
       "福泉市安宁市",
       "宣威市",
       "腾冲市",
       "楚雄市",
       "蒙自市",
       "个旧市",
       "开远市",
       "弥勒市",
       "文山市",
       "景洪市",
       "大理市",
       "芒市",
       "瑞丽市",
       "香格里拉市",
       "泸水市",
       "兴平市",
       "韩城市",
       "华阴市",
       "神木市",
       "玉门市",
       "敦煌市",
       "临夏市",
       "合作市",
       "玉树市",
       "德令哈市",
       "格尔木市",
       "灵武市",
       "青铜峡市",
       "塔城市",
       "乌苏市",
       "阿勒泰市",
       "阿克苏市",
       "喀什市",
       "和田市",
       "昌吉市",
       "阜康市",
       "博乐市",
       "阿拉山口市",
       "伊宁市",
       "奎屯市",
       "霍尔果斯市",
       "库尔勒市",
       "阿图什市",
       "阿拉尔市",
       "石河子市",
       "图木舒克市",
       "五家渠市",
       "北屯市",
       "铁门关市",
       "双河市",
       "可克达拉市",
       "昆玉市"]
dis=["东城区",
     "西城区",
     "海淀区",
     "朝阳区",
     "丰台区",
     "大兴区",
     "通州区",
     "顺义区",
     "平谷区",
     "房山区",
     "昌平区",
     "延庆区",
     "怀柔区",
     "密云区",
     "石景山区",
     "门头沟区",
     "和平区",
     "河东区",
     "红桥区",
     "河西区",
     "南开区",
     "河北区",
     "东丽区",
     "西青区",
     "津南区",
     "北辰区",
     "武清区",
     "宝坻区",
     "宁河区",
     "静海区",
     "蓟州区",
     "滨海新区",
     "长安区",
     "桥西区",
     "新华区",
     "裕华区",
     "栾城区",
     "藁城区",
     "鹿泉区",
     "井陉矿区",
     "路南区",
     "路北区",
     "古冶区",
     "开平区",
     "丰南区",
     "丰润区",
     "曹妃甸区",
     "桥东区",
     "桥西区",
     "宣化区",
     "万全区",
     "崇礼区",
     "下花园区",
     "丛台区",
     "邯山区",
     "复兴区",
     "肥乡区",
     "永年区",
     "峰峰矿区",
     "竞秀区",
     "莲池区",
     "满城区",
     "清苑区",
     "徐水区",
     "海港区",
     "抚宁区",
     "山海关区",
     "北戴河区",
     "双桥区",
     "双滦区",
     "鹰手营子矿区",
     "桥东区",
     "桥西区",
     "运河区",
     "新华区",
     "安次区",
     "广阳区",
     "桃城区",
     "冀州区",
     "小店区",
     "迎泽区",
     "杏花岭区",
     "尖草坪区",
     "万柏林区",
     "晋源区",
     "新荣区",
     "平城区",
     "云冈区",
     "云州区",
     "潞州区",
     "上党区",
     "屯留区",
     "潞城区",
     "朔城区",
     "平鲁区",
     "忻府区",
     "离石区",
     "榆次区",
     "尧都区",
     "盐湖区",
     "东河区",
     "九原区",
     "青山区",
     "石拐区",
     "昆都仑区",
     "白云鄂博矿区",
     "回民区",
     "新城区",
     "玉泉区",
     "赛罕区",
     "海南区",
     "乌达区",
     "海勃湾区",
     "红山区",
     "松山区",
     "元宝山区",
     "海拉尔区",
     "扎赉诺尔区",
     "东胜区",
     "康巴什区",
     "科尔沁区",
     "集宁区",
     "临河区",
     "沈河区",
     "皇姑区",
     "和平区",
     "大东区",
     "铁西区",
     "苏家屯区",
     "浑南区",
     "于洪区",
     "沈北新区",
     "辽中区",
     "西岗区",
     "中山区",
     "金州区",
     "沙河口区",
     "甘井子区",
     "旅顺口区",
     "普兰店区",
     "白塔区",
     "文圣区",
     "宏伟区",
     "太子河区",
     "弓长岭区",
     "海州区",
     "新邱区",
     "太平区",
     "细河区",
     "清河门区",
     "站前区",
     "西市区",
     "老边区",
     "鲅鱼圈区",
     "铁东区",
     "铁西区",
     "立山区",
     "千山区",
     "顺城区",
     "新抚区",
     "东洲区",
     "望花区",
     "平山区",
     "明山区",
     "溪湖区",
     "南芬区",
     "大洼区",
     "双台子区",
     "兴隆台区",
     "龙港区",
     "南票区",
     "连山区",
     "振兴区",
     "元宝区",
     "振安区",
     "太和区",
     "古塔区",
     "凌河区",
     "朝阳区",
     "南关区",
     "宽城区",
     "绿园区",
     "双阳区",
     "二道区",
     "九台区",
     "船营区",
     "昌邑区",
     "龙潭区",
     "丰满区",
     "东昌区",
     "二道江区",
     "铁西区",
     "铁东区",
     "龙山区",
     "西安区",
     "浑江区",
     "江源区",
     "洮北区",
     "宁江区	",
     "道里区",
     "南岗区",
     "道外区",
     "平房区",
     "松北区",
     "香坊区",
     "呼兰区",
     "阿城区",
     "双城区",
     "龙沙区",
     "建华区",
     "铁锋区",
     "昂昂溪区",
     "碾子山区",
     "富拉尔基区",
     "梅里斯达斡尔族区",
     "鸡冠区",
     "恒山区",
     "滴道区",
     "梨树区",
     "麻山区",
     "城子河区",
     "向阳区",
     "工农区",
     "兴安区",
     "兴山区",
     "东山区",
     "南山区",
     "伊美区",
     "乌翠区",
     "友好区",
     "金林区",
     "龙凤区",
     "红岗区",
     "大同区",
     "萨尔图区",
     "让胡路区",
     "尖山区",
     "岭东区",
     "宝山区",
     "四方台区",
     "东安区",
     "西安区",
     "阳明区",
     "爱民区",
     "郊区",
     "向阳区",
     "前进区",
     "东风区",
     "新兴区",
     "桃山区",
     "茄子河区",
     "爱辉区",
     "北林区",
     "黄浦区",
     "徐汇区",
     "长宁区",
     "静安区",
     "普陀区",
     "虹口区",
     "杨浦区",
     "宝山区",
     "闵行区",
     "嘉定区",
     "松江区",
     "青浦区",
     "奉贤区",
     "金山区",
     "崇明区",
     "浦东新区",
     "玄武区",
     "秦淮区",
     "建邺区",
     "鼓楼区",
     "浦口区",
     "栖霞区",
     "江宁区",
     "六合区",
     "溧水区",
     "高淳区",
     "雨花台区",
     "姑苏区",
     "虎丘区",
     "相城区",
     "吴中区",
     "吴江区",
     "锡山区",
     "惠山区",
     "滨湖区",
     "梁溪区",
     "新吴区",
     "鼓楼区",
     "云龙区",
     "贾汪区",
     "泉山区",
     "铜山区",
     "天宁区",
     "钟楼区",
     "新北区",
     "武进区",
     "金坛区",
     "淮安区",
     "淮阴区",
     "洪泽区",
     "清江浦区",
     "连云区",
     "海州区",
     "赣榆区",
     "崇川区",
     "港闸区",
     "通州区",
     "亭湖区",
     "盐都区",
     "大丰区",
     "广陵区",
     "邗江区",
     "江都区",
     "京口区",
     "润州区",
     "丹徒区",
     "海陵区",
     "高港区",
     "姜堰区",
     "宿城区",
     "宿豫区",
     "拱墅区",
     "上城区",
     "下城区",
     "江干区",
     "西湖区",
     "滨江区",
     "萧山区",
     "余杭区",
     "富阳区",
     "临安区",
     "海曙区",
     "江北区",
     "北仑区",
     "镇海区",
     "鄞州区",
     "奉化区",
     "鹿城区",
     "龙湾区",
     "瓯海区",
     "洞头区",
     "越城区",
     "柯桥区",
     "上虞区",
     "椒江区",
     "黄岩区",
     "路桥区",
     "吴兴区",
     "南浔区",
     "南湖区",
     "秀洲区",
     "婺城区",
     "金东区",
     "柯城区",
     "衢江区",
     "定海区",
     "普陀区",
     "莲都区",
     "大通区",
     "潘集区",
     "田家庵区",
     "谢家集区",
     "八公山区",
     "瑶海区",
     "庐阳区",
     "蜀山区",
     "包河区",
     "镜湖区",
     "弋江区",
     "三山区",
     "鸠江区",
     "蚌山区",
     "禹会区",
     "淮上区",
     "龙子湖区",
     "雨山区",
     "花山区",
     "博望区",
     "金安区",
     "裕安区",
     "叶集区",
     "相山区",
     "杜集区",
     "烈山区",
     "迎江区",
     "大观区",
     "宜秀区",
     "屯溪区",
     "黄山区",
     "徽州区",
     "颍州区",
     "颍东区",
     "颍泉区",
     "郊区",
     "义安区",
     "铜官区",
     "琅琊区",
     "南谯区",
     "鼓楼区",
     "台江区",
     "仓山区",
     "马尾区",
     "晋安区",
     "长乐区",
     "思明区",
     "湖里区",
     "海沧区",
     "集美区",
     "同安区",
     "翔安区",
     "城厢区",
     "涵江区",
     "荔城区",
     "秀屿区",
     "鲤城区",
     "丰泽区",
     "洛江区",
     "泉港区",
     "芗城区",
     "龙文区",
     "新罗区",
     "永定区",
     "梅列区",
     "三元区",
     "延平区",
     "建阳区",
     "蕉城区",
     "东湖区",
     "西湖区",
     "青云谱区",
     "湾里区",
     "青山湖区",
     "新建区",
     "章贡区",
     "南康区",
     "赣县区",
     "浔阳区",
     "濂溪区",
     "柴桑区",
     "信州区",
     "广丰区",
     "广信区",
     "吉州区",
     "青原区",
     "昌江区",
     "珠山区",
     "临川区",
     "东乡区",
     "安源区",
     "湘东区",
     "月湖区",
     "余江区",
     "袁州区",
     "渝水区",
     "历下区",
     "市中区",
     "槐荫区",
     "天桥区",
     "历城区",
     "长清区",
     "章丘区",
     "济阳区",
     "莱芜区",
     "钢城区",
     "市南区",
     "市北区",
     "李沧区",
     "崂山区",
     "城阳区",
     "黄岛区",
     "即墨区",
     "市中区",
     "薛城区",
     "峄城区",
     "山亭区",
     "台儿庄区",
     "张店区",
     "临淄区",
     "淄川区",
     "博山区",
     "周村区",
     "莱山区",
     "芝罘区",
     "福山区",
     "牟平区",
     "奎文区",
     "潍城区",
     "寒亭区",
     "坊子区",
     "东营区",
     "河口区",
     "垦利区",
     "兰山区",
     "罗庄区",
     "河东区",
     "任城区",
     "兖州区",
     "泰山区",
     "岱岳区",
     "环翠区",
     "文登区",
     "东港区",
     "岚山区",
     "滨城区",
     "沾化区",
     "德城区",
     "陵城区",
     "牡丹区",
     "定陶区",
     "东昌府区",
     "茌平区",
     "中原区",
     "金水区",
     "二七区",
     "管城区",
     "惠济区",
     "上街区",
     "洛龙区",
     "涧西区",
     "西工区",
     "老城区",
     "瀍河区",
     "吉利区",
     "龙亭区",
     "鼓楼区",
     "顺河区",
     "禹王台区",
     "祥符区",
     "新华区",
     "卫东区",
     "湛河区",
     "石龙区",
     "红旗区",
     "卫滨区",
     "凤泉区",
     "牧野区",
     "文峰区",
     "殷都区",
     "龙安区",
     "北关区",
     "解放区",
     "中站区",
     "马村区",
     "山阳区",
     "淇滨区",
     "山城区",
     "鹤山区",
     "郾城区",
     "源汇区",
     "召陵区",
     "湖滨区",
     "陕州区",
     "宛城区",
     "卧龙区",
     "魏都区",
     "建安区",
     "睢阳区",
     "梁园区",
     "平桥区",
     "浉河区",
     "驿城区",
     "川汇区",
     "淮阳区",
     "华龙区",
     "江岸区",
     "江汉区",
     "硚口区",
     "汉阳区",
     "武昌区",
     "青山区",
     "洪山区",
     "东西湖区",
     "汉南区",
     "蔡甸区",
     "江夏区",
     "黄陂区",
     "新洲区",
     "西陵区",
     "点军区",
     "猇亭区",
     "夷陵区",
     "伍家岗区",
     "黄石港区",
     "西塞山区",
     "下陆区",
     "铁山区",
     "华容区",
     "鄂城区",
     "梁子湖区",
     "茅箭区",
     "张湾区",
     "郧阳区",
     "襄城区",
     "樊城区",
     "襄州区",
     "东宝区",
     "掇刀区",
     "荆州区",
     "沙市区",
     "孝南区",
     "黄州区",
     "咸安区",
     "曾都区",
     "岳麓区",
     "芙蓉区",
     "天心区",
     "开福区",
     "雨花区",
     "望城区",
     "天元区",
     "荷塘区",
     "芦淞区",
     "石峰区",
     "渌口区",
     "雁峰区",
     "珠晖区",
     "石鼓区",
     "蒸湘区",
     "南岳区",
     "君山区",
     "云溪区",
     "岳阳楼区",
     "双清区",
     "大祥区",
     "北塔区",
     "永定区",
     "武陵源区",
     "零陵区",
     "冷水滩区",
     "岳塘区",
     "雨湖区",
     "赫山区",
     "资阳区",
     "鼎城区",
     "武陵区",
     "苏仙区",
     "北湖区",
     "娄星区",
     "越秀区",
     "天河区",
     "荔湾区",
     "海珠区",
     "白云区",
     "黄埔区",
     "花都区",
     "番禺区",
     "南沙区",
     "从化区",
     "增城区",
     "福田区",
     "罗湖区",
     "南山区",
     "盐田区",
     "宝安区",
     "龙岗区",
     "龙华区",
     "坪山区",
     "光明区",
     "龙湖区",
     "金平区",
     "濠江区",
     "澄海区",
     "潮阳区",
     "潮南区",
     "禅城区",
     "南海区",
     "顺德区",
     "高明区",
     "三水区",
     "赤坎区",
     "霞山区",
     "坡头区",
     "麻章区",
     "香洲区",
     "斗门区",
     "金湾区",
     "浈江区",
     "武江区",
     "曲江区",
     "端州区",
     "鼎湖区",
     "高要区",
     "蓬江区",
     "江海区",
     "新会区",
     "茂南区",
     "电白区",
     "惠城区",
     "惠阳区",
     "梅江区",
     "梅县区",
     "青秀区",
     "兴宁区",
     "江南区",
     "良庆区",
     "邕宁区",
     "武鸣区",
     "西乡塘区",
     "象山区",
     "秀峰区",
     "叠彩区",
     "七星区",
     "雁山区",
     "临桂区",
     "城中区",
     "鱼峰区",
     "柳北区",
     "柳南区",
     "柳江区",
     "海城区",
     "银海区",
     "铁山港区",
     "万秀区",
     "龙圩区",
     "长洲区",
     "港北区",
     "港南区",
     "覃塘区",
     "宜州区",
     "金城江区",
     "港口区",
     "防城区",
     "八步区",
     "平桂区",
     "玉州区",
     "福绵区",
     "钦南区",
     "钦北区",
     "江州区",
     "秀英区",
     "龙华区",
     "琼山区",
     "美兰区",
     "天涯区",
     "吉阳区",
     "海棠区",
     "崖州区",
     "渝中区",
     "江北区",
     "南岸区",
     "北碚区",
     "渝北区",
     "巴南区",
     "黔江区",
     "长寿区",
     "万州区",
     "涪陵区",
     "合川区",
     "南川区",
     "江津区",
     "永川区",
     "大足区",
     "綦江区",
     "璧山区",
     "铜梁区",
     "成华区",
     "武侯区",
     "青羊区",
     "锦江区",
     "金牛区",
     "新都区",
     "温江区",
     "双流区",
     "郫都区",
     "龙泉驿区",
     "青白江区",
     "市中区",
     "沙湾区",
     "金口河区",
     "五通桥区",
     "贡井区",
     "大安区",
     "沿滩区",
     "自流井区",
     "江阳区",
     "纳溪区",
     "龙马潭区",
     "涪城区",
     "游仙区",
     "安州区",
     "利州区",
     "昭化区",
     "朝天区",
     "翠屏区",
     "南溪区",
     "叙州区",
     "顺庆区",
     "高坪区",
     "嘉陵区",
     "东区",
     "西区",
     "仁和区",
     "旌阳区",
     "罗江区",
     "船山区",
     "安居区",
     "市中区",
     "东兴区",
     "通川区",
     "达川区",
     "雨城区",
     "名山区",
     "广安区",
     "前锋区",
     "巴州区",
     "恩阳区",
     "东坡区",
     "彭山区",
     "雁江区",
     "云岩区",
     "南明区",
     "花溪区",
     "乌当区",
     "白云区",
     "观山湖区",
     "汇川区",
     "播州区",
     "红花岗区",
     "碧江区",
     "万山区",
     "西秀区",
     "平坝区",
     "七星关区",
     "钟山区",
     "盘龙区",
     "五华区",
     "官渡区",
     "西山区",
     "东川区",
     "呈贡区",
     "晋宁区",
     "麒麟区",
     "沾益区",
     "马龙区",
     "红塔区",
     "江川区",
     "昭阳区",
     "思茅区",
     "隆阳区",
     "古城区",
     "临翔区",
     "城关区",
     "堆龙德庆区",
     "达孜区",
     "桑珠孜区",
     "卡若区",
     "乃东区",
     "巴宜区",
     "色尼区",
     "新城区",
     "碑林区",
     "莲湖区",
     "灞桥区",
     "未央区",
     "雁塔区",
     "阎良区",
     "临潼区",
     "长安区",
     "高陵区",
     "鄠邑区",
     "耀州区",
     "王益区",
     "印台区",
     "渭滨区",
     "金台区",
     "陈仓区",
     "秦都区",
     "渭城区",
     "杨陵区",
     "宝塔区",
     "安塞区",
     "临渭区",
     "华州区",
     "汉台区",
     "南郑区",
     "榆阳区",
     "横山区",
     "汉滨区",
     "商州区",
     "城关区",
     "七里河区",
     "西固区",
     "安宁区",
     "红古区",
     "白银区",
     "平川区",
     "秦州区",
     "麦积区",
     "肃州区",
     "甘州区",
     "凉州区",
     "安定区",
     "武都区",
     "崆峒区",
     "西峰区",
     "金川区",
     "城中区",
     "城东区",
     "城西区",
     "城北区",
     "乐都区",
     "平安区",
     "兴庆区",
     "金凤区",
     "西夏区",
     "惠农区",
     "大武口区",
     "利通区",
     "红寺堡区",
     "沙坡头区",
     "原州区",
     "米东区",
     "水磨沟区",
     "头屯河区",
     "达坂城区",
     "沙依巴克区",
     "独山子区",
     "白碱滩区",
     "乌尔禾区",
     "沙坪坝区",
     "克拉玛依区",
     "高昌区",
     "兴宾区",
     "顺河回族区",
     "伊州区"


]
def find_5_address(address):
    province = ""
    city = ""
    district = ""
    town = ""
    street = ""
    flag1 = 0
    flag2 = 0
    k = 0
    while k < 23:
        pos1 = address.find(province1[k]) #安徽省
        if pos1 > -1:
            province = province1[k]
            address = address[pos1+3:]
            flag1 = 1
            break
        k+=1

    k = 0
    while k < 4:
        pos1 = address.find(municipality1[k])#北京市
        if pos1 > -1:
            province = municipality1[k][0:2]
            address = address[pos1+3:]
            city = municipality1[k]
            flag1 = 1
            flag2 = 1
            break
        k+=1
    if flag1 == 0:
        k = 0
        while k < 4:
            pos1 = address.find(municipality0[k])  # 北京
            if pos1 > -1:
                province = municipality0[k]
                address = address[pos1 + 2:]
                city = municipality0[k]
                flag1 = 1
                flag2 = 1
                break
            k += 1
    if flag1 == 0:
        k = 0
        while k < 7:
            pos1 = address.find(province2[k])  # 自治区/特别行政区
            if pos1 > -1:
                province = province2[k]
                address = address[pos1 + len(province2[k]):]
                flag1 = 1
                break
            k += 1

    if flag1 == 0:
        k = 0
        while k < 23:
            pos1 = address.find(province0[k])  # 福建
            if pos1 > -1:
                province = province0[k] + "省"
                address = address[pos1 + 2:]
                flag1 = 1
                break
            k += 1

    flag1 = 0
    if flag2 == 0:
        k = 0
        pos1 = address.find("自治州")  # 自治州
        if pos1 > -1:
            city = address[:pos1 + 3]
            address = address[pos1 + 3:]
        else:
            k = 0
            while k < len(city_):
                pos1 = address.find(city_[k])  # 福州市
                if pos1 > -1:
                    city = city_[k]
                    address = address[pos1 + len(city_[k]):]
                    flag1 = 1
                    break

                pos1 = address.find(city_[k][0: len(city_[k]) - 1])  # 福州
                if pos1 > -1:
                    if city_[k][-1] == "市":
                        flag1 = 1
                        city = city_[k]
                        address = address[pos1 + len(city_[k]) - 1:]
                        break
                k += 1

    flag3 = 0
    k = 0
    while k < len(dis):
        pos1 = address.find(dis[k])  # 鼓楼区
        if pos1 > -1:
            district = dis[k]
            address = address[pos1 + len(dis[k]):]
            flag3 = 1
            break
        k += 1

    if flag3 == 0:
        pos1 = address.find("县")  # 闽侯县
        if pos1 > -1:
            if len(address) - 1 == pos1 or (len(address) > pos1 + 1 and address[pos1 + 1] != "道"):
                district = address[0:pos1 + 1]
                address = address[pos1 + 1:]
                flag3 = 1

    if flag3 == 0:
        k = 0
        while k < len(direc):
            pos1 = address.find(direc[k])  # 晋江市
            if pos1 > -1:
                district = direc[k]
                address = address[pos1 + len(direc[k]):]
                flag3 = 1
                break
            k += 1
    '''
    if flag2==0:
        pos1 = address.find("旗")#XX旗
        if pos1 > -1: 
            district = address[0:pos1 + 1]
            address = address[pos1 + 1:]
            flag2=1'''

    pos1 = address.find("镇")  # 上街镇
    if pos1 > -1:
        town = address[0:pos1 + 1]
        address = address[pos1 + 1:]

    else:
        flag4 = 0
        pos1 = address.find("街道")  # XX街道
        if pos1 > -1:
            if len(address) - 1 == pos1 + 1 or (len(address) > pos1 + 2 and address[pos1 + 2] != "办"):
                town = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1

        if flag4 == 0:
            pos1 = address.find("乡")  # XX乡
            if pos1 > -1:
                if len(address) - 1 == pos1 or (
                        len(address) > pos1 + 1 and address[pos1 + 1] != "道" and address[pos1 + 1] != "村"):
                    town = address[0:pos1 + 1]
                    address = address[pos1 + 1:]
        if flag4 == 0:
            pos1 = address.find("苏木")  # XX苏木

            if pos1 > -1:
                town = address[0:pos1 + 2]
                address = address[pos1 + 2:]
        if flag4 == 0:
            pos1 = address.find("经济开发区")  # 经济开发区

            if pos1 > -1:
                town = address[0:pos1 + 5]
                address = address[pos1 + 5:]

    street = address
    return province, city, district, town, street


def divide_address_7(address):
    province = ""
    city = ""
    district = ""
    town = ""
    street = ""
    t1 = ""
    t2 = ""
    k = 0
    flag = 0

    province, city, district, town, address = find_5_address(address)
    pos1 = address.find("路")  # 五一北路
    if pos1 > -1:

        street = address[0: pos1 + 1]
        address = address[pos1 + 1:]

    else:

        flag4 = 0
        pos1 = address.find("街")  # XX街
        if pos1 > -1:
            if len(address) - 1 == pos1 or (len(address) > pos1 + 1 and address[pos1 + 1] != "道"):
                street = address[0: pos1 + 1]
                address = address[pos1 + 1:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("巷")  # XX巷
            if pos1 > -1:
                street = address[0:pos1 + 1]
                address = address[pos1 + 1:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("国道")  # XX国道
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("省道")  # XX省道
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("乡道")  # XX乡道
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("县道")  # XX县道
            if pos1 > -1:
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("大道")  # XX大道
            if pos1 > -1:
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("街区")  # XX街区
            if pos1 > -1:
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("胡同")  # XX胡同
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        '''if flag4==0:
            pos1 = address.find("村")#XX村
            if pos1 > -1 and address[pos1+1]!="委":           
                    street = address[0:pos1 + 1]
                    address = address[pos1 + 1:]
                    flag4=1'''
        if flag4 == 0:
            pos1 = address.find("里")  # XX里
            if pos1 > -1:
                street = address[0:pos1 + 1]
                address = address[pos1 + 1:]
                flag4 = 1
        '''
        if flag4==0:
            pos1 = address.find("社区")#XX社区
            if pos1 > -1  :                   
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4=1'''

    pos1 = address.find("号")  # xx号
    if pos1 > -1 and ((pos1 + 1 <= len(address) - 1 and address[pos1 + 1] != "楼") or pos1 == len(address) - 1):
        t1 = address[0:pos1 + 1]
        address = address[pos1 + 1:]
    else:
        pos1 = address.find("弄")  # xx弄
        if pos1 > -1:
            t1 = address[0:pos1 + 1]
            address = address[pos1 + 1:]

    t2 = address

    return province, city, district, town, street, t1, t2


def find_7_address(address):
    province = ""
    city = ""
    district = ""
    town = ""
    street = ""
    t1 = ""
    t2 = ""
    k = 0
    flag = 0

    province, city, district, town, address = find_5_address(address)
    pos1 = address.find("路")  # 五一北路
    if pos1 > -1:

        street = address[0: pos1 + 1]
        address = address[pos1 + 1:]

    else:

        flag4 = 0
        pos1 = address.find("街")  # XX街
        if pos1 > -1:
            if len(address) - 1 == pos1 or (len(address) > pos1 + 1 and address[pos1 + 1] != "道"):
                street = address[0: pos1 + 1]
                address = address[pos1 + 1:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("巷")  # XX巷
            if pos1 > -1:
                street = address[0:pos1 + 1]
                address = address[pos1 + 1:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("国道")  # XX国道
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("省道")  # XX省道
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("乡道")  # XX乡道
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("县道")  # XX县道
            if pos1 > -1:
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("大道")  # XX大道
            if pos1 > -1:
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("街区")  # XX街区
            if pos1 > -1:
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        if flag4 == 0:
            pos1 = address.find("胡同")  # XX胡同
            if pos1 > -1:
                street = address[0:pos1 + 2]
                address = address[pos1 + 2:]
                flag4 = 1
        '''if flag4==0:
            pos1 = address.find("村")#XX村
            if pos1 > -1 and address[pos1+1]!="委":           
                    street = address[0:pos1 + 1]
                    address = address[pos1 + 1:]
                    flag4=1'''
        if flag4 == 0:
            pos1 = address.find("里")  # XX里
            if pos1 > -1:
                street = address[0:pos1 + 1]
                address = address[pos1 + 1:]
                flag4 = 1
        '''
        if flag4==0:
            pos1 = address.find("社区")#XX社区
            if pos1 > -1  :                   
                street = address[0: pos1 + 2]
                address = address[pos1 + 2:]
                flag4=1'''

    pos1 = address.find("号")  # xx号
    if pos1 > -1 and ((pos1 + 1 <= len(address) - 1 and address[pos1 + 1] != "楼") or pos1 == len(address) - 1):
        t1 = address[0:pos1 + 1]
        address = address[pos1 + 1:]
    else:
        pos1 = address.find("弄")  # xx弄
        if pos1 > -1:
            t1 = address[0:pos1 + 1]
            address = address[pos1 + 1:]

    t2 = address

    return province, city, district, town, street, t1, t2


def get_formatted_address(address):
    # 根据百度地图api接口获取正地址编码也就是经纬度
    url1 = 'https://restapi.amap.com/v3/geocode/geo?address=' + address + '&output=JSON&key=a22337e1181873a96bc9701887d1c349'

    # 获取经纬度
    resp1 = requests.get(url1)
    # resp1_str=resp1.text
    # resp1_str=resp1_str.replace('showLocation&&showLocation','')
    # resp1_str=resp1_str[1:-1]
    resp1_json = resp1.json()
    location = resp1_json['geocodes'][0]['location']

    # 根据经纬度获取结构化地址
    # lng=location.get('lng')
    # lat=location.get('lat')
    url2 = 'https://restapi.amap.com/v3/geocode/regeo?output=JSON&location=' + location + '&key=a22337e1181873a96bc9701887d1c349&radius=5&extensions=all'
    resp2 = requests.get(url2)

    resp2_json = resp2.json()
    # 提取结构化地址
    formattted_address = resp2_json['regeocode']['addressComponent']
    return formattted_address
def main():
    str = input()
    pos = str.find(',')
    pos_name = str.find('!')
    name = str[pos_name + 1:pos]
    temp = str[pos+1:]

    tel_pattern = re.compile(r'1[0-9]{10}')
    tel_str = tel_pattern.search(str)
    tel_number = tel_str.group(0)
    #print(temp)
    temp = tel_pattern.sub('', temp)
    temp = temp[0:len(temp)-1]
    #print(temp)
    if(str[0] == '1'):
        province, city, district, town, street = find_5_address(temp)
        info = {}
        data_info = json.loads(json.dumps(info))
        address = []
        address.append(province)
        address.append(city)
        address.append(district)
        address.append(town)
        address.append(street)

        data_info['姓名'] = name
        data_info['手机'] = tel_number
        data_info['地址'] = address
        print(json.dumps(data_info,ensure_ascii=False))
    if(str[0] == '2'):
        province, city, district, town, street,add1,add2 = find_7_address(temp)
        info = {}
        data_info = json.loads(json.dumps(info))
        address = []
        address.append(province)
        address.append(city)
        address.append(district)
        address.append(town)
        address.append(street)
        address.append(add1)
        address.append(add2)
        data_info['姓名'] = name
        data_info['手机'] = tel_number
        data_info['地址'] = address
        print(json.dumps(data_info, ensure_ascii=False))
    if(str[0] == '3'):
        province, city, district, town, street, street_number, t2 = find_7_address(temp)
        level = []
        level.append(province)
        level.append(city)
        level.append(district)
        level.append(town)
        level.append(street)
        level.append(street_number)
        level.append(t2)
        level_name = ["province", "city", "district", "township", "street", "street_number"]
        formattted_address = get_formatted_address(temp)
        #print(level)
        #print(formattted_address)
        for i in range(4):
            if level[i] == "":
                if formattted_address[level_name[i]]:
                    level[i] = formattted_address[level_name[i]]

        if level[0][-1] == "市":
            level[1] = level[0][0:2]
            print(level[1])
        '''if level[4]=="":
            if formattted_address['streetNumber']['street']:
                level[4]=formattted_address['streetNumber']['street']
        if level[5]=="":
            if formattted_address['streetNumber']['number']:
                level[5]=formattted_address['streetNumber']['number']
        if level[6]=="":
            if formattted_address['building']['name']:
                level[6]=formattted_address['building']['name']
            elif formattted_address['neighborhood']['name']:
                level[6]=formattted_address['neighborhood']['name']
        '''

        article_info = {}
        data = json.loads(json.dumps(article_info))
        data['姓名'] = name
        data['手机'] = tel_number
        data['地址'] = level

        print(json.dumps(data, ensure_ascii=False))

main()








