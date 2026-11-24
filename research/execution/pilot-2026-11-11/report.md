# Kết quả development smoke pilot, 11/11/2026

Đã hoàn tất 4/4 phiên agent trên một tác vụ development. Đây là kiểm tra khả năng thực hiện và quy trình, không phải dữ liệu nghiên cứu chính. Không ước lượng hiệu ứng layout hay test package từ bốn lượt này.

## Kết quả từng điều kiện

| Điều kiện | Layout | Thời gian agent (giây) | Acceptance | Preservation | Kiểm tra cuối |
|---|---|---:|---|---|---|
| S0V0 | Theo tầng/vai trò | 141.27 | True | True | 29 |
| S1V0 | Theo tính năng | 101.61 | True | True | 29 |
| S0V1 | Theo tầng/vai trò | 99.66 | True | True | 29 |
| S1V1 | Theo tính năng | 100.11 | True | True | 29 |

V0 có các checks cơ bản và scripts có sẵn; V1 bổ sung 10 preservation checks. Cả bốn có quyền công cụ thông thường và được tự viết tests. Model yêu cầu là GPT-6 Luna High, Standard mặc định, Codex CLI 0.166.0. Giới hạn 900 giây mỗi phiên. Model alias không chứng nhận một phiên bản weights bất biến.

## Phạm vi đánh giá

Bộ chấm cuối có 29 checks độc lập cho development pilot, gồm 16 acceptance và 13 preservation checks. Fixtures thưa theo người dùng, hai plans, nhiều orders cùng trạng thái và các ngày khác nhau; chúng khác cấu trúc với fixtures của bộ visible. Bộ chấm không có trong container agent và không trả kết quả để agent sửa tiếp. Chấm trong container sạch sau khi thu patch.

HTTP/DOM checks không chạy tương tác/hydration trình duyệt. Bộ chấm cuối kiểm tra ownership/history/status và việc đọc không đổi orders; nó không tái kiểm tra trực tiếp cancellation qua browser/server-action transport. V1 có checks cancellation với session/cache stubs. Do đó preservation pass chỉ có nghĩa trong phạm vi final checks đã thực hiện, không bảo đảm mọi hành vi của ứng dụng. Cần mở rộng oracle phù hợp với từng main task.

Trước model runs, cả hai unsolved baselines qua preservation và thất bại acceptance; cả hai reference implementations qua cả hai thành phần. Visible package qua 10/10 checks trên mỗi baseline chưa giải. Qualification không tiêu hạn mức model.

## Hạ tầng, provenance và sự cố

Từng phiên dùng container và PostgreSQL mới, không host bind mounts, Docker socket hay source history chứa lời giải. Auth ChatGPT được đặt ngoài application workspace, không dùng paid API key. Snapshot gốc và bản SmartKit của tác giả không bị agent sửa. File hashes và image IDs nằm trong manifests/isolation logs.

Có một lần setup S1V0 lỗi trước khi gọi model. Record và migrate log cũ được giữ. Readiness ban đầu dùng Unix socket, có thể báo ready ở temporary init server trước khi PostgreSQL nhận TCP. Gate đổi sang TCP và thêm lưu log DB; đây là giả thuyết có căn cứ về failure, không có DB log cũ để chứng minh nguyên nhân SQL. Lần setup-only retry được adjudicate riêng. Không chạy lại một agent outcome thất bại để chọn kết quả tốt hơn. Bản runner trước sửa còn ở pilot-v1.py.txt; mọi package, model, task, allocation và timeout giữ nguyên.

## Token và chi phí

summary.json giữ nguyên các usage events do CLI báo. Input/cached/output là trường token của provider, không quy đổi thành tiền API hoặc số quota Plus còn lại. Có thể có prompt caching và nhiễu hạ tầng; một lượt mỗi cell chưa cho phép kết luận package nào rẻ hơn.

## Bằng chứng và bước tiếp

Xem protocol.md, allocation.json, qualification-results.json, qualification-complete.json và manifests. Mỗi runs/<cell> có attempt.json, events.jsonl, final-message.txt, patch.diff, final-workspace.tgz, isolation.json và evaluation/result.json. Raw traces cần rà privacy trước khi công khai. summary.json ghi audit xem trace có chứa credential strings hay không mà không in giá trị credential.

Pilot này hỗ trợ quyết định tiếp tục kiểm tra Luna trên các development tasks đa dạng hơn. Nếu bốn cases đều pass, điều đó chỉ xác nhận một tác vụ mẫu có thể thực hiện trong cấu hình này; không chứng minh đủ năng lực cho mọi main task hoặc có khác biệt giữa điều kiện. Tiếp theo cần main task frame/provenance, oracle tương ứng và pilot precision/cost có repetitions phù hợp, rồi mới freeze protocol chính.
