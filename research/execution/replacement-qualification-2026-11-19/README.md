# Kiểm chứng Next.js SaaS Starter và Makerkit Lite

**Kết luận ngày 19/11/2026.** Cả hai kit đủ điều kiện kỹ thuật cho thí nghiệm thăm dò trên ba tác vụ tài khoản và hai layout đã kiểm chứng. Lịch ứng viên có 48 phiên. Chưa mở thu thập dữ liệu từ agent.

## Kết quả ma trận

| Kit | Số ca | Baseline giữ hành vi cũ | Bản tham chiếu đạt yêu cầu mới và giữ hành vi cũ | Hồi quy bị phát hiện |
| --- | ---: | ---: | ---: | ---: |
| Next.js SaaS Starter | 36 | 12/12 | 12/12 | 12/12 |
| Makerkit Lite | 36 | 12/12 | 12/12 | 12/12 |

Mỗi layout có hai vòng với dữ liệu mới. Mỗi vòng thử ba tác vụ, mỗi tác vụ có ba bản. Cả 24 bản gây hồi quy vẫn qua kiểm tra trình duyệt cơ bản. Các phép kiểm theo tác vụ phát hiện việc làm mất khoảng trắng trong tên cũ, giữ phiên sau đăng xuất hoặc hiển thị mật khẩu ngay khi mở trang. [Ca Next.js về xác thực](nextjs-cases.json), [ca Next.js về tên hiển thị](nextjs-profile.json), [ca Makerkit](makerkit-cases.json), [kiểm tra TypeScript của Makerkit](makerkit-type-audit.json).

Bộ dữ liệu Next.js về xác thực lưu thêm 12 ca của tác vụ đăng ký đã rút. Các ca đó nằm ngoài tổng 72 ca hiện hành. Cả hai kit dùng cơ sở dữ liệu cục bộ và kiểm tra trình duyệt thật. Khi thao tác đặt lại Supabase trả lỗi, vòng đó được chạy lại từ dữ liệu mới.

## Diễn tập và phân bổ

Hai lượt diễn tập áp dụng lại bản sửa từ tệp patch và chấm trên dữ liệu mới, mỗi kit một lượt ở layout bố trí lại mã. Các lượt này dùng cách triển khai khác bản tham chiếu trong ma trận. Kiểm tra theo tác vụ và các lệnh sẽ cấp cho agent đều đạt. [Diễn tập Next.js](nextjs-rehearsal.json), [diễn tập Makerkit](makerkit-rehearsal.json).

Kiểm tra nội dung 24 cấu hình gói xác nhận V0 và V1 có cùng mã, lockfile và đặc tả trong từng tổ hợp kit, layout và tác vụ. V1 thêm script bảo toàn và lệnh chạy. Phân bổ gồm 2 kit × 3 tác vụ × 4 điều kiện × 2 lần lặp. Thứ tự được xáo trộn trong từng khối kit, tác vụ và lần lặp. [Kiểm tra gói](package-audit.json), [lịch ứng viên 48 phiên](allocation-candidate.json).

Kết quả áp dụng cho runtime cục bộ và ba luồng tài khoản đã kiểm tra. Các lượt diễn tập dùng bản sửa chuẩn bị sẵn, mỗi kit một lượt đại diện. Chúng cung cấp bằng chứng về công cụ đo, môi trường và quy trình chấm trước collection.

## Thiết kế

Hai kit dùng chung ba [đặc tả tác vụ](task-cards.md). So sánh trong từng tổ hợp kit và tác vụ. Thiết kế dự kiến gồm hai layout và hai mức kiểm tra, với hai lần lặp trong mỗi điều kiện. Các ca kiểm chứng dùng tài khoản tổng hợp và bản sửa do nghiên cứu chuẩn bị.

| Tác vụ | Hành vi mới | Hành vi hiện có dùng để kiểm tra hồi quy |
| --- | --- | --- |
| Tên hiển thị | Khi lưu, bỏ khoảng trắng ở hai đầu và giữ khoảng trắng bên trong | Khi mở cài đặt, tên cũ chưa được sửa vẫn hiển thị đúng như đã lưu |
| Đăng xuất | Xác nhận trước khi đăng xuất. Hủy giữ phiên, kể cả khi dùng bàn phím | Sau khi đăng xuất, yêu cầu mới tới trang được bảo vệ cần đăng nhập lại |
| Mật khẩu đăng nhập | Nút hiện/ẩn dùng được bằng bàn phím, giữ giá trị và không gửi form | Trường mật khẩu được che khi vừa mở trang |

