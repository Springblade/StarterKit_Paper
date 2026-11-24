# Reviewer 3

## Overall assessment

Hướng này có cơ sở để phát triển thành paper nghiên cứu trường hợp trong kỹ thuật phần mềm. Câu hỏi can thiệp, endpoint kết hợp chức năng mới và bảo toàn hành vi, cùng hai layout đã kiểm tra cục bộ tạo thành điểm xuất phát có thể thực hiện. Tuy nhiên, bằng chứng hiện có xác nhận một phần instrument, chưa xác nhận hiệu quả của SmartKit hay khả năng ước lượng hiệu ứng đủ chính xác. Không có kết quả agent mới không phải khuyết điểm của một đề xuất.

Đánh giá chỉ dựa trên packet bất biến, gồm đề xuất, protocol, task audit, bằng chứng qualification và trích đoạn nguồn. Không đọc mã, log gốc hoặc artifact ngoài packet. Trọng tâm là lấy mẫu tác vụ, bất định, tính khả thi và tái lập. Các điều kiện blocking dưới đây áp dụng trước khi chạy và diễn giải nghiên cứu chính, không phủ nhận giá trị tiếp tục phát triển hướng này.

## Who would be interested in the results, and why

Nhà nghiên cứu coding agent và kiểm thử phần mềm có thể quan tâm đến tác động của cách bố trí mã và gói kiểm chứng trên cùng yêu cầu thay đổi. Người xây starter kit có thể sử dụng kết quả để cân nhắc chi phí hỗ trợ agent. Giá trị thực dụng phụ thuộc vào mô tả rõ loại tác vụ và giới hạn áp dụng cho SmartKit, thay vì suy rộng thành năng suất lập trình viên.

## Major strengths

- P1 §5 và P2 §7 phân biệt session nhận điều kiện với task tạo cấu trúc phụ thuộc. Nhiều lần chạy không được coi là nhiều tác vụ độc lập.
- E1 và E2 báo cáo baseline, reference, biến thể sai và một cách triển khai đúng khác. Đây là bằng chứng cụ thể cho khả năng kiểm định instrument, vượt ra ngoài việc đếm tests.
- P2 §4 xác định can thiệp là cả verification package; P1 §6 giới hạn layout effect vào phép chuyển đổi đã thực hiện. Cách diễn đạt này tránh quy kết cơ chế vượt dữ liệu.
- P1 §3 và P2 §3 chấp nhận kết quả bằng không hoặc bất lợi; E3 tách development task khỏi dữ liệu chính.

## Major Concerns

### R3-M1 [experimental-design]

**Severity** Major  
**Blocking** No  
**Claim pointer** Nghiên cứu dự kiến so sánh tỷ lệ joint success trên tập tác vụ mở rộng đã chọn, với trọng số bằng nhau giữa tác vụ.  
**Evidence pointer** P1 §4.2 và §5; P2 §5; P3 SK-T01 đến SK-T06; E3.  
**Concern** Năm trong sáu ứng viên thuộc billing; T01 và T05 cùng dùng lịch sử đơn hàng, còn T06 tiếp tục dựa vào trạng thái đơn. Quy tắc “tránh toàn bộ billing” chưa xác định cách lấy mẫu hoặc xử lý các tác vụ chung family. Tác vụ đã qualification cũng thuộc lịch sử đơn hàng và được dành cho development. Tập ứng viên hiện chưa tạo căn cứ cho một tập chính đa dạng ngay trong SmartKit.  
**Why it matters** Trọng số bằng nhau giữa task vẫn có thể đặt phần lớn trọng số lên một workflow được chia thành nhiều yêu cầu. Khi đó hiệu ứng trung bình và khoảng bất định dễ phản ánh lựa chọn của tác giả hơn phạm vi câu hỏi mong muốn.  
**Resolution test** Trước freeze, công bố khung ứng viên, nguồn yêu cầu, tiêu chí chọn/loại và nhãn domain/family. Giải thích phạm vi tập được chọn, xác định cách xử lý family liên quan trong phân tích và kiểm tra độ nhạy với trọng số family nếu thích hợp. Nếu chỉ dựng được tác vụ billing, thu hẹp câu hỏi và kết luận tương ứng; không bắt buộc thêm repository.

### R3-M2 [statistical-rigor]

