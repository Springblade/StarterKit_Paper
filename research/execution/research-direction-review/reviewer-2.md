# Reviewer 2

## Overall assessment

Hướng có cơ sở để phát triển thành nghiên cứu tình huống software engineering. Thiết kế hỏi được tác động của hai can thiệp cụ thể, chấp nhận kết quả bất lợi và có bằng chứng instrument ban đầu. Chưa có dữ liệu agent để kết luận hiệu quả. Tôi đánh giá đề xuất và qualification trong packet, không đánh giá một paper thực nghiệm đã hoàn tất. Các điểm chặn dưới đây là điều kiện trước khi thu dữ liệu chính, không phải lý do bác bỏ hướng.

## Who would be interested in the results, and why

Người xây starter kit, coding-agent harness và hệ thống kiểm thử có thể dùng kết quả để cân nhắc cách tổ chức mã, gói checks và chi phí tương ứng. Phạm vi sử dụng ban đầu là SmartKit với những tasks và cấu hình được đánh giá.

## Major strengths

- Joint success yêu cầu cả chức năng mới lẫn preservation; báo cáo hai thành phần tránh che regression bằng acceptance thành công.
- P1 §4.1 và P2 §4 xác định đúng verification package gồm thông tin và feedback, chưa quy hiệu quả cho execution riêng.
- E1 thử ba implementation sai và một cách lọc đúng khác reference. E2 có kiểm tra baseline, reference rồi phục hồi trên cả hai layouts. Đây là bằng chứng qualification cụ thể, không phải hiệu quả agent.
- Fresh sessions, randomization theo block, all-attempt outcomes và uncertainty ở cấp task đã được dự kiến hợp lý.

## Major Concerns

### R2-M1 [experimental-design]
**Severity** Major  
**Blocking** Yes  
**Claim pointer** Bốn điều kiện sẽ khác layout và quyền tiếp cận verification package, với evaluator cuối độc lập.  
**Evidence pointer** P1 §4.1–4.4; P2 §4; E2 “Limits and next gate”.  
**Concern** E2 nói rõ chưa phân bổ V0/V1; snapshots còn chứa development evaluator và nằm trong parent research workspace. Vì vậy hiện có hai layouts được qualification, chưa có bốn treatment packages đủ điều kiện chạy agent. Đặt gold ngoài snapshot chưa chứng minh agent không thể đọc nó.  
**Why it matters** Leakage hoặc checks khác phạm vi giữa layouts có thể tạo chênh lệch được hiểu nhầm thành hiệu quả can thiệp.  
**Resolution test** Đóng băng manifest cho từng cell gồm files, instructions, commands, checks và budget. Từ đúng quyền của trial agent, kiểm tra không truy cập được gold, hidden evaluator, sibling artifacts hoặc parent rules. Dry run xác nhận V0 giống nhau giữa layouts, V1 chỉ thêm gói đã khai báo và mọi patch được chấm bằng cùng evaluator trong môi trường sạch. Không cần cấm V0 tự viết tests; đó là hành vi hợp lệ cần ghi trace.

### R2-M2 [data-resource-quality]
**Severity** Major  
**Blocking** Yes  
**Claim pointer** Joint success sẽ đo chức năng mới hoạt động đồng thời giữ những hợp đồng hành vi còn hiệu lực.  
**Evidence pointer** P2 §6; P3; E1 “Evaluator and evidence” và “Interpretation and next gate”; E3.  
**Concern** Bằng chứng hiện tại thuộc một development task phải loại khỏi outcomes chính. HTTP/DOM không chạy scripts; action checks stub session/cache. Những ranh giới này được công khai đúng, nhưng không đủ qualification cho browser interaction, authorization qua mọi entry point hoặc các tasks transaction/concurrency khác trong danh sách ứng viên.  
**Why it matters** Hidden tests độc lập vẫn có thể bỏ sót lỗi hoặc phạt giải pháp đúng nếu thiếu contract và qualification tương ứng. Số tests pass không xác lập độ bao phủ hành vi.  
**Resolution test** Trước khi nhận mỗi main task, lập mapping requirement → acceptance/preservation assertion → mức tích hợp → negative probe. Chứng minh baseline chưa giải task, reference qua cả hai layouts, lỗi hợp lý bị đúng assertion bắt và một giải pháp đúng khác reference được chấp nhận. Với contract tương tác trình duyệt hoặc transaction, chạy ở mức thật cần thiết; nếu không kiểm tra được thì thu hẹp endpoint, không suy rộng từ E1. Ghi người xác nhận business contract và mọi phần chỉ có tác giả tự rà soát.

