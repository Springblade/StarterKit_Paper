# Reviewer 1

## Overall assessment

Hướng này đủ cơ sở để tiếp tục phát triển thành nghiên cứu tình huống về kỹ thuật phần mềm, nhưng chưa đủ bằng chứng để xác nhận đóng góp thực nghiệm hoặc tính mới. Trọng tâm có ích là tác động của hai lựa chọn thiết kế repository lên việc thêm chức năng đồng thời giữ hành vi cũ. Giá trị tiềm năng nằm ở phép can thiệp được kiểm soát và phạm vi kết luận rõ, không nằm ở việc xây thêm starter kit.

Tôi chỉ đánh giá packet gồm P1–P3, E1–E3 và các trích đoạn nguồn. Không đọc artifact gốc, không xác minh nguồn ngoài packet. E1/E2 báo cáo kiểm định công cụ và hai layout; chưa có thử nghiệm hiệu năng agent. Những điều kiện dưới đây là yêu cầu trước nghiên cứu chính, không phải lý do phủ nhận một đề xuất vì chưa có kết quả.

## Who would be interested in the results, and why

Nhà nghiên cứu coding agent, người thiết kế starter kit và nhóm xây công cụ kiểm thử có thể quan tâm. So sánh trên cùng yêu cầu giúp họ biết việc sắp xếp mã và cung cấp checks bổ sung có đổi xác suất hoàn thành đúng trong ngân sách cố định hay chỉ tăng chi phí. Người bảo trì phần mềm có thể tham khảo trong phạm vi SmartKit; chưa thể chuyển thành khuyến nghị chung hoặc năng suất của lập trình viên.

## Major strengths

- P1 §3 và P2 §3 chấp nhận kết quả bằng không hoặc bất lợi, tách giả thuyết cơ chế khỏi phát hiện.
- P1 §4.1 và P2 §4 nhận diện V1 là gói thông tin cùng feedback, tránh đồng nhất với hiệu quả thuần của execution.
- Theo báo cáo E1, oracle bác bỏ ba biến thể sai và chấp nhận một cách lọc đúng khác reference. Đây là bằng chứng kiểm định cục bộ có ích, không phải chứng nhận đầy đủ oracle.
- E2 báo cáo hai layout vượt cùng checks đã thực thi; manifest ghi phép chuyển đổi. P2 §7 nhận diện phụ thuộc trong task và không coi repetitions là task độc lập.

## Major Concerns

### R1-M1 [novelty-significance]

