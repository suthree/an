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


class DataSourceChoice(models.IntegerChoices):
    """
    数据源 choice

    """

    DATA_SOURCE_EM = 1, "东方财富"
    DATA_SOURCE_THS = 2, "同花顺"


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
    source = models.IntegerField(
        choices=DataSourceChoice.choices, default=DataSourceChoice.DATA_SOURCE_EM, verbose_name="平台"
    )

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


# class FundInfo(CodeInfoBase):
#     """
#     基金 etf
#     TODO 暂时不研究

#     Args:
#         CodeInfoBase (_type_): _description_
#     """
#     class Meta:
#         db_table = "fund_info"


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


# class StockFund(IdActiveMixin):
#     """
#     个股与基金关系
#     """

#     stock = models.CharField(max_length=10, verbose_name="债券代码")
#     fund = models.CharField(max_length=10, verbose_name="基金名称")
#     date = models.DateField(verbose_name="关联日期")


#     class Meta:
#         db_table = "stock_bond"
#         unique_together = ["stock", "fund"]


class IndiVolChoice(models.TextChoices):
    """
    量变指标 choice
    """

    INDI_DAY_1 = "d1", "日线量变"
    INDI_MIN_30 = "m30", "30分钟线量变"


class StockMarketDay(IdMixin):
    """
    个股日线数据
    """

    code = models.CharField(max_length=10, verbose_name="代码")
    date = models.DateField(verbose_name="日期")

    pe = models.FloatField(verbose_name="市盈率")
    pb = models.FloatField(verbose_name="市净率")
    market_cap = models.FloatField(verbose_name="总市值")
    float_cap = models.FloatField(verbose_name="流通市值")

    open = models.FloatField(verbose_name="开盘价")
    close = models.FloatField(verbose_name="收盘价")
    low = models.FloatField(verbose_name="最低价")
    high = models.FloatField(verbose_name="最高价")
    average = models.FloatField(verbose_name="日均价")

    close_1 = models.FloatField(null=True, verbose_name="前收盘价")
    volume = models.FloatField(verbose_name="成交量")
    turnover = models.FloatField(verbose_name="成交额")

    change = models.FloatField(verbose_name="涨幅")
    change_rate = models.FloatField(verbose_name="涨幅")
    change_rate_5 = models.FloatField(verbose_name="5日涨幅")
    amplitude = models.FloatField(verbose_name="振幅")

    volume_rate = models.FloatField(verbose_name="量比")
    turnover_rate = models.FloatField(verbose_name="换手率")

    money_ma = models.FloatField(db_column="m_ma", verbose_name="主力资金")
    money_rate_ma = models.FloatField(db_column="mr_ma", verbose_name="主力资金比例")
    money_sb = models.FloatField(db_column="m_sb", verbose_name="超大单资金")
    money_rate_sb = models.FloatField(db_column="mr_sb", verbose_name="超大单资金比例")
    money_b = models.FloatField(db_column="m_b", verbose_name="大单净流入")
    money_rate_b = models.FloatField(db_column="mr_b", verbose_name="大单净流入比例")
    money_m = models.FloatField(db_column="m_m", verbose_name="中单资金")
    money_rate_m = models.FloatField(db_column="mr_n", verbose_name="中单资金比例")
    money_s = models.FloatField(db_column="m_s", verbose_name="小单资金")
    money_rate_s = models.FloatField(db_column="mr_s", verbose_name="小单资金比例")

    # indi
    indi_vol = models.CharField(
        db_column="i_vol",
        max_length=4,
        choices=IndiVolChoice.choices,
        default=IndiVolChoice.INDI_DAY_1,
        verbose_name="量变指标",
    )

    # indi_price = models.BooleanField(default=False, verbose_name="价格指标")
    # indi_chip_70
    class Meta:
        db_table = "stock_market_day"
        unique_together = ["code", "date"]


# hot order

# class StockMarketDayBid(IdMixin):
#     """
#     个股日线竞价数据
#     TODO 需要好好研究
#     """
#     code = models.CharField(max_length=10, verbose_name="代码")
#     date = models.DateField(verbose_name="日期")
#     volume_match = models.FloatField(verbose_name="匹配成交量")
#     volume_unmatch = models.FloatField(verbose_name="未匹配成交量")
#     turnover_match = models.FloatField(verbose_name="匹配成交额")
#     turnover_unmatch = models.FloatField(verbose_name="未匹配成交额")

#     class Meta:
#         db_table = "stock_market_day_bid"
#         unique_together = ["code", "date"]