**Severity** Major  
**Blocking** No  
**Claim pointer** RQ2 và RQ3 dự kiến ước lượng chênh lệch xác suất và tương tác, kèm bất định có xét dependence.  
**Evidence pointer** P1 §5; P2 §7, §8 và §10; L-precedent, External Validity.  
**Concern** Protocol đã chọn estimand nhưng chưa chọn phương pháp bất định, mục tiêu precision hoặc quy tắc quyết định interaction là confirmatory hay exploratory. Chưa có ngân sách API/compute được xác định. Đây là quyết định được hoãn có chủ đích, không phải bằng chứng thiết kế sai; tuy nhiên chưa đủ để kết luận nghiên cứu chính có thể trả lời cả hiệu ứng riêng và tương tác. L-precedent cũng phân biệt biến thiên giữa repetitions với biến thiên giữa task/repository.  
**Why it matters** Tăng repetitions trong phạm vi tài nguyên có thể giảm nhiễu session nhưng không giải quyết tập task hẹp. Một interaction không chính xác không cho phép kết luận hai yếu tố không tương tác.  
**Resolution test** Dùng pilot development để ước lượng chi phí và kiểm tra precision bằng các kịch bản hiệu ứng, clustering và tỷ lệ thất bại hợp lý. Trước dữ liệu chính, khóa số task/repetitions, cấu hình model/harness, phân tích, giới hạn tài nguyên và quy tắc dừng. Nêu độ chính xác đạt được; nếu không đủ, xác định trước phạm vi mô tả hoặc exploratory. Không cần một cỡ mẫu tùy ý do reviewer đặt ra.

### R3-M3 [reproducibility]

**Severity** Major  
**Blocking** Yes  
**Claim pointer** Bốn điều kiện sẽ khác nhau về layout và verification package, với evaluator cuối độc lập và mọi trial được reset.  
**Evidence pointer** P2 §4, §7 và §10; E2, Reference isolation and reproducibility và Limits and next gate.  
**Concern** E2 xác nhận snapshots còn chứa development evaluator, nằm dưới workspace nghiên cứu và chưa có phân bổ V0/V1. Vì vậy chúng chưa phải gói trial bảo đảm hidden tests, gold patches và parent instructions không thể bị agent đọc. Qualification hai layout chưa chứng minh điều kiện tiếp xúc thông tin của thiết kế bốn ô.  
**Why it matters** Truy cập evaluator hoặc lời giải có thể phá hỏng phép so sánh chính; instruction kế thừa hoặc reset không hoàn chỉnh có thể thay đổi can thiệp và làm kết quả khó tái lập.  
**Resolution test** Tạo bốn gói cô lập có manifest visibility và hash, chỉ rõ checks agent thấy, evaluator ngoài phạm vi truy cập và cách loại memory/instructions kế thừa. Chạy audit từ chính quyền truy cập của agent, kiểm tra reset liên tiếp và chấm lại patch trong môi trường sạch. Khóa phiên bản baseline đã sửa, harness và oracle trước main trials. Chỉ chuyển bước khi audit không tìm được gold/hidden artifacts và các hợp đồng qualification vẫn đạt.

## Minor Comments

### R3-m1 [writing-clarity]

**Severity** Minor  
**Affected element** Trạng thái triển khai trong đề xuất và protocol.  
**Evidence pointer** P1 §4.1; P2 §2 và §4; E2.  
**Issue** P1/P2 còn mô tả chưa chạy build và chưa triển khai phép chuyển đổi, trong khi E2 đã ghi qualification hai layout. Người đọc phải tự phân biệt kế hoạch cũ với bằng chứng mới.  
**Required correction** Thêm mốc trạng thái có ngày và dẫn E2, đồng thời giữ rõ giới hạn qualification. Không chuyển số test đạt thành kết quả agent.

## Technical failings that need to be addressed before the case is established

R3-M3 phải được đóng trước main trials. R3-M1 và R3-M2 cần được quyết định minh bạch trước freeze để kết luận có phạm vi và bất định phù hợp.

## Assessment against Nature-style criteria

- **Originality** Chưa được xác lập. L-constraint, L-featurearc và L-codethread đã có đánh giá hành vi mới cùng hành vi cần giữ; L-verification đã nghiên cứu công cụ kiểm chứng. Khác biệt tiềm năng nằm ở can thiệp layout × package trong cùng SmartKit, cần đối chiếu artifact cụ thể. Factorial tự nó không chứng minh novelty.
- **Scientific importance** Có tiềm năng cho một case study kỹ thuật phần mềm; chưa có kết quả cho thấy tầm quan trọng rộng.
- **Interdisciplinary readership** Chưa thiết lập lợi ích ngoài cộng đồng coding agent, kiểm thử và thiết kế repository. Không phải điều kiện bắt buộc để tiếp tục hướng chưa chọn venue này.
- **Technical soundness** Lập luận thiết kế có cơ sở và qualification hữu ích; các giới hạn lấy mẫu, precision và trial isolation còn phải giải quyết.
- **Readability for nonspecialists** P1 giải thích agent, regression và oracle khá rõ. Mâu thuẫn trạng thái ở R3-m1 gây trở ngại; chưa có bản thảo kết quả để đánh giá khả năng giải thích phát hiện.

## Recommendation posture

Ủng hộ tiếp tục phát triển có điều kiện thành nghiên cứu trường hợp trong kỹ thuật phần mềm. Ưu tiên hoàn tất trial isolation, tập task và precision plan. Chưa có căn cứ khẳng định SmartKit cải thiện agent hoặc nghiên cứu đạt ý nghĩa rộng theo tiêu chí Nature.
