# Tác vụ ghép: xác nhận trước khi đăng xuất

**Yêu cầu chung:** khi người đang đăng nhập chọn Đăng xuất trên dashboard, hiển thị lựa chọn xác nhận hoặc hủy. Xác nhận thực thi đăng xuất sẵn có và phải khiến người dùng không còn truy cập được dashboard trong ngữ cảnh đó. Hủy giữ nguyên phiên và quyền truy cập. Kiểm tra thao tác chuột và bàn phím.

Hai snapshot và môi trường giống [cặp đăng ký](registration-pair.md). Bản tham chiếu gọi xác nhận trước khi thực hiện thao tác sẵn có. Bản lỗi hiển thị cùng lời nhắc nhưng vẫn thực hiện đăng xuất khi hủy. SmartKit dùng nút đăng xuất của dashboard. Kit ngoài dùng form trong menu tài khoản. Bộ chạy tắt chỉ báo phát triển của Next.js để nó không chặn nút; thay đổi cấu hình và bản sửa thử được khôi phục sau khi chạy.

Mỗi ca dùng ngữ cảnh Chromium mới và một tài khoản tổng hợp. Bộ chạy đợi phản hồi của thao tác đăng xuất khi có, rồi dùng yêu cầu HTTP mới tới dashboard và kiểm tra thông tin phiên để xác minh kết quả. Hai phép hủy dùng hai tài khoản và thao tác chuột/bàn phím khác nhau. Chạy bằng `python -X utf8 research/execution/starter-kit-selection-2026-11-16/probe-registration.py --signout`. PostgreSQL dùng một container tự dọn, từ image có sẵn và dữ liệu trong RAM.

**Phạm vi của phép đo:** hủy là một nhánh mới của tác vụ. Lỗi hủy mà vẫn đăng xuất là lỗi *acceptance*. Đóng phiên và bảo vệ dashboard sau khi đăng xuất là hành vi có từ bản gốc và được kiểm tra riêng. Việc phép thử chỉ bấm xác nhận bỏ sót nhánh hủy chưa chứng minh lợi ích của gói kiểm tra bảo toàn hành vi cũ. Muốn nhận cặp vào so sánh gói kiểm tra, cần xác minh thêm một hồi quy của nghĩa vụ đã tồn tại trên cả hai kit, với bộ kiểm tra cơ bản và bộ chấm cuối đúng phạm vi.

## Kết quả

Chạy hoàn tất [12 ca](signout-probe.json), gồm hai kit, ba biến thể và hai vòng với DB mới. Hai vòng cho cùng kết quả trên cả hai kit.

| Biến thể | Hộp xác nhận | Phiên sau khi xác nhận | Phiên sau khi hủy, mở hộp bằng chuột hoặc bàn phím |
| --- | --- | --- | --- |
| Bản gốc | Không xuất hiện | Đăng xuất trực tiếp | Không áp dụng |
| Bản tham chiếu | Có | Kết thúc, dashboard yêu cầu đăng nhập | Giữ nguyên và vẫn vào được dashboard |
| Bản lỗi | Có | Kết thúc, dashboard yêu cầu đăng nhập | Kết thúc dù đã hủy |

Cặp khả thi về yêu cầu chung và về phép chấm hành vi qua dashboard. Bản lỗi ở bảng này làm hỏng nhánh hủy mới.

## Kiểm chứng bổ sung về bảo toàn phiên

Một biến thể lỗi riêng hiển thị hộp xác nhận, xử lý hủy đúng, và chuyển tới trang đích thông thường sau khi xác nhận. Biến thể bỏ thao tác kết thúc phiên. Đây là hồi quy của chức năng đăng xuất sẵn có: sau khi người dùng đã thực hiện đăng xuất, phiên đó không còn được vào dashboard.

Chạy `python -X utf8 research/execution/starter-kit-selection-2026-11-16/probe-registration.py --signout-preservation`. [Dữ liệu 12 ca](signout-preservation-probe.json) bao gồm hai kit, ba biến thể, và hai vòng độc lập về dữ liệu. Trong cả bốn ca lỗi, thao tác xác nhận chuyển trang đúng nhưng yêu cầu mới tới dashboard vẫn thành công và endpoint phiên vẫn trả về đúng tài khoản. Với bản gốc và bản tham chiếu, phiên kết thúc và dashboard yêu cầu đăng nhập lại. Bản tham chiếu và bản lỗi đều giữ phiên khi hủy.

Quan sát chuyển trang đơn thuần bỏ sót lỗi, trong khi phép kiểm phiên và truy cập lại dashboard phân biệt được bản tham chiếu với bản lỗi. Cặp này có bằng chứng bước đầu cho phép so sánh gói kiểm tra bảo toàn. Còn phải xác nhận lỗi vượt toàn bộ bộ kiểm tra cơ bản dự kiến và bị phát hiện bởi gói cấp agent cũng như bộ chấm giữ kín khi hai bộ được hoàn thiện. Chưa kiểm chứng layout thứ hai, chưa chạy phiên coding agent.
