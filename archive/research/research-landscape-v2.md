# Từ tuân thủ quy ước đến bảo toàn hành vi: hướng nghiên cứu từ SmartKit

> Cập nhật quyết định 2026-11-10: sau trao đổi, tác giả chọn nghiên cứu thiết kế starter kit với SmartKit làm trung tâm, gồm tổ chức mã và kiểm chứng hành vi. Kế hoạch triển khai hiện hành nằm trong [protocol SmartKit](../../research/smartkit-study-protocol-v0.md). Báo cáo này giữ nguyên khảo sát và các phương án đã cân nhắc; thứ tự ưu tiên cũ không phải protocol đã chốt.

Ngày tra cứu: 2026-11-09. Báo cáo định hướng nghiên cứu; chưa phải manuscript hoặc preregistration. Báo cáo này thay thế việc ưu tiên Server/Client boundaries trong [bản định hướng ban đầu](paper-direction.md). Không sửa thesis và không sử dụng pilot đã mất artifact làm dữ liệu mới.

## Tóm tắt

Khảo sát này xem xét những vấn đề có thể nghiên cứu khi coding agent sửa và mở rộng repository thực tế, thay vì giữ trước rubric hay giải pháp SmartKit. Ba nhánh tra cứu độc lập xem xét tính đúng của ứng dụng, tiến hóa phần mềm và bằng chứng từ pull request; nhánh bổ sung xem xét môi trường chạy và phép đo. Các nguồn cho thấy những đề xuất rộng như benchmark SaaS, đánh giá security bên cạnh functionality, hoặc theo dõi code erosion đều có công trình gần. Bằng chứng cũng không nhất quán với nhận định rằng AI luôn làm giảm khả năng bảo trì hoặc chất lượng test. Hướng ưu tiên được đề xuất là kiểm tra tác động của sai lệch hợp đồng hành vi được thừa hưởng đối với một thay đổi tiếp theo, bằng can thiệp mã có đối chứng. Hai phương án khác là truy vết sự cải thiện khả năng phát hiện lỗi trong quá trình review PR và đo tác động của việc cung cấp môi trường chạy đã kiểm chứng. Các hướng này đều cần kiểm tra dữ liệu và đối chiếu artifact trước khi chốt novelty. SmartKit có thể hỗ trợ thử nghiệm công cụ nhưng không đủ làm nguồn duy nhất cho kết luận rộng. Bước triển khai phù hợp nhất là kiểm tra khả năng dựng lại những chuỗi thay đổi có nguồn gốc, yêu cầu rõ và oracle độc lập.

## 1. Câu hỏi cần trả lời trước khi chọn paper

Thesis hiện có đặt trọng tâm vào thiết kế và vận hành một phép đo. Muốn phát triển thành paper mạnh hơn, cần xác định kiến thức mà phép đo tạo ra: nó giải thích một thất bại thực tế nào, phân biệt những nguyên nhân nào, và thay đổi quyết định phát triển phần mềm như thế nào. Không có lý do bắt buộc giữ ba dimensions, Next.js hoặc SmartKit làm đối tượng trung tâm.

Ba câu hỏi của khảo sát, được ghi trước khi tra cứu trong [brief đã lưu trữ](research-brief-v2.md):

- RQ-S1: Bằng chứng gốc chỉ ra vấn đề nào khi coding agents thay đổi phần mềm, được đo như thế nào và có phản chứng gì?
- RQ-S2: Công trình gần nhất đã giải quyết đến đâu; hướng nào còn có thể tạo kiến thức bổ sung thay vì chỉ đổi stack hoặc metric?
- RQ-S3: Hướng nào nên được ưu tiên từ kinh nghiệm SmartKit, cần dữ liệu gì và thí nghiệm nào có thể bác bỏ kỳ vọng?

Đây là câu hỏi khảo sát. RQ cuối cùng của paper cần được chọn sau bước kiểm tra nguồn dữ liệu.

## 2. Cách tra cứu và giới hạn

