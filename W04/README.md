# 第四周 青禾会员复购演示

[下载第四周完整作业（ZIP）](../packages/w04-submit.zip)

本次承接第三周的查询库，把青禾的新 CRM 导出接入运营助手。八月有 5,473 个会员账户发生有效购买，646 个在月内复购，复购率为 11.80%。部分旧 POS 门店的交易缺失，结果仅限本次接入范围。

解压后可按以下顺序复核。

1. 阅读 docs/w04/data_diagnosis.md，查看来源、隔离记录与运营工作账对照。
2. 阅读 docs/w04/demo_plan.md，再看 artifacts/w04/demo_run.json 中同一问题的两次真实查询及回答。
3. 用 artifacts/w04/adapter_test_report.json 查看两次独立导入对账，用 metrics_run.json 查看 38 项指标的八月结果。
4. customer/w04 含适配源码、单元测试、回答提示和逐指标运行入口，配合老师的第四周工程使用。
