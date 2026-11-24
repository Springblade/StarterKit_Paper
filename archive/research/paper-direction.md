# Từ thesis SmartKit đến một nghiên cứu mới

> Bản lịch sử, không dùng làm kế hoạch hiện hành. Xem [protocol SmartKit](../../research/smartkit-study-protocol-v0.md) và [khảo sát tài liệu](research-landscape-v2.md).

Ngày tra cứu: 2026-11-09. Đây là báo cáo định hướng và thiết kế sơ bộ, chưa phải manuscript, preregistration hay kết quả thực nghiệm.

## Tóm tắt

Đề xuất ưu tiên kiểm chứng: nghiên cứu cách coding agent bảo toàn các ràng buộc Server/Client khi mở rộng ứng dụng Next.js, với oracle thực thi độc lập và các can thiệp hướng dẫn được kiểm soát. SmartKit là một substrate, không phải đối tượng cần chứng minh là tốt hơn. Hướng này có liên hệ rõ với lỗi thúc đẩy thesis, nhưng tính mới vẫn cần kiểm tra sâu ở cấp task và evaluator. Không nên chạy hàng loạt trước khi vượt qua bước kiểm chứng đó.

Không tiếp tục lập luận rằng chưa có benchmark về framework conventions, hoặc rằng AGENTS.md và mã mẫu chưa được nghiên cứu. Nghiên cứu mới đã đi khá xa ở cả hai hướng. Các runs cũ đã bị xóa: có thể mô tả thesis như công trình tiền thân, nhưng không dùng pilot đó làm dữ liệu thực nghiệm có thể kiểm chứng cho paper mới.

## 1. Câu hỏi và phạm vi tra cứu

Ba câu hỏi định hướng:

1. Repository instructions và code precedents đã được nghiên cứu đến đâu, và phần nào còn có thể đóng góp?
2. Các benchmark hiện có phân biệt functional correctness, framework constraints và project conventions như thế nào?
3. Với SmartKit, nghiên cứu mới nào có thể tạo ra bằng chứng kiểm chứng được, thay vì chỉ tăng điểm trên rubric do tác giả tự thiết kế?

Tra cứu theo ba nhánh độc lập: hiệu quả và phản chứng của context files; benchmark web/framework; độ tin cậy của phép đo. Nguồn gồm bài gốc trên arXiv/ACL, trang tác giả, tài liệu chính thức Next.js và repository SmartKit. Tìm cả nguồn có kết quả tích cực, không cải thiện và suy giảm. Metadata/abstract chỉ hỗ trợ kết luận ở mức đó; không suy diễn chi tiết phương pháp từ snippet.

Các chuỗi truy vấn đã dùng ở lượt tra cứu chính gồm: `AGENTS.md repository instructions coding agents empirical study 2026`; `Next.js benchmark coding agents framework conventions evaluation`; `coding agents architectural constraints convention adherence runtime correctness benchmark server client boundary Next.js`; `LLM code generation framework constraints static analysis feedback Next.js server client benchmark`; `coding agents repository conventions semantic cosmetic compliance benchmark evaluation`; `React Server Components benchmark agents`; `Next.js use client benchmark evaluation agents boundary`.

Đây là khảo sát có mục tiêu để ra quyết định, chưa phải systematic review toàn diện. Không tìm thấy một công trình qua các truy vấn trên không chứng minh rằng công trình đó không tồn tại. Một số công trình sát nhất mới ở dạng preprint.

## 2. Những gì tài liệu thay đổi trong cách đặt vấn đề

### 2.1. Có hướng dẫn không đồng nghĩa với làm đúng hơn

