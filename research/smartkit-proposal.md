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
