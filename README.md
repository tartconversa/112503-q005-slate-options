# 剧集组合预订与分阶段投拍

片单委员会的企划、历史窗口和合同承诺。金额为人民币万元。scenario_id 绑定同一个市场状态下的多项假设，不能在不同项目间任意换用。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- projects.csv 的字段为 project、kind、market、delivery_due、option_until、plan。
- stages.csv 的字段为 stage、project、quarter、cost、condition、resource、first、last、max_delay_days。
- reservations.csv 的字段为 commitment、project、resource、start、stop、fee_paid、cancel_fee、settlement、state。
- history.csv 的字段为 comparable、kind、market、channel、settled_quarter、min_guarantee、total_received、days_late。
- offers.csv 的字段为 offer、package、project、market、minimum、receipt_quarter、expiry、rev。
- scenarios.csv 的字段为 scenario_id、market、quarter、receipt_factor、delay_days。
- committee.csv 的字段为 decision、project、reported、quarter、cash_cap、kind、signal。
- committee_limits.csv 的字段为 quarter、cash_available、min_regional_short、min_member_long、as_of。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
