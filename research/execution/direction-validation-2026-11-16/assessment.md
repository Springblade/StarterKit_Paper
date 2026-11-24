# Kiểm chứng hướng preservation-primary

Ngày 16/11/2026. **Verdict: Accept with Revisions — một hướng empirical replication/extension có điều kiện; chưa đủ căn cứ chốt pivot hoặc chạy 48 phiên theo thiết kế mới.** Đây là đánh giá hướng nghiên cứu, không phải quyết định nhận paper. Nhánh khảo sát tài liệu dùng context mới nhưng không phải independent human peer review.

Skills áp dụng: `idea-evaluator`, `experimental-design`, `statistical-power`, `scientific-critical-thinking` và `research`. Review chỉ tạo tài liệu và phép tính giả định; không sửa main48, không chạy app hay model thực nghiệm.

## 1. First impression và hai đính chính

Paper type phù hợp là **New Setting / focused empirical extension**, chưa có phương pháp coding agent mới. Câu chuyện có thể bảo vệ: đo trade-off của việc cung cấp thêm gói kiểm tra hành vi hiện hữu cho agent thực hiện feature tasks, giữ nguyên công cụ và ngân sách, trên workload đã chốt.

**Đính chính về novelty:** preservation-primary làm câu hỏi gọn hơn, không tự làm nó mới hơn. Prior work đã nghiên cứu verification capabilities, brownfield feature work, regression, visible tests và held-out outcomes. Thêm chữ SaaS, kit thứ hai hoặc joint success chưa đủ làm đóng góp mới. Xem [literature-review.md](literature-review.md).

**Đính chính về số quan sát:** bỏ S không tự tăng N cho V. Thiết kế cũ có 6 tasks × 2S × 2V × 2 lần =48, tức 24 runs/V và 4/task/V khi gộp S. Đề xuất 2 kits ×3 tasks ×2V ×4 lần =48 có đúng các số đó. Câu hỏi đổi từ V trung bình qua hai layout sang V tại layout cố định trong mỗi kit, đồng thời đổi task mix. Có thể giảm số primary questions và công can thiệp layout; không thể hứa power tự tăng hoặc coi hai estimands là một.

## 2. Fatal-flaws audit

Hai rủi ro lớn còn có thể xử lý, chưa có bằng chứng cho thấy bất khả sửa trong mọi phạm vi:

| Rủi ro | Căn cứ | Cách xử lý cụ thể |
|---|---|---|
| F1: đóng góp chưa phân biệt đủ với prior work | Verification access, regression context và feature/preservation endpoints đều có tiền lệ trực tiếp | Định vị replication/extension cho quyết định cung cấp authored legacy-check package ở cùng shell/tool access. Nêu khác biệt và tri thức bổ sung; không claim novel preservation method |
| F6: kết luận vượt thiết kế | Hai kits và sáu tasks chọn có chủ đích; partial executable oracle; chưa có main outcomes | Giới hạn finite-workload estimand; không suy ra mọi starter kit, correctness toàn phần, feedback mechanism hoặc efficiency ở mức success tương đương |

Chưa có main data bác bỏ hiệu ứng package. Bốn smoke runs trước đây đạt trên một task không chứng minh regression phổ biến hay package vô ích. Seeded faults là bằng chứng về bộ chấm, không thay lỗi thực tế của agent.