[Gloaguen và cộng sự, Evaluating AGENTS.md (2026)](https://arxiv.org/abs/2602.11988) báo cáo rằng context files không nhìn chung cải thiện task success trong các thiết lập họ đánh giá, dù agent thường làm theo chỉ dẫn và chi phí suy luận tăng. [Khatri, Do Context Files Help Coding Agents? (2026)](https://aclanthology.org/2026.realm-1.5/) cũng không tìm thấy khác biệt đo được về correctness trong thí nghiệm hai agent của mình. Ngược lại, [Lulla và cộng sự (2026)](https://arxiv.org/abs/2601.20404) báo cáo cải thiện một số chỉ số hiệu suất với hành vi hoàn thành tương đương. Các kết quả này đo những outcome và thiết lập khác nhau; chúng không cho phép kết luận chung rằng instructions luôn có lợi hoặc luôn có hại.

Trong web development, [Yang và Ding, Signal or Noise? (2026)](https://arxiv.org/abs/2608.23067) cho thấy Skill injection có thể làm giảm functional performance và tăng chi phí trong benchmark của họ, với tác động phụ thuộc model và project. Bài học cho thiết kế mới: đo riêng adherence, correctness và chi phí; kiểm soát độ dài context khi cần diễn giải cơ chế. Không giả định SmartKit sẽ cải thiện cả ba.

### 2.2. Instructions so với code examples đã là một hướng có cạnh tranh trực tiếp

[Zhu và cộng sự, Precedent or Intent? (2026)](https://arxiv.org/abs/2610.38244) tách default preferences, repository precedents và task instructions, đồng thời thay đổi vị trí và số lượng examples. [Xu và Wu, Stale Instruction Files Override the Code in Coding Agents (2026)](https://arxiv.org/abs/2610.30571) nghiên cứu xung đột giữa instructions lỗi thời và mã hiện có. Vì vậy, một factorial instructions × examples hay một thí nghiệm về xung đột đơn thuần không còn đủ để tuyên bố đóng góp mới. Chuyển các thí nghiệm đó sang Next.js cần được định vị là replication/extension và chỉ rõ kiến thức bổ sung.

### 2.3. Khoảng cách giữa passing tests và compliance cũng đã được nghiên cứu

[SWE-CC, Truong và cộng sự (2026)](https://arxiv.org/abs/2610.06193) đánh giá repository policy compliance bằng các checker và audit quá trình thực hiện. [RepoNorm, He và cộng sự (2026)](https://arxiv.org/abs/2610.07757) thu nhận và kiểm chứng explicit/implicit norms. Trong khi hai hướng này tập trung vào quy định repository, [Constraint Decay, Dente và cộng sự (2026)](https://arxiv.org/abs/2605.06445) kết hợp behavioral tests và static verifiers để nghiên cứu structural requirements trong backend frameworks. Không thể coi việc bổ sung static checks bên cạnh functional tests là mới tự thân.

[RAL-Bench, Pan và cộng sự (2026)](https://arxiv.org/abs/2602.03462) mở rộng đánh giá sang ứng dụng hoàn chỉnh và nonfunctional dimensions; [Wang, Pradel và Liu (ICSE 2026)](https://arxiv.org/abs/2503.15223) cho thấy patch được chấp nhận bởi benchmark vẫn có thể có sai lệch hành vi hoặc regression. Cả hai củng cố nhu cầu kiểm tra nhiều lớp, đồng thời bác bỏ cách mở bài rằng mọi benchmark trước đây chỉ xem snippets hoặc unit-test success.

### 2.4. Next.js đã có đối chứng trực tiếp

[Next.js Agent Evals chính thức](https://nextjs.org/evals) đánh giá các tác vụ Next.js và công bố điều kiện có/không có AGENTS.md trỏ đến bundled documentation. [NextBench](https://huggingface.co/datasets/baablabs/nextbench) đánh giá Next.js/React/TypeScript completion bằng deterministic pattern checks. Hai nguồn khác nhau về task và oracle nhưng đều khiến tuyên bố “chưa có đánh giá framework-specific” không thể giữ nguyên. Công cụ công nghiệp là đối chứng liên quan, không tự động có cùng mức thẩm định với bài báo phản biện.

## 3. Kiểm toán ban đầu thesis và artifact

Đã lấy repo từ URL trong thesis: https://github.com/Springblade/SmartKit. Bản clone ở `research/SmartKit`, commit `2c92d3920d967b9ebf0960ba7890754baa3c90d7`. Đây là snapshot hiện tại, chưa xác nhận trùng phiên bản dùng trong thesis. Chưa cài dependencies, chạy test hay build; không có kết luận rằng baseline đã hoạt động.

Những vấn đề cần xử lý trước nghiên cứu mới:

- `features/`, centralized tests và lựa chọn Zod là project conventions; không mặc nhiên là yêu cầu của Next.js. Phân biệt chúng với semantic constraints như client/server import boundaries.
- Có Zod schema không chứng minh input được validate ở runtime; có test file không chứng minh tests phát hiện lỗi.
- So sánh SmartKit bundle với scaffold nghèo tín hiệu chỉ ước lượng bundle effect, không xác định thành phần gây tác động.
- Rubric/scorer thay đổi hoặc không khớp khiến so sánh cũ không thể chuyển nguyên sang nghiên cứu mới. Không tái tạo các con số cũ từ trí nhớ.
- Trong snapshot hiện tại, Vitest alias `server-only` sang mock. Vì vậy test suite này riêng lẻ không đủ làm oracle cho compiler boundary enforcement; phải kiểm tra build và runtime thật.
- AGENTS.md trong snapshot còn trỏ đến parent instructions và Cursor rules bên ngoài. Thí nghiệm phải xác định chính xác file nào được tải; không để hướng dẫn ngoài treatment vô tình tham gia.
- Độc lập giữa các dimensions không thể được chứng minh chỉ bằng correlation thấp hoặc một mốc n tùy chọn. Cần xác định rõ mỗi construct và giá trị của phép đo.

Những nhận xét trên là audit tài liệu/source ban đầu, chưa phải audit đầy đủ chất lượng SmartKit.

## 4. So sánh hướng paper

| Hướng | Giá trị có thể đạt | Rủi ro chính | Quyết định hiện tại |
|---|---|---|---|
| SmartKit tốt hơn scaffold trống | Đánh giá artifact trong bối cảnh hẹp | Bundle confounding, rubric thiên vị, kết quả khó khái quát | Không ưu tiên |
| Instructions × examples | Replication/extension cơ chế context | Trùng sát Precedent or Intent? | Chỉ làm khi có khác biệt substantively rõ |
| Benchmark conventions tổng quát | Dataset/checker có thể tái sử dụng | SWE-CC, RepoNorm và Constraint Decay đã chiếm phần lớn câu chuyện | Không chọn chỉ bằng cách đổi tên metric |
| Bảo toàn semantic Server/Client constraints khi thêm tính năng | Tác vụ có hành vi thực, oracle framework, phân tích lỗi và can thiệp kiểm soát | Có thể vẫn trùng eval hiện hành hoặc lỗi quá dễ/hiếm | Ưu tiên kiểm chứng, chưa chốt novelty |

Không chấm điểm 1–10 cho tính mới hay feasibility khi chưa có dữ liệu và thông tin tài nguyên. Không dự báo khả năng accept trước khi có kết quả.

## 5. Hướng ưu tiên và câu hỏi nghiên cứu mới

Tên làm việc: **Preserving Server–Client Boundaries in Agent-Generated Next.js Changes: An Executable Evaluation**.

Câu hỏi trung tâm: khi coding agent thêm tính năng tương tác vào ứng dụng Next.js có sẵn, nó có giữ các yêu cầu thực thi và phân tách Server/Client không; và can thiệp nào giúp cải thiện joint success?

- RQ1: Các lỗi nào xuất hiện khi đánh giá đồng thời behavior, build/runtime và boundary requirements đã được xác định trước?
- RQ2: Chỉ dẫn ngắn, đúng phiên bản và feedback thực thi ảnh hưởng thế nào đến tỷ lệ đáp ứng đồng thời các yêu cầu, so với baseline được kiểm soát?
- RQ3: Điểm từ các proxy tĩnh, chẳng hạn presence của directives/schema/test files, nhận diện đúng và bỏ sót những trường hợp nào so với executable oracle?

Đây là câu hỏi nghiên cứu, không phải các phát hiện đã xác nhận. Tài liệu hiện có làm hướng này đáng khảo sát, nhưng chưa chứng minh rằng riêng nó là một khoảng trống mới.

[Tài liệu Next.js chính thức](https://nextjs.org/docs/app/getting-started/server-and-client-components) mô tả boundary theo module graph, props serialization, interleaving và khuyến nghị giữ client boundary nhỏ để giảm client JavaScript. Dựa trên đó, có thể thiết kế tasks để phân biệt sửa đúng với chuyển tùy tiện nhiều module sang client. Tuy nhiên, nhiều `'use client'` hơn không tự thân là lỗi: chỉ đánh fail khi vi phạm yêu cầu task có lý do và đã công bố trước; bundle size là outcome riêng.

## 6. Dữ liệu có nguồn gốc và oracle

Nguồn task ưu tiên: issue/PR công khai có thể tái hiện, test chính thức của framework, tình huống tích hợp có thật trong SmartKit. Mỗi task cần URL nguồn, commit trước thay đổi, lý do chọn và bản tái hiện cục bộ. Không gọi task tự thiết kế là dữ liệu production. Không lấy một fix có sẵn rồi để fix đó trong git history mà agent có thể truy cập.

Ví dụ giả định để minh họa: thêm nút lưu trên trang đọc dữ liệu server-only, vừa giữ tương tác đúng vừa giữ module dữ liệu khỏi client graph. Ví dụ này chưa được ghi nhận là task thực tế; cần thay bằng trường hợp có provenance hoặc ghi nhãn constructed task. Trường hợp synthetic có ích để kiểm tra cơ chế, nhưng cần external validation.

SmartKit nên là một repo trong tập đánh giá, kèm repo độc lập nếu muốn claim vượt khỏi SmartKit. Chọn repo dựa trên khả năng dựng môi trường, provenance, license và tính đại diện cho failure families, không chọn sau khi thấy kết quả thuận lợi.

Oracle gồm:

1. Functional acceptance và regression tests do evaluator quản lý, không lấy tests do agent viết làm nguồn sự thật duy nhất.
2. Typecheck, production build, khởi động production server và browser/HTTP interactions cho route liên quan. Build pass không đồng nghĩa runtime pass.
3. Task-specific import/data-flow checks với ý nghĩa rõ ràng; không chấm chỉ bằng đường dẫn SmartKit hoặc regex presence.
4. Cost, latency và bundle measurements nếu đã định nghĩa cách đo và baseline. Không diễn giải giảm bundle như chứng minh trải nghiệm người dùng tốt hơn khi chưa đo.

Trước khi chấm agent, từng oracle phải chấp nhận reference implementation và các phương án hợp lệ khác, từ chối unchanged task khi thiếu tính năng, và bắt được các lỗi cấy có chủ đích. Các mutation này là dữ liệu kiểm định evaluator, không phải bằng chứng rằng agent thực tế hay tạo ra lỗi đó. Cần kiểm tra không bị lộ lời giải và review độc lập một mẫu oracle nếu có thể.

## 7. Thiết kế can thiệp sơ bộ

Thiết kế factorial 2 × 2 trong từng block task × repo × model/harness:

| Điều kiện | Chỉ dẫn semantic ngắn | Feedback kiểm tra bổ sung |
|---|---|---|
| C00 | Không | Không |
| C10 | Có | Không |
| C01 | Không | Có |
| C11 | Có | Có |

“Không” ở đây là không có can thiệp bổ sung. Mọi nhóm giữ cùng quyền chạy công cụ thông thường, dependency versions, task prompt, và giới hạn tài nguyên. Feedback bổ sung phải được định nghĩa là script/report cụ thể; evaluator acceptance tests vẫn giữ kín và không tự động được dùng làm feedback.

Nếu auto-feedback chạy thêm lượt sửa, cho các nhóm đối chứng cơ hội revision và tổng resource budget tương ứng, đồng thời ghi nhận số vòng và chi phí. Nếu mục tiêu là hiệu quả thực dụng của cả package thì có thể báo cáo package effect; nếu mục tiêu là tác động riêng của nội dung feedback, cần active control tương ứng. Không đồng nhất hai estimand này.

Giữ code examples cố định trong thiết kế chính. Thay đổi examples/length chỉ làm ablation có lý do sau đó, để tránh biến nghiên cứu thành bản lặp của các công trình context hiện hành. Cần đối chứng length-matched khi muốn quy tác động cho nội dung instructions thay vì context length.

Mỗi trial bắt đầu từ snapshot sạch và session mới; không dùng chung memory, workspace thay đổi hoặc cache chứa lời giải. Randomize thứ tự điều kiện trong block, ghi batch/time và phân biệt agent failure với infrastructure failure. Không rerun riêng output xấu mà không có quy tắc đã định trước.

Primary endpoint đề xuất: joint success = functional acceptance đạt AND các hard boundary requirements áp dụng đạt. Báo cáo riêng từng thành phần và bảng nhầm lẫn proxy–oracle, không chỉ tổng điểm. Báo cáo effect size và uncertainty; phân tích phải xét cấu trúc task/repo và repeated runs. Nhiều lần chạy trên một task không thay thế được nhiều task độc lập. Chưa đặt cỡ mẫu cố định; pilot riêng để kiểm định instrument và ước lượng biến thiên, sau đó mới xác định cỡ mẫu dựa trên effect/precision có ý nghĩa.

## 8. Quy tắc quyết định trước khi đầu tư thí nghiệm lớn

1. **Novelty gate:** đối chiếu từng failure family, task và checker với Next.js Evals, Constraint Decay, SWE-CC và các công trình sát nhất. Nếu đã có cùng câu hỏi và phép đo, chuyển sang replication rõ ràng hoặc đổi hướng; không che bằng tên mới.
2. **Validity gate:** chứng minh evaluator phân biệt được implementations hợp lệ và lỗi thật; task baseline phải dựng và chạy được.
3. **Signal gate:** pilot trên tasks riêng để xem có lỗi đủ đáng nghiên cứu và can thiệp thực sự thay đổi exposure. Không chọn chỉ các task/model tạo ra hiệu ứng mong muốn.
4. **Generalization gate:** kiểm tra trên tasks/repo độc lập. Nếu chỉ làm được SmartKit, giới hạn claim thành case study.
5. **Freeze:** khóa protocol, criteria, snapshot, model/harness và analysis plan trước confirmatory runs. Không gọi kế hoạch được viết sau khi xem outcomes là preregistered.

Kết quả null, feedback không có lợi, hoặc proxy gần như đủ tốt đều có thể trả lời câu hỏi. Nhưng một null study với uncertainty lớn không chứng minh equivalence; không có lỗi trong vài task không chứng minh agent đáng tin cậy tổng quát.

## 9. Hồ sơ dữ liệu cần lưu

Mỗi run lưu: run/task/condition ID; repo commit và dependency lock; OS/runtime/framework versions; model ID và snapshot nếu nhà cung cấp công bố; harness/settings; prompt và toàn bộ instructions được tải; tool trace; diff cuối; stdout/stderr; test/build/browser artifacts; token/cost/time; trạng thái timeout và nguyên nhân loại trừ. Ghi rõ khi provider không cho pin model chính xác. Chỉ dùng dữ liệu test và credentials giả trong artifact công khai.

Lưu task provenance, oracle version, reference variants và mutation checks thành bộ riêng. Phân biệt development pilot với confirmatory data. Không có dữ liệu nào mới được tạo trong lượt nghiên cứu này.

## 10. Kết luận theo ba câu hỏi ban đầu

RQ1: Context instructions và code precedents đã có nhiều nghiên cứu sát; một bundle comparison hoặc factorial chung không đủ tạo novelty.

RQ2: Functional correctness, policy compliance và structural requirements đã được đo cùng hoặc song song. Paper mới cần semantic scope, oracle và task provenance có khác biệt cụ thể; rubric 0–5 cũ chưa đáp ứng điều đó.

RQ3: Hướng đáng kiểm chứng trước là bảo toàn Server/Client constraints trong feature changes, với SmartKit làm một substrate. Chưa có cơ sở khẳng định hướng này chắc chắn mới hoặc sẽ cho hiệu ứng tích cực. Bước tiếp theo có giá trị nhất là lập task–oracle–prior-work matrix và dựng vài task có provenance để kiểm định evaluator, trước khi chốt manuscript hay chạy lớn.

## Cần tác giả xác nhận

- Snapshot SmartKit nào tương ứng với thesis và quyền tái phân phối artifact/task từ các repo khác.
- Khả năng dùng API/model và compute khi cần chạy pilot; không suy ra ngân sách vô hạn từ việc không giới hạn thời gian.
- Các ví dụ minh họa ở trên là giả định, chưa phải quan sát thực nghiệm.
- Yêu cầu khai báo hỗ trợ AI của venue và cơ sở đào tạo; lưu bản nháp, quyết định nghiên cứu và lịch sử kiểm chứng.
