> **Resolution update, 16 November 2026:** the current [prospective protocol](../main48/protocol.md) narrows the claim to six fixed constructed SmartKit tasks, declares heterogeneous S exposure, and separates acceptance from preservation. The revised workload has passed all 48 qualification cases with full V0, required reliability, named old/shared fault detection on both layouts, and 24 no-model capture/reset/score rehearsals. G1-G3 now have current instrument evidence; G4 is addressed only for this scoped exploratory comparison and contract audit, with broad uncertainty, prior-work limits and unavailable independent review disclosed. This is not evidence of a treatment effect, general design superiority or guaranteed publishability. The earlier holds below document the reasons for revision; consult [readiness](../main48/readiness.json) for the technical freeze. No main model session has been invoked.

# Xác minh giá trị nghiên cứu trước khi chạy SmartKit

## Cập nhật sau kiểm chứng runtime ngày15/11

**Đã kiểm tra thực tế; không chỉ đọc plan.** [Báo cáo mới](../task-feasibility-2026-11-15/report.md) ghi24 trường hợp lời giải đúng (6tasks ×2implementations ×2layouts),12 trường hợp lỗi cấy bị assertion dự kiến bắt, browser/DB thật và type/unit/build. U03 xác nhận fresh-login role đúng và stale-cookie caller không được ghi; baseline/cache source giữ nguyên.

Kết quả cũng cho thấy cả12 cặp task–implementation có0 edits vào module cũ được relocation; năm task mới chủ yếu dùng routes cùng vị trí ở hai layouts. Imports còn khác nên chưa kết luận S=0. Các faults mới chủ yếu là acceptance của feature mới, không chứng minh V1 preservation phát hiện chúng. Phát hiện này làm yếu lý do chi48 runs để khuyến nghị hai lựa chọn thiết kế: feasibility đã có, nhưng treatment relevance và giá trị suy luận còn chưa đạt mục tiêu đó.

Khuyến nghị hiện hành: **chưa chạy đợt48 cho mục tiêu so sánh thiết kế mạnh; cần xem lại workload/câu hỏi dựa trên bằng chứng này.** Không bịa thêm độ khó hoặc bắt số files để tạo effect; không tự tăng runs hoặc đổi roster. Chưa cần làm thêm reliability rounds chỉ để sửa một vấn đề về hướng nghiên cứu. Full qualification, V-gate năm task và independent review vẫn chưa hoàn tất; không gọi các probes hiện có là evaluator cuối.

Phần đánh giá trước khi chạy kiểm chứng được giữ bên dưới để đối chiếu; các câu “chưa chạy runtime” trong phần đó mô tả thời điểm trước lượt này.

Ngày 15/11/2026. **Kết luận: câu hỏi đáng khảo sát, nhưng chưa xác minh đủ giá trị suy luận và mức sẵn sàng để khuyến nghị chạy ngay đợt 48 phiên.** Khuyến nghị là tiếp tục có điều chỉnh (*Accept with Revisions* theo rubric ý tưởng), không phải quyết định nhận paper. Việc đổi cách diễn đạt đóng góp hoặc bổ sung audit chưa đóng được các khoảng thiếu dưới đây.

Đây là đánh giá trước thực nghiệm của trợ lý, có một lượt nghiên cứu nền AI riêng. Không phải phản biện độc lập của chuyên gia con người. Lượt này không gọi model thí nghiệm, không chạy lại application, không đổi task hoặc baseline.

## 1. Phần có giá trị thực tế đã xác định được

Người xây SmartKit có hai lựa chọn có thể triển khai: nhóm mã theo tầng/theo tính năng, và có/không cung cấp thêm bộ kiểm tra hành vi cũ. Câu hỏi cần trả lời là:

> Trên cùng các yêu cầu thêm tính năng và cùng ngân sách agent, hai lựa chọn này làm thay đổi khả năng hoàn thành tính năng mà giữ hành vi cũ và chi phí thực hiện đến đâu?

Kết quả đó có thể hỗ trợ quyết định cấu hình cho **SmartKit với workload và agent đã thử**. Nó không đo lợi ích cho mọi starter kit, năng suất người lập trình hoặc hiệu quả kinh tế của việc refactor/viết tests. Muốn khuyên ưu tiên đầu tư giữa hai việc còn phải tính công chuẩn bị và bảo trì; log token/time của agent chưa đo khoản này.

