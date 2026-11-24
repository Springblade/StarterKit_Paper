# Cross-review synthesis

Post-review synthesis. Ba báo cáo được tạo từ cùng packet bất biến trong ba ngữ cảnh tách biệt, đóng băng trước khi tổng hợp. Không gửi nhận xét hay audit trở lại reviewer. Đây là các lượt phản biện do AI tạo, không phải ba chuyên gia con người hoặc quyết định editorial.

## Kết luận dành cho tác giả

**Hướng có đủ cơ sở để tiếp tục nghiên cứu và phát triển thành một paper thực nghiệm dạng case study về kỹ thuật phần mềm. Chưa đủ căn cứ để khẳng định đóng góp mới đã được xác lập hoặc chắc chắn có bài được nhận.** Khuyến nghị của idea-evaluator là Accept with Revisions, hiểu là tiếp tục có điều kiện, không phải nhận bài.

SmartKit có thể làm đối tượng thực nghiệm vì có baseline chạy được trong phạm vi cục bộ, hành vi cần bảo toàn cụ thể, task-development example và hai layout đã kiểm tra trên cùng contracts. Không cần nó tốt nhất trên GitHub. Việc chọn repo tác giả tự xây cần được công khai, cùng nguồn yêu cầu và giới hạn suy rộng.

## Consensus strengths

Cả ba báo cáo ủng hộ câu hỏi can thiệp có thể đo, tách acceptance/preservation và chấp nhận kết quả null hoặc bất lợi. Cả ba đánh giá qualification task/layout là bằng chứng khả thi hữu ích. Chúng không diễn giải số tests đạt thành hiệu quả của agent.

## Consensus blocking concerns

| Synthesis key | Reviewer anchors | Vấn đề và điều kiện đóng |
|---|---|---|
| C1 Trial isolation và bốn packages | R1-M2, R2-M1, R3-M3 | Hiện mới có hai qualification workspaces; V0/V1 chưa định nghĩa, gold/evaluator có thể nằm ngoài snapshot nhưng vẫn trong parent workspace. Tạo bốn gói có manifest visibility, quyền truy cập, reset và budget; audit từ quyền của agent; chấm patch bằng evaluator ngoài workspace. |
| C2 Main-task validity | R1-M3, R2-M2; R3-M1 bổ sung sampling | Mới có một development example; sáu constructed candidates chưa thành main set. Chốt task frame, provenance, inclusion/exclusion, family, contract-to-check map và qualification tương ứng từng task. Không suy từ HTTP/DOM checks sang browser hoặc transaction contracts chưa thử. |

Blocking ở đây là trước main trials/central empirical inference, không cấm tiếp tục pilot và chuẩn bị phương pháp. R3 không đánh dấu sampling là blocking riêng; bảng giữ đúng khác biệt đó.

## Other consensus major concerns

- **C3 Đóng góp chưa phân biệt đủ.** R1-M1 và phần originality của R2/R3 đều nhận xét prior art đã bao phủ các thành phần chính. Chưa xác lập novelty không có nghĩa đã chứng minh trùng lặp. Cần contribution statement và đối chiếu intervention/artifact; extension hoặc replication có lý do vẫn là định vị hợp lệ.
- **C4 Task sampling và precision.** R1-M3, R3-M1/M2 yêu cầu xử lý task families, tài nguyên và uncertainty trước freeze. Repetitions không thay thế task diversity. Không áp một con số tasks/runs tùy ý khi chưa có pilot cost/precision và ngân sách.

## Where emphasis differs

- R1 nhấn mạnh tri thức bổ sung cần giải thích được so với prior work, ngay cả khi effect bằng không.
- R2-M3 phân biệt hiệu quả package với cơ chế riêng của colocation hoặc feedback. Nếu giữ claim ở mức package, chưa cần thêm active control phức tạp; nếu muốn claim execution riêng, cần đối chứng tương đương thông tin. Đây là major concern được R2 nêu riêng, không gán giả thành consensus blocking.
- R3 nhấn mạnh cân bằng theo task có thể vẫn overweight một workflow khi nhiều task chung family; cần scope hoặc sensitivity theo family phù hợp.

## Đối chiếu nguồn bổ sung của người tổng hợp

