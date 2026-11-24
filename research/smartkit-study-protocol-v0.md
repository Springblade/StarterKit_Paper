# SmartKit study — protocol v0

Ngày: 2026-11-10. Trạng thái: kế hoạch khả thi, chưa preregistered, chưa chạy pilot mới. Chủ sở hữu quyết định khoa học: tác giả thesis. Hướng đã được tác giả đồng ý: nghiên cứu ảnh hưởng của thiết kế starter kit lên khả năng agent mở rộng ứng dụng đúng và giữ hành vi đang có.

## 1. Câu hỏi trung tâm

Tổ chức mã theo tính năng và khả năng chạy kiểm chứng hành vi ảnh hưởng thế nào đến việc coding agent hoàn thành yêu cầu mở rộng ứng dụng SaaS mà không làm hỏng những hành vi vẫn còn hiệu lực?

SmartKit là đối tượng thiết kế/thực thi trung tâm. Không giả định SmartKit tốt hơn trước khi đo. Kết luận đầu tiên chỉ áp dụng cho tasks, snapshot, agents và điều kiện được đánh giá; kết luận ngoài SmartKit cần replication ở repository độc lập.

## 2. Điều đã biết và điều chưa biết

- Snapshot đã đọc: `research/SmartKit`, commit `2c92d3920d967b9ebf0960ba7890754baa3c90d7`. Chưa xác nhận trùng phiên bản thesis và chưa kiểm tra upstream mới hơn.
- Đã đọc source về orders, payment processing, schemas, permissions và một số unit tests. Các nhận xét source không phải chứng nhận baseline đúng.
- `process-sepay-payload.test.ts` mock thao tác persistence và completion. Do đó riêng file này không đủ kiểm chứng hành vi thực của DB transaction, uniqueness hoặc concurrent delivery.
- Chưa cài dependencies/chạy build/test/runtime trong lượt chuẩn bị này. Chưa có task mới được xác minh end-to-end. Không sử dụng số liệu của runs cũ đã xóa.
- `AGENTS.md` của snapshot có chỉ dẫn tổ chức feature và tham chiếu parent/rules ngoài repo. Cần kiểm soát instruction exposure trước mọi trial.
- Bằng chứng nền và đối chứng gần nhất ở [khảo sát đã lưu trữ](../archive/research/research-landscape-v2.md) và [bảng nguồn](evidence-ledger-v2.csv); những tài liệu đó không xác nhận novelty của factorial được đề xuất ở đây.

## 3. RQ và giả thuyết ứng viên

RQ1 (mô tả): Những failure modes nào xuất hiện khi agent làm các feature-change tasks đã chọn, xét riêng tính năng mới và hành vi cũ?

RQ2 (can thiệp): Trên cùng task, tổ chức mã theo tính năng khác tổ chức theo tầng thế nào về joint success?

RQ3 (can thiệp): Cung cấp bộ kiểm chứng hành vi bổ sung ảnh hưởng thế nào đến joint success, và ảnh hưởng có khác giữa hai cách tổ chức không?

| Giả thuyết ứng viên | Cơ chế đề xuất | Quan sát phân biệt | Kết quả làm yếu kỳ vọng |
|---|---|---|---|
| H-S | Colocation theo feature giúp tìm đủ consumer liên quan | Ít omission có chứng cứ và joint success cao hơn | Agent đã tìm đủ vị trí nhưng thất bại triển khai; không cải thiện hoặc kém hơn |
| H-V | Behavioral feedback giúp phát hiện và sửa regression | Agent thực sự chạy checks; sửa lỗi đúng nguyên nhân | Chỉ thêm lượt chạy/chi phí; không cải thiện joint success |
| H-SV | Khả năng định vị mã làm thay đổi lợi ích feedback | Tương tác giữa hai yếu tố trên endpoint đã định nghĩa | Không thấy interaction với uncertainty đủ nhỏ, hoặc tác động chỉ do instruction leakage |

Đây là candidate explanations, không phải findings. Không cần H-S hay H-SV đúng để nghiên cứu có giá trị. Null chưa chính xác không được gọi là equivalence.

Giải thích thay thế: khác biệt instructions; khác số lượng/examples trong mã; baseline lỗi; schema/test oracle thiên vị path; tests bổ sung tiết lộ nhiều thông tin hơn; task/model selection; cơ hội revision khác nhau; hành vi tool/harness khác. Ghi cách xử lý từng yếu tố trước pilot.

## 4. Hai yếu tố và bốn điều kiện

S0: tổ chức theo tầng có quy tắc rõ và hoạt động hợp lệ. S1: tổ chức theo feature của SmartKit. Cùng logic, dependencies, chức năng, domain facts và môi trường. Cách chuyển đổi cụ thể chưa được triển khai.

