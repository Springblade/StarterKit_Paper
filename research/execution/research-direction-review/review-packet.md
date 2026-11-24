# Immutable review packet ? SmartKit research direction

Date 2026-11-10. Review a research proposal and instrument-development evidence, not a completed empirical paper. No main coding-agent trials or new agent outcome data have been collected. The user asks whether the direction has enough scientific basis to develop into a paper. No target journal, hours/week, API budget or deadline is specified. Do not infer a Nature submission target. Assess software-engineering case-study suitability and separately report whether broad Nature-style significance is established. Three AI review contexts are separate, not human peer reviewers.

The author agreed to study one SmartKit case, layout by accessible behavioral-verification package, accepting null/adverse results. Existing code is a qualification workspace; test counts describe instrument checks.

Preassigned emphasis briefs, fixed before any report
- R1 originality, motivation and contribution positioning.
- R2 intervention validity, controls and measurement.
- R3 task sampling, uncertainty, feasibility and reproducibility.
All reviewers assess all five common axes and can raise overlapping concerns independently.

Grounding rules
Use only the packet and the common criterion/skeleton references provided. Do not inspect sibling review files or message other reviewers. Every major concern needs a stable ID, claim pointer, evidence pointer and resolution test. Distinguish observations, proposed choices and missing evidence. No invented references, acceptance probabilities or sample sizes. Preserve source scopes and citation URLs. Neither failure to find exact overlap nor a factorial design establishes novelty.



# [P1] research/smartkit-proposal.md

# Ảnh hưởng của tổ chức mã và kiểm chứng hành vi đến khả năng coding agent mở rộng ứng dụng SaaS: nghiên cứu trên SmartKit

Đề xuất nghiên cứu để trao đổi với giáo sư hướng dẫn

Phiên bản 0.1 | Ngày 10 tháng 11 năm 2026

## Tóm tắt

Nghiên cứu đề xuất kiểm tra hai quyết định thiết kế của starter kit: tổ chức mã theo tính năng và cung cấp bộ kiểm chứng hành vi mà coding agent có thể chạy trong quá trình sửa mã. SmartKit là ứng dụng dùng để xây dựng và so sánh các điều kiện thực nghiệm. Với cùng yêu cầu mở rộng tính năng, nghiên cứu sẽ đánh giá khả năng hoàn thành chức năng mới và bảo toàn những hành vi cũ vẫn còn hiệu lực. Thiết kế gồm bốn điều kiện, kết hợp hai cách tổ chức mã với hai mức hỗ trợ kiểm chứng. Mỗi điều kiện phải có cùng chức năng ban đầu, yêu cầu nghiệp vụ và ngân sách thực thi. Kết quả được chấm bằng các kiểm tra độc lập với bộ test cung cấp cho agent. Nghiên cứu dự kiến tạo ra dữ liệu về tác động của từng quyết định thiết kế, các kiểu thất bại và chi phí thực thi. Hiện chưa có kết quả thực nghiệm mới; việc dựng baseline, lựa chọn tác vụ và kiểm định bộ đánh giá là những bước đầu tiên cần hoàn thành.

## 1. Vấn đề nghiên cứu và cơ sở từ thesis

SmartKit là starter kit SaaS dựa trên Next.js, có mã cho xác thực, thanh toán và email, cùng cách tổ chức theo tính năng [1]. Thesis đã sử dụng SmartKit để đánh giá mức độ coding assistant tuân thủ một số quy ước repository. Các phép đo tập trung vào cấu trúc file, type/schema và sự hiện diện của những thành phần được yêu cầu.

Trong đề xuất này, coding agent là hệ thống có thể đọc repository, sửa mã và chạy công cụ để thực hiện một yêu cầu. Regression chỉ việc thay đổi mới làm hỏng hành vi đã có; bảo toàn hành vi là giữ các yêu cầu cũ vẫn còn hiệu lực sau thay đổi.

Những phép đo này cho biết mã được tạo ra có phù hợp với quy ước đã đặt hay không. Khi một ứng dụng tiếp tục được phát triển, tác giả còn cần biết thay đổi mới có hoạt động và có giữ được các yêu cầu đang có hay không. Một tính năng tìm kiếm đơn hàng, chẳng hạn, có thể trả đúng kết quả cho người dùng hiện tại nhưng vẫn làm lỏng điều kiện kiểm soát quyền truy cập. Đây là tình huống minh họa cho nghiên cứu, chưa phải lỗi đã được quan sát trong SmartKit.

Hướng đề xuất sẽ sử dụng SmartKit để kiểm tra tác động của những quyết định thiết kế cụ thể lên kết quả sửa đổi phần mềm. Tổ chức theo tính năng có thể giúp agent tìm các thành phần liên quan. Bộ kiểm chứng hành vi có thể giúp phát hiện một số regression trong quá trình thực hiện yêu cầu. Cả hai tác động đều cần được đo. Việc SmartKit đã triển khai các thành phần này chưa xác nhận rằng chúng giúp agent làm việc tốt hơn.

Thực nghiệm mới sẽ sử dụng dữ liệu được lưu đầy đủ từ đầu. Pilot trong thesis không được dùng để ước lượng hiệu ứng hoặc làm dữ liệu kiểm chứng vì artifact của các lần chạy đó không còn.

## 2. Nghiên cứu liên quan và vị trí của đề xuất

Các nghiên cứu về repository context cho thấy cung cấp hướng dẫn không tự bảo đảm task success. Gloaguen và cộng sự không tìm thấy cải thiện nhìn chung từ context files trong các thiết lập được đánh giá [2]. Zhu và cộng sự nghiên cứu cách agent lựa chọn giữa repository precedents và chỉ dẫn của tác vụ [3]. Những kết quả này đặt ra yêu cầu kiểm soát cả instructions và những ví dụ mã mà agent có thể đọc khi so sánh hai cách tổ chức repository.

Constraint Decay đã đánh giá structural requirements bằng behavioral tests kết hợp static verifiers trong backend coding [4]. CodeThread xem xét khả năng thực hiện yêu cầu tiếp theo trên những implementation khác nhau và cho thấy static metrics chưa giải thích đầy đủ kết quả downstream [5]. Vì vậy, một framework chấm quy ước hoặc thêm số lượng file được kiểm tra chưa đủ phân biệt đề xuất này với công trình hiện có.

Bằng chứng về khả năng bảo trì còn phụ thuộc thiết lập. Echoes of AI không phát hiện bất lợi downstream có hệ thống trong thí nghiệm con người tiếp tục phát triển mã được viết với AI hỗ trợ [6]. Nghiên cứu đó khác thiết lập autonomous agent. Đề xuất hiện tại sẽ giới hạn kết luận vào khả năng hoàn thành thay đổi của agent; thời gian bảo trì của lập trình viên cần một nghiên cứu người dùng riêng nếu muốn đo.

Đóng góp dự kiến là phép so sánh có kiểm soát giữa những phiên bản của cùng một starter kit trên cùng tác vụ, với outcome về chức năng mới và hành vi cần giữ. Tính mới ở mức can thiệp và bộ dữ liệu vẫn cần đối chiếu thêm với artifact của các công trình gần nhất trước khi chốt phạm vi paper. Đề xuất chưa khẳng định đây là nghiên cứu đầu tiên về kiến trúc repository hay kiểm chứng bằng test.

## 3. Mục tiêu, câu hỏi và giả thuyết

Mục tiêu là xác định những quyết định thiết kế nào của SmartKit hỗ trợ agent thực hiện thay đổi đúng, tác động xuất hiện trong điều kiện nào và chi phí đi kèm là bao nhiêu.

RQ1. Khi coding agent thực hiện các yêu cầu mở rộng ứng dụng đã chọn, những thất bại nào xuất hiện đối với chức năng mới và những hành vi cũ vẫn phải giữ?

RQ2. Với cùng tác vụ và mức hỗ trợ kiểm chứng, tổ chức mã theo tính năng ảnh hưởng thế nào đến tỷ lệ hoàn thành đúng so với cách tổ chức theo tầng?

RQ3. Cung cấp bộ kiểm chứng hành vi bổ sung ảnh hưởng thế nào đến tỷ lệ hoàn thành đúng, và ảnh hưởng đó có thay đổi theo cách tổ chức mã hay không?

Giả thuyết về cấu trúc là việc đặt những thành phần cùng tính năng gần nhau có thể giảm bỏ sót khi sửa đổi. Giả thuyết về kiểm chứng là feedback thực thi có thể giúp agent phát hiện và sửa regression trước khi kết thúc. Hai cơ chế cũng có thể tương tác. Kết quả bằng không hoặc bất lợi vẫn trả lời các RQ; nghiên cứu không đặt điều kiện SmartKit phải đạt kết quả cao hơn để được báo cáo.

## 4. Thiết kế thực nghiệm

### 4.1. Hệ thống và điều kiện so sánh

Nghiên cứu bắt đầu từ một commit SmartKit được cố định và kiểm tra trong môi trường cục bộ. Bản snapshot đã đọc hiện là 2c92d3920d967b9ebf0960ba7890754baa3c90d7. Chưa xác nhận đây là baseline đủ điều kiện cho thực nghiệm. Trước pilot, cần chạy build, test và các luồng nghiệp vụ liên quan, đồng thời ghi lại lỗi có sẵn.

Từ baseline, tác giả dự kiến tạo một phiên bản tổ chức theo tầng và một phiên bản tổ chức theo tính năng. Hai phiên bản phải giữ cùng logic nghiệp vụ, dependencies và hành vi đã đặc tả. Chuyển đổi đường dẫn và import được ghi thành manifest. Bộ kiểm tra độc lập phải cho cùng kết quả ban đầu trên cả hai phiên bản. Điều kiện này xác nhận sự tương đương trong phạm vi kiểm tra, chưa chứng minh tương đương ngữ nghĩa tuyệt đối.

| Điều kiện | Cách tổ chức mã | Hỗ trợ kiểm chứng agent được sử dụng |
|---|---|---|
| C00 | Theo tầng | Bộ kiểm tra cơ bản |
| C01 | Theo tầng | Bộ cơ bản và bộ kiểm chứng hành vi bổ sung |
| C10 | Theo tính năng | Bộ kiểm tra cơ bản |
| C11 | Theo tính năng | Bộ cơ bản và bộ kiểm chứng hành vi bổ sung |

Tổ chức theo tầng phải là một phương án hợp lệ, được thiết kế và rà soát trước khi có kết quả agent. Bộ kiểm tra cơ bản có cùng khả năng gọi và cùng phạm vi hành vi ở cả hai layouts. Nghiên cứu không chủ động làm yếu baseline để tạo chênh lệch.