**Severity** Major  
**Blocking** No  
**Claim pointer** P1 §2, §7 định vị đóng góp dự kiến là so sánh có kiểm soát và dữ liệu về layout kết hợp kiểm chứng trên SmartKit.  
**Evidence pointer** P1 §2, §6; L-featurearc II-A/B; L-codethread §3.1; L-precedent §3.3; L-verification I-A/B, I-E.  
**Concern** Quan sát từ nguồn trong packet cho thấy đánh giá đồng thời chức năng mới và hành vi cũ đã có ở FeatureArc/CodeThread; thao tác repository context đã có ở Precedent or Intent; can thiệp khả năng kiểm chứng và đo chi phí đã có ở nghiên cứu Mehta. Trích đoạn này chưa chứng minh có nghiên cứu trùng đúng can thiệp layout × gói kiểm chứng của SmartKit. Suy luận của tôi là tính mới còn chưa được xác lập, không phải đã chứng minh trùng lặp. P1 chưa đặt FeatureArc và Mehta cạnh đóng góp dự kiến dù packet đã chứa hai nguồn gần trực tiếp.  
**Why it matters** Nếu chỉ trình bày joint success, test chạy được hoặc factorial như đóng góp mới, paper có thể đánh đồng phương pháp đã tồn tại với khoảng trống còn mở.  
**Resolution test** Bổ sung đối chiếu có nguồn về intervention, task setting, endpoint và artifact của các công trình gần nhất, giữ nguyên phạm vi từng nguồn ([FeatureArc](https://arxiv.org/html/2610.37434v1), [Mehta](https://arxiv.org/pdf/2608.28795v2)). Chỉ rõ tri thức nào phép so sánh SmartKit có thể bổ sung ngay cả khi hiệu ứng bằng không. Nếu artifact xác nhận cùng câu hỏi đã được kiểm tra, định vị replication/extension và nêu phần mở rộng cụ thể.

### R1-M2 [experimental-design]

**Severity** Major  
**Blocking** Yes  
**Claim pointer** RQ3 dự kiến ước lượng tác động của gói kiểm chứng bổ sung trong từng layout và tương tác giữa hai yếu tố.  
**Evidence pointer** P1 §4.1; P2 §4; E2 “Limits and next gate”.  
**Concern** Quan sát trực tiếp từ báo cáo E2 là chưa phân bổ quyền thấy tests V0/V1; snapshots hiện còn chứa evaluator phát triển và nằm trong workspace nghiên cứu. Vì vậy, chưa có bốn điều kiện đủ cô lập để thực hiện suy luận dự kiến. Đây là gate còn mở được tác giả thừa nhận, không phải bằng chứng rằng agent đã tiếp cận gold.  
**Why it matters** Leakage hoặc khác biệt ngoài gói hỗ trợ sẽ khiến chênh lệch khó quy cho can thiệp. Cùng shell access cũng cho phép V0 tự viết checks; cần diễn giải hiệu quả của việc cung cấp gói, không phải có hay không có khả năng kiểm thử.  
**Resolution test** Trước pilot, đóng băng danh mục V0/V1, nội dung requirements chung và evaluator ngoài workspace; chứng minh gold, parent instructions và hidden tests không truy cập được. Chạy kiểm tra isolation/reset trên cả bốn packages, ghi hashes và instructions thực nạp. Giữ V0 hợp lệ; không cần thêm đối chứng thông tin nếu claim vẫn giới hạn ở toàn gói.

### R1-M3 [data-resource-quality]

**Severity** Major  
**Blocking** Yes  
**Claim pointer** P1 §7 dự kiến cung cấp dữ liệu đáng diễn giải về hai lựa chọn thiết kế trên tập tác vụ SmartKit.  
**Evidence pointer** P3; E1 “Interpretation and next gate”; E3 “Origin”; P2 §5, §7, §10.  
**Concern** P3 có sáu constructed candidates, phần lớn thuộc billing; E1/E3 chỉ cung cấp một task phát triển và yêu cầu loại nó khỏi kết quả held-out. Chưa có task set chính đủ điều kiện, kế hoạch precision hoặc ngân sách xác định. Suy luận của tôi là độ đa dạng và khả năng thu được ước lượng có ích còn chưa biết, không phải task nhân tạo tự thân không hợp lệ.  
**Why it matters** Thêm nhiều repetitions cho một thay đổi UI nhỏ không giải quyết sự hạn chế task; tương tác có thể không đủ chính xác để hỗ trợ đóng góp dự kiến.  
**Resolution test** Trước confirmatory runs, cố định task cards có provenance và lý do chọn, oracle/reference trên hai layout, nhật ký loại trừ và ranh giới development/main. Dùng pilot để chốt precision, clustering, ngân sách và phân tích; nếu không đủ, thu hẹp câu hỏi hoặc ghi interaction là thăm dò trước khi xem main outcomes. Không cần một số task tùy ý hay repository thứ hai khi claim chỉ về SmartKit.

## Minor Comments

### R1-m1 [writing-clarity]

**Severity** Minor  
**Blocking** No  
**Affected element** Trạng thái thực hiện trong P1/P2.  
**Evidence pointer** P1 §4.1; P2 §2, §4; E1/E2.  
**Issue** Kế hoạch còn nói chưa chạy build/test và chưa triển khai layout, trong khi E1/E2 báo cáo đã thực hiện ở qualification workspace.  
**Required correction** Thêm mốc trạng thái phân biệt snapshot gốc, bản có baseline repairs, qualification workspace và trial package chưa đóng băng. Kiểm tra đạt yêu cầu khi người đọc xác định được bằng chứng thuộc phiên bản nào và gate nào còn mở.

## Technical failings that need to be addressed before the case is established

R1-M2 và R1-M3 chặn suy luận thực nghiệm chính. R1-M1 cần xử lý để xác lập vị trí đóng góp, nhưng không ngăn tiếp tục kiểm định tính khả thi.

## Assessment against Nature-style criteria

- **originality** Chưa xác lập, chưa chứng minh trùng lặp. Factorial tự nó không xác nhận novelty.
- **scientific importance** Có tiềm năng trong kỹ thuật phần mềm; chưa có kết quả để xác nhận mức ảnh hưởng.
- **interdisciplinary readership** Chưa được thiết lập. Đây không phải điều kiện bắt buộc cho nghiên cứu tình huống đang đề xuất và chưa có venue được chọn.
- **technical soundness** Lập luận thiết kế hợp lý, có bằng chứng instrument bước đầu; các gate R1-M2/M3 còn mở.
- **readability for nonspecialists** P1 giải thích regression và dùng ví dụ có ghi rõ giả định. Mâu thuẫn thời điểm cần sửa; chưa có manuscript kết quả để đánh giá đầy đủ.

## Recommendation posture

Ủng hộ tiếp tục phát triển có điều kiện thành paper nghiên cứu tình huống về kỹ thuật phần mềm. Ưu tiên xác lập đóng góp và hoàn tất trial packages, task qualification trước nghiên cứu chính. Chưa có căn cứ cho significance rộng kiểu Nature; điều đó không phủ định sự phù hợp của hướng với paper chuyên ngành.