V0: bộ checks cơ bản giống nhau giữa S0 và S1. V1: cùng checks cơ bản và thêm bộ kiểm chứng hành vi chạy được bởi agent. Bộ bổ sung được port sang cả S0 và S1; không chỉ có ở SmartKit.

| ID | Tổ chức | Kiểm chứng agent thấy |
|---|---|---|
| C00 | S0 | V0 |
| C01 | S0 | V1 |
| C10 | S1 | V0 |
| C11 | S1 | V1 |

Các nhóm có cùng văn bản requirements và cùng tổng budget. Trial nào cũng được chạy công cụ thông thường. Hidden acceptance/regression tests nằm ngoài workspace và không trùng bộ feedback được cung cấp.

V1 bổ sung executable examples và feedback, nên estimand ban đầu là tác động của verification package, không phải tác động thuần của execution. Nếu muốn tách thông tin khỏi feedback, phải bổ sung active control tương đương về thông tin. Chưa mở rộng thành nhiều yếu tố trước khi xác nhận thiết kế chính khả thi.

S0/S1 không chỉ khác tên folder: chuyển import paths, exports và proximity làm thay đổi context. Ghi transformation manifest và giới hạn claim vào cách tổ chức được triển khai. Không tuyên bố đo được một nguyên lý kiến trúc phổ quát từ một phép refactor.

Instruction files cần trung lập về ưu thế kiến trúc; mapping đường dẫn được điều chỉnh tương ứng và mọi thay đổi được ghi. Không để AGENTS.md yêu cầu S0 phải viết lại thành S1. Không để parent workspace skills/rules hay model memory vô tình vào trial. Ghim tool/harness/system instructions và log nội dung thực sự được tải.

## 5. Chọn tasks trước khi biết kết quả agent

Bảng `smartkit-task-audit-v0.csv` chứa đề xuất được dựng từ bề mặt source. Tất cả đều là constructed candidates chưa xác minh; chưa có task được coi là historical requirement hoặc production incident.

Mỗi task cần: nguồn yêu cầu; starting commit; hành vi mới; hành vi cũ phải giữ; thay đổi hành vi được phép; acceptance oracle; preservation oracle; reference solution; các giải pháp hợp lệ khác; dependency/service assumptions; tiêu chí loại trừ.

Ưu tiên issue/PR có provenance khi có thể dựng lại. Nếu task do tác giả đặt, ghi rõ constructed và lý do thực dụng; không biến mong muốn cá nhân thành quy luật framework. Requirements phải đủ để người triển khai độc lập biết đúng/sai, nhưng không cung cấp lời giải hoặc gold file list.

Tránh toàn bộ task chỉ nằm trong billing. Bảng ban đầu thiên về billing do source/tests hiện có; đây là giới hạn cần khắc phục, không phải sample đại diện. Task discovery/exploration và confirmatory task set được tách trước khi điều chỉnh thiết kế dựa trên outcomes.

## 6. Instrument và endpoint

Primary endpoint cho mỗi trial: `joint_success = new_behavior_pass AND preserved_behavior_pass`. Các predicate phải được định nghĩa theo task và do evaluator độc lập chạy. Pass chỉ có nghĩa đáp ứng phạm vi checks đã công bố, không chứng minh mã hoàn toàn đúng.

Secondary outcomes: từng thành phần pass/fail; build/runtime status; cost/tokens/time; omission hoặc regression có chứng cứ; thay đổi ngoài phạm vi. Không dùng vị trí file, số test hoặc schema presence làm ground truth về correctness/maintainability.

Trước khi thử agent, yêu cầu:

1. Baseline chạy được, đáp ứng preservation checks và chưa đáp ứng yêu cầu mới.
2. Reference solution qua acceptance và preservation checks trên cả S0 và S1.
3. Những implementation sai hợp lý phải bị đúng oracle phát hiện; chỉ chèn text đúng vào comment không được qua.
4. Một implementation hợp lệ khác không bị phạt vì khác path/style của human reference.
5. Dữ liệu/clock/order/database state reset được; flaky/infrastructure errors được phân loại riêng.

Với property DB/auth/state, sử dụng môi trường test cục bộ và fixture có kiểm soát; không gọi dịch vụ thanh toán/email production. Mock chỉ phù hợp với phần không phải mục tiêu kiểm định. Không dùng unit test đã mock chính transaction như bằng chứng transaction thực đúng.

## 7. Đơn vị, allocation và phân tích dự kiến

