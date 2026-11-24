# Research brief v2 — mở lại bài toán trước khi chọn giải pháp

Ngày đóng brief: 2026-11-09. Đây là brief của lượt khảo sát, chưa phải RQ cuối cùng của paper.

## Mục tiêu

Tìm hướng paper thực nghiệm có động cơ thực tế, nguồn dữ liệu kiểm chứng được và đóng góp phân biệt với công trình gần nhất. Không ràng buộc Server/Client boundaries, ba dimensions cũ hay kết quả có lợi cho SmartKit. Các runs cũ đã xóa; không tái sử dụng chúng làm bằng chứng.

## Câu hỏi khảo sát

1. Bằng chứng gốc hiện có chỉ ra những vấn đề nào khi coding agents sửa và mở rộng ứng dụng/repository thực tế; những vấn đề đó được đo bằng gì và có phản chứng nào?
2. Trong các nhóm vấn đề về bảo toàn hành vi, tiến hóa mã, chuẩn bị repository và tích hợp thay đổi, công trình gần nhất đã giải quyết đến đâu; câu hỏi nào còn có thể kiểm chứng mà không chỉ đổi framework hoặc metric?
3. Hướng nào phù hợp nhất để phát triển từ kinh nghiệm SmartKit thành nghiên cứu mới, cần dữ liệu gì, thí nghiệm nào có thể bác bỏ kỳ vọng, và điều kiện nào buộc bỏ/chuyển hướng?

## Góc nhìn độc lập

- Bảo toàn application/domain invariants và cross-layer consistency.
- Maintenance, change propagation, regression và long-horizon evolution.
- Public PR evidence, human rework và test reliability.
- Repository readiness/environment/architecture là điều kiện tác động; nhánh này do agent chính tra cứu.

## Nguyên tắc bằng chứng

Ưu tiên paper/dataset/repository gốc. Xác minh title/authors/year trên nguồn gốc; trích kết quả theo abstract/full text thực sự đọc. Ghi trạng thái preprint/peer review khi kiểm chứng được. Không dùng marketing/blog thứ cấp làm bằng chứng chính. Không suy ra causal effect từ PR observational data; không đồng nhất merged với correct. Không gọi dữ liệu synthetic là production. Không khẳng định novelty từ việc không tìm thấy bài.

## Sản phẩm

Báo cáo tiếng Việt, evidence ledger, ghi chú scout, so sánh 3–4 hướng và đề xuất bước thu thập bằng chứng đầu tiên. Chưa chạy model trả phí, chưa kết luận hiệu ứng can thiệp, chưa thay thesis.