Ba scout độc lập đã xác minh 25 công trình: 8 về application invariants/features, 9 về maintenance/evolution, 8 về PR thực tế/testing. Agent chính đối chiếu thêm 7 nguồn về setup, repository effects, tool architecture, kiến trúc phần mềm, backend oracles, test metrics và môi trường đánh giá. Danh mục hợp nhất 32 công trình nằm trong `evidence-ledger-v2.csv`; dataset AIDev là nguồn bổ sung, không được đếm thành một paper thứ hai. Các công trình về instructions ở lượt trước chỉ là bối cảnh, không nằm trong số 32 này.

Tra cứu gồm ít nhất một vòng rộng và một vòng hẹp theo từng nhánh; tiếp tục theo công trình gần nhất và tìm phản chứng. Nguồn chính: arXiv, ACL Anthology, PMLR, nhà xuất bản, bản tác giả và dataset/repository chính thức. Những phần được đọc toàn văn là các mục liên quan đến construction, evaluation, kết quả và limitations; không có nghĩa mọi appendix hoặc test trong artifact đã được kiểm toán. Các nguồn chỉ đọc abstract không được dùng để suy diễn chi tiết phương pháp.

Các scout ghi author/title/year, version, phạm vi thực sự đọc và query strings trong ba file `scout-*.md`. Các truy vấn bổ sung của agent chính gồm: `coding agents API contract change propagation cross layer consistency benchmark 2026`; `coding agents scaffolding architecture repository structure causal experiment benchmark 2026 maintainability`; `coding agents environment setup preconfigured environment controlled experiment benchmark failures`; `coding agents invariant preservation`; `coding agents idempotency benchmark`; `coding agents behavioral drift causal`; `code contract restoration maintainability agent`; `agent test review mutation pull requests 2026 coding`. Tra cứu theo title của bài gốc để xác minh và lần theo related work.

Đây là khảo sát có mục tiêu, không phải systematic review có screening toàn bộ cơ sở dữ liệu. Không ước lượng coverage toàn ngành. Không tìm thấy bài trùng qua các truy vấn không chứng minh novelty. Một số bài mới là preprint. Bản OpenReview của BackendForge gặp browser challenge, nên được thay bằng arXiv gốc có tác giả; bản anonymous VibeSweBench chưa được đối chiếu đủ metadata nên không dùng làm bằng chứng kết luận.

## 3. Phân loại bằng chứng theo câu hỏi được đo

| Nhánh chính | Đơn vị quan sát | Outcome hữu ích | Không được suy ra tự động |
|---|---|---|---|
| Đúng hành vi khi thay đổi tính năng | Task/patch trên snapshot xác định | Hành vi mới, regression, domain/security requirements | Task lấy từ OSS đại diện cho mọi công việc production |
| Tiến hóa và tác động downstream | Chuỗi thay đổi hoặc mã giao cho người/agent tiếp theo | Thành công lần sửa sau, lỗi tích lũy, thời gian làm việc được đo | Complexity thấp đồng nghĩa dễ bảo trì |
| Review và tích hợp thực tế | PR, review concern, revision | Sửa đổi kiểm chứng được, fault detection theo phiên bản | Merge = correct; comment count = công sức lao động |
| Điều kiện thực thi/quan sát | Repo/environment/tool configuration | Setup success, joint task success, chi phí | Không dựng được hệ thống = không hiểu nghiệp vụ |

Một công trình có thể hỗ trợ nhiều nhánh; ledger gán nhánh theo câu hỏi chính để tránh đếm lặp. Những kết luận cần thiết lập nguyên nhân phải dựa vào can thiệp hoặc giả định nhận dạng rõ ràng, không chỉ so sánh các nhóm PR khác nhau.

## 4. Đúng tính năng và giữ đúng hành vi là hai yêu cầu cần phân biệt

