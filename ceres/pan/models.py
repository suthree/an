from django.db import models


class DateTimeMixin(models.Model):
    """
    时间 mixin

    """

    create_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


STATE_DELETE = 0
STATE_NORMAL = 1
CHOICE_STATE = ((STATE_DELETE, "删除"), (STATE_NORMAL, "正常"))


class StateMixin(models.Model):
    """
    状态mixin

    Args:
        models (_type_): _description_
    """

    state = models.IntegerField(choices=CHOICE_STATE, default=STATE_NORMAL, verbose_name="关系类型")

    class Meta:
        abstract = True


class ActiveMixin(models.Model):
    """
    是否有效 mixin

    Args:
        models (_type_): _description_
    """

    is_active = models.BooleanField(default=True, verbose_name="是否删除")

    class Meta:
        abstract = True


class IdMixin(models.Model):
    """
    主键id mixin

    Args:
        models (_type_): _description_
    """

    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class IdActiveMixin(IdMixin, ActiveMixin):
    """
    主键id 有效 mixin

    Args:
        models (_type_): _description_
    """

    class Meta:
        abstract = True


DATA_SOURCE_EM = 1
DATA_SOURCE_THS = 2
CHOICE_SOURCE = (
    (DATA_SOURCE_EM, "东方财富"),
    (DATA_SOURCE_THS, "同花顺"),
)


class CodeInfoBase(IdActiveMixin):
    """
    代码基类
    code 代码
    name 现用名
    names 曾用名 拼音缩写 首字母查询
    source 同花顺 东财
    is_active 是否有效(退市)
    """

    code = models.CharField(max_length=10, db_index=True, verbose_name="代码")
    name = models.CharField(max_length=10, verbose_name="名称")
    names = models.TextField(verbose_name="搜索")
    date = models.DateField(verbose_name="日期")
    source = models.IntegerField(choices=CHOICE_SOURCE, default=DATA_SOURCE_EM, verbose_name="平台")

    class Meta:
        abstract = True


class StockInfo(CodeInfoBase):
    """
    股票

    Args:
        CodeInfoBase (_type_): _description_
    """

    class Meta:
        db_table = "stock_info"


class TopicInfo(CodeInfoBase):
    """
    题材

    Args:
        CodeInfoBase (_type_): _description_
    """

    class Meta:
        db_table = "topic_info"


class BondInfo(CodeInfoBase):
    """
    转债

    Args:
        CodeInfoBase (_type_): _description_
    """

    class Meta:
        db_table = "bond_info"


class FundInfo(CodeInfoBase):
    """
    基金 etf
    TODO 暂时不研究

    Args:
        CodeInfoBase (_type_): _description_
    """

    market_cap = models.CharField(verbose_name="总市值")
    float_cap = models.CharField(verbose_name="流通市值")

    class Meta:
        abstract = True
        # db_table = "fund_info"


class StockTopic(IdActiveMixin):
    """
    个股与题材的关系
    """

    stock = models.CharField(max_length=10, verbose_name="题材代码")
    topic = models.CharField(max_length=10, verbose_name="题材名称")
    date = models.DateField(verbose_name="关联日期")

    class Meta:
        db_table = "stock_topic"
        unique_together = ["stock", "topic"]


class StockBond(IdActiveMixin):
    """
    个股与转债的关系
    """

    stock = models.CharField(max_length=10, verbose_name="债券代码")
    bond = models.CharField(max_length=10, verbose_name="债券名称")
    date = models.DateField(verbose_name="关联日期")

    class Meta:
        db_table = "stock_bond"
        unique_together = ["stock", "bond"]


class StockMarketDay(IdMixin):
    """
    个股日线数据
    """

    stock = models.CharField(max_length=10, verbose_name="代码")
    date = models.DateField(verbose_name="日期")

    open = models.CharField(verbose_name="开盘价")
    close = models.CharField(verbose_name="收盘价")
    high = models.CharField(verbose_name="最高价")
    low = models.CharField(verbose_name="最低价")
    close_1 = models.CharField(verbose_name="前收盘价")
    volume = models.CharField(verbose_name="成交量")
    turnover = models.CharField(verbose_name="成交额")

    # increase = models.CharField(verbose_name="涨幅")
    increase_rate = models.CharField(verbose_name="涨幅")
    amplitude_rate = models.CharField(verbose_name="振幅")
    turnover_rate = models.CharField(verbose_name="换手率")

    pe = models.CharField(verbose_name="市盈率")
    pb = models.CharField(verbose_name="市净率")
    market_cap = models.CharField(verbose_name="总市值")
    float_cap = models.CharField(verbose_name="流通市值")

    money_ma = models.CharField(db_column="m_ma", verbose_name="主力资金")
    money_ma_rate = models.CharField(db_column="m_ma_r", verbose_name="主力资金比例")
    money_sb = models.CharField(db_column="m_sb", verbose_name="超大单资金")
    money_sb_rate = models.CharField(db_column="m_sb_r", verbose_name="超大单资金比例")
    money_b = models.CharField(db_column="m_b", verbose_name="大单净流入")
    money_b_rate = models.CharField(db_column="m_b_r", verbose_name="大单净流入比例")
    money_m = models.CharField(db_column="m_m", verbose_name="中单资金")
    money_m_rate = models.CharField(db_column="m_m_r", verbose_name="中单资金比例")
    money_s = models.CharField(db_column="m_s", verbose_name="小单资金")
    money_s_rate = models.CharField(db_column="m_s_r", verbose_name="小单资金比例")

    # TODO 常用的入库
    # hot_order, chip_70
    indi_vol = models.CharField(verbose_name="量变指标")  # d1, m30
    indi_price = models.BooleanField(default=False, verbose_name="价格指标")
    # 临时的 redis

    class Meta:
        db_table = "stock_market_day"
        unique_together = ["stock", "date"]


class StockMarketDayBid(IdMixin):
    """
    个股日线竞价数据
    TODO 需要好好研究
    """

    stock = models.CharField(max_length=10, verbose_name="代码")
    date = models.DateField(verbose_name="日期")
    volume_match = models.CharField(verbose_name="匹配成交量")
    volume_unmatch = models.CharField(verbose_name="未匹配成交量")
    turnover_match = models.CharField(verbose_name="匹配成交额")
    turnover_unmatch = models.CharField(verbose_name="未匹配成交额")

    class Meta:
        abstract = True