Đóng góp chính vẫn là bằng chứng thực nghiệm trả lời câu hỏi trên. Trace và audit là bằng chứng hỗ trợ giải thích/kiểm tra giới hạn. Chúng chỉ thành đóng góp riêng nếu có phát hiện đáng kể và đối chiếu nguồn, không chỉ vì tạo được ma trận hoặc thêm lượt chấm.

## 2. Kết quả xác minh theo từng tiêu chí

| Tiêu chí | Kết quả hiện tại | Căn cứ và ý nghĩa |
|---|---|---|
| Có người sử dụng và quyết định cụ thể | Có, trong phạm vi SmartKit | Hai lựa chọn starterkit và feature delivery dưới budget cố định; không cần giả định layout đang gây lỗi hoặc phải thắng |
| Prior work đã trả lời chính xác chưa? | Chưa tìm thấy exact comparison trong phạm vi đã đọc; chưa chứng minh vắng mặt | Đã có location/context interventions, checks/regression và failure analysis; khác tổ hợp yếu tố chưa tự đủ novelty |
| Task có tiếp xúc với khác biệt S/V không? | Chưa xác minh cho toàn bộ sáu task | DP-03 reference/alternative có 0 relocated existing modules bị sửa; có modules mới đặt theo layout. Agent vẫn có thể đọc mã chuyển vị trí, nên không kết luận S=0 từ file count |
| Bộ chấm phân biệt đúng/sai có căn cứ không? | Có bằng chứng cho DP-03 trong scope cũ; chưa cho năm task còn lại | Baseline/reference/alternative/fault records; V1 có điểm mạnh và giới hạn qua actual old/new paths |
| 48 runs có trả lời được chênh lệch nhỏ? | Chưa có căn cứ để hứa | Hai observations/ô và 24 sessions mỗi phía của một marginal contrast; local information check dưới đây cho độ nhạy thấp ở chênh lệch10pp trong một kịch bản đơn giản |
| Nghiên cứu vẫn có ích nếu không thấy khác biệt? | Có thể, nhưng không tự động | Có thể ghi kết quả, cost, trace và giới hạn; wide-null/all-pass chưa chứng minh equivalence hoặc đủ đóng góp để nộp |
| Có thể release đợt mới ngay? | Chưa | Năm task chưa qualification; U03 contract/runtime còn mở; threshold cho quyết định thực tế chưa chốt; model/analysis/allocation chưa freeze |

[Registry hiện hành](../main-task-candidates-v1.csv), [reference metrics](../prepilot-2026-11-12/reference-metrics.json) và [qualification report](../prepilot-2026-11-12/report.md) là căn cứ trạng thái. Đây là đọc hồ sơ, không gán là runtime kiểm chứng mới.

## 3. Những gì đối chiếu tài liệu xác nhận