Mọi nhóm nhận cùng yêu cầu chức năng và nghiệp vụ, có cùng quyền sử dụng công cụ thông thường và cùng giới hạn tài nguyên. Instructions chỉ mô tả chính xác từng layout, không yêu cầu nhóm đối chứng viết lại theo cấu trúc SmartKit. Các rules từ parent workspace, memory hoặc công cụ khác phải được kiểm soát và ghi trong log.

Bộ bổ sung cung cấp cả executable examples và feedback. Tác động được ước lượng vì vậy là tác động của cả gói hỗ trợ kiểm chứng. Nếu muốn xác định riêng tác động của việc thực thi so với thông tin trong test, cần thêm đối chứng tương đương về thông tin. Đây là phần mở rộng chỉ được cân nhắc sau khi thiết kế chính được xác nhận khả thi.

### 4.2. Xây dựng tập tác vụ

Tập tác vụ sẽ gồm yêu cầu mở rộng trên ứng dụng đã có, với hành vi mới và các yêu cầu cũ cần giữ được đặc tả riêng. Nguồn ưu tiên là issue, PR hoặc yêu cầu phát triển có thể truy vết. Những tác vụ do tác giả xây dựng sẽ được ghi rõ nguồn gốc và lý do lựa chọn.

Các ứng viên ban đầu gồm bộ lọc lịch sử đơn hàng, tìm kiếm theo mã đơn và bộ lọc vai trò trên trang quản trị. Đây là tác vụ giả định, chưa được xác minh về nhu cầu hoặc khả năng dựng. Tác giả cần kiểm tra tính năng đã có trong baseline hay chưa và hoàn thiện specification trước khi đưa vào pilot. Tập chính cũng cần tránh tập trung toàn bộ vào billing.

Mỗi tác vụ phải có starting commit, nguồn yêu cầu và acceptance criteria cho chức năng mới. Các yêu cầu preservation cần căn cứ từ specification, test hoặc tài liệu nghiệp vụ. Ví dụ, tìm kiếm đơn hàng có thể cần giữ giới hạn dữ liệu theo người dùng, nhưng quyền truy cập cụ thể phải được tác giả xác nhận. Chỉ những hành vi còn hiệu lực mới được giữ trong oracle; thay đổi có chủ đích theo yêu cầu mới không bị tính là regression.

Task card, reference implementation và bộ kiểm tra được hoàn thiện trước confirmatory runs. Tập development dùng để sửa instrument được tách khỏi tập chính. Khi loại một tác vụ vì thiếu specification, không dựng được hoặc có nguy cơ lộ lời giải, tác giả lưu lý do loại và nguồn ban đầu.

### 4.3. Kiểm định bộ đánh giá

Agent được dùng visible tests theo điều kiện của mình. Kết quả cuối được chấm trong môi trường evaluator riêng bằng hidden acceptance và regression tests, không trùng bộ feedback được cung cấp. Những yêu cầu được chấm đều phải có căn cứ trong specification mà người triển khai được biết. Hidden tests giữ cách kiểm tra độc lập; chúng không được bổ sung yêu cầu nghiệp vụ bí mật.

Oracle ở đây là bộ tiêu chí và phép kiểm tra dùng để quyết định implementation có đáp ứng yêu cầu hay không. Tác giả phải kiểm định oracle trước khi dùng nó để đánh giá agent.

Trước pilot, baseline phải vượt qua preservation checks và chưa đáp ứng chức năng mới. Reference implementation phải vượt qua cả hai nhóm kiểm tra trên mỗi layout. Bộ đánh giá cũng cần loại được những implementation sai hợp lý và chấp nhận giải pháp đúng có cấu trúc khác reference.

Các tính chất về quyền truy cập hoặc trạng thái dữ liệu cần được kiểm tra ở mức tích hợp phù hợp. Khi kiểm định transaction hoặc uniqueness, test không thể mock chính thao tác cần xác minh. Dữ liệu thử nghiệm và các dịch vụ cục bộ được reset giữa các lần chạy. Các tích hợp bên ngoài dùng sandbox hoặc fixture có kiểm soát, không thực hiện thanh toán hay gửi email production.

### 4.4. Quy trình chạy

Mỗi lần chạy sử dụng một workspace và session mới. Thứ tự điều kiện được ngẫu nhiên hóa trong từng block tác vụ và cấu hình model/harness. Prompt, trạng thái dữ liệu và giới hạn tài nguyên được cố định. Tác giả lưu toàn bộ instructions được tải, tool trace, patch cuối và kết quả kiểm tra.

Đơn vị nhận điều kiện là một agent session. Các lần lặp trên cùng tác vụ có quan hệ phụ thuộc; task là cấp cần xét khi đánh giá độ bất định và phạm vi suy rộng. Nhiều runs trên một task không thay thế được sự đa dạng của task. Nếu nhiều model được dùng, kết quả chính được báo cáo riêng theo model/harness để tránh việc lấy trung bình che mất khác biệt.

## 5. Phép đo và kế hoạch phân tích

Outcome chính là joint success: chức năng mới đạt acceptance checks và những hành vi cũ cần giữ đạt preservation checks. Hai thành phần cũng được báo cáo riêng để phân biệt trường hợp thiếu chức năng với trường hợp thêm được chức năng nhưng gây regression. Build/runtime failure được ghi như một giai đoạn thất bại riêng.

Chi phí token, thời gian và số vòng sửa là các outcome bổ sung. Những chỉ số này mô tả hệ thống agent trong giới hạn tài nguyên được chọn; chúng không được diễn giải thành năng suất con người. Phân tích lỗi dựa trên trace và hành vi quan sát được. Một mẫu lỗi cần được người đánh giá thứ hai rà soát, nếu có thể bố trí, để hạn chế việc chỉ dựa vào phân loại của tác giả hoặc LLM.

Coverage và mutation testing có thể hỗ trợ kiểm tra instrument. Zhao và cộng sự cho thấy quan hệ giữa các proxy này với khả năng phát hiện lỗi phụ thuộc vào setting [7]. Vì thế, kết luận chính sẽ dựa vào yêu cầu hành vi có căn cứ và checks thực thi đã được kiểm định.

Trong từng cấu hình model/harness, nghiên cứu dự kiến ước lượng chênh lệch xác suất joint success, lấy trọng số bằng nhau giữa những tác vụ đủ điều kiện trong tập đã cố định. Gọi p00, p01, p10 và p11 là xác suất tương ứng của bốn điều kiện. Tác động của kiểm chứng được so trong từng layout; tác động của layout được so ở từng mức kiểm chứng. Tương tác trên thang chênh lệch xác suất là (p11 − p10) − (p01 − p00).

Kết quả cần kèm khoảng bất định và cách xử lý phụ thuộc giữa repetitions. Mô hình phân cấp hoặc resampling ở cấp task sẽ được lựa chọn trước confirmatory runs, dựa trên cấu trúc dữ liệu khả thi. Chưa ấn định số task hay số lần lặp. Pilot dùng để đánh giá instrument và hỗ trợ lập kế hoạch precision. Nếu tài nguyên không đủ để ước lượng interaction chính xác, phần này được ghi trước là phân tích thăm dò.

Mọi lần thử đều được ghi nhận. Timeout hoặc thất bại do agent trong budget không được tùy ý chạy lại đến khi thành công. Lỗi hạ tầng có quy tắc xử lý riêng được xác định trước. Phân tích chỉ trên những runs build được sẽ được coi là bổ sung vì có thể chọn ra những tập con khác nhau giữa các điều kiện.

## 6. Phạm vi và những nguy cơ cần kiểm soát

Chuyển từ layout theo tầng sang theo tính năng có thể đổi import graph, proximity và những ví dụ mã dễ nhìn thấy. Kết quả vì vậy gắn với phép chuyển đổi được triển khai. Nghiên cứu cần ghi lại khác biệt và kiểm tra những giải thích thay thế trước khi quy tác động cho colocation.

Tác giả đồng thời xây SmartKit và thiết kế phép đo nên có nguy cơ ưu tiên yêu cầu hoặc cách triển khai quen thuộc. Oracle cần kiểm tra hành vi, chấp nhận nhiều implementation đúng và được rà soát độc lập khi có thể. Kiểm tra bắt buộc đúng đường dẫn SmartKit chỉ phù hợp khi chính đường dẫn là yêu cầu task có lý do rõ ràng.

Nghiên cứu chính trên một repository cho phép kết luận về SmartKit trong thiết lập được đánh giá. Khả năng chuyển giao sang starter kit khác cần replication riêng. Để giữ scope khả thi, bước replication được quyết định sau pilot và trước khi đưa claim vượt khỏi SmartKit vào paper.

Novelty vẫn là một rủi ro cần xử lý ở giai đoạn chuẩn bị. Nếu đối chiếu artifact cho thấy công trình trước đã kiểm tra cùng can thiệp và outcome, nghiên cứu cần được định vị là replication có mở rộng cụ thể hoặc điều chỉnh câu hỏi. Không có chênh lệch thống kê với uncertainty lớn cũng chưa chứng minh hai thiết kế tương đương.

## 7. Đóng góp dự kiến và kế hoạch thực hiện

Nghiên cứu dự kiến cung cấp dữ liệu về ảnh hưởng của hai quyết định thiết kế trong SmartKit, cùng tập tác vụ và công cụ đánh giá có thể chạy lại. Kết quả có thể xác định thành phần hỗ trợ agent, thành phần chỉ tăng chi phí hoặc những điều kiện làm tác động thay đổi. Những kết luận đó sẽ là căn cứ để cải tiến SmartKit.

| Giai đoạn | Công việc và sản phẩm cần có |
|---|---|
| Chuẩn bị baseline | Snapshot, môi trường chạy và báo cáo lỗi có sẵn; xác nhận hai layouts đạt cùng checks ban đầu |
| Xây dựng tasks và oracle | Task cards, nguồn yêu cầu, reference implementations, acceptance/preservation checks và nhật ký loại trừ |
| Pilot | Chạy trên development tasks; kiểm tra instrument, instruction exposure, chi phí và cấu trúc biến thiên |
| Cố định nghiên cứu chính | Chốt tasks, agent settings, allocation, sample/precision plan, quy tắc rerun và phân tích trước outcomes mới |
| Thực nghiệm và viết paper | Phân tích dữ liệu, công bố artifact phù hợp và thực hiện replication nếu scope kết luận yêu cầu |