### R2-M3 [mechanism-evidence]
**Severity** Major  
**Blocking** No  
**Claim pointer** Các quan sát H-S, H-V và interaction có thể giúp giải thích colocation và feedback tác động thế nào.  
**Evidence pointer** P2 §3–4; P1 §6; E2 “Snapshots and transformation”; L-precedent §5; L-verification §I và §E.  
**Concern** Layout đổi cả paths, proximity và imports; V1 thêm cả executable examples lẫn feedback. Interaction trên joint success không tự phân biệt cơ chế định vị mã với thông tin test hay chi phí sử dụng công cụ. Trace chạy checks rồi sửa lỗi cũng chỉ tương thích với cơ chế, chưa nhận diện nguyên nhân riêng. Packet đã nhận giới hạn này nhưng bảng “quan sát phân biệt” vẫn dễ bị dùng quá mức khi viết kết quả.  
**Why it matters** Có thể ước lượng hiệu quả phân bổ package mà chưa chứng minh cơ chế trung gian.  
**Resolution test** Ghi trước estimand là hiệu quả của hai packages cụ thể; phân tích trace chỉ tạo giải thích có giới hạn. Nếu giữ claim execution riêng, thêm đối chứng tương đương thông tin. Nếu giữ claim colocation riêng, cần can thiệp phân biệt nó với các thay đổi context khác. Không bắt buộc mở rộng thiết kế khi paper chỉ kết luận ở mức package.

## Minor Comments

### R2-m1 [writing-clarity]
**Severity** Minor  
**Blocking** No  
**Affected element** Trạng thái triển khai baseline và layouts.  
**Evidence pointer** P1 §4.1; P2 §2, §4; E2.  
**Issue** P2 còn mô tả chưa chạy checks/chưa chuyển đổi, trong khi E2 ghi qualification đã hoàn thành trong phạm vi cục bộ.  
**Required correction** Gắn trạng thái theo ngày và dẫn E2; phân biệt hoàn thành qualification với chưa tạo trial packages. Dùng snapshot thực gồm repairs và manifest thay vì chỉ upstream commit. Đối chiếu lại hai văn bản là phép kiểm tra đóng điểm này.

## Technical failings that need to be addressed before the case is established

R2-M1 và R2-M2 chặn chuyển sang main trials. R2-M3 được giải quyết bằng giới hạn claim nếu không nghiên cứu cơ chế riêng.

## Assessment against Nature-style criteria

- **originality** Chưa xác lập. L-featurearc đã dùng F2P/P2P; L-codethread đo thay đổi tiếp theo; L-verification đã so verification surface. Cần chỉ rõ khác biệt can thiệp và câu hỏi, không lấy factorial hoặc tên SmartKit làm novelty.
- **scientific importance** Có giá trị tiềm năng trong software engineering; quy mô hiệu ứng, chi phí và độ ổn định chưa được đo.
- **interdisciplinary readership** Chưa có bằng chứng sức hút rộng kiểu Nature. Điều này không phủ định nghiên cứu tình huống ở lĩnh vực chuyên môn.
- **technical soundness** Thiết kế khả thi về nguyên tắc; qualification hỗ trợ tiếp tục. Chưa đủ cơ sở cho claim hiệu quả hoặc cơ chế. Task set, precision plan và tài nguyên phải được chốt trước dữ liệu chính; không thể định lượng khả thi từ packet.
- **readability for nonspecialists** Định nghĩa regression và joint success tương đối rõ; cần sửa trạng thái tài liệu theo R2-m1. Chưa có bản thảo kết quả để đánh giá đầy đủ.

## Recommendation posture

Ủng hộ tiếp tục phát triển có điều kiện. Ưu tiên hoàn thiện và kiểm tra bốn trial packages cùng oracle cho main tasks. Chưa có căn cứ khẳng định SmartKit tốt hơn, chứng minh cơ chế riêng hay đạt tầm quan trọng rộng kiểu Nature.
