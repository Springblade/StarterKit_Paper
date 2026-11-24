# Hồ sơ nhận hai starter kit vào thí nghiệm

**Kết luận:** nhận SmartKit và Next.js SaaS Starter vào thiết kế thí nghiệm thăm dò trên ba cặp tác vụ tài khoản. Cả hai đủ điều kiện về runtime, layout và độ nhạy của các phép kiểm trên workload này. Chưa mở thu thập dữ liệu từ coding agent.

## Phạm vi

Hai kit được xem xét là SmartKit và Next.js SaaS Starter. Các phép so sánh được thực hiện trong từng kit và từng tác vụ. Sau đó mới đối chiếu kết quả giữa hai kit trên cùng yêu cầu chức năng. Kết quả chính là joint success. Các kết quả acceptance và preservation được báo riêng. Các tác vụ dưới đây do nghiên cứu xây dựng và đều thuộc luồng tài khoản.

| Cặp tác vụ | Hành vi mới | Hành vi có ở cả hai bản gốc |
| --- | --- | --- |
| Chính sách đăng ký | Mật khẩu đăng ký tối thiểu 12 ký tự | Tài khoản đã tồn tại với mật khẩu ngắn hơn vẫn đăng nhập được |
| Xác nhận đăng xuất | Xác nhận kết thúc phiên, hủy giữ phiên | Sau khi đăng xuất, phiên cũ mất quyền truy cập dashboard |
| Hiện/ẩn mật khẩu khi đăng nhập | Từ bàn phím có thể hiện và che lại mật khẩu, giữ nguyên giá trị và không tự gửi form | Mật khẩu được che khi mới mở form đăng nhập |

## Kiểm chứng công cụ đo

Bộ kiểm tra cơ bản dùng chung gồm kiểm tra kiểu TypeScript, mở trang đăng ký, đăng nhập bằng tài khoản thử có mật khẩu 12 ký tự, kiểm tra phiên và kiểm tra người chưa đăng nhập bị chuyển từ dashboard sang trang đăng nhập. Đây là bộ cơ bản cho workload tài khoản của hai kit, khác với năm lệnh của protocol SmartKit cũ. Việc gửi form đăng ký và xác minh tài khoản có được lưu thuộc phần chấm tác vụ. Với từng tác vụ, phần bắt lỗi bảo toàn được bổ sung ngoài bộ cơ bản. Tất cả phép thử dùng browser và cơ sở dữ liệu cục bộ. Bộ chạy và log dữ liệu đánh giá nằm ngoài checkout của kit.

| Tác vụ | Bản sửa tham chiếu | Lỗi được dùng để kiểm tra độ nhạy |
| --- | --- | --- |
| Đăng ký | Chỉ nâng ngưỡng khi đăng ký | Áp dụng ngưỡng mới cả lúc đăng nhập |
| Đăng xuất | Hỏi xác nhận rồi gọi thao tác đăng xuất hiện hữu | Hộp thoại và chuyển trang hoạt động, nhưng không kết thúc phiên |
| Hiện/ẩn mật khẩu | Thêm nút hiện/ẩn và giữ trạng thái che mặc định | Nút vẫn hoạt động nhưng mật khẩu mặc định hiện |

Bản tham chiếu và bản có lỗi là vật liệu kiểm chứng. Chúng cần được giữ ngoài workspace cấp cho agent. Không dùng số lỗi cài chủ đích để suy ra tỷ lệ lỗi agent. Các kiểm tra bản tham chiếu không tự thiết lập rằng bộ chấm chấp nhận mọi triển khai hợp lệ.

[Đặc tả chung của ba tác vụ](matched-task-cards.md) được dùng cho cả hai kit. Bộ [kiểm tra công khai](public-preservation.py) chỉ được cấp ở điều kiện có gói bổ sung. Bộ chạy kiểm chứng và dữ liệu giữ lại chứa kiểm tra cuối cùng, bản tham chiếu và biến thể lỗi, nên nằm ngoài workspace cấp cho agent.

Hai layout đối chứng của SmartKit lấy từ các gói A04 theo tầng và theo tính năng. Với Next.js SaaS Starter, layout gốc chia mã xác thực giữa nhóm route và thư mục thư viện. [Script chuyển nhóm](prepare-external-layout.py) đưa biểu mẫu, server actions và helper xác thực vào một thư mục tính năng chung, vẫn giữ các file entry point và đường dẫn công khai. Đây là cùng một nguyên tắc tổ chức mã nhưng hai thao tác cụ thể phụ thuộc vào kit. Không coi layout gốc của Next.js SaaS Starter là một bản sao của layout theo tầng của SmartKit. Mức độ tác vụ buộc agent tiếp xúc với các module đã di chuyển có thể khác nhau, đặc biệt ở tác vụ xác nhận đăng xuất.