- Experimental unit: một fresh agent session/workspace trên task, condition và model/harness đã xác định.
- Cấu trúc dependence: repetitions lồng trong task; tasks có thể cùng family/repo. Không đồng nhất số runs với số task độc lập.
- Block theo task × model/harness; randomize run order trong block, ghi batch/date. Mọi trial reset workspace, DB và memory.
- Main contrast: S1−S0 trong từng mức V; V1−V0 trong từng mức S; interaction trên thang risk difference. Báo effect size và uncertainty, không chỉ p-value.
- Nếu đủ task độc lập, cân nhắc hierarchical analysis hoặc resampling ở cấp task, không bootstrap riêng từng run. Chốt phương pháp sau feasibility và trước confirmatory outcomes; số repository ít không cho suy luận vững về quần thể repo.
- Ghi all-attempt outcomes và failure stage. Model refusal/agent timeout là outcome của hệ thống theo budget; infrastructure failures được xử lý theo quy tắc rerun cố định. Không rerun chỉ những output xấu.
- Chưa chốt số task, model hoặc repetitions. Pilot instrument dùng tập development riêng; cỡ mẫu sau đó dựa trên precision/effect thực dụng và cấu trúc clustering. Không chọn model/task chỉ vì tạo chênh lệch lớn.

## 8. Trình tự thực hiện và sản phẩm cần có

| Giai đoạn | Việc làm | Sản phẩm | Điều kiện chuyển bước |
|---|---|---|---|
| 1. Baseline | Ghim snapshot; dựng local env; ghi build/test/runtime; kiểm tra business contracts | Baseline audit + environment manifest | Biết lỗi nền nào tồn tại; hai layout có thể tương đương về hành vi đã định nghĩa |
| 2. Task audit | Viết đầy đủ spec cho một nhóm candidates; tìm nguồn/historical tasks | Task cards + inclusion/exclusion log | Requirements có căn cứ và oracle không thiên vị một layout |
| 3. Conditions | Tạo layout đối chứng và port cùng tests/instructions | Transformation manifest + 4 fixtures | Reference/no-op outcomes phù hợp và điều kiện chỉ khác yếu tố đã khai báo |
| 4. Pilot | Chạy nhỏ trên development tasks; kiểm tra trace và scorer | Pilot report + protocol deviations | Instrument hoạt động; có dữ liệu để lên precision plan; không sửa thiết kế chỉ để tạo hiệu ứng |
| 5. Freeze | Khóa tasks/oracles/settings/allocation/analysis/exclusions | Protocol v1 timestamped/preregistration nếu dùng | Confirmatory data chưa được xem |
| 6. Main + replication | Chạy có lưu toàn bộ artifact; kiểm chứng độc lập/ngoài SmartKit nếu claim rộng | Dataset + analysis + manuscript evidence | Kết luận phù hợp thiết lập và uncertainty |

Không bắt đầu bằng viết Introduction hay chạy nhiều model. Công việc ngay trước mắt là giai đoạn 1 và 2.

## 9. Tiêu chí điều chỉnh hoặc dừng phiên bản thiết kế

- Không tạo được S0/S1 tương đương: sửa thiết kế hoặc thu hẹp claim; không dùng baseline hỏng.
- Không tìm được task có hành vi preservation rõ: thay task domain hoặc đổi RQ; không thêm hidden requirements không có căn cứ.
- Current tests đã bắt gần hết lỗi: vẫn là kết quả có ích; đánh giá xem câu hỏi bổ sung còn đủ giá trị, không cố làm yếu V0.
- Pilot quá dễ/quá khó: sửa development tasks dựa trên quy tắc minh bạch; giữ log, không đưa dữ liệu đã chọn lọc thành confirmatory sample.
- Literature/artifact cho thấy cùng intervention và outcome đã được kiểm tra: định vị replication/extension hoặc thay đóng góp; không chỉ đổi tên thành SmartKit.

## 10. Dữ liệu và trách nhiệm tác giả

Lưu nguyên trial traces, instructions, model/harness version, repo commit, lockfile/image digest, prompt, patch, check outputs, cost/time, exclusion/rerun log và oracle version. Credentials/fixtures chỉ dùng test data. Chưa xác định API budget/compute hoặc người review độc lập; không coi thời gian không giới hạn là ngân sách không giới hạn.

Tác giả cần xác nhận intended business behavior khi tài liệu/source mâu thuẫn; source implementation riêng lẻ không đủ chứng minh đó là yêu cầu đúng. Mọi task mới ở bảng audit là giả định và cần kiểm chứng trước khi dùng làm dữ liệu. Lưu quyết định nghiên cứu và khai báo hỗ trợ AI theo yêu cầu áp dụng khi viết/nộp paper.
