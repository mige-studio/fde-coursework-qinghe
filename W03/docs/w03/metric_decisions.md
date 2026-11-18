# 指标核定与未决项

## 采用依据和边界

适用青禾本周合成数据，覆盖2024-09-01含至2026-09-01不含。统计对象是CRM账户，不做跨系统自然人去重。下面为Codex依据材料的核对记录，不是用户本人或真实客户验收。最终38项逐项定义、依赖与连续原句来源见artifacts/w03/library/catalog.json及同目录语义模型；完整目标见customer/w03/targets.json。

| 指标族 | 采用依据 | 重点核定 | 独立验证题 |
|---|---|---|---|
| 订单、金额、账户、商品件数16项 | materials/w03/01_订单日报说明.md、05_数据字典.md | paid包括后续全退；有效须净额正；退款归原订单日期；件数是有效订单原始件数，不推算退货件数 | orders-16、12种分组、渠道与成交店组合筛选 |
| 8项比率/均值 | 02_财务邮件.md | 分母逐项对应，金额保留整数分，展示元换算；零分母null | ratios-8、零购买月份 |
| 注册1项 | 03_会员运营周报.md | 按注册时间，归属店与等级，不是订单成交店 | registrations、registered-home-tier |
| 观测首购及后续4项 | 同上 | 全覆盖历史内先筛有效再按日期/单号排序，再筛查询期；不是终身首购，也不是月内复购人数 | first-and-later、first-early-window |
| 月内购买/复购3项 | 同上当前调整版本 | 分母为当月有效购买账户，不能沿旧草稿用全部注册会员；整月全范围，多月逐月，不能相加冒充跨月去重 | all-member-month、two-months |
| 付费月报6项 | 04_本期统计确认邮件.md、本人W3小林/陈姐原问答09材料 | 年卡/家庭季卡资格，端点、多卡去重，月底判资格后取整月有效订单；等级不代替卡资格 | paid-six、two-months、零月、整月限制及规模同义问法 |

## 独立期望与比较方式

customer/w03/reference_all.py独立读取4张原CSV，核对manifest哈希、行数及主键，以原始记录计算全部38项与分组结果；付费细节由paid_reference.py核算。它不读取被测SQL、生成库或产品答案。期望先保存，实际问数后不按结果改数字。

所有用例核对status、指标、时间、分组、筛选、数据版本、单位、按列名映射的分组行及数字。整数精确比较；非整数按明确容差；null不等于0。仅将时间维度的午夜ISO表示与同一天日期规范化，不忽略其他时刻。行列重排可以等价，缺组/重组不得通过。

第一次全量对照发现我们独立期望把商品件数标为count，而产品为items；01原文明确是quantity件数，修正独立核算单位为items，数值未改，保留v1与v2。这个属于期望元数据错误，不能算作产品算错。v3在已冻结v2基础上增加4道拒绝/澄清题，未按产品回答改期望。

## 冲突、未决与不支持

旧复购分母被本期周报显式替代，有版本依据。小林统计选择与陈姐日期规则互补，不把职责差异伪造为冲突。多卡资格去重明确，但真实卡费分账、真实覆盖完整性和生产权限仍未知；这些未知不阻止规定的合成订单计算，也不能据测试反推生产已具备。

缺时间和含糊复购先澄清；覆盖外、未知筛选值、未定义指标、整月指标拆门店或非整月查询须明确拒绝；营销触达不在本期能力内。缺记录不自动填零。预算、合同、验收、效果目标见sow.md，不是统计指标待补定义。

## 失败、修订与复测

| 轮次 | 发现 | 所属问题与处理 | 保留证据 |
|---|---|---|---|
| build-v1/v2 | 连续引用不精确；v2候选首单顺序与月粒度还有风险 | 修学生方法，补逐字索引、先有效后排序、月汇总粒度 | 各次input/response和检查文件 |
| build-v3、小样本全量v1 | 25/27，件数单位期望错；归属门店实体ID原生查询失败 | 期望按原定义修单位；生成方法要求订单直接保留归属门店角色外键，仍一订单一行，不联多卡 | test-small-full-v1及trace db9f5761-eb60-4b43-a8f6-7e959f6f696f |
| 规模v1 | 11/11，但未覆盖归属店ID失败路径 | 只证明该版这11题；新库仍须重新回归 | test-large-v1 |
| build-v4 | 自定义query_policy键超出契约 | 学生方法只允许full_month_only布尔键，其他解释写constraints | build-v4，未发布 |
| build-v5 | SQL引用未声明的r别名 | 学生方法增加别名逐项检查与明确ON关系，重新真实生成，不手改SQL | build-v5，未发布 |

build-v7再次被一处来源原句改写拒绝；随后改为在本人既有build-v3原样生成稿上限定增量修订，避免无关定义漂移。基线仅是既有工程输出，不作为业务证据；未注入实际答案。build-v8真实调用模型后，差异仅为order_fact新增账户归属门店连接及外键，catalog、38项指标公式与其他模型完全一致。来源、粒度、12维度和原生编译检查通过；单输入merge定稿，旧库留存library-v3。全量复测另附，旧失败不覆盖。