Năm nguồn sát nhất và phần đã đọc được lưu ở [pre-run evidence review](../../paper-proposal/citation-evidence.md#pre-run-research-value-verification--15-november-2026).

| Nguồn | Phần đã có trước | Khác biệt còn phải chứng minh có ích |
|---|---|---|
| PV1, Zhu và cộng sự, *Precedent or Intent?*, v1 | Thay vị trí/tần suất examples; quan sát lựa chọn implementation | So sánh hai cách nhóm modules cùng logic, endpoint feature + preservation, có supplied executable checks |
| PV2, Chen và cộng sự, *Schrödinger's Code Repository*, v1 | Thay representation/path/symbol và bố trí trong file | Starterkit grouping policy khác can thiệp làm mất cues quen thuộc; không được gọi mọi layout experiment là mới |
| PV3, Trivedi & Schmitt, *Does Code Cleanliness Affect Coding Agents?*, v1 | Matched repository intervention, navigation và chi phí | Giữ domain logic, thay organization và package; cần outcome hoàn thành tính năng kèm bảo toàn |
| PV4, Alonso và cộng sự, *TDAD*, v2 | Test-context/impact map và resolution/regression | Cấp thêm test hành vi cũ khác chỉ dẫn test map; không chuyển test-level benefit sang patch-level success |
| PV5, Feng và cộng sự, *FeatureLoop*, v2 | Feature evolution, preservation, alternative/fault qualification | Fresh sessions và hai can thiệp cấu hình cụ thể; qualification tự thân không phải novelty |

Nghiên cứu nguồn hỗ trợ **một extension thực nghiệm hoặc replication có lý do**, chưa xác nhận một phương pháp mới. Search có mục tiêu, không systematic; các artifacts trước chưa được tái chạy. Số runs lớn của một bài khác không phải yêu cầu mẫu áp cho SmartKit.

## 4. Kiểm tra thông tin định lượng, không tiêu model runs

Tính toán được lưu tại [pre-run-information-check.json](pre-run-information-check.json), gồm assumptions, versions, recipe, kiểm tra tự động và nguồn hồ sơ. Không thay script/phương pháp main đã có.

Trong allocation cân bằng48, một marginal comparison có24 observations ở mỗi phía. Xét **kịch bản minh họa**, không phải dữ liệu SmartKit: độc lập, đồng nhất trong mỗi phía, chỉ có một effect, không có V effect/interaction, không task heterogeneity/batch/missing. Dùng Fisher hai phía và liệt kê chính xác toàn bộ625 bảng counts; không Monte Carlo.

| Xác suất giả định hai phía | Chênh lệch | Xác suất bác bỏ ở alpha .05 | Ở alpha .025 |
|---|---:|---:|---:|
| 45% và55% | 10pp | 7,0% | 3,8% |
| 40% và60% | 20pp | 21,5% | 13,8% |
| 35% và65% | 30pp | 47,0% | 35,3% |
| 30% và70% | 40pp | 75,0% | 64,3% |

`.025` chỉ là mức mỗi test khi chia alpha cho hai tests; đây không phải mô phỏng thủ tục Holm. Null error tính được lần lượt2,94% và1,34% trong kịch bản50%/50%. Fisher chỉ là phép sensitivity minh họa, không được chọn thay estimator/interval main, không là cận power tối ưu và không chứng minh mọi phương pháp cần một N lớn cụ thể. Task blocking hoặc baseline rate khác có thể thay đổi thông tin.

Kết quả này cho thấy sự lo ngại không chỉ do cận Hoeffding quá bảo thủ. Cận ±42,7 điểm trong plan vẫn chỉ thuộc phương pháp đó. Mình không dùng nó để nói408 là bắt buộc. 48 runs có thể cho tín hiệu nếu khác biệt lớn, nhưng chưa nên hứa quyết định đáng tin cậy cho mốc10pp đã bàn.

Ở một task-condition, `2/2` có khoảng nhị thức exact95% xấp xỉ[15,8%;100%] dưới giả định i.i.d.; không chứng minh probability=1. Đây là ví dụ cho một ô, không phải interval cho marginal effect. Repetitions có thể độc lập conditional; không giản lược rằng mọi phép tính chỉ có n=6. Sáu task chủ yếu giới hạn độ đa dạng và suy rộng.

**Thiếu quyết định khoa học:** mốc10pp trước đây chỉ là anchor, chưa là mức nhỏ nhất hữu ích. Phương án48 là nguồn lực đề xuất, chưa được xác nhận có đủ giá trị thông tin cho một quyết định. Phải chốt trước mức kết luận muốn dùng: mô tả thăm dò hữu hạn hay khuyến nghị cấu hình đáng tin cậy. Đổi wording, tăng số assertions hay gọi bài là case study không tạo thêm information.

## 5. Kiểm chứng từ artifact: điểm mạnh và giới hạn của V

Đã đối chiếu [visible-check.cjs](../prepilot-2026-11-12/visible-check.cjs), [final-check.cjs](../prepilot-2026-11-12/final-check.cjs), source reference/alternative và [sweep-faults.json](../prepilot-2026-11-12/sweep-faults.json). Các số sau thuộc **faults cấy trong qualification**, không phải outcomes agent, không phải tần suất lỗi thật.

- Với DP-03, fault làm tên được render thành HTML không an toàn bị V1 và hidden preservation phát hiện, ở cả hai layouts. Đây là bằng chứng gói bổ sung có khả năng phát hiện một regression cụ thể.
- Fault ghi sang user khác trên endpoint mới vẫn pass visible V1; hidden acceptance từ chối. V1 gọi API update-user cũ, không tự exercise endpoint mới. Đây là giới hạn phạm vi; không tự gọi là regression cũ.
- Fault sửa protected role qua endpoint mới cũng pass V1 nhưng fail cả hidden acceptance và identity/preservation checks. Cần map rõ invariant chung và tác động state, không đếm như hai independent defects hoặc đổi nhãn sau khi xem agent outcomes.

Điều có thể đo có ý nghĩa: **gói test được cấp thực sự phát hiện loại lỗi nào, và việc được cấp gói đó có đổi xác suất patch đúng trong budget không?** Hai câu hỏi khác nhau: seeded-fault pass không chứng minh agent biết dùng feedback; offline rescore V0 patch không đo phản ứng counterfactual của agent nếu được cấp V1.

V-gate hiện tuyển task có một fault cũ V1 bắt/V0 bỏ sót. Vì vậy randomized comparison chỉ áp dụng cho tập đã được chọn như vậy; không được gọi đó là lợi ích trên mọi yêu cầu SmartKit. Một audit tìm lại chính fault dùng tuyển task chỉ xác nhận instrument, không là discovery độc lập. Thiết kế vẫn hợp lệ khi khai báo scope và dùng agent-generated outcomes độc lập với qualification faults.

## 6. Trước khi chạy, bằng chứng nào phải đóng được?

| Điều kiện | Cách kiểm tra cụ thể | Trạng thái |
|---|---|---|
| Một contribution gắn quyết định và nguồn gần nhất | Một đoạn nêu lựa chọn của người dùng, knowledge bổ sung so với PV1/PV4, positive/adverse/null sẽ cho biết gì; audit giữ vai trò hỗ trợ | Có framing khả dĩ ở mục1, chưa xác lập novelty/paper-level value |
| S/V có cơ hội tác động trong task thực | Ma trận public operation → logical modules/old obligations; reference và alternative trên cả layouts; không đặt quota files hay lỗi nhân tạo xa task | DP-03 có evidence một phần; năm task còn thiếu |
| Đo đúng hỏng hành vi cũ và thiếu feature mới | Baseline/reference/alternative/faults; actual transport; classification old/new/shared; evaluator errors không đổi thành agent fail | Chưa hoàn tất toàn bộ, U03 là điểm feasibility cụ thể |
| Information phù hợp claim dưới48 | Báo counts/effect intervals; không superiority/equivalence promise; resource justification và cost preparation; giữ kế hoạch đủ48 không chạy thêm theo outcome | Đã làm sensitivity; adequacy cho quyết định mạnh chưa xác lập |

Đây là điều kiện dựa trên bằng chứng, không yêu cầu phải có kết quả dương hoặc phải thấy agent thất bại trước khi được nghiên cứu. Không bắt đầu lại vòng pilot mới chỉ để tìm task có chênh lệch đẹp. Không tăng48 hoặc đổi sang single-factor trong lượt xác minh này. Với cùng48, bỏ một factor cũng không tự tăng số observations mỗi phía marginal của factor còn lại; nó chủ yếu thay câu hỏi và phân bổ repeats.

Nếu mục tiêu là một nghiên cứu thăm dò có thể kiểm tra trên SmartKit, hướng có thể tiếp tục sau qualification. Nếu mục tiêu là chứng minh một lựa chọn giúp đáng kể hoặc quyết định đầu tư cho starterkits nói chung, thiết kế hiện tại chưa hỗ trợ lời hứa đó. Không trình bày vế thứ nhất như đã đáp ứng vế thứ hai.

## 7. Giá trị khi kết quả không như kỳ vọng

| Outcome sau collection | Có thể nói | Chưa thể nói |
|---|---|---|
| Success/cost khác nhất quán trong scope | Effect estimate có uncertainty, task pattern và dấu vết observable | Hiệu quả chung hoặc nguyên nhân trung gian từ trace |
| Contrast gần0, interval rộng | Chưa phân biệt được ở setting này | Hai lựa chọn tương đương hoặc layout vô ích |
| Mọi patch pass preservation | Không quan sát regression trong các checks/runs đã chạy; báo cost/process | Sensitivity của suite trên lỗi agent bằng100%; denominator lỗi bằng0 là không ước lượng |
| Mọi patch fail joint success | Failure stages trong budget/task cụ thể; xem instrument trước diễn giải | Một intervention vô dụng ở mọi task/model |
| Audit tìm escape có căn cứ | Giới hạn cụ thể của suite trên patch/obligation được tái hiện | Đây là hiện tượng chưa ai biết hoặc đủ cho paper chỉ vì có ví dụ |

Artifact hữu ích và báo cáo trung thực có thể được tạo ra ngay cả khi bất định lớn. Tuy nhiên, đóng góp để nộp bài còn cần một kết quả/diễn giải có thông tin đáng kể so với prior work. Không thể bảo đảm trước kết quả thực nghiệm; có thể kiểm tra tính quyết định, tính hợp lệ và ích lợi có điều kiện của thiết kế.

## 8. Giới hạn của lần xác minh

Không gọi model thí nghiệm, không khởi động Docker/application, không xác minh lại runtime hoặc hoàn thiện năm oracle còn thiếu. Chỉ đọc source/logs đã lưu và tính toán local mới. Search là targeted, comparator artifacts chưa reproduce; thiếu independent human reviewer. Không đo quota khả dụng hay effort chuẩn bị và không dùng deadline/giờ làm hàng tuần của tác giả làm ràng buộc mới.

Nguồn phương pháp: [SIGSOFT General/Benchmarking](https://www2.sigsoft.org/EmpiricalStandards/docs/standards), [Lakens, Sample Size Justification](https://lakens.github.io/statistical_inferences/08-samplesizejustification.html), [SciPy fisher_exact](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html), [SciPy binomtest](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html). Các nguồn live được xem ngày15/11/2026; local versions và recipe nằm trong numerical artifact. Bibliographic/version details của nearest work trong evidence ledger PV1–PV5.

<details>
<summary>Ghi chú rubric idea-evaluator, không phải điểm chất lượng bài báo</summary>

Định vị: empirical extension trong một setting; chưa có new method hoặc novelty được xác nhận. Hai concerns theo rubric là F1 (khác biệt có ý nghĩa so với prior work chưa xác lập) và F6 (claim mạnh vượt khả năng định lượng đã chứng minh). Đây là vấn đề phải sửa trước run, không phải bằng chứng ý tưởng đã bị dữ liệu bác bỏ. Bốn smoke runs trên một task đều pass không falsify S/V. Không suy từ việc nghiên cứu kết quả hai chiều sang bắt buộc phải thắng baseline.

Đánh giá tiềm năng bằng cơ chế, chưa có kết quả main: Higher6/10 do executable feedback có thể giúp sửa lỗi nhưng agent use chưa đo; Faster5/10 vì navigation có giả thuyết nhưng chưa có dữ liệu; Stronger6/10 cho yêu cầu bảo toàn cụ thể và hidden checks, không cho cross-domain robustness; Cheaper5/10 vì mới đo resource dùng, chưa chứng minh giảm total effort; Broader3/10 do một repo/một cấu hình và task chọn có chủ đích. Các điểm chỉ là phán đoán nội bộ để tránh Strong Accept vô căn cứ, không phải số liệu khoa học hoặc xác suất được nhận.

Khả năng thực hiện: đã có baseline và một task main-candidate có qualification; compute/resource và công chuẩn bị năm task là rủi ro chưa đo; dữ liệu synthetic tạo được nhưng provenance và validity cần kiểm tra. Không chấm năng lực cá nhân hoặc đặt lifecycle deadline từ assumptions. Paradigm probe: chưa xác lập hidden assumption mới, vấn đề đã được các nguồn nghiên cứu, agent capability cho phép setting hiện tại, chưa có căn cứ kỳ vọng đổi ưu tiên toàn ngành. Hướng phù hợp incremental empirical research hơn lời hứa paradigm shift.

Verdict ý tưởng: Accept with Revisions. Kết luận về execution: chưa nên release48 để tìm một đóng góp rồi mới định nghĩa claim. Tiếp tục sửa/qualification không model theo bốn điều kiện ở mục6; không xin thêm runs.

</details>

<details>
<summary>Đánh giá lịch sử trước khi chốt phương án48</summary>

Hồ sơ cũ giữ nguyên dưới đây; trạng thái cũ không thay đánh giá hiện hành ở trên.

# ??nh gi? h??ng nghi?n c?u SmartKit

## Review setup

- Input scope. Proposal, protocol v0, candidate task audit, newer development-task/layout qualification reports and scoped primary-source excerpts.
- Assessment boundary. Research-direction suitability for an empirical software-engineering case study, not a completed manuscript or a prediction of journal acceptance.
- Shared claim summary. Estimate effects of concrete repository organization and supplied behavioral-verification packages on extension acceptance plus preservation, under controlled agent conditions.
- Visible evidence. Same immutable packet in three isolated AI contexts, with common criteria and preassigned lenses. Packet and report digests archived. New artifact landing-page reading is labelled separately in the synthesis.
- Missing materials. Main agent trials, qualified main task set, V0/V1 allocation and isolated trial packages, precision/budget decisions, target venue and independent human review.
- Overall recommendation. Accept with Revisions in the idea-evaluation sense. Continue research while establishing contribution and closing main-study gates. This is not a venue acceptance decision.

C?c nh?n x?t l? m? ph?ng b?ng AI; kh?ng ??i di?n ba ph?n bi?n con ng??i. C?c ti?u ch? Nature ???c d?ng nh? c?c tr?c ph?n bi?n; kh?ng ??t Nature l?m venue m?c ti?u.



---

﻿# Reviewer 1

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


---

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


---

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


---

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

</details>
