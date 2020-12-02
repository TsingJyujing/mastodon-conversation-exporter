import datetime
import json

import numpy

zh_family_name_list = [
    "赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "楮",
    "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许", "何", "吕",
    "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶", "姜", "戚",
    "谢", "邹", "喻", "柏", "水", "窦", "章", "云", "苏", "潘", "葛",
    "奚", "范", "彭", "郎", "鲁", "韦", "昌", "马", "苗", "凤", "花",
    "方", "俞", "任", "袁", "柳", "酆", "鲍", "史", "唐", "费", "廉",
    "岑", "薛", "雷", "贺", "倪", "汤", "滕", "殷", "罗", "毕", "郝",
    "邬", "安", "常", "乐", "于", "时", "傅", "皮", "卞", "齐", "康",
    "伍", "余", "元", "卜", "顾", "孟", "平", "黄", "和", "穆", "萧",
    "尹", "姚", "邵", "湛", "汪", "祁", "毛", "禹", "狄", "米", "贝",
    "明", "臧", "计", "伏", "成", "戴", "谈", "宋", "茅", "庞", "熊",
    "纪", "舒", "屈", "项", "祝", "董", "梁", "杜", "阮", "蓝", "闽",
    "席", "季", "麻", "强", "贾", "路", "娄", "危", "江", "童", "颜",
    "郭", "梅", "盛", "林", "刁", "锺", "徐", "丘", "骆", "高", "夏",
    "蔡", "田", "樊", "胡", "凌", "霍", "虞", "万", "支", "柯", "昝",
    "管", "卢", "莫", "经", "房", "裘", "缪", "干", "解", "应", "宗",
    "丁", "宣", "贲", "邓", "郁", "单", "杭", "洪", "包", "诸", "左",
    "石", "崔", "吉", "钮", "龚", "程", "嵇", "邢", "滑", "裴", "陆",
    "荣", "翁", "荀", "羊", "於", "惠", "甄", "麹", "家", "封", "芮",
    "羿", "储", "靳", "汲", "邴", "糜", "松", "井", "段", "富", "巫",
    "乌", "焦", "巴", "弓", "牧", "隗", "山", "谷", "车", "侯", "宓",
    "蓬", "全", "郗", "班", "仰", "秋", "仲", "伊", "宫", "宁", "仇",
    "栾", "暴", "甘", "斜", "厉", "戎", "祖", "武", "符", "刘", "景",
    "詹", "束", "龙", "叶", "幸", "司", "韶", "郜", "黎", "蓟", "薄",
    "印", "宿", "白", "怀", "蒲", "邰", "从", "鄂", "索", "咸", "籍",
    "赖", "卓", "蔺", "屠", "蒙", "池", "乔", "阴", "郁", "胥", "能",
    "苍", "双", "闻", "莘", "党", "翟", "谭", "贡", "劳", "逄", "姬",
    "申", "扶", "堵", "冉", "宰", "郦", "雍", "郤", "璩", "桑", "桂",
    "濮", "牛", "寿", "通", "边", "扈", "燕", "冀", "郏", "浦", "尚",
    "农", "温", "别", "庄", "晏", "柴", "瞿", "阎", "充", "慕", "连",
    "茹", "习", "宦", "艾", "鱼", "容", "向", "古", "易", "慎", "戈",
    "廖", "庾", "终", "暨", "居", "衡", "步", "都", "耿", "满", "弘",
    "匡", "国", "文", "寇", "广", "禄", "阙", "东", "欧", "殳", "沃",
    "利", "蔚", "越", "夔", "隆", "师", "巩", "厍", "聂", "晁", "勾",
    "敖", "融", "冷", "訾", "辛", "阚", "那", "简", "饶", "空", "曾",
    "毋", "沙", "乜", "养", "鞠", "须", "丰", "巢", "关", "蒯", "相",
    "查", "后", "荆", "红", "游", "竺", "权", "逑", "盖", "益", "桓",
    "公", "万俟", "司马", "上官", "欧阳", "夏侯", "诸葛", "闻人",
    "东方", "赫连", "皇甫", "尉迟", "公羊", "澹台", "公冶", "宗政",
    "濮阳", "淳于", "单于", "太叔", "申屠", "公孙", "仲孙", "轩辕",
    "令狐", "锺离", "宇文", "长孙", "慕容", "鲜于", "闾丘", "司徒",
    "司空", "丌官", "司寇", "仉", "督", "子车", "颛孙", "端木",
    "巫马", "公西", "漆雕", "乐正", "壤驷", "公良", "拓拔", "夹谷",
    "宰父", "谷梁", "晋", "楚", "阎", "法", "汝", "鄢", "涂", "钦",
    "段干", "百里", "东郭", "南门", "呼延", "归", "海", "羊舌",
    "微生", "岳", "帅", "缑", "亢", "况", "后", "有", "琴", "梁丘",
    "左丘", "东门", "西门", "商", "牟", "佘", "佴", "伯", "赏", "南宫",
    "墨", "哈", "谯", "笪", "年", "爱", "阳", "佟"
]
zh_family_name_prob = numpy.array([1.0 / (i + 1) for i in range(len(zh_family_name_list))])
zh_family_name_prob = zh_family_name_prob / zh_family_name_prob.sum()