## 38项目标与独立题目对应（目标清单，不是通过声明）

| 指标 | 验证题编号 |
|---|---|
| 创建订单数（order_count） | orders-16 |
| 支付订单数（paid_order_count） | orders-16 |
| 有效订单数（valid_order_count） | orders-16, filter-channel-store |
| 取消订单数（cancelled_order_count） | orders-16 |
| 退款订单数（refund_order_count） | orders-16 |
| 部分退款订单数（partial_refund_order_count） | orders-16 |
| 全额退款订单数（full_refund_order_count） | orders-16 |
| 实付金额（payment_cents） | orders-16 |
| 退款金额（refund_cents） | orders-16 |
| 净销售额（net_sales_cents） | orders-16, dimension-store, dimension-store__region, dimension-store__store_name, dimension-home_store等 |
| 支付订单原价金额（gross_cents） | orders-16 |
| 优惠金额（discount_cents） | orders-16 |
| 购买会员数（buyer_count） | orders-16 |
| 退款会员数（refund_buyer_count） | orders-16 |
| 成交门店数（selling_store_count） | orders-16 |
| 有效订单商品件数（valid_order_items） | orders-16 |
| 有效订单均额（avg_order_value） | ratios-8 |
| 购买会员人均消费（avg_buyer_value） | ratios-8 |
| 购买频次（purchase_frequency） | ratios-8 |
| 退款金额占比（refund_amount_rate） | ratios-8 |
| 取消率（cancel_rate） | ratios-8 |
| 退款订单率（refund_order_rate） | ratios-8 |
| 优惠率（discount_rate） | ratios-8 |
| 单均商品件数（items_per_order） | ratios-8 |
| 注册会员数（new_member_count） | registrations, registered-home-tier |
| 观测期首购会员数（first_buyer_count） | first-and-later, first-early-window |
| 观测期首单净销售额（first_order_sales_cents） | first-and-later, first-early-window |
| 观测期首单数（first_order_count） | first-and-later, first-early-window |
| 观测期后续购买订单数（repeat_order_count） | first-and-later, first-early-window |
| 月内购买会员数（monthly_buyer_count） | all-member-month, two-months |
| 月内复购会员数（monthly_repeat_buyer_count） | all-member-month, two-months |
| 月内复购率（monthly_repeat_rate） | all-member-month, two-months |
| 月末付费会员购买人数（monthly_paid_buyer_count） | paid-six, two-months, paid-zero-month-2024-09 |
| 月末付费会员有效订单数（monthly_paid_order_count） | paid-six, two-months, paid-zero-month-2024-09 |
| 月末付费会员净销售额（monthly_paid_sales_cents） | paid-six, two-months, paid-zero-month-2024-09 |
| 月末付费会员复购人数（monthly_paid_repeat_buyer_count） | paid-six, two-months, paid-zero-month-2024-09 |
| 月末付费会员复购率（monthly_paid_repeat_rate） | paid-six, two-months, paid-zero-month-2024-09 |
| 月末付费会员订单均额（monthly_paid_avg_order_value） | paid-six, two-months, paid-zero-month-2024-09 |


## 最终验证结论（2026-11-18）

- 定稿为build-v8经merge生成的library；全部38项、12项目标维度通过构建检查，小样本和规模分别新加载qinghe-small-v2/large-v2。
- 小样本实际自然语言31/31结构化比较通过，覆盖38项、12分组、联合筛选、首购窗口、跨月、零/null、澄清与拒绝；规模3万账户/30万订单11/11通过，覆盖38项和多种问法。独立期望均在本次查询前保存，未把实际结果当标准答案。
- 新版原Edge网页按账户归属门店查数成功，S01 546.50元、S02 456.50元、S03 0，合计1003元，与独立核算一致。证据qinghe_home_store_ui_run；原六项网页演示另保留。
- 错误注入15/15达到预期：3个等价正例通过、12个错误反例拒绝；包括错误指标/日期/筛选/分组、单位、比例、null、数值、状态、版本、缺组/重组。输入来自新版已核对实际结果的副本，原报告未改；它们是人为模拟错误，不冒充模型实发事故。
- 独立核算及判定单元验证10项和5个子例通过。教师tools/platform/product共47文件与原包哈希一致，未改老师引擎。
- **解释单独核对：42题已逐题读取，小样本31题未发现实质错误；规模paid-six有1次均额172.16→应172.17的舍入错误**。另两个同口径问法输出正确，原偏差仍留存；详见[解释核对](answer_review.md)，不能用42题结构化通过替代解释验收。
- 本材料支持课程限定范围内的能力演示，不证明真实数据、合同批准或收益。未向课程平台提交W03，待用户看学习结论及范围。

证据：test-small-full-v2/metric_test_report.json（选作根汇总）、test-large-v2/metric_test_report.json、judge-checks-v2/summary.json、teacher_original_check.json。每题含自然语言原问题、意图、查询、结果、解释、版本及比较差异；具体模型调用耗时在trace.seconds，未虚构响应SLA。失败与修订记录均保留。
