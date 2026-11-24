# Research canon

## Literature facts

- L1: Gloaguen et al. 2026, arXiv:2602.11988v3: context files không nhìn chung cải thiện task success trong thiết lập được đánh giá. Không suy ra mọi instructions vô ích.
- L2: Zhu et al. 2026, arXiv:2610.38244v1: nghiên cứu default preferences, repository precedents và task instructions. Instructions/examples không phải hướng chưa được nghiên cứu.
- L3: Dente et al. 2026, arXiv:2605.06445v2: nghiên cứu structural constraints, behavioral tests và static verifiers trong backend coding. Không lấy rubric/framework constraints tự thân làm novelty.
- L4: Patel et al. 2026, arXiv:2606.21804v2: downstream success không được giải thích đầy đủ bởi static metrics trong thiết lập CodeThread. Không dùng làm bằng chứng causality cho feature folders.
- L5: Zhao et al. 2026, arXiv:2607.22880v1: quan hệ proxy test metrics và bug detection phụ thuộc setting. Không phủ định mọi coverage/mutation measurement.
- L6: Borg et al. 2026, DOI 10.1007/s10664-026-10889-1: không phát hiện bất lợi downstream có hệ thống trong setting human-assisted/human-evolved. Không đồng nhất với autonomous agents.

## Experimental facts

- E1: tác giả đã bảo vệ thesis; muốn paper có bằng chứng thật. Các runs cũ đã xóa theo lời tác giả; không có fresh experimental outcomes.
- E2: local SmartKit snapshot 2c92d3920d967b9ebf0960ba7890754baa3c90d7 có feature layout, auth/billing/email và tests. Đã đọc source, chưa chạy baseline trong dự án paper này.
- E3: sáu task candidates là constructed, unvalidated; không có task historical đã được xác minh end-to-end.

## Supervisor constraints

Giáo sư muốn tác giả viết paper từ thesis, theo thông tin tác giả cung cấp. Không có yêu cầu venue, số trang, cỡ mẫu hay deadline nào được xác nhận.

## Terminology

Starter kit = mã ứng dụng khởi đầu; scaffold trong proposal chỉ source organization, không phải agent harness. Behavioral preservation = các yêu cầu cũ vẫn còn hiệu lực được kiểm tra qua executable observations. Joint success = chức năng mới đạt và preservation đạt trong phạm vi oracle.

## Forbidden claims

SmartKit tốt hơn; dữ liệu chứng minh hiệu ứng; novelty đầu tiên; FSD là Next.js requirement; baseline đã chạy; mọi test pass bảo đảm đúng tuyệt đối; khái quát ra mọi SaaS/framework; claims productivity hoặc human maintainability khi không đo.

## Unresolved

Baseline health; khả năng chuyển layout tương đương; task provenance/diversity; exact feedback package; novelty ở artifact level; agents/budget/sample size; independent replication. Tất cả phải xuất hiện đúng mức trong proposal.