zh_first_name_char_list = [
    "嘉", "哲", "俊", "博", "妍", "乐", "佳", "涵", "晨", "宇", "怡",
    "泽", "子", "凡", "悦", "思", "奕", "依", "浩", "泓", "彤", "冰",
    "媛", "凯", "伊", "淇", "淳", "一", "洁", "茹", "清", "吉", "源",
    "渊", "和", "函", "妤", "宜", "云", "琪", "菱", "宣", "沂", "健",
    "信", "欣", "可", "洋", "萍", "荣", "榕", "含", "佑", "明", "雄",
    "梅", "芝", "英", "义", "淑", "卿", "乾", "亦", "芬", "萱", "昊",
    "芸", "天", "岚", "昕", "尧", "鸿", "棋", "琳", "孜", "娟", "宸",
    "林", "乔", "琦", "丞", "安", "毅", "凌", "泉", "坤", "晴", "竹",
    "娴", "婕", "恒", "渝", "菁", "龄", "弘", "佩", "勋", "宁", "元",
    "栋", "盈", "江", "卓", "春", "晋", "逸", "沅", "倩", "昱", "绮",
    "海", "圣", "承", "民", "智", "棠", "容", "羚", "峰", "钰", "涓",
    "新", "莉", "恩", "羽", "妮", "旭", "维", "家", "泰", "诗", "谚",
    "阳", "彬", "书", "苓", "汉", "蔚", "坚", "茵", "耘", "喆", "国",
    "仑", "良", "裕", "融", "致", "富", "德", "易", "虹", "纲", "筠",
    "奇", "平", "蓓", "真", "之", "凰", "桦", "玫", "强", "村", "沛",
    "汶", "锋", "彦", "延", "庭", "霞", "冠", "益", "劭", "钧", "薇",
    "亭", "瀚", "桓", "东", "滢", "恬", "瑾", "达", "群", "茜", "先",
    "洲", "溢", "楠", "基", "轩", "月", "美", "心", "茗", "丹", "森",
    "学", "文"
]

en_family_name_list = [
    "Smith", "Jones", "Taylor", "Williams", "Brown", "Davies", "Evans", "Wilson", "Thomas", "Roberts", "Johnson",
    "Lewis", "Walker", "Robinson", "Wood", "Thompson", "White", "Watson", "Jackson", "Wright", "Green", "Harris",
    "Cooper", "King", "Lee", "Martin", "Clarke", "James", "Morgan", "Hughes", "Edwards", "Hill", "Moore", "Clark",
    "Harrison", "Scott", "Young", "Morris", "Hall", "Ward", "Turner", "Carter", "Phillips", "Mitchell", "Patel",
    "Adams", "Campbell", "Anderson", "Allen", "Cook", "Bailey", "Parker", "Miller", "Davis", "Murphy", "Price", "Bell",
    "Baker", "Griffiths", "Kelly", "Simpson", "Marshall", "Collins", "Bennett", "Cox", "Richardson", "Fox", "Gray",
    "Rose", "Chapman", "Hunt", "Robertson", "Shaw", "Reynolds", "Lloyd", "Ellis", "Richards", "Russell", "Wilkinson",
    "Khan", "Graham", "Stewart", "Reid", "Murray", "Powell", "Palmer", "Holmes", "Rogers", "Stevens", "Walsh", "Hunter",
    "Thomson", "Matthews", "Ross", "Owen", "Mason", "Knight", "Kennedy", "Butler", "Saunders"
]