Các nguồn sau được truy cập trực tiếp; reviewer chỉ nhận excerpt trong packet. Đối chiếu README/landing page bổ sung được thực hiện ở bước tổng hợp và không được trình bày như nhận xét do reviewer đã đọc toàn artifact.

| Nguồn | Phần đã có liên quan | Phần SmartKit dự kiến kiểm tra thêm | Ranh giới bằng chứng |
|---|---|---|---|
| Zhu và cộng sự 2026, [Precedent or Intent?](https://arxiv.org/html/2610.38244v1) | Thao tác số lượng/vị trí code precedent và explicit instructions; outcome về lựa chọn triển khai | Hai regroupings của cùng code và outcome chức năng mới/bảo toàn, kết hợp supplied checks | Nguồn tự nhận local/sibling đồng thời đổi relatedness và location; không dùng làm bằng chứng feature layout tốt hơn |
| Dente, Satriani, Papotti 2026, [Constraint Decay](https://arxiv.org/html/2605.06445v2) | Constraint accumulation, architecture và functional/static checks; có feature-ablation tasks | Role-first/domain-first cùng logic baseline, supplied regression package và preservation | [Artifact README](https://github.com/francdente/constraint-decay) cho thấy có cả feature tasks. Không được gọi toàn công trình là chỉ greenfield. Chưa audit mọi task/code. |
| Patel và cộng sự 2026, [CodeThread](https://arxiv.org/html/2606.21804v2) | Controlled two-step human/agent base implementations và follow-on issue, F2P/P2P | Giữ logic baseline, đổi organization thay vì authorship, kết hợp package access | Đọc [README](https://github.com/shaswatpatel123/CodeThread), không tái chạy pipeline; phải pin artifact revision khi so khớp paper. |
| Wang và cộng sự 2026, [FeatureArc](https://arxiv.org/html/2610.37434v1) | Feature evolution, executable new/existing checks, persistent stages | Fresh-session trials trên một baseline có hai yếu tố được can thiệp | Khác biệt setting/intervention có thể hữu ích nhưng tự nó chưa chứng minh đóng góp đủ mạnh. Chưa inspect toàn artifact. |
| Achint Mehta 2026, [verification-surface study](https://arxiv.org/pdf/2608.28795v2) | Cố định agent, thay verification tool capabilities, đánh giá quality và cost | Giữ công cụ thông thường cho mọi cell, thay việc cung cấp sẵn project-specific behavioral tests trong extension tasks, và xét cùng layout | Behavioral arm của nguồn yêu cầu model tự viết tests, khác với supplied project checks. [Artifact landing page](https://zenodo.org/records/23197787) được xem; chưa tải/tái chạy dataset. |

Đây là các khác biệt thiết kế quan sát được trong nguồn, chưa là kết luận về ưu thế hoặc xác nhận “đầu tiên”. Tìm kiếm có mục tiêu chưa xác định nghiên cứu trùng chính xác hai intervention, nhưng không phải systematic novelty proof. Nhiều nguồn là preprint; không gán trạng thái peer-reviewed khi chưa xác minh.

## Định vị được đề xuất

Phát triển paper thành nghiên cứu thực nghiệm kiểm tra ảnh hưởng của **hai lựa chọn thiết kế cụ thể trong SmartKit** tới xác suất hoàn thành yêu cầu mới đồng thời bảo toàn hợp đồng cũ, với chi phí và failure patterns đi kèm. Nhóm độc giả chính là empirical software engineering, coding-agent evaluation và kiểm thử phần mềm.

Câu hỏi có thể làm sắc nét là việc cung cấp sẵn executable regression checks có làm thay đổi ảnh hưởng của repository organization trong các loại tác vụ khác nhau hay không. Đây là câu hỏi ứng viên, cần đối chiếu prior work và precision trước khi đặt interaction thành trọng tâm confirmatory. Hai hiệu ứng chính có thể vẫn là primary; interaction chuyển secondary/exploratory nếu tài nguyên chưa đủ.

Giá trị khả dĩ là effect estimates với uncertainty, trade-off chi phí và lỗi có căn cứ trên tasks hợp lệ. Không cần ép kết quả dương. Một null result chỉ có ích cho câu hỏi được đặt khi khoảng bất định, phạm vi task và độ nhạy của phép đo cho phép diễn giải; không mặc nhiên chứng minh hai layout tương đương.

## Forensic consistency findings

Audit này được chạy sau khi đóng băng ba báo cáo; không gán thành reviewer consensus. Bản ghi máy ở `forensic-audit.json`.

- **Passed A1–A5.** Packet hash giữ nguyên; ba reviewer reports đã đóng băng. Manifest có 284 copied/transformed records và 47 module moves. Sáu runtime stages là baseline/reference/restored-baseline trên hai layouts. Các số 14 unit tests, 10 baseline integration checks và 15 checks có task reference là các tập kiểm tra khác nhau, không phải số task/agent trials.
- **Provenance gap A6.** Proposal/protocol v0 có mô tả trạng thái cũ. Khi soạn bản hiện hành cần dẫn qualification evidence mới, ghi đúng upstream revision cộng baseline repairs và layout transformation. Không ghi source là unchanged upstream snapshot.
- **Not assessable A7.** Chưa có main trial dataset, effect size hay uncertainty để audit kết quả thực nghiệm. Không phát hiện số liệu agent bị mâu thuẫn vì chưa có số liệu đó.
- **Unresolved input A8.** Chưa biết venue, API budget, thời gian làm của tác giả và người review độc lập; không cam kết chi phí, timeline hoặc khả năng được nhận.
- **Provenance gap A9.** Đã đọc scoped full-text passages của năm nguồn, và README/landing page của ba artifacts. Chưa audit toàn code hoặc reproduce các công trình. Một số artifact documentation là bản mutable và có thể khác revision của paper.

## Minor revision checklist

Sửa trạng thái tài liệu theo R1-m1/R2-m1/R3-m1; nêu ranh giới instrument-development và main trials; thống nhất tên role-first layout thay vì ngầm coi là Clean Architecture; lập citation-to-claim matrix; cập nhật contribution statement và nguồn gần nhất. Giữ protocol v0 như hồ sơ lịch sử có nhãn, không sửa âm thầm thành preregistered protocol.

## Ba việc ưu tiên trước khi chi lớn cho agent

1. **Chốt contribution statement và prior-work matrix.** Tác giả phải giải thích điều phép so sánh này cho biết thêm; “SmartKit của tôi”, “có joint success” và “2 × 2” chưa đủ làm đóng góp.
2. **Chốt khung main tasks và requirement-grounded oracle.** Có thể dùng constructed tasks nếu khai báo và có lý do, nhưng không chọn theo condition thắng/thua hay gọi chúng là nhu cầu thật chưa có nguồn. Đa dạng family hoặc thu hẹp claim theo tập đủ khả năng dựng.
3. **Cô lập bốn packages rồi pilot development.** Chọn model/harness, cùng quyền công cụ, thông tin requirements, ngân sách và cách chấm; khóa precision/analysis/stopping trước main. Giữ log mọi attempts và tách lỗi agent khỏi hạ tầng.

## Broad-interest / significance readout

Có lý do khoa học và kỹ thuật để nghiên cứu, cùng nền tảng thực thi khả thi. Bằng chứng hiện tại phù hợp với việc tiếp tục một case study chuyên ngành. Chưa xác lập tầm quan trọng liên ngành kiểu Nature hoặc venue fit cụ thể; chưa có yêu cầu nào buộc paper phải đạt mức đó. Không xem việc thiếu Nature-level breadth là lý do bác bỏ paper software engineering.

## Risk / unsupported claims

Chưa được hỗ trợ gồm SmartKit/layout feature tốt hơn; mọi starter kit đều có cùng hiệu ứng; số tests pass chứng nhận oracle hoàn chỉnh; interaction xác nhận cơ chế; một null result chứng minh equivalence; và chắc chắn có paper được nhận. Không cần repository thứ hai chỉ để cho phép nghiên cứu case SmartKit. Replication độc lập trở nên cần khi mở claim chuyển giao hoặc khi yêu cầu venue cụ thể đòi hỏi.

Tác giả cần xác nhận intended business contracts, nguồn task, ngân sách và scope cuối; reviewer AI không thay thế đánh giá chuyên môn độc lập. Khi viết/nộp paper, khai báo hỗ trợ AI theo quy định của cơ sở/venue và giữ ghi chú, nguồn, decisions cùng các bản nháp để giải thích được quá trình nghiên cứu.
