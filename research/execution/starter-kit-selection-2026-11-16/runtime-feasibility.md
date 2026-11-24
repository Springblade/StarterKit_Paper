# Kiểm chứng bước đầu cho Next.js SaaS Starter

**Kết luận:** giữ `nextjs/saas-starter` làm ứng viên cho kit thứ hai. Runtime cục bộ và luồng tài khoản đã qua kiểm tra bước đầu. Cần xác minh tập tác vụ ghép, bộ chấm và, nếu giữ phép so sánh tổ chức mã, hai layout trước khi nhận kit vào thí nghiệm chính.

## Nguồn và môi trường

- Repository: [Next.js SaaS Starter](https://github.com/nextjs/saas-starter), snapshot `6e33e58b1e553a41fe22e6b941a7229a002de361` như trong [hồ sơ sàng lọc](findings.md).
- Next.js 15.6.0-canary.59 với Turbopack trên Windows, Node 24.15.0, pnpm 12.16.1. Cài theo lockfile với `pnpm install --frozen-lockfile`. Next.js tự cập nhật `tsconfig.json` trong checkout tạm khi khởi động; đây là thay đổi duy nhất trên các tệp được Git theo dõi.
- Một container tạm từ image `postgres:18` có sẵn, chỉ mở cổng trên loopback. Thư mục dữ liệu dùng tmpfs giới hạn 256 MiB, không gắn thư mục host. Dùng migration có sẵn qua `pnpm db:migrate`; tạo dữ liệu bằng đăng ký qua giao diện. Không chạy setup/seed Stripe và không dùng thông tin xác thực Stripe thật.

## Quan sát

| Kiểm tra | Kết quả |
|---|---|
| Migration và khởi động dev server | Migration thành công. Next.js phục vụ trang đăng ký và dashboard. |
| Đăng ký tài khoản thử | Form đăng ký đưa người dùng tới dashboard; PostgreSQL ghi nhận tạo nhóm và đăng ký. |
| Sửa tên | Form General Settings báo lưu thành công. PostgreSQL lưu tên gồm cả khoảng trắng ở hai đầu và ghi nhận sự kiện cập nhật. |
| Đặt lại dữ liệu | Xóa dữ liệu ở năm bảng ứng dụng trong DB thử và đặt lại bộ đếm ID. Số user, team và activity log đều về 0. Dùng ngữ cảnh trình duyệt mới cho lượt kế tiếp. |
| Luồng sau reset | Truy cập dashboard khi chưa đăng nhập chuyển về trang đăng nhập. Đăng ký lại cùng email với mật khẩu thử 10 ký tự thành công. Ngữ cảnh trình duyệt sạch khác đăng nhập được bằng tài khoản đó, và PostgreSQL ghi nhận sự kiện đăng nhập. |

Các bước trên kiểm tra được một lần reset dữ liệu ứng dụng, với một dev server chạy xuyên suốt. Chưa kiểm tra cold start/reset nhiều vòng, production build, Stripe checkout/webhook hay tính tương đương của hai layout. Không chạy phiên coding agent. Sau kiểm tra đã dừng Next.js và xác nhận container PostgreSQL thử được tự xóa. Không tạo image hay volume lưu trữ mới.

## Đối chiếu tác vụ

Đối chiếu với [task cards SmartKit](../main48/task-cards.json):

- **A01, thêm form đổi tên:** kit ngoài đã có form sửa tên. Thử nghiệm xác nhận một phần quy tắc A01 (trim) chưa có ở kit ngoài, nhưng toàn bộ chức năng A01 chưa tạo thành một cặp cùng điểm xuất phát. Chỉ nên xem xét một yêu cầu mới nếu cả hai kit có cùng hành vi nền.
- **A04, đổi chính sách tạo mật khẩu:** kit ngoài có đăng ký, đăng nhập và đổi mật khẩu khi đã đăng nhập. Chưa tìm thấy luồng đặt lại mật khẩu tương ứng với A04 trong snapshot khảo sát. Một cặp mới chỉ giới hạn ở đăng ký có cơ sở ban đầu: SmartKit đặt mức tối thiểu là 8 trong cấu hình và kit ngoài đã chấp nhận mật khẩu thử 10 ký tự khi đăng ký và đăng nhập. Cần kiểm tra thật trên baseline SmartKit, đối chiếu nghĩa vụ cần giữ và kiểm chứng gói chấm trước khi nhận cặp.
- **B05/B06, xử lý chuyển khoản và hết hạn đơn:** các yêu cầu gắn với hành vi SePay và vòng đời đơn của SmartKit. Nguồn hiện có chưa cho thấy chức năng tương ứng trong Stripe subscription của kit ngoài.
- **U02/U03, quản trị tài khoản toàn hệ thống:** thao tác trên danh sách tài khoản của quản trị viên chưa có đối ứng trong các luồng Owner/Member theo nhóm đã khảo sát.

**Tác vụ ghép đã xác nhận đủ điều kiện: 0.** Kiểm chứng này đủ để tiếp tục khảo sát ứng viên, chưa đủ để khóa kit, số cặp tác vụ, thiết kế hai layout hoặc phân bổ số phiên.