en_first_name_list = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph", "Thomas", "Christopher",
    "Daniel", "Paul", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony", "Kevin",
    "Jason", "Matthew", "Gary", "Timothy", "Jose", "Larry", "Jeffrey", "Frank", "Scott", "Eric", "Stephen", "Andrew",
    "Raymond", "Gregory", "Joshua", "Jerry", "Dennis", "Walter", "Patrick", "Peter", "Harold", "Douglas", "Henry",
    "Carl", "Arthur", "Ryan", "Roger", "Mary", "Patricia", "Linda", "Barbara", "Elizabeth", "Jennifer", "Maria",
    "Susan", "Margaret", "Dorothy", "Lisa", "Nancy", "Karen", "Betty", "Helen", "Sandra", "Donna", "Carol", "Ruth",
    "Sharon", "Michelle", "Laura", "Sarah", "Kimberly", "Deborah", "Jessica", "Shirley", "Cynthia", "Angela", "Melissa",
    "Brenda", "Amy", "Anna", "Rebecca", "Virginia", "Kathleen", "Pamela", "Martha", "Debra", "Amanda", "Stephanie",
    "Carolyn", "Christine", "Marie", "Janet", "Catherine", "Frances", "Ann", "Joyce", "Diane", "Joe", "Juan", "Jack",
    "Albert", "Jonathan", "Justin", "Terry", "Gerald", "Keith", "Samuel", "Willie", "Ralph", "Lawrence", "Nicholas",
    "Roy", "Benjamin", "Bruce", "Brandon", "Adam", "Harry", "Fred", "Wayne", "Billy", "Steve", "Louis", "Jeremy",
    "Aaron", "Randy", "Howard", "Eugene", "Carlos", "Russell", "Bobby", "Victor", "Martin", "Ernest", "Phillip", "Todd",
    "Jesse", "Craig", "Alan", "Shawn", "Clarence", "Sean", "Philip", "Chris", "Johnny", "Earl", "Jimmy", "Antonio",
    "Alice", "Julie", "Heather", "Teresa", "Doris", "Gloria", "Evelyn", "Jean", "Cheryl", "Mildred", "Katherine",
    "Joan", "Ashley", "Judith", "Rose", "Janice", "Kelly", "Nicole", "Judy", "Christina", "Kathy", "Theresa", "Beverly",
    "Denise", "Tammy", "Irene", "Jane", "Lori", "Rachel", "Marilyn", "Andrea", "Kathryn", "Louise", "Sara", "Anne",
    "Jacqueline", "Wanda", "Bonnie", "Julia", "Ruby", "Lois", "Tina", "Phyllis", "Norma", "Paula", "Diana", "Annie",
    "Lillian", "Emily", "Robin"
]


def generate_random_name_zh(name_size: int = None) -> str:
    """
    Generate a Chinese random name
    :param name_size: the size of first name
    :return: name text
    """
    if name_size is None:
        name_size = numpy.random.choice([1, 2])
    return numpy.random.choice(zh_family_name_list, p=zh_family_name_prob) + "".join(
        numpy.random.choice(zh_first_name_char_list, size=name_size)
    )


def generate_random_name_en(split_str: str = " ") -> str:
    """
    Generate a English random name
    :type split_str: Split between first name and last name
    :return: name text
    """
    return "{}{}{}".format(
        numpy.random.choice(en_first_name_list),
        split_str,
        numpy.random.choice(en_family_name_list)
    )


def dump_json(item, indent: int = 2):
    def default(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    return json.dumps(
        item,
        sort_keys=True,
        indent=indent,
        default=default
    )


class NameAlias:
    def __init__(self, name_generator=generate_random_name_zh):
        self.name_generator = name_generator
        self._name_pool = dict()
        self._name_set = set()

    def alias_name(self, uid: str) -> str:
        if uid in self._name_pool:
            return self._name_pool[uid]
        else:
            while True:
                alias = self.name_generator()
                if alias not in self._name_set:
                    break
            self._name_set.add(alias)
            self._name_pool[uid] = alias
            return alias