[SIGSOFT General Standard](https://www2.sigsoft.org/EmpiricalStandards/docs/standards) không xem replication hoặc negative results là lý do tự động bác nghiên cứu; vẫn cần đóng góp, cách đo và diễn giải phù hợp. Dùng general/software benchmarking guidance; không tuyên bố tuân thủ nguyên xi human-participant experiment standard cho software agents.

## 3. Đối chiếu nguồn và đóng góp có thể bảo vệ

Nhánh nghiên cứu đã đọc lại primary full texts của năm nghiên cứu gần nhất, thêm FeatureArc và một technical report audit tháng 11. Phiên bản, authors và phần đã đọc ở [literature-review.md](literature-review.md); đây là targeted adversarial review, không phải systematic review hay novelty clearance.

- [Mehta, verification surface, v2](https://arxiv.org/pdf/2608.28795v2): đã có brownfield task và grading hành vi cũ/mới. Phần khác biệt còn lại là cung cấp thêm authored runnable legacy checks với shell/tools cố định, thay vì đổi khả năng verification của toolset.
- [Ahmed et al., Investigating Test Overfitting on SWE-bench, v2](https://arxiv.org/html/2511.16858v2): đã phân biệt tests dùng khi refinement, golden issue tests và regression tests. Visible green nhưng regression fail không phải phát hiện mới tự thân.
- [TDAD v2](https://arxiv.org/html/2603.17973v2): đã cung cấp code-test impact information và đo resolution/regression. Package thêm assertions khác graph tìm tests, nhưng đều là verification information.
- [FeatBench v2](https://arxiv.org/html/2509.22237v2): đã có F2P/P2P. Không claim phát minh joint success hoặc feature-preservation endpoint.
- [FeatureLoop v2](https://arxiv.org/html/2610.35488v2) và [FeatureArc v1](https://arxiv.org/html/2610.37434v1): đã xét evolving features, preservation và feedback/self-verification. Fresh checkpoint sessions là khác biệt scope với continuing workspace, không tự chứng minh ưu thế.

Knowledge increment khả dĩ: **ước lượng có kiểm soát, giới hạn workload, về trade-off giữa giao tính năng, giữ nghĩa vụ cũ và tài nguyên khi maintainer cung cấp thêm package**. Audit saved patches hỗ trợ phân biệt package không được dùng, execution lỗi, lỗi quan sát nhưng chưa sửa, acceptance chưa xong, hoặc hidden preservation fail dù visible pass. Không gọi qualification artifacts hay codebook là novel framework nếu chưa có đóng góp tương ứng.

Nếu không có lỗi thực tế của agent, không ước lượng được package sensitivity đối với loại lỗi đó; phải báo dữ liệu và giới hạn. Không đổi claim để buộc tìm positive effect hay escape. Chưa đánh giá venue fit vì chưa biết venue/deadline.

## 4. Experimental-design audit

**RQ dự kiến:** trên sáu task thuộc hai kits cố định, việc được cung cấp thêm legacy-check package có thay đổi xác suất hoàn thành yêu cầu mới cùng bảo toàn nghĩa vụ cũ dưới 900 giây không? Người hưởng lợi là maintainer cân nhắc có chuẩn bị package cho agent; không phải người chọn kit nào tốt hơn.

**Experimental unit:** phiên agent mới được phân điều kiện. Kit/task là fixed contexts/blocks. 48 phiên không phải 48 repositories/tasks độc lập. Không dùng session N để suy ra starter-kit population; cũng không máy móc đổi N thành 2 bằng một cluster correction. Phụ thuộc do batch/model/quota phải được ghi và giới hạn inference tương ứng.

**Đề xuất allocation chưa được tạo:** 2 kits ×3 tasks ×4 repetition blocks; mỗi block hai phiên V0/V1, tổng24 pairs/48 slots. Randomize V order trong kit/task/repetition block và block order, giữ các cặp gần nhau về lịch để giảm drift. Workspace/DB/history tách biệt. Không đổi task/thứ tự theo outcomes; chỉ resume slot chưa gọi sau recovery, không thay slot đã gọi.

**Estimand:** trung bình đều sáu task-specific V1−V0 differences tại layout cố định đã chốt. Báo counts/task/kit trước aggregate. Hai kits không đủ để ước lượng đáng tin random-effect distribution cho population kits; kit×V chỉ descriptive heterogeneity. Thiết kế này bỏ causal question về S, không thể kết luận layout nào tốt hơn.

**Treatment:** V0 không có nghĩa bị cấm test. Hai arms có cùng spec, dependencies, shell và quyền tự viết/chạy checks; V1 chỉ thêm package. Contrast đo toàn bộ package-access effect, gồm readable examples, executable feedback và chi phí chạy. Hai arms không tách documentation khỏi execution. Không phân tích primary causal effect chỉ trên nhóm thực sự chạy tests: usage là post-treatment behavior, chỉ mô tả qua trace.

**Measurement:** mọi assessable final patch được replay trusted V0/V1 và held-out public-contract evaluator trong reset riêng. Báo acceptance, preservation, build/runtime và missing riêng. Visible pass + hidden acceptance fail không tự là preservation escape; cần hidden preservation violation cùng visible preservation pass. Dùng public path/assertion evidence, không suy từ coverage. Oracle khác fixtures/assertions không loại hết shared-author bias và không phải independent human validation.

**Selection:** yêu cầu task có plausible old/shared fault qua V0 nhưng bị V1 bắt tạo enriched workload. Chọn trước outcomes vẫn không làm mẫu đại diện mọi maintenance task. Nếu use cases do nghiên cứu dựng, ghi constructed; không giả thành production issues. Không ép task SePay/admin SmartKit sang Stripe/team model của kit khác.

## 5. Statistical-power và precision audit

Chưa có SESOI do tác giả xác nhận hoặc prior effect phù hợp. Không thể xác nhận 48 đủ cho confirmatory superiority, equivalence hoặc reliable ranking. [Lakens, Sample Size Justification](https://doi.org/10.1525/collabra.33267) cho phép resource justification nhưng đòi xem thông tin có phục vụ inferential goal không.

Đã chạy [design-sensitivity.py](design-sensitivity.py), lưu [JSON](design-sensitivity.json). Đây là **kịch bản giả định**, không phải expected effect hay kết quả agent. Script tính exact rejection probability cho phép kiểm hai phía sharp no-factor-effect null, alpha .05,24 pairs, giả định independent pairs và joint outcome distribution cụ thể trong pair. Kiểm probability mass, null calibration và swap symmetry đã đạt. Chưa chọn phép kiểm này làm analysis chính thức cho study mới; nó không kiểm zero-average-effect null.

Ví dụ baseline joint success giả định50%, within-pair correlation0:

| V1 giả định | Chênh lệch | Xác suất bác bỏ của phép kiểm minh họa |
|---|---:|---:|
| 60% | +10 điểm % | 5.9% |
| 70% | +20 điểm % | 19.0% |
| 80% | +30 điểm % | 45.7% |
| 90% | +40 điểm % | 79.9% |

Đổi baseline/correlation làm kết quả đổi; JSON có cả correlation .3 và heterogeneous task rates. Đây không phải cận tối ưu cho mọi phương pháp, dự báo về agent hoặc yêu cầu tăng N cụ thể. Nó không ủng hộ lời hứa bốn repetitions tự bảo đảm phát hiện hiệu ứng nhỏ.

Conditional independent-slot Hoeffding 95% half-width cho một finite-task contrast ở N48 khoảng0.392, so với khoảng0.427 cho hai contrasts trong family trước đây. Đó là thay đổi multiplicity của conservative bound, không phải thêm observations; không phải mọi interval đều phải rộng đúng mức đó. Mỗi task/arm chỉ4 lần, counts bước25 điểm%; mỗi kit12/arm. Không significant không có nghĩa không có tác dụng.

Nếu giữ48, phạm vi có thể bảo vệ là exploratory finite-workload comparison với complete outcomes/cost/patch audit, chấp nhận inconclusive estimates. Nếu cần kết luận về một cải thiện tối thiểu, chốt SESOI rồi thiết kế lại trước collection. Không tăng runs hoặc chọn threshold thuận lợi sau outcomes.

## 6. Capability, feasibility và rubric

| Mặt | Bằng chứng | Kết luận |
|---|---|---|
| SmartKit | main48 đã đạt24 package audits,48 qualification cases,24 rehearsals | Xác nhận setting cũ, không tự admission cho design2kit |
| Kit ngoài | Source screening: Next.js Starter gần stack nhưng seed gọi Stripe, không có behavioral test scripts tìm thấy | Runtime chưa qualified; chưa thể nói design2kit ready |
| Baseline V0 | Upstream suites không tương đương giữa kits | Ghi rõ checks do nghiên cứu thêm; contrast là package bổ sung trên baseline đã công bố |
| Resources | Docker memory/framework errors từng xuất hiện; SmartKit serial setup đã kiểm chứng | Cần đo external cold start/reset/duration bằng non-model checks; không quy infra failure thành agent failure |
| Budget | Một model,900s,48 slots => tối đa12 giờ model wall time | Chưa gồm preparation/scoring; quota không bảo đảm đủ48calls |
| Capability/deadline/venue | Chưa có giờ/tuần hoặc deadline; chưa có human reviewer độc lập | Không hứa timeline, lifecycle hoặc acceptance probability |

Rubric idea-evaluator, không phải điểm chất lượng hay xác suất được nhận: Higher5 (chưa có gain); Faster5 (chưa có gain, overhead có thể bất lợi); Stronger6 mechanism-based chưa xác nhận (checks có thể làm rõ old obligations); Cheaper5 (chưa có tổng preparation/maintenance cost); Broader5 (kit thứ hai chưa qualified). Không có hai trục8+ để khuyên Strong Accept.

Paradigm probe: chưa xác lập hidden assumption mới hoặc vấn đề cộng đồng bỏ qua; technology cycle chỉ là bối cảnh công cụ; chưa có field-level Hamming impact. Định vị incremental empirical work phù hợp hơn breakthrough.

Chỉ đo model tokens/time không đủ kết luận tiết kiệm tổng chi phí maintainer; cần đo hoặc công bố chưa đo công viết/duy trì package. Nếu chưa đo, chỉ gọi là agent execution cost.

## 7. Quyết định và contribution draft để review

**Chưa chốt pivot.** Khuyến nghị bỏ S chỉ được ủng hộ về tính gọn của câu hỏi và giảm công xây layout; chưa xác nhận mới hơn, mạnh hơn thống kê hay ready trên hai kits. Giữ V-only như ứng viên focused replication/extension, không tự hủy S hoặc rewrite paper.

Contribution statement dự thảo, chưa phải kết quả:

> Nghiên cứu ước lượng ảnh hưởng của việc cung cấp thêm gói kiểm tra hành vi hiện hữu đối với khả năng coding agent hoàn thành feature tasks và giữ nghĩa vụ cũ dưới ngân sách cố định. Phép so sánh xét sáu tasks được chọn trước trong hai SaaS starter kits cố định; báo kết quả theo task/kit, chi phí thực thi và đối chiếu visible checks với public obligations được evaluator riêng xác minh. Đây là empirical extension của nghiên cứu verification và feature preservation, không phải phương pháp agent mới hay khuyến nghị cho mọi starter kit.

Ba việc cần giải quyết trước main:

1. Chốt knowledge increment và mục tiêu paper bằng contribution draft cùng literature overlap table. Xác định exploratory replication có đáp ứng mục tiêu tác giả/venue không; thêm kit không tự xử lý bước này.
2. Non-model feasibility cho một external kit và task frame: actual workflow, services/reset/common baseline tests, public obligations và package runtime. Không chọn task bằng agent outcomes; không transplant gold patch.
3. Chốt estimand và mức thông tin cần có: giữ48 với exploratory scope hoặc tính lại budget theo SESOI, rồi mới tạo allocation/analysis/rehearsal/freeze mới. Không sửa freeze cũ để trông như prospectively approved cho design mới.

## 8. Ranh giới

Không có dữ liệu mới về hiệu quả agent, novelty clearance toàn lĩnh vực, venue acceptance prediction hoặc independent human review. Tài liệu mới nằm ngoài main48; không tạo start release. Mã/manifest/analysis cho thiết kế mới phải được kiểm riêng, không chỉ đổi tên số kit trong paper.