[SusVibes](https://arxiv.org/abs/2512.03262) đã đo chức năng và bảo mật khi triển khai feature; [BaxBench](https://www.sri.inf.ethz.ch/publications/vero2025baxbench) làm điều tương tự cho backend được sinh từ specification. [SecureVibeBench](https://arxiv.org/abs/2509.22097) bổ sung bối cảnh lịch sử đưa vulnerability vào mã. Vì vậy, chỉ thêm security tests vào functional tests không tạo novelty; mẫu được tuyển từ lịch sử lỗ hổng cũng không cho biết tần suất lỗi trong feature thông thường.

Trong khi [FEA-Bench](https://aclanthology.org/2025.acl-long.839/) và [FeatureBench](https://arxiv.org/abs/2602.10975) đã nghiên cứu feature development trong repository, [BackendForge](https://arxiv.org/abs/2607.11042) kiểm tra backend theo contract HTTP với oracle được tăng cường. Chúng bác bỏ cách đặt vấn đề rằng đánh giá hiện hành chỉ có snippets hoặc algorithmic correctness.

Điểm có thể tiếp tục kiểm tra là bảo toàn những quy tắc đang có của một ứng dụng đang chạy khi thực hiện thay đổi mới. Tuy nhiên, đây là đề xuất về unit và sampling frame; chưa có bằng chứng rằng nó chưa được benchmark hiện hành bao phủ. Cần đối chiếu từng task và property, không chỉ so tên benchmark.

Ví dụ giả định cho loại property cần kiểm tra: một sự kiện được gửi lại không tạo thêm entitlement; một thao tác thất bại không để lại trạng thái cập nhật nửa chừng. Chúng là minh họa, chưa phải lỗi quan sát được trong SmartKit hay PR thật. [LIMBO](https://arxiv.org/abs/2609.29095) đã nghiên cứu duplicate side effects của agent vận hành tools; đó là bối cảnh khác với agent viết mã ứng dụng. Không được dùng kết quả ấy làm số liệu về lỗi thanh toán do coding agent sinh ra.

## 5. Bằng chứng về bảo trì phụ thuộc người sửa, tác vụ và phép đo

[CodeThread](https://arxiv.org/abs/2606.21804) liên hệ thay đổi input/error contracts với khó khăn downstream; [Echoes of AI](https://link.springer.com/article/10.1007/s10664-026-10889-1) không phát hiện bất lợi bảo trì có hệ thống trong thiết lập con người dùng AI rồi người khác sửa mã. Khác biệt về người thực hiện, công cụ và tác vụ ngăn việc rút ra một kết luận chung “mã AI khó bảo trì hơn”.

[SlopCodeBench](https://arxiv.org/abs/2603.24755), [SWE-Milestone](https://proceedings.mlr.press/v306/deng26d.html) và [SWE-EVO](https://arxiv.org/abs/2512.18470) đã đánh giá tiến hóa nhiều bước. [RoadmapBench](https://arxiv.org/abs/2605.15846) và [CrossSWE](https://arxiv.org/abs/2611.01484) mở rộng sang nâng cấp lớn hoặc thay đổi liên repository. Vì vậy, tăng số feature hay số file chưa đủ phân biệt nghiên cứu mới.

[FeatureLoop](https://arxiv.org/abs/2610.35488) nghiên cứu requirements thay đổi và feedback; [Multi-step SWE](https://arxiv.org/abs/2611.07166) đo khả năng tiếp tục phát triển mã qua chuỗi tác vụ. Feedback có thể giúp kết quả trong thiết lập được đánh giá; không nên giả định mọi bước lặp đều gây hại. Scout dùng FeatureLoop v1; record hiện hành đã đổi title ở v2. Báo cáo này không trộn số liệu giữa hai version.

Suy luận của khảo sát: một nghiên cứu tiếp theo nên tách cơ chế cụ thể trong mã khỏi nhãn “agent-generated” và các proxy hình thức. Việc một điểm số đồng biến với thất bại chưa cho biết sửa điểm đó sẽ giúp; thí nghiệm có thể can thiệp vào hành vi và kiểm tra một yêu cầu downstream chưa được giải quyết. Đây là đề xuất phương pháp của báo cáo, chưa phải kết quả mới.

## 6. Artifact cuối PR không đại diện nguyên vẹn cho đầu ra ban đầu

[Haque và cộng sự](https://doi.org/10.1145/3793302.3793604) quan sát test trong agentic PR; [Dipongkor và cộng sự](https://arxiv.org/abs/2607.18057) thực thi để đo coverage. [Milanese và cộng sự](https://arxiv.org/abs/2610.35297) dùng so sánh trong repository và không phát hiện chênh lệch coverage production changes ở tập dựng được. Các phép đo khác nhau không hỗ trợ kết luận rằng test của agent luôn kém.

[Ehsani và cộng sự](https://arxiv.org/abs/2601.15195) cho thấy PR không tích hợp có nhiều nguyên nhân; [Njoku và cộng sự](https://doi.org/10.1145/3805760.3814909) mô tả khác biệt hợp tác và tích hợp. Chúng không biến trạng thái closed/unmerged thành nhãn code sai. Các revision sau review phải được gắn với actor và nội dung thực tế trước khi gọi là sửa lỗi do con người.

[METR/Becker và cộng sự](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf) đo năng suất ở task được ngẫu nhiên hóa với công cụ đầu 2025; [Chen–Stratton](https://fion.ac/jellyfish.pdf) nghiên cứu rollout trong doanh nghiệp bằng dữ liệu quan sát. Chúng có đối tượng và estimand khác nhau, không cung cấp một hệ số năng suất áp dụng trực tiếp cho agent hiện tại hoặc SmartKit.

Theo [Zhao, Zhou và Cohen](https://arxiv.org/abs/2607.22880), giá trị của coverage/mutation phụ thuộc setting; trong khi những nghiên cứu PR trên chủ yếu mô tả artifact, cần đo trực tiếp test có phát hiện lỗi đã biết hay không. Không nên thay rubric cũ bằng mutation score rồi mặc nhiên gọi phép đo mới là ground truth.

## 7. Môi trường và repository là một phần của hệ thống được đánh giá

[SetupBench](https://arxiv.org/abs/2507.09063) tách nhiệm vụ bootstrap; [R2E](https://proceedings.mlr.press/v235/jain24c.html) xây môi trường cho đánh giá code. [ABC-Bench](https://aclanthology.org/2026.findings-acl.1142/) đã có nhóm runtime chuẩn bị sẵn và nhóm phải setup, cùng phân tích build/functional stages. Do đó, “setup là nút thắt” đã có tiền lệ; so hai tập task khác nhau chưa đo tác động trên cùng task.

[SaaSBench](https://arxiv.org/abs/2605.17526) đánh giá tái xây SaaS và mô tả thất bại sớm. Denominator trong phân tích chi tiết là capability units, không phải những task độc lập. [For Coding Agents, the Repository Matters](https://arxiv.org/abs/2606.28235) nghiên cứu khác biệt giữa các repo bằng dữ liệu PR; kết quả quan sát đó không xác định thay đổi cụ thể nào của repo sẽ giúp agent.

[The Devil Is in the Interface](https://arxiv.org/abs/2608.11386) cho thấy tool architecture có thể thay đổi hành vi; [Larsen–Moghaddam](https://arxiv.org/abs/2606.13298) chỉ ra nguy cơ diễn giải density metric khi kích thước mã thay đổi. Hai nguồn củng cố việc giữ tool/budget ổn định và báo cả tử số, mẫu số, thay vì gọi mọi chênh lệch là hiệu ứng cấu trúc SmartKit.

## 8. Tổng hợp: ba câu hỏi có thể kiểm chứng

### Hướng A — sai lệch hợp đồng hành vi và thành công lần sửa tiếp theo

**Câu hỏi đề xuất:** Với những implementation vượt qua test hiện tại, khôi phục một quy tắc hành vi đã bị thay đổi có làm tăng khả năng hoàn thành một yêu cầu tiếp theo không?

Đây là hướng ưu tiên về câu hỏi khoa học, với điều kiện tìm được dữ liệu và phép can thiệp hợp lệ. Không cần gắn sẵn Next.js, security hoặc Server/Client boundaries. “Contract” ở đây là hành vi có chứng cứ mà người gọi hoặc hệ thống phụ thuộc, không đồng nghĩa schema Zod hay lựa chọn folder.

Đối chứng gần nhất bắt buộc là CodeThread. Phần cần bổ sung là can thiệp vào một hành vi được xác định trước và đo tác động trên yêu cầu tiếp theo, thay vì thêm một tương quan hoặc đổi stack. Chưa xác nhận không có công trình khác làm đúng can thiệp này; các truy vấn cơ chế đã được thực hiện nhưng artifact-level overlap vẫn chưa hoàn tất.

RQ dự kiến:

- A1: Trong tập chuỗi thay đổi đã chọn, những implementation vượt qua current tests có khác hành vi yêu cầu ở điểm nào? Đây là mô tả trong mẫu, không ước lượng mọi mã agent.
- A2: So với bản giữ nguyên và bản chỉnh sửa đối chứng, việc khôi phục đúng hành vi đó có thay đổi tỷ lệ giải quyết yêu cầu sau không?
- A3: Khi có tác động, lỗi sau thuộc loại nào và agent có tự sửa sai lệch được thừa hưởng hay không?

Thiết kế quyết định:

1. Chọn chuỗi issue/PR phụ thuộc nhau có base SHA, nguồn yêu cầu cùng thời điểm và executable checks. Hành vi nào được phép thay đổi phải ghi rõ; không coi mọi khác biệt với human patch là lỗi.
2. Nếu sử dụng agent implementation, tạo dữ liệu mới với trace đầy đủ. Current-test pass là điều kiện quan sát, không bằng chứng tương đương ngữ nghĩa.
3. Tạo ba starting states cho cùng một implementation: giữ nguyên; sửa tối thiểu contract drift; chỉnh sửa đối chứng không phục hồi contract, có quy mô/vị trí được cân nhắc tương ứng. Bản historical reference chỉ là đối chứng bổ sung, không thay cho so sánh chính.
4. Các trạng thái phải đều qua current tests và đều chưa đáp ứng yêu cầu feature tiếp theo. Nếu bản restored đã giải quyết feature tiếp theo trước khi agent bắt đầu, task không kiểm định được câu hỏi này.
5. Đóng băng specification của yêu cầu tiếp theo; dùng cùng model/harness/budget và session sạch, ngẫu nhiên thứ tự trong block task. Không lộ target patch hay hidden tests trong history.
6. Outcome chính là giải quyết yêu cầu tiếp theo và giữ các hành vi vẫn còn hiệu lực. Việc bản restored qua đúng test dùng để kiểm tra contract không phải kết quả chính; nếu chỉ đo điều đó, thí nghiệm sẽ tự xác nhận thao tác sửa.

Giới hạn: can thiệp code có thể đồng thời thay representation hoặc cung cấp gợi ý cho agent. Cần normalized edits, active control, review độc lập và phân tích độ nhạy; không gọi đó là tác động thuần của semantics nếu chưa loại được giải thích thay thế. Mẫu được chọn vì có drift chỉ cho hiệu ứng có điều kiện ở mẫu ấy, không cho prevalence trong toàn bộ agent outputs.

Điều kiện bác bỏ/chuyển hướng: khó tìm đủ contract có chứng cứ; patch phục hồi không thể tách khỏi feature tương lai; restored không hơn sham; khác biệt chỉ phản ánh benchmark lỗi; hoặc current full tests đã phát hiện gần hết các trường hợp. Null chỉ có sức nặng khi precision và task diversity đủ; không dùng vài kết quả không khác biệt để tuyên bố equivalence.

### Hướng B — review thực sự bổ sung khả năng phát hiện lỗi nào?

**Câu hỏi đề xuất:** Từ lúc PR có agent tham gia được gửi đến lúc tích hợp, test thay đổi thế nào về khả năng phát hiện lỗi thực tế đã được mô tả?

Dữ liệu chủ yếu là PR/issue/review/diff có sẵn, có thể bắt đầu mà không cần inference trả phí. So sánh trên cùng production snapshot: test có trước; test ở initial submission; test sau review. Dùng real-bug witness đã xác minh và buggy/fixed snapshots. Test hợp lệ phải fail/pass đúng lý do; compile error không được tính thành phát hiện lỗi. Mutation chỉ là kiểm tra phụ, có xử lý equivalent mutants và flaky tests.

Điểm khác biệt cần có là liên kết concern → revision → hành vi phát hiện được. Nghiên cứu gần đã đề xuất tách initial/final và mutation; chỉ dùng hai ý ấy chưa đủ novelty. Dataset truy vết và kết quả thực nghiệm mới phải mang phần đóng góp.

Không suy ra human review gây cải thiện từ lịch sử quan sát; không suy ra số giờ review từ timestamps. Nên giữ closed/unmerged PR để mô tả sampling funnel, đồng thời phân tích paired executable subset riêng. Nếu không phục hồi được initial commit hoặc test adaptation làm mất so sánh công bằng, phải ghi missingness và thu hẹp claim.

### Hướng C — hiệu ứng cung cấp môi trường chạy trên cùng một yêu cầu

**Câu hỏi đề xuất:** Với cùng mã nguồn và yêu cầu tính năng, cung cấp environment đã kiểm chứng có cải thiện joint success gồm tính năng mới và hành vi cũ không?

Đây là can thiệp thực dụng vào cùng task, phân biệt với việc so hai nhóm task của ABC-Bench. Chỉ thay environment preparation; giữ source, domain facts, công cụ và ngân sách như nhau. Nếu cấp thêm source scaffold, tests hoặc instructions thì phải tách thành treatment khác. Báo cả all-attempt joint success và các stage outcomes; không chỉ so nhóm build được vì nhóm đó đã bị chọn bởi treatment.

Lợi ích chỉ đến từ tiết kiệm setup budget vẫn là package effect có thể có giá trị thực dụng; không được đổi tên thành cải thiện năng lực suy luận nghiệp vụ. Hiệu quả có thể thấp hoặc hết khi agent mới setup tốt hơn. Cần kiểm tra artifact của ABC-Bench và các setup methods trước khi tuyên bố đóng góp cơ chế.

### So sánh để ra quyết định

| Tiêu chí | A: contract drift | B: verification qua review | C: supplied environment |
|---|---|---|---|
| Kiến thức cần tạo | Tác động của một thay đổi hành vi lên công việc sau | Những thiếu sót kiểm chứng được sửa qua revision | Hiệu ứng chuẩn bị môi trường trên cùng nhiệm vụ |
| Bằng chứng đầu vào | Chuỗi task, implementation, contract và oracle | PR histories, issue witnesses, test revisions | Cùng task có hai environment states |
| Công trình phải vượt qua | CodeThread và evolution benchmarks | Các nghiên cứu tests/coverage trong PR | ABC-Bench, SetupBench, SaaSBench |
| Rủi ro lớn nhất | Can thiệp thay nhiều thứ; task selection | Mất lịch sử; actor uncertainty; build bias | Chỉ đo setup time; overlap gần |
| Vai trò hợp lý của SmartKit | Fixture kiểm tra instrument | Minh họa kiểm chứng về sau, không dataset chính | Một instance trong paired environments |
| Khuyến nghị hiện tại | Ưu tiên audit dữ liệu cho câu hỏi cơ chế | Phương án mạnh nếu muốn bắt đầu từ dữ liệu quan sát thật | Phương án phụ, novelty cần kiểm tra kỹ |

Không có hướng nào được xác nhận Strong Accept hay hứa khả năng publish. Skill idea-evaluator được dùng để kiểm tra novelty, motivation, verifiability và solution-first framing. Chưa có đóng góp phương pháp được thực nghiệm nên không chấm các chiều Higher/Faster/Stronger/Cheaper/Broader như kết quả đã đạt. Chưa đủ thông tin để đánh giá capability match hoặc chi phí. Thời gian không phải ràng buộc do tác giả đặt; API budget, compute và nhân lực đánh giá độc lập vẫn chưa xác định.

## 9. Nguồn dữ liệu và việc nên làm trước khi chạy lớn

Phân biệt ba lớp dữ liệu: artifact lịch sử có sẵn; task/oracle do nghiên cứu dựng từ artifact đó; outputs/trajectories của agent được tạo mới. “Dữ liệu thật” nghĩa là nguồn gốc và quy trình thu thập có thể kiểm tra. Mã do agent tạo trong thí nghiệm là dữ liệu thực nghiệm hợp lệ khi lưu được provenance; task lấy ý tưởng từ sản phẩm thật vẫn cần ghi là task được dựng.

Nguồn đã xác minh ở cấp release:

- [AIDev](https://huggingface.co/datasets/hao-li/AIDev): PR metadata và subresources. Card v5 ghi sửa lỗi pagination ở các release trước. Pin revision và kiểm tra completeness từng PR; tín hiệu agent involvement không chứng minh toàn bộ patch tự chủ.
- Artifact của FEA-Bench/FeatureBench và CodeThread: nơi sàng lọc historical task chains; kiểm tra license và granularity trước khi dùng. Không khẳng định đã có đủ billing cases.
- [Coverage replication](https://doi.org/10.5281/zenodo.21419686) và [testing comparison replication](https://doi.org/10.5281/zenodo.21914644): điểm bắt đầu cho executable PR subset; chưa rerun nên chưa xác nhận dựng được trên máy hiện tại.

Chưa có task nghiệp vụ riêng lẻ nào được xác minh end-to-end trong lượt này. Việc chưa biết đủ task là một bất định về feasibility, không được che bằng cách hứa dataset lớn.

Gói audit dữ liệu đề xuất trước confirmatory experiments:

1. Lập selection rules độc lập với outcome: nguồn yêu cầu, semantics còn hiệu lực, historical dependency, khả năng dựng và absence of solution leakage.
2. Kiểm tra khoảng 15–20 candidate histories như một đợt khám phá có giới hạn; đây là khối lượng audit dự kiến, không phải sample size thống kê hoặc quota để chọn kết quả đẹp. Ghi mọi trường hợp bị loại cùng lý do.
3. Trên các trường hợp dựng được, xác minh baseline, reference và new-feature checks. Tìm giải pháp hợp lệ khác để phát hiện oracle quá khớp human patch.
4. Với hướng A, yêu cầu một minimal restoration cùng active control chưa giải quyết future task. Với B, yêu cầu test phiên bản cũ và mới so được trên cùng fault/snapshot.
5. Sau khi biết số task độc lập, biến thiên và effect/precision có ý nghĩa mới lập analysis plan và cỡ mẫu. Repeated runs được lồng trong task/repo; không coi nhiều lần chạy một task thành nhiều task độc lập.

Run manifest tối thiểu: task/source URL; repo/base/reference SHA; evidence cho contract; environment image/dependency lock; oracle version; model/harness/settings; visible instruction files; token/time budget; trace và patch; stage/test outputs; exclusions. Không tự sửa protocol sau outcomes rồi gọi là preregistration.

## 10. Kết luận trả lời brief

RQ-S1: Có bằng chứng về thất bại functional/security, khó khăn tiến hóa, khác biệt review và setup. Nhưng mức độ và ý nghĩa phụ thuộc setting; có phản chứng đối với nhận định rằng AI luôn làm giảm maintainability hoặc test quality.

RQ-S2: Phần lớn ý tưởng mở rộng thesis theo số dimensions, số tool hoặc số feature đã có đối chứng sát. Khả năng đóng góp đáng kiểm tra hơn nằm ở cơ chế có thể can thiệp và truy vết: behavior drift ảnh hưởng công việc sau; verification repair theo phiên bản; setup effect trên cùng task. Chưa được phép dùng từ “đầu tiên” cho bất kỳ hướng nào.

RQ-S3: Ưu tiên audit dữ liệu cho hướng A vì nó chuyển một mối liên hệ quan sát thành câu hỏi có đối chứng và outcome downstream độc lập. Nếu task chains/oracles không đủ, hướng B là lựa chọn có nguồn dữ liệu công khai rõ hơn. Hướng C có ý nghĩa thực dụng nhưng gần prior work hơn. Đây là khuyến nghị có điều kiện sau khảo sát, không phải bảo đảm novelty, hiệu ứng hay acceptance.

## Tài liệu và hồ sơ kiểm chứng

Danh mục có title/authors/year/status/URL/read scope: [bảng nguồn](../../research/evidence-ledger-v2.csv). Các đoạn trong báo cáo liên kết trực tiếp đến nguồn hỗ trợ; ba scout trong cùng thư mục giữ chi tiết điều kiện, version và phản chứng. Chưa có thí nghiệm trả phí, chưa thu thập kết quả agent mới và chưa thay đổi SmartKit.

## Cần tác giả kiểm tra trước khi chuyển sang paper

- Các ví dụ nghiệp vụ trong báo cáo là giả định; chỉ đưa vào manuscript như quan sát sau khi có artifact kiểm chứng.
- Quyền sử dụng dữ liệu/code, nguồn specification và tính đúng của contract trong từng task.
- Khả năng API/compute, người đánh giá độc lập và định hướng trao đổi với thầy; không suy ra ngân sách vô hạn từ thời gian không giới hạn.
- Yêu cầu khai báo hỗ trợ AI của venue/cơ sở đào tạo; lưu nguồn, quyết định, bản nháp và lịch sử thí nghiệm.
