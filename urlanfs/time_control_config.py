#-*- coding: utf-8 -*-

# 时间段配置文件
# 每天为一个周期

# in_section_direct: True 是时间段内重定向, False 是时间段内正常代理, 时间段外重定向
# 注意True, False首字母大写
in_section_direct = True

# 优先级0(最高)
# 包含日期和时间的区间定义, 24小时制, 可以精确到秒
# example:
#datetime_sections = [
#    ("2012.3.3 12:00", "2012.3.3 14:00"),
#    ("2012.3.4 00:00:00", "2012.3.5 23:59:59"),
#]
datetime_sections = [
    ("2012.3.4 2:00", "2012.3.4 0300"),
    ("2012.3.5 0:00", "2012.3.8 14:00"),
]

# 优先级1
# 每日循环时间段定义, 24小时制, 可以精确到秒
# 遇到 24:00 点的时间段, 因为和 0:00 无法区分, 所以要写成 23:59:59
# 遇到跨0:00或者24:00的时间段,可以分开定义 xx:xx - 23:59:59, 0:00 - yy:yy
# example:
#everyday_sections = [
#    ("12:00", "14:00"),
#    ("18:12:34", "20:34:56"),
#]
everyday_sections = [
    ("12:00", "14:00"),
    ("02:35:00", "08:00:00"),
]