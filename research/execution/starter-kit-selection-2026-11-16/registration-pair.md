# Tác vụ ghép: siết chính sách mật khẩu khi đăng ký

Hai kit: SmartKit (bản tác vụ A04, layout theo tính năng, điều kiện chỉ cấp kiểm tra cơ bản) và Next.js SaaS Starter (snapshot ghi trong [hồ sơ runtime](runtime-feasibility.md)). Đây là một tác vụ ghép mới, chỉ lấy phần đăng ký của A04.

- Người chưa đăng nhập phải dùng mật khẩu có độ dài tối thiểu 12 khi đăng ký qua luồng tài khoản sẵn có. Ở hai biên được kiểm tra, mật khẩu 11 ký tự ASCII bị từ chối và không tạo tài khoản, còn mật khẩu 12 ký tự tạo được tài khoản.
- Người dùng đã đăng ký trước thay đổi và đã đủ điều kiện đăng nhập theo kit của mình vẫn đăng nhập được bằng mật khẩu cũ. Phép thử dùng hai tài khoản đã tạo từ bản gốc, với mật khẩu 10 và 11 ký tự.
- Giữ nguyên xác minh email của SmartKit. Để cô lập phép thử và không gửi email, thiết lập trạng thái đã xác minh trực tiếp cho các tài khoản thử trước khi kiểm tra đăng nhập. Với kit ngoài, tạo tài khoản và dùng quy trình đăng nhập sẵn có.

## Cách kiểm chứng

[Script chạy thử](probe-registration.py) dùng Chromium với ngữ cảnh mới cho từng lần gửi form. Khi kiểm tra đăng ký, script đối chiếu kết quả với bảng người dùng trong PostgreSQL. Với đăng nhập, script kiểm tra danh tính tài khoản trong phản hồi phiên. Mỗi vòng khởi tạo và migrate một DB mới cho từng kit, tạo các tài khoản cũ trên bản gốc rồi kiểm tra bản gốc, bản sửa tham chiếu và bản sửa gây hồi quy trên cùng DB với tài khoản mới riêng theo biến thể. Mã tham chiếu chỉ áp dụng quy tắc 12 ký tự tại đăng ký. Bản lỗi áp dụng thêm quy tắc đó tại đăng nhập.

Smoke check cơ bản dùng tài khoản mới có mật khẩu 12 ký tự. Kiểm tra bổ sung dùng tài khoản cũ với 10 ký tự. Bộ chấm thử dùng tài khoản khác có mật khẩu cũ 11 ký tự và kiểm tra biên đăng ký. Đây là ba phép thử mô phỏng vai trò của các bộ kiểm tra. Chúng chưa phải toàn bộ bộ kiểm tra cơ bản, gói cấp agent hay bộ chấm cuối của nghiên cứu hai kit.

SmartKit được sao chép từ `research/execution/main48/packages/A04/S1V0`, bỏ `.env` của gói. Kit ngoài dùng checkout cục bộ đã chuẩn bị ở lượt kiểm chứng runtime. Script yêu cầu hai checkout tạm có sẵn dependency theo lockfile ở dưới thư mục temp của Windows, lần lượt tại `paper-paired-registration/smartkit` và `paper-external-kit-6e33e58`. Cần Node, pnpm, Python Playwright với Chromium và image `postgres:18` có sẵn. Chạy `python -X utf8 research/execution/starter-kit-selection-2026-11-16/probe-registration.py` từ thư mục Paper.

## Kết quả

Cả hai vòng trên mỗi kit cho cùng kết quả. [Dữ liệu 12 ca](registration-probe.json) gồm hai kit, ba biến thể và hai vòng, với các kiểm tra qua luồng đăng ký và đăng nhập thật.

| Biến thể | Đăng ký mới 11 ký tự | Đăng ký mới 12 ký tự | Đăng nhập tài khoản mới 12 ký tự | Đăng nhập tài khoản cũ 10 và 11 ký tự |
| --- | --- | --- | --- | --- |
| Bản gốc | Tạo tài khoản | Tạo tài khoản | Đạt | Cả hai đạt |
| Bản sửa tham chiếu | Không tạo tài khoản | Tạo tài khoản | Đạt | Cả hai đạt |
| Bản sửa gây hồi quy | Không tạo tài khoản | Tạo tài khoản | Đạt | Cả hai trượt |

**Kết luận:** cặp đăng ký đáp ứng kiểm chứng khả thi bước đầu trên cả hai kit. Smoke check đăng nhập tài khoản mới bỏ sót lỗi đã cài, còn cả hai phép kiểm bằng tài khoản cũ phát hiện lỗi. Tác vụ vẫn cần bộ kiểm tra cơ bản hoàn chỉnh, một bộ chấm cuối với thêm tình huống phản biện và kiểm tra layout thứ hai nếu giữ phép so sánh tổ chức mã.

Mỗi lượt dùng một container PostgreSQL từ image có sẵn, với dữ liệu trong tmpfs và tự xóa khi dừng. Next.js chạy trên máy chủ local. Không tạo image hoặc volume lưu trữ mới trong Docker. Không có phiên coding agent hay dữ liệu hiệu ứng.

## Kiểm tra khả năng mở rộng tập tác vụ

Đọc mã trên cùng hai snapshot để sàng lọc các cặp ngoài tác vụ đăng ký. Các mục sau là yêu cầu giả định do nghiên cứu xây dựng.

| Ứng viên | Hành vi nền quan sát từ mã | Điều phải kiểm chứng |
| --- | --- | --- |
| Xác nhận trước khi đăng xuất | Cả hai dashboard có thao tác đăng xuất trực tiếp. SmartKit gọi client auth; kit ngoài gọi server action từ menu tài khoản. | Cùng thao tác xác nhận/hủy cho người đã đăng nhập. Hủy giữ quyền truy cập dashboard trong phiên hiện tại. Xác nhận kết thúc phiên và dashboard yêu cầu đăng nhập lại. Cần chạy luồng nền và xác nhận gói bổ sung có thể bắt lỗi làm nút hủy vô tình gửi form mà kiểm tra cơ bản bỏ sót. |
| Hiện/ẩn mật khẩu khi đăng nhập | Cả hai form mặc định che mật khẩu và chưa có nút hiện/ẩn trong snapshot đã đọc. | Nút hoạt động bằng bàn phím, giữ nguyên giá trị đã nhập và không gửi form. Đăng nhập hợp lệ vẫn hoạt động. Cần xác định lỗi bảo toàn mà gói kiểm tra bắt được. Yêu cầu tập trung ở giao diện đăng nhập nên khả năng phân biệt hai cách tổ chức mã cần được xem xét riêng. |

Đăng xuất đã qua [kiểm chứng chức năng bước đầu trên cả hai kit](signout-pair.md). Tác vụ hiện/ẩn vẫn chỉ qua sàng lọc nguồn. Hai ứng viên này vẫn tập trung vào tài khoản và xác thực.

Điều kiện nhận kit vào thí nghiệm chính: có tập cặp tác vụ đủ để trả lời câu hỏi trong phạm vi đã mô tả; kiểm chứng trên cả hai kit với bộ kiểm tra cơ bản, gói bổ sung và bộ chấm giữ kín đã chốt; xác định các layout giữ cùng hành vi nếu ước lượng hiệu ứng tổ chức mã; sau đó chọn số lần lặp và báo độ chính xác dự kiến. Số cặp tối thiểu và phân bổ chưa chốt. Nếu sau sàng lọc và kiểm chứng không đủ cặp, áp dụng Q16 để đánh giá ứng viên Next.js SaaS khác.