Tác giả đã chọn thay tác vụ ngưỡng mật khẩu khi đăng ký bằng tác vụ tên hiển thị. Trên Supabase cục bộ, ngưỡng 12 chặn đăng ký với mật khẩu 11 ký tự và vẫn cho tài khoản cũ đăng nhập. Nó cũng chặn đổi sang mật khẩu 11 ký tự, thao tác chấp nhận được với cấu hình gốc. [Dữ liệu thử chính sách mật khẩu](makerkit-password-policy.json).

## Baseline và layout

- **Next.js SaaS Starter.** Giữ layout upstream làm mức so sánh. Layout thứ hai nhóm biểu mẫu, server actions, middleware xác thực và xử lý phiên trong cùng thư mục tính năng. Dùng PostgreSQL cục bộ và không kết nối Stripe thật. [Upstream](https://github.com/nextjs/saas-starter), [script bố trí lại mã](../starter-kit-selection-2026-11-16/prepare-external-layout.py).
- **Makerkit Lite.** Dùng cấu trúc upstream làm mức so sánh. Layout thứ hai nhóm biểu mẫu đăng ký và đăng nhập trong package xác thực, đưa phần quản lý đăng xuất vào thư mục tính năng xác thực của ứng dụng và chuyển biểu mẫu tên hiển thị vào thư mục profile của package tài khoản. Giữ nguyên entry point, cấu hình dịch vụ và dependencies. Baseline của cả hai layout thêm `type="submit"` cho nút lưu tên vì trình duyệt quan sát nút upstream có `type="button"` và thao tác bấm không gửi form. [Upstream](https://github.com/makerkit/nextjs-saas-starter-kit-lite), [chuẩn bị baseline và layout](qualify-makerkit.py).

Makerkit Lite chạy Next.js trong container Linux từ lockfile upstream vì SWC native không tải được với quyền thư mục cache trên Windows. Cho ứng dụng truy cập Supabase cục bộ và xác minh email qua Mailpit. Kiểm tra tương tác đăng xuất ẩn phần hiển thị chẩn đoán của Next.js dev trong trình duyệt thử sau khi quan sát nó che menu. Kiểm chứng ghi nhận cảnh báo hydration trên một số trang cài đặt.

## Tái lập

Yêu cầu Docker Desktop, Git, Node, pnpm, Python Playwright và Chromium. Checkout hai snapshot vào thư mục dùng riêng cho thí nghiệm. Script kiểm tra đúng revision trước khi chạy. Giữ các thư mục checkout tách khỏi mã và dữ liệu cá nhân.

1. Dùng [qualify-nextjs.py](qualify-nextjs.py) với đường dẫn checkout Next.js SaaS Starter. Lệnh mặc định chạy lại ma trận tài khoản trước đó và lưu đầy đủ ca đăng ký để lưu vết. Thêm `--profile` để kiểm tra tác vụ tên hiển thị. Phân bổ hiện hành chỉ dùng tên hiển thị, đăng xuất và hiện/ẩn mật khẩu.
2. Khởi động Supabase của checkout Makerkit Lite thử nghiệm bằng `pnpm supabase:web:start` từ gốc của checkout. Cấu hình upstream dùng các cổng 54321–54326 và không gửi email ra ngoài. Chạy [prepare-makerkit-runtime.ps1](prepare-makerkit-runtime.ps1) với đường dẫn checkout để dựng ứng dụng Linux cục bộ. Chạy [qualify-makerkit.py](qualify-makerkit.py) với cùng checkout và đối số `types` để kiểm tra kiểu trên các bản thử, rồi `matrix` để chạy các ca trình duyệt. Lệnh đặt lại dữ liệu của đúng dự án Supabase thử nghiệm trước mỗi vòng. Dùng `matrix-resume` để tiếp tục từ vòng chưa hoàn tất.
3. Kiểm tra lưu bản sửa và chạy chấm bằng `--rehearsal` của script Next.js, hoặc đối số `rehearsal` của script Makerkit. Các bản sửa tham chiếu và các ca chấm giữ kín nằm ngoài gói cấp agent.
4. Chạy [audit-replacement.py](audit-replacement.py) với hai đường dẫn checkout theo thứ tự Next.js rồi Makerkit. Script đối chiếu ma trận và gói V0/V1 trước khi ghi lịch ứng viên. Dừng ứng dụng Linux bằng `docker stop paper-makerkit-node` và dừng bản Supabase thử bằng `pnpm supabase:web:stop` từ gốc checkout Makerkit.