Chỉ chốt quy mô thí nghiệm chính sau khi baseline và tasks có thể chạy được. Nếu không tạo được hai layout tương đương trong phạm vi hành vi đã đặc tả, cần sửa phép can thiệp trước khi chạy agent. Nếu bộ checks cơ bản đã bao phủ hầu hết hành vi mục tiêu, cần xem lại giá trị của V1 thay vì cố làm yếu V0.

Artifact mỗi run sẽ gồm repo commit, môi trường và dependencies, model/harness version, prompt/instructions, tool trace, patch, kết quả checks và số liệu chi phí. Nhật ký thay đổi protocol giúp phân biệt phát hiện thăm dò với kiểm định đã lên kế hoạch. Khi gửi bài, tác giả khai báo hỗ trợ AI theo yêu cầu của venue và giữ lại các bản nháp cùng hồ sơ kiểm chứng.

## 8. Những nội dung cần trao đổi với giáo sư

Buổi trao đổi cần xác định phạm vi đóng góp phù hợp: một nghiên cứu thực nghiệm sâu trên SmartKit hay một nghiên cứu có thêm replication độc lập. Cũng cần thống nhất tiêu chí chọn yêu cầu SaaS có ý nghĩa, cách rà soát oracle và nguồn lực để chạy nhiều cấu hình agent.

Quyết định trước mắt là liệu nên đầu tư giai đoạn baseline và task validation cho thiết kế này. Kết quả của giai đoạn đó sẽ cho biết phép so sánh có công bằng, tasks có đủ căn cứ và quy mô thí nghiệm nào khả thi trước khi chốt RQ cùng kế hoạch paper.

## Tài liệu tham khảo