### Tái lập ma trận

Chuẩn bị bốn checkout cục bộ dưới thư mục tạm của Windows, dùng dependency theo lockfile. Cách chuẩn bị hai checkout đầu nằm trong [hồ sơ đăng ký](registration-pair.md). Checkout `paper-paired-registration/smartkit-layered` lấy từ `main48/packages/A04/S0V0`. Với `paper-paired-registration/nextjs-feature`, bắt đầu từ bản sao của snapshot Next.js SaaS Starter đã khảo sát, rồi chạy [script chuyển nhóm](prepare-external-layout.py). Không sao chép tệp `.env` của các gói SmartKit. Cấu hình bài kiểm chứng dùng credential cục bộ riêng và không kết nối Stripe thật.

Chạy [bộ kiểm chứng](probe-registration.py) lần lượt với không đối số, `--signout-preservation`, và `--visibility`. Chạy lại ba cấu hình với `--alternate` để kiểm tra layout còn lại của từng kit. Chỉ dùng một container PostgreSQL với dữ liệu trong RAM tại một thời điểm. [Kiểm tra lịch và kết quả](qualify-admission.py) đối chiếu dữ liệu ma trận. [Kiểm tra gói](audit-two-kit-packages.py) lắp ráp tạm các gói để kiểm tra phần nào khác giữa V0 và V1.

## Phân bổ và giới hạn

Hai thiết kế cân bằng có thể phân bổ trong 48 phiên nếu có ba cặp đủ điều kiện:

| Yếu tố được giữ | Phân bổ | Phép so sánh chính |
| --- | --- | --- |
| Gói kiểm tra bảo toàn | 2 kit × 3 tác vụ × 2 điều kiện × 4 lần | Chênh lệch joint success giữa có và không có gói trong các block kit–tác vụ–lần lặp |
| Tổ chức mã và gói kiểm tra | 2 kit × 3 tác vụ × 4 điều kiện × 2 lần | Hai hiệu ứng chính trong block kit–tác vụ–lần lặp. Tương tác và khác biệt giữa kit mang tính thăm dò |

Mỗi tác vụ có trọng số bằng nhau. Tỷ lệ theo kit chỉ mô tả kit và các tác vụ đã chọn. Kết quả từ sáu tổ hợp kit–tác vụ không đại diện cho sáu kit độc lập. Phân tích [độ nhạy đã có](../direction-validation-2026-11-16/design-sensitivity.json) dùng các xác suất giả định cho 24 cặp. Nó không ước lượng trước hiệu ứng hay xác nhận đủ lực phát hiện hiệu ứng nhỏ. Với workload giới hạn ở tài khoản, bất kỳ kết luận nào cũng phải ghi phạm vi này. Chưa khóa lịch chạy.

## Kết quả nhận kit

- **72 ca kiểm chứng đạt kỳ vọng.** Hai kit, hai layout mỗi kit, ba tác vụ, và hai vòng cơ sở dữ liệu mới. Mỗi vòng chấm bản gốc, bản tham chiếu và bản gây hồi quy. Cả 24 ca lỗi vượt qua các kiểm tra cơ bản. Gói bổ sung và phép chấm hành vi cũ phát hiện cả 24. Các bản tham chiếu qua kiểm tra tính năng mới và hành vi cũ.
- **24 gói cấp cho agent được kiểm tra.** Trong từng tổ hợp kit–layout–tác vụ, mã và yêu cầu giống nhau giữa V0 và V1. V1 chỉ thêm lệnh và file chạy kiểm tra bảo toàn. Các ca chấm giữ kín, bản tham chiếu và bản lỗi nằm ngoài gói. [Hồ sơ gói](two-kit-package-audit.json)
- **48 phiên có lịch dự kiến hợp lệ.** Thiết kế giữ cả hai yếu tố và có hai lần lặp trong mỗi tổ hợp kit–tác vụ–điều kiện. Lịch ghép đúng 24 gói. [Lịch dự kiến và liên kết dữ liệu ma trận](two-kit-allocation-candidate.json)

Phạm vi kỹ thuật là các luồng tài khoản đã kiểm tra trong runtime local. Đợt này không chấm các luồng Stripe, thanh toán, hay quản trị toàn hệ thống. Chưa diễn tập toàn bộ quy trình thu thập của thiết kế hai kit từ phiên agent đến replay bản sửa. Lịch cũ riêng cho SmartKit không dùng để mở thu thập trên hai kit. Không có phiên model hay kết quả so sánh tác động. Container PostgreSQL tự dọn cuối từng lượt và không cần tạo image hoặc volume Docker mới.