[1] Springblade. SmartKit. Repository phần mềm, snapshot 2c92d3920d967b9ebf0960ba7890754baa3c90d7. [Mã nguồn](https://github.com/Springblade/SmartKit/tree/2c92d3920d967b9ebf0960ba7890754baa3c90d7).

[2] Thibaud Gloaguen và cộng sự. Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? 2026. arXiv:2602.11988, phiên bản 3. [Bài gốc](https://arxiv.org/abs/2602.11988v3).

[3] Haichao Zhu và cộng sự. Precedent or Intent? What Coding Agents Follow When Evolving Existing Code. 2026. arXiv:2610.38244, phiên bản 1. [Bài gốc](https://arxiv.org/abs/2610.38244v1).

[4] Francesco Dente, Dario Satriani và Paolo Papotti. Constraint Decay: The Fragility of LLM Agents in Backend Code Generation. 2026. arXiv:2605.06445, phiên bản 2. [Bài gốc](https://arxiv.org/abs/2605.06445v2).

[5] Shaswat Patel và cộng sự. Is Agent Code Less Maintainable Than Human Code? 2026. arXiv:2606.21804, phiên bản 2. [Bài gốc](https://arxiv.org/abs/2606.21804v2).

[6] Markus Borg và cộng sự. Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability. Empirical Software Engineering, 31, bài 161, 2026. DOI: 10.1007/s10664-026-10889-1. [Bài gốc](https://link.springer.com/article/10.1007/s10664-026-10889-1).

[7] Junda Zhao, Shurui Zhou và Eldan Cohen. Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability Study). 2026. arXiv:2607.22880, phiên bản 1; được chấp nhận tại ISSTA 2026 theo thông tin bài gốc. DOI: 10.1145/3832093. [Bài gốc](https://arxiv.org/abs/2607.22880v1).


# [P2] research/smartkit-study-protocol-v0.md

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


# [P3] research/smartkit-task-audit-v0.csv

task_id,origin,status,proposed_change,source_surface,preservation_candidate,required_oracle,next_validation
SK-T01,constructed_candidate,unvalidated,"Thêm bộ lọc trạng thái vào lịch sử đơn hàng","src/features/billing/actions/list-orders.ts; src/app/dashboard/billing/history/page.tsx","Người dùng chỉ nhận đơn thuộc quyền truy cập của mình; hành vi không lọc giữ nguyên","Fixture nhiều user và trạng thái; kiểm tra API/action và UI trên DB test","Đọc đầy đủ listOrders; chốt pagination/empty/error semantics; xác nhận yêu cầu mới chưa có"
SK-T02,constructed_candidate,unvalidated,"Thêm thao tác hủy nhiều đơn pending của người dùng","src/features/billing/actions/cancel-order.ts; src/features/billing/actions/list-orders.ts","Không hủy đơn của người khác hoặc đơn không còn pending","Acceptance cho batch; ownership/state tests; xác định chính sách partial failure trước","Xác nhận nhu cầu thực tế; chọn rõ atomic hay partial success; không tự suy ra từ cancelOrder đơn lẻ"
SK-T03,constructed_candidate,unvalidated,"Hiển thị hướng dẫn xử lý khác nhau theo lý do giao dịch bị bỏ qua","src/features/billing/process-sepay-payload.ts; src/features/billing/process-order-completion.ts; src/features/billing/errors.ts","Hiển thị mới không đổi persistence/audit/completion; không lộ dữ liệu người dùng khác","Reference behavior trước thay đổi; DB integration và browser checks theo reason","Tìm nguồn nhu cầu; xác định ai được thấy reason; kiểm tra UI/route đang có trước khi chọn"
SK-T04,constructed_candidate,unvalidated,"Thêm bộ lọc vai trò cho danh sách người dùng quản trị","src/app/dashboard/admin/users/page.tsx; src/features/auth/lib/permissions.ts","Người không có quyền admin không đọc được danh sách; filter không làm lỏng authorization","Admin/non-admin HTTP/browser sessions và dữ liệu nhiều role","Kiểm tra trang hiện tại; ghi chính sách role được phép; xác nhận filter chưa có"
SK-T05,constructed_candidate,unvalidated,"Thêm tìm kiếm theo mã đơn vào lịch sử đơn hàng","src/features/billing/actions/list-orders.ts; src/features/billing/payment-content.ts; src/app/dashboard/billing/history/page.tsx","Search không bỏ ownership guard; không đổi cách nhận diện mã trong luồng thanh toán","Search matching contract; cross-user fixtures; existing payment-content regressions","Xác định exact hay prefix search và case handling; kiểm tra tính năng hiện có; không suy từ gold patch"
SK-T06,constructed_candidate,unvalidated,"Thêm hiển thị trạng thái đơn trong một view dashboard mới","src/features/billing/actions/check-order-status.ts; src/app/dashboard/page.tsx; src/features/billing/components/OrderStatusBadge.tsx","Không lộ trạng thái đơn ngoài quyền truy cập; giữ semantics thời gian và trạng thái gốc","Multi-user acceptance; expired/cancelled/completed fixtures; route/browser integration","Chốt mục đích view và các trường được hiển thị; xác nhận baseline/reference và giải pháp hợp lệ khác"


# [E1] research/execution/history-filter-qualification.md

# Development task qualification — history status filter

Date: 2026-11-10. Status: locally development-qualified for the exercised contracts; not an independently reviewed main-study task and not yet ported to both layouts.

## Deliverables

- `history-filter-task-card.md`: implementer-facing behavior contract and provenance.
- `history-filter-reference.patch`: reference feature patch relative to the baseline history page.
- `history-page-before-filter.tsx.txt`: exact pre-feature page saved before implementation.
- `SmartKit/scripts/check-order-baseline.integration.ts`: 10 existing baseline checks plus 5 filter-task checks.
- `SmartKit/vitest.orders.config.ts`: explicit integration configuration; no extra packages installed.
- `verify-history-filter-mutations.py`: development evaluator probes with page restoration in a finally block.

The working tree currently contains the reference implementation. The task starting snapshot must exclude `history-filter-reference.patch`; retain migration/seed and ownership repairs. These repairs, reference solution and evaluator are distinct artifacts. No baseline/task set has been frozen or committed by this work.

## Reference behavior

The history page offers a labelled native select and GET form, backed by a status query parameter. It accepts pending/completed/cancelled/expired, with completed labelled Paid. All statuses is represented by the empty value. Invalid or repeated parameters fall back to All statuses. Valid filters with no matches have a clear message and a View all orders link. The SQL combines owner and optional status predicates; descending creation time and existing row data remain intact.

## Evaluator and evidence

The isolated local `smartkit_orders_test` PostgreSQL database is shared with a local development server on port 3107. Each run creates three ordinary users: two with one order in each of four states, one without orders. The evaluator performs real HTTP login, parses server-rendered HTML and checks exact fixture order codes. It checks every status for both owners, URL/selection agreement, controls/reset, invalid inputs, ordering, empty results, unchanged order rows and unauthenticated redirects. Existing action checks still use stubbed session/cache boundaries with real SQL.

The initial HTML parser, Happy DOM, misreported the selected value in a minimal native select example. A standalone comparison with installed JSDOM showed the correct value. The evaluator now uses JSDOM without executing page scripts. Selection checks were retained rather than removed.

| Implementation | Observed result | Evidence |
|---|---|---|
| Unsolved baseline | 4 failures, 11 passes | `logs/history-filter-unsolved.log` |
| SQL-filter reference | 15/15 pass | `logs/history-filter-reference-final.log` |
| Ignore status filter | 1 assertion failure | `logs/history-filter-ignore-filter.log` |
| Remove ownership predicate | 6 assertion failures, including foreign codes in history | `logs/history-filter-remove-owner.log` |
| Always query pending | 1 assertion failure on completed subset | `logs/history-filter-wrong-status.log` |
| Correct in-memory filtering after owner-scoped query | 15/15 pass | `logs/history-filter-correct-in-memory-filter.log` |

Mutation outcomes and individual variant patches are retained in `logs/history-filter-mutation-results.json` and `logs/history-filter-*.patch`. The deliberately incorrect variants failed behavioral assertions, not merely compilation or infrastructure checks. The alternative correct implementation passed, providing limited evidence that the evaluator accepts more than the SQL reference approach. The reference was restored and passed again afterward.

Existing 14 unit/component tests and TypeScript passed after the feature; see `logs/history-filter-check-1.log` and `history-filter-check-0.log` respectively. Production build passed (`logs/history-filter-build.log`); this does not establish production TLS connectivity. Post-test SQL confirmed zero remaining users/orders/plans (`logs/history-filter-cleanup.log`); test server and container were stopped.

## Reproduce

Follow the database/server setup in `order-baseline-verification.md`. With the server running and local environment pointing to `smartkit_orders_test`, run:

```powershell
pnpm exec vitest run --config vitest.orders.config.ts
python ../execution/verify-history-filter-mutations.py
```

Run mutation probes alone while nobody else edits the page; they temporarily replace the reference page and restore its exact bytes. The integration command needs the history-filter reference applied to pass all 15 cases. To exercise only baseline behavior on an unsolved task, use `pnpm exec vitest run --config vitest.orders.config.ts -t "real HTTP ownership checks|actual server actions"`, rather than reporting task acceptance failures as baseline defects.

## Interpretation and next gate

This supplies a concrete development example of extending SmartKit while checking preservation. It does not show that one layout improves agent performance, that these checks detect every defect, or that the task represents typical SaaS requirements.

Browser interaction/hydration, independent review, performance, and error/loading UX are not qualified by these HTTP/DOM checks. Test fixtures and gold patches have been seen during instrument development; keep this task outside held-out main-study outcomes.

Next gate: construct equivalent layered/feature baseline variants and port this development task, reference solution and evaluator to both. Preserve identical logic, domain information, dependencies, instructions appropriate to each layout, and check visibility. Freeze task contracts and review limits separately before main trials.


# [E2] research/execution/layout-qualification.md

# Paired layout qualification — 2026-11-10

Status: both layouts pass the exercised local development contracts. Not a proof of equivalence for every possible execution. No coding-agent performance trial has been run.

## Snapshots and transformation

- `layouts/feature`: the existing domain-first layout, with the earlier baseline migration/seed and ownership repairs, and without the history-filter solution.
- `layouts/layered`: a role-first counterpart built from exactly the same inputs. Next.js `src/app` routes, database schema/migrations, UI primitives, public assets and test locations stay in place.
- `build-layout-variants.py`: stdlib-only generator that refuses to overwrite an existing snapshot directory.
- `layout-manifest.json`: original revision, source-to-destination mapping, SHA-256 file digests and instruction digests. The source is the recorded working tree, not an unchanged upstream commit.

Each snapshot contains 142 copied/transformed files plus its own AGENTS.md. Forty-seven modules move in the layered layout:

| Original | Role-first location |
|---|---|
| `src/features/{domain}/components/*` | `src/components/{domain}/*` |
| `.../hooks/*` | `src/hooks/{domain}/*` |
| `.../actions/*` | `src/actions/{domain}/*` |
| `.../types/*` | `src/types/{domain}/*` |
| `.../lib/*` | `src/lib/{domain}/*` |
| `.../emails/*` | `src/emails/{domain}/*` |
| Root processing modules/config/entry points | `src/services/{domain}/*` |
| Root `types.ts` | `src/types/{domain}.ts` |
| Auth `client.ts` | `src/lib/auth/client.ts` |

Imports/exports, dynamic imports and mock module paths are mechanically updated. Some relative paths become `@/` aliases. The generator resolves quoted local module paths to original module identities and checks that transformed code/config bodies are otherwise identical. It rejects path collisions. No business logic, dependency, schema, function signature, error handling or server/client directive was intentionally changed. One historical source comment still mentions a former features path; comments were preserved by the mechanical transformation.

Both original AGENTS.md files are replaced with the same common instructions and a layout-specific paragraph. Shared domain facts remain in the same README and code. The original feature-only instructions are not used to steer the layered counterpart. Existing tests stay in the same centralized locations to avoid also changing test placement.

## Behavioral checks

`check-layout-behavior.py` starts one development server at a time on localhost:3107, using the isolated local PostgreSQL `smartkit_orders_test` database. It creates/cleans fixtures through the previously qualified integration evaluator. For each layout it checks the unsolved baseline, temporarily applies the corresponding reference page, tests the development task, then restores and rechecks the unsolved baseline.

| Check | Feature | Layered |
|---|---|---|
| Frozen-lockfile dependency install | Pass | Pass |
| TypeScript | Pass | Pass |
| Existing unit/component suite | 14/14 | 14/14 |
| Production compilation | Pass | Pass |
| Baseline ownership/status/cancel integration | 10/10 | 10/10 |
| Reference history-filter task + preservation | 15/15 | 15/15 |
| Restored unsolved baseline | 10/10 | 10/10 |

The 5 filter-specific checks are intentionally excluded from baseline-only runs; their absence is the task to solve. Read the detailed test boundaries in `history-filter-qualification.md`: history/status use real HTTP and database; direct action checks stub session lookup and cache invalidation.

Evidence: `layout-behavior-results.json`, `logs/layout-{feature,layered}-{install,types,unit,build,baseline,reference,restored-baseline,server}.log`. `layout-snapshot-verification.json` confirms all 284 copied/transformed file hashes match after restoring solutions and the generated next-env declarations. `logs/layout-cleanup.log` confirms zero remaining fixture users/orders/plans. Development servers and the test database container were stopped.

## Reference isolation and reproducibility

Gold pages and patches are stored outside the snapshots:

- `history-reference-feature.tsx.txt` / `history-reference-feature.patch`.
- `history-reference-layered.tsx.txt` / `history-reference-layered.patch`.

The generator excludes `.git`, `.next`, node_modules, real `.env`, local memory and IDE instructions from its input set. For this local qualification only, ignored `.env` files were created from the known local test setup. Each snapshot ran `pnpm install --frozen-lockfile`. Production compilation passing does not resolve the separate production database TLS issue.

To repeat runtime checks, start the existing isolated test container, configure each snapshot with the same localhost:3107 auth/app URLs and the dedicated `smartkit_orders_test` database, and run `python research/execution/check-layout-behavior.py` from the Paper workspace. Fixtures reset on each run. The development-task reference is restored to baseline even on failure. Generation requires a new output location or explicit archival of previous snapshots; it will not silently overwrite them.

## Limits and next gate

These snapshots are qualification workspaces. They contain development evaluator files and are nested under the research workspace; they are not yet isolated agent trial packages. Both gold solutions and parent-workspace instructions/artifacts must be inaccessible in actual agent trials. No V0/V1 test-visibility allocation is claimed here.

Scope is one domain-first layout and one concrete role-first layout of SmartKit. Local structural checks and tested contracts support moving forward; browser interaction, production runtime, all billing integrations, independent review and general equivalence remain outside these observations. There is no evidence here that either layout improves agent outcomes.

Next: specify which checks the agent sees in V0 and V1, keep the final evaluator hidden and identical across all four cells, and build isolated resettable trial packages. Then perform the development pilot before locking main-study tasks and protocol.


# [E3] research/execution/history-filter-task-card.md

# DEV-HISTORY-STATUS-01 — development task, not a main-study task

Origin: constructed from the SmartKit history workflow; no historical issue or user-demand evidence is claimed. The existing listOrders action already supports status filtering, but the history page has a separate query and no filter control.

Starting point: upstream revision `2c92d3920d967b9ebf0960ba7890754baa3c90d7` plus separately recorded migration/seed and listOrders ownership repairs. History-filter reference code must not be included in the task's starting snapshot.

## Requirement supplied to the implementer

Add a labelled status filter to the authenticated payment history page. Offer All statuses, Pending, Paid (stored as completed), Cancelled and Expired. Apply the chosen filter through a GET submission using the `status` query parameter. Reloading or opening that URL must preserve the selected option and displayed results. Selecting All statuses must restore the complete history for the current user.

Accept exactly pending/completed/cancelled/expired. Missing, empty, invalid or repeated status parameters fall back to All statuses. If a valid filter has no matches, show a clear empty-result message while retaining the filter and an accessible way to return to all orders.

Preserve authentication, ownership restrictions, descending creation-time ordering, and existing order information. Viewing/filtering must not alter stored orders or change the status API or cancellation behavior. Multiple correct implementations are allowed; no required file list, query method, component structure or patch is part of the task contract.

## Qualification evidence to collect

Acceptance: correct subsets for all four states, URL/selection agreement, functional GET form and reset, invalid input policy and empty results.

Preservation: cross-user exclusion for every filter, unfiltered history/order fields/order, unauthenticated redirect, unchanged database rows, and existing status/cancel checks.

Evaluator uses a real local development server, real login cookies, PostgreSQL and rendered HTML parsed as a DOM. Server action preservation tests stub only session/cache boundaries. This is not a browser interaction test or an independent human review.

Development fixtures: two ordinary users with four states each plus one user without orders. Fixture IDs are generated per run and removed afterward. Development fixtures and outcomes must not be reused as held-out main-study tasks or observations.

Only call this task development-qualified after the reference passes and deliberately incorrect implementations fail for the intended assertions. Layout portability and independent review remain separate gates.


# [L-precedent] Primary-source excerpts
Archive research/execution/research-direction-review/sources/precedent.md. Source URL Source: https://arxiv.org/html/2610.38244v1

### 3.3 Stage 2: Manipulating Repository Precedents

Stage 2 restores the six endpoints and rewrites the construct under study in a controlled subset of them. For ID serialization, we change an existing endpoint from "id": task.id to "id": str(task.id); all other code in that endpoint stays identical. The other pairs are rewritten analogously, changing only the construct under study. Throughout Stage 2, the task description asks the agent to follow the conventions of the existing code without naming the implementation choice, mirroring common contribution guidelines. Any shift toward the alternative must therefore come from the code itself.

Support Level and Conditions.
We call the number of files in a group (local or sibling-resource) that use the alternative the group’s _support level_ (k/3k/3). For each pair, we construct eight conditions (Figure [4](https://arxiv.org/html/2610.38244v1#S3.F4 "Figure 4 ‣ 3.3 Stage 2: Manipulating Repository Precedents ‣ 3 Approach ‣ Precedent or Intent?What Coding Agents Follow When Evolving Existing Code"), upper rows):

- •


_Agreeing groups:_ all six existing endpoints use the baseline (“Both baseline”; 0/30/3, 0/30/3) or the alternative (“Both alternative”; 3/33/3, 3/33/3).

- •


_Local support:_ local support 1/31/3, 2/32/3, or 3/33/3, with all sibling-resource files at the baseline.

- •


_Sibling-resource support:_ sibling-resource support 1/31/3, 2/32/3, or 3/33/3, with all local files at the baseline.


We call this design _bidirectional_ because each group is varied while the other is held at the baseline, so the influence of the two groups can be compared at the same support level. Whenever one group supports the alternative, the two groups conflict; at 3/33/3 they disagree completely, and comparing local 3/33/3 with sibling-resource 3/33/3 shows which group prevails in a direct conflict. Comparing these conflicting conditions with the agreeing ones shows whether agreement between the groups strengthens adoption.

File Identity.
In the eight conditions, each intermediate support level uses one fixed assignment of the alternative to files; at local support 1/31/3, for example, it appears in tasks\_list (Figure [4](https://arxiv.org/html/2610.38244v1#S3.F4 "Figure 4 ‣ 3.3 Stage 2: Manipulating Repository Precedents ‣ 3 Approach ‣ Precedent or Intent?What Coding Agents Follow When Evolving Existing Code"), “default”). Raising the support level therefore also changes _which_ files carry the alternative, so example count and file identity are confounded. To separate them, we hold the support level fixed and vary only the placement: at 1/31/3 support, we place the alternative in the create, update, or list endpoint (Figure [4](https://arxiv.org/html/2610.38244v1#S3.F4 "Figure 4 ‣ 3.3 Stage 2: Manipulating Repository Precedents ‣ 3 Approach ‣ Precedent or Intent?What Coding Agents Follow When Evolving Existing Code"), lower rows); at 2/32/3 support, in each of the three pairs of these endpoints. We first conduct this analysis exploratorily for ID serialization with one agent, including a control that changes only module registration and import order, and then replicate it in three further pair–agent settings (Section [4.3](https://arxiv.org/html/2610.38244v1#S4.SS3 "4.3 RQ2: Influence of Local Precedent ‣ 4 Evaluation ‣ Precedent or Intent?What Coding Agents Follow When Evolving Existing Code")).

|  | Tasks (local resource) | Projects (sibling resource) |
|  | create | update | list | create | update | list |
| Varying precedent support |
| All numeric |  |  |  |  |  |  |
| Local support 1/31/3 |  |  |  |  |  |  |
| Local support 2/32/3 |  |  |  |  |  |  |
| Sibling support 1/31/3 |  |  |  |  |  |  |
| All string |  |  |  |  |  |  |
| Fixed 1/31/3 local support, different file |
| In create |  |  |  |  |  |  |
| In update |  |  |  |  |  |  |
| In list (default) |  |  |  |  |  |  |

numeric ID (task.id)   string ID (str(task.id))

Figure 4: Illustrative repository interventions for ID serialization. Each square is one existing endpoint file. The upper rows vary how many local or sibling-resource files use string IDs; the lower rows hold the local support level at 1/31/3 and change only which file carries the alternative (“default” marks the assignment used for local support 1/31/3 above). The requested new endpoint is absent from every variant.


### 3.5 Measuring Outcomes

We evaluate each generated edit on two separate outcomes. _Functional success_ indicates whether the edit passes the pair-specific hidden tests, which accept either implementation; sessions that produce no implementation count as functional failures. _Implementation choice_ indicates which alternative the edit adopts, determined by pair-specific classifiers that inspect the produced code. Outputs that use neither or both alternatives are reported as unclassifiable rather than assigned a label. For Stages 1 and 2, we report the _adoption rate_: the share of classifiable outputs that use the designated alternative. For Stage 3, where the task prescribes a target, we use a _joint outcome_ that requires both functional success and adoption of the target. Separating the two outcomes prevents a passing test suite from hiding which implementation an agent selected.


## 5 Threats to Validity

Construct Validity.
Our local–sibling comparison jointly varies task relatedness and repository location, so it does not distinguish their individual effects. The experiments control which precedents are available, not which ones agents attend to. The zero-precedent condition measures task-specific choices without relevant endpoint examples rather than context-free model preferences. Native instruction-file experiments evaluate rules loaded by the harness, not autonomous discovery. Our classifiers capture selected implementation patterns, and the outcomes concern implementation choice, not maintainability or overall code quality.

Internal Validity.
In the support-level experiments, example count and file assignment vary together. The separate placement analysis reveals sensitivity to file identity but does not explain the influence of tasks\_list. The zero-precedent and precedent conditions were collected under different execution settings. Technical interruptions required retries and disrupted scheduling in RQ4. An initial misconfigured Opus file-placement run was excluded and rerun; open-source outcome audits also led to revised classifications and recapture of incomplete patches. These changes and the trial accounting are documented in the artifact. Finally, differences between agents cannot be attributed to models alone, as each agent combines a model with its harness.

External Validity.
Fifteen repetitions per cell characterize variability under fixed conditions, not across tasks or repositories. The controlled experiments use one Flask API task family. The open-source study extends the local–sibling comparison to four repositories in three languages, but covers only two implementation choices, with explicit guidance evaluated for one. Support-level and file-placement effects remain untested beyond the controlled repository. The placement and guidance experiments cover selected settings, and the study evaluates agents from two providers.



# [L-constraint] Primary-source excerpts
Archive research/execution/research-direction-review/sources/constraint.md. Source URL Source: https://arxiv.org/html/2605.06445v2

### 3.2 Constraint Dimensions

To systematically evaluate the effect of constraints, we define three orthogonal non-functional axes, which can be either included in or omitted from the code specification.

Architectural pattern. The code architecture is fixed: it must be organized following the Clean Architecture pattern ( [Martin, 2017](https://arxiv.org/html/2605.06445v2#bib.bib5 "")). Rather than spontaneously define a monolithic or arbitrary file structure, the agent must split the codebase into four domain layers with strict top-down dependency direction: routes/handlers, services/use cases, models/entities, and repository/data access. Each layer must reside in its own directory.

Database backend. The database layer is fixed: PostgreSQL or SQLite. The agent must persist data using a specific database engine. For PostgreSQL tasks, a pre-configured instance is provided in the execution environment; for SQLite, no external service is needed. In both cases, the schema must be created automatically at server startup.

ORM integration. The Object-Relational Mapper (ORM) framework is fixed: SQLAlchemy for Python, Sequelize for Node. The agent must adhere to the idiomatic query logic of the prescribed framework, instead of falling back to raw SQL or alternative mapping.

|     |     |     |
| --- | --- | --- |
| Level | Active Constraints | \# Variants |
| L0 | WF only (baseline) | 8 |
| L1 | WF+Arch \|\\,\|\\,WF+SQLite \|\\,\|\\,WF+PG | 24 |
| L2 | WF+Arch+SQLite \|\\,\|\\,WF+Arch+PG \|\\,\|\\,WF+SQLite+ORM \|\\,\|\\,WF+PG+ORM | 32 |
| L3 | WF+Arch+SQLite+ORM \|\\,\|\\,WF+Arch+PG+ORM | 16 |

Table 1: Constraint levels and task variants. WF = Web Framework (always active), Arch = Clean Architecture, PG = PostgreSQL. Variants within a level are separated by \|\|.

Unlike the three axes above, the web framework is always specified: an agent must target some framework to produce executable code. We therefore treat framework as a fixed baseline constraint present at every level. To quantify the effect of additional structural complexity, we systematically compose the three axes into task variants of increasing specification density (L0 to L3), as in Table [1](https://arxiv.org/html/2605.06445v2#S3.T1 "Table 1 ‣ 3.2 Constraint Dimensions ‣ 3 Methodology ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation").
Each variant is instantiated across all 8 frameworks, yielding 80 generation tasks in total.

Although simple and helpful for human developers, these non-functional requirements isolate constraint composition as an added challenge for LLM agents.


### 3.3 Evaluation Pipeline

To guarantee reproducibility and preclude state contamination, each task is executed in an isolated Docker environment following a build and evaluate pipeline. In the build phase, the agent operates within a first container, where it can code, build, and start the server. Next, in the evaluation phase, the agent code patch is applied in a pristine container and the behavioral test suite is executed. In both phases, a container-dedicated, ephemeral PostgreSQL 16 instance is available (full infrastructure details in Appendix [J](https://arxiv.org/html/2605.06445v2#A10 "Appendix J Execution Pipeline ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation")).

Behavioral testing. Since all task instances target a unified OpenAPI specification, all implementations are evaluated against a unified HTTP behavioral test suite covering the whole specification.
The suite comprises 32 requests covering all 19 API endpoints and 291 assertions that verify response structure, types, status codes, and state transitions across a stateful sequence of interdependent CRUD operations (breakdown in Appendix [H](https://arxiv.org/html/2605.06445v2#A8 "Appendix H Behavioral Test Suite ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation")). This is a methodological choice: by testing the API behavior rather than its implementation, we decouple functional evaluation from internal code structure.

Verifier functions. To separate functional correctness from structural compliance, we introduce orthogonal verifier functions that detect whether the required architecture, database, and ORM constraints are actually satisfied (details in Appendix [C](https://arxiv.org/html/2605.06445v2#A3 "Appendix C Verifier Functions ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation")). (i) Architecture verifier: assesses the compliance to the four canonical Clean Architecture layers (routes, services, repositories, models) and scans every import to verify dependency order. (ii) Database verifier: scans the source lines for usage evidence of the imposed database engine while checking that no alternative engines are used; lock files are excluded. (iii) ORM verifier: detects whether the designated Object-Relational Mapper is used rather than raw SQL or framework-native data layer.

We define task success as the intersection of behavioral validity and constraint compliance. A completed task passes the entire behavioral test suite and satisfies each applicable verifier.


Sanity check: feature implementation tasks.
A natural concern is whether constraint decay is an artifact of the synthetic greenfield setting.
To test this, we construct 20 feature implementation tasks by ablating feature groups (161–2,604 lines across 2–46 files) from community-maintained RealWorld repositories (actual implementations of the API contract used in the generation tasks) that already embed a layered architecture, PostgreSQL, and an ORM, effectively simulating an L3 condition with implicit constraints. Each agent must read the existing codebase, infer its conventions, and re-implement the missing functionality (full task design in Appendix [G](https://arxiv.org/html/2605.06445v2#A7 "Appendix G Feature Implementation Task Design ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation")). As shown in Table [3(b)](https://arxiv.org/html/2605.06445v2#S5.T3.st2 "In Table 3 ‣ 5.1 RQ1: Effect of Constraint Accumulation ‣ 5 Results ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation"), performance remains low: only GPT-5.2 exceeds 50% pass@1. While we cannot isolate structural constraints as the sole cause of difficulty in this setting, the results confirm that the challenges observed in greenfield generation are not artifacts of asking agents to build repositories from scratch; they persist when agents must infer and respect constraints from an existing codebase.

Takeaways for RQ1. Structural constraints cause steep, universal decay: capable configurations
lose 27.48 pp A% from L0 to L3 on average. Database constraints drive most of this decline.


### C.4 Limitations

All three verifiers are deliberately conservative in their design:

Static-only. The verifiers analyze source text, not runtime behavior. An agent could satisfy the verifier’s patterns while violating constraints at runtime (e.g., importing SQLAlchemy but executing raw SQL). This means false positives are possible, but as discussed in Appendix [D](https://arxiv.org/html/2605.06445v2#A4 "Appendix D Verifier Impact on Reported Metrics ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation"), they can only weaken the observed decay signal.

Pattern-based. Regex matching cannot capture all possible naming conventions or import patterns. We mitigate this with broad alias sets and case-insensitive matching, and validate empirically that the false-reject rate is ≤\\leq0.5% (§ [D](https://arxiv.org/html/2605.06445v2#A4 "Appendix D Verifier Impact on Reported Metrics ‣ Constraint Decay: The Fragility of LLM Agents in Backend Code Generation")).



# [L-featurearc] Primary-source excerpts
Archive research/execution/research-direction-review/sources/featurearc.md. Source URL Source: https://arxiv.org/html/2610.37434v1

### II-ATask Definition

A _task_ follows one user-visible feature through an ordered sequence of nn stages, m0,…,mn−1m\_{0},\\dots,m\_{n-1}, in one repository.
The first stage implements the initial version, and each later stage extends the same feature.
We call this sequence a _same-feature chain_.

In the task illustrated in Figure [1](https://arxiv.org/html/2610.37434v1#S1.F1 "Fig. 1 ‣ I Introduction ‣ FeatureArc: Benchmarking Coding Agents on Evolving Features"), the first stage, m0m\_{0}, adds app.run(), which starts a run and returns its task identifier.
The second stage, m1m\_{1}, adds app.runAndWait(), which calls app.run() and waits for completion.
The third stage, m2m\_{2}, extends the feature to accept file input and adds files.upload().
Each stage builds on the agent’s implementation of the preceding requirements.

The task provides an initial repository state S0S\_{0}, a container image with the required dependencies, and a specification for each stage.
Each specification has two parts: a _requirements document_ describing the requested behavior and acceptance criteria, and an _interface contract_ stating the names, signatures, constants, and error messages needed to use that behavior.
The agent receives the specifications one at a time and implements each new request on top of its own earlier work.

Hidden _fail-to-pass_ (F2P) tests check the new behavior requested at a stage, and _pass-to-pass_ (P2P) tests check existing behavior \[ [19](https://arxiv.org/html/2610.37434v1#bib.bib19 "")\].
A separate pair of chain-level suites checks the complete feature on the final workspace.
Section [III](https://arxiv.org/html/2610.37434v1#S3 "III Benchmark Construction ‣ FeatureArc: Benchmarking Coding Agents on Evolving Features") explains how we recover the stages, write their specifications, and validate these tests against reference code.


### II-BEvaluation Process

![Refer to caption](https://arxiv.org/html/2610.37434v1/fig-2b-eval-protocol.png)Fig. 2: L4 evaluation process.

Figure [2](https://arxiv.org/html/2610.37434v1#S2.F2 "Fig. 2 ‣ II-B Evaluation Process ‣ II Task Formulation ‣ FeatureArc: Benchmarking Coding Agents on Evolving Features") shows the L4 evaluation process.
One session and workspace persist through the whole task.
The agent can inspect its code and run its own checks; reference patches, hidden test suites, and future specifications stay private.
When the agent finishes a stage, a hidden acceptance check, called a stage gate, runs its F2P and P2P suites.
The stage is the implementation request; the gate checks its result, and both suites must pass for the stage to pass.
Failed stages are neither rolled back nor reported to the agent: the next stage starts from the code the agent just produced.
After mn−1m\_{n-1}, a chain gate runs the chain-level F2P and P2P suites on the final workspace to check the complete feature.


### III-FEvaluation-Set Curation

Multi-stage evaluation requires repeated model calls and sequential execution within each feature, with costs incurred for every evaluated agent.
Given these economic constraints, we select a high-quality subset of the constructed task pool as our evaluation set through three steps.

Stratified sampling.
To cover different languages and evolution lengths, we sample 100 candidate tasks, 25 per language, stratified by chain length.
This retains both short and longer feature-evolution chains in the candidate set.
A scan for test-used identifiers missing from the specifications identifies descriptions and contracts that need revision before execution.

Task-defect exclusion.
To identify task defects, we run candidate tasks with several models and inspect their execution trajectories.
We check these trajectories against the specifications, hidden tests, and reference implementations to distinguish task defects from agent errors.
This screening excludes seven tasks: five whose chain-level suites require unspecified behavior, one with a defective test suite, and one with a repository hook that intercepts the prompt.

Manual check.
To ensure that the selected tasks measure the intended feature-evolution setting, we manually check them for specification quality, alignment between interface contracts and hidden tests, and whether successive stages extend the same feature.
The resulting FeatureArc evaluation set contains 73 tasks with 263 stages from 53 repositories.
All reported agent comparisons use this same set.


### IV-DMetrics and Statistics

We adopt the following metrics; table abbreviations appear in parentheses.

- •


Single-stage pass rate m0m\_{0}: the fraction of tasks whose first stage passes both F2P and P2P, starting from the initial state S0S\_{0}.

- •


Chain-gate pass rate (Gate): the fraction of tasks whose chain gate passes on the final workspace.

- •


Continuation rate (Cont.): the stage pass rate at m1m\_{1} and later, conditioned on all earlier stages of that chain having passed.

- •


Stage F2P rate (F2P): the fraction of evaluated stages whose F2P suite passes.

- •


Prefix depth (Depth): the number of consecutive passed stages before the first failure, divided by chain length.

- •


Survival at mkm\_{k}: the fraction of tasks with more than kk stages whose stages m0..mkm\_{0}..m\_{k} all pass.

- •


Chain-level P2P failure (P2P↓\\downarrow): the fraction of tasks whose chain-level P2P suite fails.

- •


In-chain regression rate: among runs in which every stage passed F2P at completion, the fraction whose final workspace fails chain-level F2P.

- •


Pure regression rate: among runs whose final workspace passes chain-level F2P, the fraction that fail chain-level P2P.


For comparisons within the same task and stage, we split agents by the condition being compared and retain only task-stage groups containing both conditions.
We compute each condition’s F2P pass rate within each group, then average these rates equally across groups.
The agents in each group face the same requested stage but retain their own code and conversation histories.

Confidence intervals for agent performance are 95% bootstrap intervals \[ [35](https://arxiv.org/html/2610.37434v1#bib.bib35 "")\] with 4,000 resamples over tasks in FeatureArc.


### VI-BThreats to Validity

FeatureArc may not cover the full range of workflows encountered in real-world feature development.
To broaden coverage, it includes four widely used programming languages—Python, TypeScript, Rust, and Go—and seven application domains, with tasks stratified by language and chain length (Figure [4](https://arxiv.org/html/2610.37434v1#S3.F4 "Fig. 4 ‣ III-G Benchmark Characteristics ‣ III Benchmark Construction ‣ FeatureArc: Benchmarking Coding Agents on Evolving Features")).
This breadth, together with tasks mined from repository histories, helps the benchmark reflect agents’ performance on evolving requirements across practical development settings.



# [L-codethread] Primary-source excerpts
Archive research/execution/research-direction-review/sources/codethread.md. Source URL Source: https://arxiv.org/html/2606.21804v2

### 3.1 Step 1: Create a Two-Step Task

From each benchmark instance, we construct a two-step chain consisting of two dependent tasks and three code states: the Implementation Task and Follow-On Issue, and code states PR0\\text{PR}\_{0}, PR1\\text{PR}\_{1}, and PR2\\text{PR}\_{2}. To create the first state, PR0\\text{PR}\_{0}, we remove the target function bodies while preserving their signatures, leaving a skeleton version of the benchmark’s initial code state. This provides a starting point from which different authors can implement the intended functionality, similar to the use of skeleton code in prototyping, where an initial code structure is later fleshed out with implementation details [Ryoo et al. (2008)](https://arxiv.org/html/2606.21804v2#bib.bib32 ""); [Queirós (2013)](https://arxiv.org/html/2606.21804v2#bib.bib31 "").

The Implementation Task (PR0→PR1{\\text{PR}\_{0}}\\rightarrow{\\text{PR}\_{1}}) produces human and agent implementations of the same task. Using an LLM, we create an issue asking the author to restore the missing functionality in the skeletonized code. This issue is provided to the agent, which implements the requested functionality to produce the agent PR1\\text{PR}\_{1}. We filter out PR1\\text{PR}\_{1} solutions that have already solved the benchmark issue by requiring them to pass all Pass-to-Pass tests, confirming that the original functionality is restored, while still failing all Fail-to-Pass tests, confirming that the downstream issue is not yet resolved. This ensures that the agent PR1\\text{PR}\_{1} reflects the benchmark’s initial code state rather than a partial or complete solution to the Follow-On Issue; accordingly, the target methods are functionally equivalent across the two PR1\\text{PR}\_{1} versions. Although agents sometimes incidentally satisfy Fail-to-Pass tests while restoring functionality, the filter retains a large majority of instances. Appendix [A](https://arxiv.org/html/2606.21804v2#A1 "Appendix A Synthetic Problem Statement Construction for \"PR\"_1 ‣ Is Agent Code Less Maintainable Than Human Code?") shows the prompt used to generate Implementation Task statements, as well as the prompt given to models when solving it.

The Follow-On Issue (PR1→PR2\\text{PR}\_{1}\\rightarrow\\text{PR}\_{2}) is the original benchmark issue applied on top of the PR1 implementation. The problem statement and testing criteria for the Follow-On Issue are unchanged from the original benchmark, making it a downstream task whose difficulty may depend on the maintainability of the PR1 implementation. We evaluate whether the Follow-On Issue is resolved using the original benchmark test suite: a PR2\\text{PR}\_{2} solution is considered correct if it passes both the Pass-to-Pass tests, confirming that existing functionality is preserved, and the Fail-to-Pass tests, confirming that the original benchmark issue has been fixed.


### 3.2 Step 2: Set-up Authorship Scenarios

Using the two-step issue resolution pipeline, we vary authorship on PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2}, creating a total of three comparable authorship scenarios: human PR1\\text{PR}\_{1} followed by human PR2\\text{PR}\_{2} (HH), human PR1\\text{PR}\_{1} followed by agent PR2\\text{PR}\_{2} (HA), and agent PR1\\text{PR}\_{1} followed by agent PR2\\text{PR}\_{2} (AA).
The HH condition consists of the original developer’s PRs provided by each benchmark, acting as the human baseline against which the other conditions are compared. Comparing AA to HA isolates the downstream effect of PR1\\text{PR}\_{1} authorship on PR2\\text{PR}\_{2} success, allowing us to directly evaluate whether agent code imposes a maintainability burden on subsequent agent work in comparison to human code.

We focus on the maintainability costs that agents incur when building on prior code, comparing the outputs from the AA versus HA scenarios, as a growing fraction of developers use AI agents to extend existing codebases ( [Li et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib20 "")). The AH setting of a human performing the follow-on task on top of agent code would offer a complementary human-centric view (by comparing AH versus AA), but would require recruiting a substantial number of developers and is out of scope for this study. By keeping the PR2\\text{PR}\_{2} author fixed, CodeThread is scalable and can be applied to many existing issue-resolution benchmarks without additional data collection from humans.

| Benchmark | \# Instances | Filtered Subset | PR1 (Avg.) | PR2 (Avg.) | Task Types |
| --- | --- | --- | --- | --- | --- |
|  | Total | Filtered. | #Repos | #Lang | Files | Funcs | Files | Funcs |  |
| SWE-Bench Verified | 500 | 441 | 12 | 1 | 1.12 | 1.60 | 1.18 | 1.71 | BF |
| SWE-Bench Multilingual | 300 | 171 | 34 | 7 | 1.29 | 1.90 | 1.84 | 3.28 | BF |
| SWE-Bench Pro | 731 | 641 | 11 | 4 | 2.43 | 5.51 | 5.22 | 10.70 | BF, FI & RF |
| FeatBench | 156 | 124 | 22 | 1 | 1.52 | 2.54 | 2.35 | 4.03 | FI |
| Total | 1,687 | 1,377 | 78 | 10 | 1.79 | 3.54 | 3.25 | 6.30 |  |

Table 1: Benchmarks used in our CodeThread evaluation. We list each benchmark’s full and filtered instance counts, retaining only instances requiring function-level edits. For the filtered subset, we report repository and language coverage (#Repos, #Lang), the mean files and functions modified per PR stage (PR1\\text{PR}\_{1}, PR2\\text{PR}\_{2}), and a breakdown of task types: bug fixes (BF), feature implementation (FI), and refactoring (RF).


## Limitations

We present limitations of our study. First, we consider only two-step pull request chains (PR1→\\rightarrowPR2). Although this setup is sufficient to study whether the quality of an intermediate patch affects a downstream modification, it does not capture longer-horizon development trajectories, where technical debt may compound over multiple successive edits. Future work should explore constructing longer PR chains with function-level overlap across successive tasks.

Second, we filter PR1\\text{PR}\_{1} by instances where the agent PR1\\text{PR}\_{1} did not already address the Follow-On Issue. This filtering is necessary for the two-step chain to be well-defined, maintaining the separation between the two tasks so that the effect of authorship can be evaluated in isolation from functionality. However, it may introduce selection bias, since restricting the analyzed instances to where the agent did not solve the Follow-On Issue at PR1\\text{PR}\_{1} may not represent the agent’s natural behavior across the full benchmark. Nonetheless, the filter retains a large majority of instances, and we verify that cases where the model satisfies Fail-to-Pass tests in the Implementation Task are often incidental.

Third, as discussed in Section [3.2](https://arxiv.org/html/2606.21804v2#S3.SS2 "3.2 Step 2: Set-up Authorship Scenarios ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?"), our work does not study the effect of human-authored PR2\\text{PR}\_{2} on top of agent-authored PR1\\text{PR}\_{1} (AH) setting. Doing so would allow for a comparison of how difficult it is for human developers to build on agent code versus human code, and provide a more human-centric analysis of code maintainability. However, constructing this condition at scale would require recruiting developers to author PR2\\text{PR}\_{2} across all instances, which is infeasible in our current setting and difficult to control due to factors such as familiarity with the codebase. Future work could examine the AH setting on a smaller curated subset.



# [L-verification] Achint Mehta 2026, primary PDF
Source https://arxiv.org/pdf/2608.28795v2
Source: https://arxiv.org/pdf/2608.28795v2

# The reach of a verification tool decides its value: A controlled study of verification surface, artifact quality, and cost in AI coding agents

**Achint Mehta**

## ABSTRACT

Modern artificial-intelligence coding agents can be equipped with tools for checking their own 
work e.g. a linter, a boot probe, a shell, a screenshot tool. We call this set the agent's verification surface. This 
study asks whether increasing only that surface, with everything else held fixed, produces a matching growth 
in the quality of the software the agent ships. We built a minimal coding agent whose tool list is the single 
controlled variable and used it to implement 1,116 web applications across six models and eight tool 
configurations. A condition-blind human graded every application against a frozen rubric, and automatic 
probes stress-tested the API-observable behaviors. Verification's cheapest benefit arrives first, which is to 
make sure that the application comes up. Without any tools, about one build in seven fails to launch at all and
a single boot probe removes nearly all of these failures at roughly 35 percent of a full shell's token cost, while 
the full shell multiplies the no-tools cost by 2.35. Screenshots help most where mistakes are visible (e.g.
element placement, interaction), though even there the gain over a shell is modest and does not survive 
correction for multiple statistical comparisons. In cases where failures can only be measured rather than seen, 
such as keeping scrolling smooth over a 100,000-row list, screenshots add nothing. A verification tool 
improves the output artifact only where its reach covers the way the application actually fails.

**INDEX TERMS** Artificial intelligence, benchmark testing, large language models, program testing, 
software agents, software quality, software reliability

## I. INTRODUCTION

## A. Goal

This study asks how the verification surface of an artificialintelligence coding agent, the set of tools through which the 
agent can observe and check its own work, affects the quality 
of the software the agent actually ships i.e. its output files, as 
opposed to the transcript of what it said while working.

To change only the verification surface while holding 
everything else constant, we built a custom, minimal coding 
agent. Because the agent is ours, the system prompt is fixed, 
and the only thing that changes between conditions is the list 
of verification tools the agent is handed. The agent ran with 
one of five core tool sets: none at all, a linter only, a boot probe 
only, a full shell, or the shell plus screenshots (three further 
targeted configurations are described in Section II). A linter 
reads code and flags likely mistakes without running it. The 
boot probe is a single check that installs dependencies, starts 
the application's server, and reports whether it listens. The full 
shell is an unrestricted command line that can run anything.

Six models, claude-4.6-sonnet, claude-4.6-opus, claude-
4.8-opus, gpt-5.5, gemini-3.1-pro, and grok-4.3, each 
implemented seven web applications under these 
configurations, four to five times per combination. We call 
these repeats runs replicates and each replicate was an 
independent run which received no feedback from any other
run. In total, 1,116 applications were built. A human grader 
then scored every application in shuffled order against a fixed 
rubric, and an automatic probing tool checked the subset of 
behaviors observable through the API.

## B. Contributions

## 1) A controlled dose-response measurement

Similar to medicine's dose-response studies, each rung of our 
verification tools ladder adds one capability and we measure 
what the increment buys. With our custom coding agent, we 
controlled every configuration and provided tools to the model 
via this coding agent in an ordered ladder, with each 
configuration increasing the verification capability over the 
last.  These capabilities are: none, linter only, boot probe only, full shell, and shell plus screenshots. Because we controlled 
everything else, only a single parameter changed between 
conditions. This lets us tie the outcomes to the tools rather than 
other uncontrollable environment parameters.

## 2) The boot probe result

The boot probe tool (install dependencies and see if the server 
starts or not) recovered nearly all the launch failures observed 
with the “no tools” configuration. This single-tool 
configuration gave the highest ratio of artifact quality to token 
usage (tokens are the unit in which model usage is billed, so 
token counts are our measure of cost in this study).

## 3) A more nuanced look into the question “does sight help”

$$
h e l p ^ {\prime \prime}
$$

In our study we measure where the value of sight (the 
screenshot tool) starts and stops. The likeliest gains from sight 
over a shell (which allows the model to run any arbitrary 
command) alone appear where the failures involve element 
placement or interaction. Though this visual advantage is 
modest and does not survive correction for multiple 
comparisons, we treat this as suggestive rather than 
established. The gains are smaller for static page-layout issues, 
which a model can often get right from the code alone, without 
seeing the page. Whether a section is present and roughly 
arranged is visible in the markup, while whether elements 
collide or misalign at real sizes is not. It also seems to provide 
minimal value in detecting issues that can be measured but not 
seen through code such as drag-and-drop that flickers, or 
scrolling that is not smooth.

## C. Prior Work

Prior work shows that the scaffolding around an artificialintelligence coding agent, its prompts, tools, and control loop, 
strongly affects output quality [1]. Those studies compare 
whole systems against whole systems but this study changes a 
single part of the scaffold and measures what that part buys. 
Our tasks were chosen to make the measurement possible with
some applications are API-heavy while others are visually 
demanding.

The design choices for this study and our test harness were 
also motivated by the limitations of existing studies. SWEagent [2] showed that interface design alone can roughly triple 
task resolution. Agentless [3] showed a simple pipeline 
competitive with full agents at a tenth of the cost. These 
existing works also compare complete systems by counting 
how many benchmark p
*behavioral:* This adds only a run-tests tool that 
executes the project’s own test command. The model 
must write its own test suite. The question it answers 
is whether self-authored testing could be a substitute 
for granted verification?

## D. Why a passive screenshot rather than browser automation

Our screenshot tool is built on Playwright driving headless 
Chromium, the same library that can click, type, drag, and 
resize a live page. Our agent exposed only its rendering call to 
the model for this study. A model in the visual conditions 
(visual and visual_no_shell) passes a URL to the agent and 
receives an image in response, and nothing more. The 
passivity is therefore a deliberate restriction rather than a 
limitation of the tooling available to us.

We restricted it for three reasons. The first is isolation. 
Exposing the interaction API of playwright would have 
granted seeing and acting together, making the visual 
condition a combination of multiple abilities and making it 
difficult to determine which half earned any gain. That is the 
failure this study exists to avoid, and it is why visual_no_shell 
exists as well, to separate seeing ability from execution ability. 
The second is measurability. Every screenshot is a single call 
with a single argument, so we can count exactly what a model 
chose to look at, which is what makes the attribution analysis 
of Section IV-D possible. A browser-automation session has 
no such unit. Its actions could be logged and counted too, but 
every click both changes the page and shows the result, so the 
count would mix acting with looking. And if the model 
chooses to drive the browser from a script, a single call can 
hide fifty actions. Either way, we could no longer count how 
often the model chose to look, which is what Section IV-D 
needs. The third is prior evidence. Our earlier study granted 
this same library with its interaction capability intact and 
found it raised cost by 42 to 68 percent without improving 
reliability, so testing the narrower channel in this study was 
the more informative order.

The restriction has a real cost. Faults that only appear when 
someone clicks lie outside what this channel can reach, so our 
visual conditions understate what sight could achieve. The 
boundary was not merely theoretical. One model, gemini-3.1-
pro, installed its own scriptable browser in three runs to click 
elements the granted tool would not, and in 21 further runs 
models stated the limit in their reasoning before working 
around it or falling back on reading the code.

## E. Why the execution configuration does not trump the other configurations

A natural concern about the tool configurations above is that 
the execution configuration provides full shell access, and a 
capable model could use that shell to rebuild almost all of the 
functionality in the configuration ladder such as running a 
linter, starting the application and probing it, or installing 
browser-automation tools to take screenshots. Our study 
design does not prevent this, and it does not need to, mainly 
for two reasons. First, granted versus self-built is itself part of 
what we measure. The boot probe, for example, is a 
guaranteed single tool call and a model that wants the same 
functionality without boot probe (boot_check) tool must 
instead find the entry point and manage the process itself, 
which costs tokens. So, if a model rebuilds a capability, its 
token count rises accordingly, and token usage is one of our 
measured outcomes. Second, self-built sight cannot reach the 
model's eyes. When the granted screenshot tool runs, the 
harness attaches the captured image to the model's next 
message as visual input, so the model sees actual pixels. A
model that installs a browser and takes it

## VII. LIMITATIONS

## A. Passive Screenshot tool

Our screenshot tool takes a single argument, a URL. It renders 
a page and returns an image. It cannot click, type, drag, hover, 
or resize. This limits what the visual arms could ever have 
caught, and the run logs show the agents meeting that bound 
repeatedly rather than merely in principle.

Across the 264 runs in the two sight conditions, visual and 
visual_no_shell, 214 took at least one screenshot, making 
1,326 calls to 260 distinct URLs. Of those calls, 512, or 39 
percent, pointed somewhere other than the application's own 
root. These figures are a measure of effort spent reaching states

the agent could not click its way into. In 110 runs the agent 
used at least one such URL, and in 67 runs it went further and 
authored a purpose-made page whose only role was to be 
photographed, with names such as preview.html, testvisual.html, viewport-360.html, and, in one seat-booking run, 
static-preview-hold.html and static-preview-booked.html, 
which are mock-ups of the states a click would have produced.
The workarounds take three forms: Models forced state 
through the address bar, using fragments and query parameters 
such as #scroll-bottom, ?scrollTo=22, ?demo=edit, 
?theme=dark, and ?width=360. They also built the harness 
pages described above. And in several runs they edited the 
application itself purely to make a state photographable, one 
agent noting that it would "temporarily make the API return 
dark unconditionally, screenshot, revert", and another adding 
"a GET variant of seed temporarily so I can hit it via 
screenshot navigation". One calendar run resorted to a 
javascript: URL that posted four events and reloaded the page.
In 21 runs the model even stated the limit outright before 
working around it or giving up on the check. One wrote, "Let 
me verify the edit form opens by clicking. I can't click in 
screenshot tool. Let me trust the code." Some other models 
recorded that the tool "can't type into inputs", "can't resize", 
and "can't interact", each time falling back on reading the code 
instead of observing the behavior.

Two inferences can be made from this. Our visual 
conditions therefore measure the low end of what sight can do, 
since a tool that cannot click will never find a fault that only 
appears on clicking. And the inert page of Section V, a 
calendar that renders correctly and ignores every click, is 
precisely the defect this channel is structurally unable to see, 
which is why it survived the visual condition.

## B. Reasoning is not carried across turns

Because no reasoning content was returned to the agent, a 
model's reasoning could not be carried from one turn to the 
next, and every turn proceeded from the message history 
alone. This was identical across all conditions, so it does not 
distort the comparisons, but it does bound what the results 
speak to. Conditions differ in how many turns they take, and 
the arms with a shell run much longer than the arms building blind, so whatever benefit reasoning continuity might confer 
would accrue unevenly across the ladder. On an interface that 
returns and preserves reasoning, the quality gaps we report 
could widen and the cost gaps could narrow.

## C. Single Grader

The human interface scores come from a single grader. The 
grades were produced condition-blind, in shuffled order, 
against written per-item criteria. The repeatability of the scores 
was measured with a condition-blind regrade of a 10 percent 
sample after a four-week washout. The regrade process 
reproduced item verdicts at 98.8 percent (weighted kappa 0.97 
pooled, 0.94 on launched runs) and agreed on every survival 
call (Section II-J). However, this addresses stability, not 
correctness. The limitation remains contain

## G. Controlled test environment

We wanted the environment to be as controlled as possible, so 
we took the following steps:

---

• *Identical text:* The base prompt template, the environment 
briefing, and each task spec are identical across 
conditions. We enforce this by fingerprinting. Each run's 
log records a cryptographic hash of every text component, 
and we confirmed that every run reported the same hash 
for the prompt template, the briefing, and the task text. 
The one thing that changes between runs is the workspace 
path. The base prompt is a template with a placeholder for 
the working directory, and each run fills in its own folder, 
so the final prompt the model reads is the same in every 
run except for that path. Each run records its workspace 
path, and the fully assembled prompt is hashed into the 
manifest as well. One could take the one published 
prompt template, fill in that run's recorded path, append 
the one published briefing, and hash the result and it 
would match the run's recorded hash. Because the only 
ingredient that changed was the workspace path, and 
every other piece came from the single published copy, a 
match proves nothing else was altered. We checked this 
reconstruction for all 1,116 runs.

• *Environment briefing:* The environment briefing tells 
every model, in every condition, that the listed tools 
are the complete set and that dependencies declared in 
the package manifests would be installed once the run 
finished. We added this after a few initial test runs 
(not part of the 1,116 runs for the final study) showed 
that some models ignored some tools unless told they 
were available. The briefing is identical across all 
runs and expresses no preference for any tool or 
configuration.

• *Sampling settings:* We fix temperature to 0.0 and 
top_p to 1.0 (the two settings that control randomness 
in a model’s output, with temperature 0 requesting the 
most deterministic behavior available) for every 
model that accepts these parameters, with two 
caveats. First, some models, notably the Claude Opus 
family and gpt-5.5, reject explicit temperature and 
top_p. These models run with their provider's default 
sampling. This does not distort the comparison. When 
a model falls back to its provider's default sampling, 
it uses that same default in every one of its 
conditions, so the sampling setting never differs 
between the conditions we compare. It matters that 
we only ever compare a model against itself. We 
never read a result by placing one model next to 
another, only by placing a model's tools-on runs next 
to its own tools-off runs. Since the sampling setting is 
the same on both sides of that comparison, it cannot 
be mistaken for the effect of the tools. Second, 
temperature 0 does not guarantee identical outputs 
across repeats, because providers are not perfectly 
deterministic, which is why we run replicates (repeat 
runs of the same model, task, and condition).

• *Provenance and budgets:* The 1,116 runs that created 
the applications executed between June 12 and July 
11, 2026, and every request from every model

traveled through the same single API gateway, so no 
model was reached through different infrastructure 
than another. The exact model identifier sent with 
each request is recorded in that run's manifest, 
alongside its start and end times, step count, and 
token totals Every run ended with the model declaring 
completion and none was cut short by the harness or 
by any resource limit.

## H. Analysis rules

We encountered two situations in the study that required 
explicit handling rules.

## Situation 1: A model ignores a granted tool

Granting a screenshot tool, or any other tool, does not 
guarantee that a model will use it. Some models took zero 
screens


# Common criteria
# Editorial criteria and processes

This document provides an outline of the editorial process involved in publishing a scientific paper (Article) in _Nature_, and describes how manuscripts are handled by editors between submission and publication.

Editorial processes are described for the following stages: At submission | After submission | After acceptance

## At submission

**Criteria for publication**

The criteria for publication of scientific papers (Articles) in _Nature_ are that they:

- report original scientific research (the main results and conclusions must not have been published or submitted elsewhere)
- are of outstanding scientific importance
- reach a conclusion of interest to an interdisciplinary readership.

Further editorial criteria may be applicable for different kinds of papers, as follows:

- **large dataset papers**: should aim to either report a fully comprehensive data set, defined by complete and extensive validation, or provide significant technical advance or scientific insight.
- **technical papers:** papers that make solely technical advances will be considered in cases where the technique reported will have significant impacts on communities of fellow researchers.
- **therapeutic papers:** in the absence of novel mechanistic insight, therapeutic papers will be considered if the therapeutic effect reported will provide significant impact on an important disease.

Articles published in Nature have an exceptionally wide impact, both among scientists and, frequently, among the general public.


## After submission

### **What happens to a submitted Article?**

The first stage for a newly submitted Article is that the editorial staff consider whether to send it for peer-review. On submission, the manuscript is assigned to an editor covering the subject area, who seeks informal advice from scientific advisors and editorial colleagues, and who makes this initial decision. The criteria for a paper to be sent for peer-review are that the results seem novel, arresting (illuminating, unexpected or surprising), and that the work described has both immediate and far-reaching implications. The initial judgement is not a reflection on the technical validity of the work described, or on its importance to people in the same field.  
Special attention is paid by the editors to the readability of submitted material. Editors encourage authors in highly technical disciplines to provide a slightly longer summary paragraph that descries clearly the basic background to the work and how the new results have affected the field, in a way that enables nonspecialist readers to understand what is being described. Editors also strongly encourage authors in appropriate disciplines to include a simple schematic summarizing the main conclusion of the paper, which can be published with the paper as Supplementary Information. Such figures can be particularly helpful to nonspecialist readers of cell, molecular and structural biology papers.  
Once the decision has been made to peer-review the paper, the choice of referees is made by the editor who has been assigned the manuscript, who will be handling other papers in the same field, in consultation with editors handling submissions in related fields when necessary. Most papers are sent to two or three referees, but some are sent to more or, occasionally, just to one. Referees are chosen for the following reasons:

- independence from the authors and their institutions
- ability to evaluate the technical aspects of the paper fully and fairly
- currently or recently assessing related submissions
- availability to assess the manuscript within the requested time.

### **Referees' reports**

The ideal referee's report indicates

- who will be interested in the new results and why
- any technical failings that need to be addressed before the authors' case is established.

Although _Nature_'s editors themselves judge whether a paper is likely to interest readers outside its own immediate field, referees often give helpful advice, for example if the work described is not as significant as the editors thought or has undersold its significance. Although _Nature_'s editors regard it as essential that any technical failings noted by referees are addressed, they are not so strictly bound by referees’ editorial opinions as to whether the work belongs in _Nature_.