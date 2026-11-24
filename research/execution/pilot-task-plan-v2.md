> **16/11/2026 ? b?n th?c thi hi?n h?nh:** [main48/protocol.md](main48/protocol.md) v? [plan](../paper-completion-plan.md) thay c?c h??ng d?n roster/gates ?ang hold b?n d??i. ?? ho?n t?t 48 tr??ng h?p qualification v? 24 di?n t?p kh?ng model; tr?ng th?i technical freeze ? [readiness](main48/readiness.json). Collection ch?a b?t ??u v? c?n start release ri?ng. C?c ph??ng ?n pilot/roster c? ch? c?n gi? tr? l?ch s?.

> **Cập nhật thực thi 16/11/2026:** bộ hồ sơ chuẩn bị cho 48 slots nằm tại [main48](main48/protocol.md). Đã dựng 24 packages, hợp đồng public, bộ chấm browser/auth/webhook/cron HTTP, runner có chốt start và phân tích prospective. Đang hoàn tất qualification toàn V0, reliability và 24 rehearsal; chưa technical freeze và chưa gọi model thí nghiệm. Không coi các probes trước đây là main admission. Trạng thái quyết định được tính lại bằng `main48/audit.py`; không chạy `collect.py run` trước freeze và start release.

# SmartKit plan: revised workload after feasibility, 15 November 2026

**Model collection remains on hold; no task admitted.** Keep A01/U02/U03 and replace A03/B03/B04 with A04/B05/B06. The 24 correct cases and 12 seeded-fault cases belong to the OLD roster. A04/B05/B06 now pass bounded runtime/basic/type probes with two closely related implementation variants on both layouts. Old-behavior seeded faults pass the basic suite but fail added preservation assertions. Combined reference production builds pass on both layouts. These results do not complete the frozen V1/independent hidden oracle, cron transport, alternative breadth or reliability qualification. The retained tasks also still need G1-G4. This proposal does not authorize model calls or baseline/freeze changes.


| Task | Current proposal | Slots |
|---|---|---:|
| MT-A01 / DP-03 | Keep: display name | 8 |
| MT-A04 | New: password policy across registration/reset | 8 |
| MT-B05 | New: payment-code recognition across existing consumers | 8 |
| MT-B06 | New: expiry enforcement during order completion | 8 |
| MT-U02 | Keep: admin account detail | 8 |
| MT-U03 | Keep: admin role change | 8 |
| Total | 6 tasks x 4 conditions x 2 repetitions | 48 |

The [current plan](../paper-completion-plan.md) defines proposed replacement contracts, G1-G4, collection and stop rules. This section takes precedence over the historical roster below. No measured qualification transfers to replacement tasks. Audit, analysis and missingness methods below remain reference material pending freeze; no schedule is released.

Cập nhật kiểm chứng bổ sung: [báo cáo](task-feasibility-2026-11-15/report.md) và ma trận JSON đã ghi 12 correct replacement cases, 6 baseline cases, 6 regression detections; old-directory preservation trên U02/U03 cũng đã thử. **Giữ hold collection.** Việc còn thiếu là contract B06, actual cron/solution-independent oracle, V1/hidden packages, reliability và exposure audit, rồi manuscript/author freeze. Không tăng 48 slots.

<details>
<summary>Earlier protocol and roster: historical reference</summary>

# Kế hoạch thực nghiệm SmartKit: hold trước model collection

Cập nhật 15/11/2026 sau kiểm chứng khả thi. **Chưa gọi model.** Allocation dự phòng là 6 task × 4 điều kiện × 2 lần = 48 slots; nó không phải author release.

## 1. Kết quả kiểm chứng đã có

- 24 trường hợp reference/alternative × layout đã pass browser/API/DB probes và typecheck/build trong phạm vi ghi ở [report](task-feasibility-2026-11-15/report.md).
- 12 seeded fault/layout cases bị assertion dự kiến bắt. Đây là fault cấy, không phải lỗi agent và không đo prevalence.
- 284 manifest records của hai layouts khớp; anonymous DB volumes của các case đã được dọn.
- Cả 12 cặp task–implementation sửa 0 existing relocated modules. Imports tới module relocated vẫn khác; static evidence này chưa đo agent navigation.
- U03 đã kiểm tra promotion/demotion, fresh-login permissions và stale-cookie caller bị từ chối ghi trong phạm vi reference. Baseline không sửa.

Các kết quả trên chứng minh khả năng xây task và probe. Chúng chưa chứng minh treatment reach, V1 preservation value hoặc main-study validity.

## 2. G1: treatment reach

Mỗi task phải có bảng:

| Trường | Nội dung |
|---|---|
| Public operation | Người dùng/admin làm gì, qua entry point nào |
| New state change | Dữ liệu/trạng thái nào được thêm hoặc đổi |
| Preserved obligations | Behavior cũ nào phải giữ |
| Layout exposure | Module nào được đọc/tái sử dụng; path nào khác giữa S0/S1 |
| Observable evidence | Trace/source/HTTP/DB evidence nào chứng minh exposure |

G1 đạt khi task có ít nhất một lý do nghiệp vụ khiến cách tổ chức mã có thể ảnh hưởng việc tìm hoặc tái sử dụng code, và reference/alternative vẫn đúng trên hai layouts. `source_files` hoặc `changed_files` không phải bằng chứng đủ. Nếu task chỉ sửa một route giữ nguyên và import surface không tạo khác biệt quan sát được, đánh dấu `S-uninformative` và thu hẹp claim S.

## 3. G2: preservation V-gate

V0 là checks cơ bản. V1 giữ V0 và thêm checks cho behavior cũ. Mỗi task phải có:

1. baseline: acceptance mới fail, preservation cũ pass;
2. reference và alternative: acceptance/preservation pass;
3. một old/shared fault hợp lý: V0 pass, V1 fail, hidden evaluator fail;
4. reliability rounds và reset logs trên cả layouts.

Lỗi chỉ có ở endpoint/feature mới thuộc acceptance. Không dùng nó để gọi V1 bắt regression. Shared invariant phải có mapping đường cũ/đường mới. Không thêm fault xa task để qua gate. Nếu không tạo được fault hợp lý từ public contract, task không vào V workload.

## 4. G3: task and evaluator validity

U03 phải kiểm tra server-side current role, self-demotion, anonymous/ordinary writes, target fresh-login role và stale cookie theo baseline scope. B03 phải nêu rõ expiry/concurrency ngoài phạm vi nếu chưa chấm. B04 phải kiểm tra own/completed-only export. A03 phải kiểm tra old/new credential, protected fields và session policy. Mỗi task cần actual transport, browser/DB fixtures, reset, valid alternative và missing/unassessable policy.

Các reference/alternative hiện có là assistant-authored feasibility artifacts. Full generic evaluator chưa hoàn tất. V1/hidden packages, parent access, instructions và trial visibility phải được audit trước freeze. Không gọi feasibility probe là main qualification.

## 5. G4: research value

Contribution phải trả lời một quyết định cụ thể:

> Trong SmartKit, với cùng yêu cầu và budget agent, cách nhóm mã và quyền tiếp cận preservation checks có thay đổi joint success/cost trong các task thật sự tiếp xúc với hai can thiệp không?

Plan phải đối chiếu prior work. FeatBench đã có feature + retained behavior; Precedent/SchrödingerRepo đã có repository representation/location interventions; TDAD đã có test context/regression; FeatureLoop đã có preservation/alternative/fault qualification; Code Cleanliness đã có repository interventions/cost. Vì vậy novelty không nằm ở 2×2, joint success, trace, seeded faults hay “dùng SmartKit”.

Một kết quả null vẫn được báo. Null với interval rộng không là equivalence. All-pass preservation không ước lượng được detection sensitivity trên agent faults. Không cần có escape để hợp thức hóa báo cáo; không được hứa paper-level contribution trước khi biết kết quả và mức tri thức bổ sung.

## 6. Nếu G1–G4 đạt: collection

| Task | S0V0 | S0V1 | S1V0 | S1V1 | Tổng |
|---|---:|---:|---:|---:|---:|
| A01 | 2 | 2 | 2 | 2 | 8 |
| A03 | 2 | 2 | 2 | 2 | 8 |
| B03 | 2 | 2 | 2 | 2 | 8 |
| B04 | 2 | 2 | 2 | 2 | 8 |
| U02 | 2 | 2 | 2 | 2 | 8 |
| U03 | 2 | 2 | 2 | 2 | 8 |
| **Tổng** | **12** | **12** | **12** | **12** | **48** |

Block theo task/repetition, randomize bốn conditions trong block, một config agent, workspace/DB mới mỗi slot, 0 replacement attempts. Bảo toàn mọi outcomes và missingness. Không dừng hoặc thêm runs theo hướng kết quả.

Báo task-cell counts trước; hai contrasts S/V là thăm dò trên task set cố định. Phân tích leave-one-task-out và domain-out là sensitivity, không tạo thêm independent tasks. Trace/patch audit, V0/V1/hidden replay và examples là evidence bổ sung, không tăng N.

## 7. Điểm dừng

- G1 không đạt: thu hẹp hoặc bỏ claim S.
- G2 không đạt: bỏ V effect hoặc dừng 2×2; không gọi V1 có tác dụng.
- G3 không đạt: sửa task/oracle, không chạy model.
- G4 không đạt: đổi contribution/estimand hoặc dừng hướng.

Không có release nếu bất kỳ task nào chỉ “chạy được” nhưng chưa qua G1–G4. Không thêm B01 để đủ sáu task. Không biến kết quả feasibility thành agent outcome.

<details>
<summary>Hồ sơ phương pháp và pilot trước đây: không phải lịch chạy hiện hành</summary>

### Phương án 408 runs đã được rút sau phản hồi nguồn lực

Nội dung sau là căn cứ của đề xuất đã rút, không phải lịch cần chạy. Phương án hiện hành đề xuất 48 runs theo nguồn lực, không duy trì mục tiêu precision cũ.

## 3. Cơ sở chọn 408 runs

Chọn theo độ chính xác cho tập task cố định, không lấy chênh lệch từ bốn runs cũ làm effect kỳ vọng. Trợ lý đề xuất **nửa độ rộng không quá 15 điểm phần trăm cho hai khoảng 95% đồng thời**. Mức này chỉ hỗ trợ mô tả hiệu ứng còn khá thô trong case study; chưa đủ để khẳng định một chênh lệch 10 điểm hoặc equivalence. Đây là lựa chọn nghiên cứu cần được review cùng tổng tài nguyên, không phải chuẩn bắt buộc của ngành [1].

Dùng nhánh fixed-tasks của [script hiện có](simulate-precision-power.py). Công thức ở đây áp dụng cho allocation cân bằng, không áp thẳng vào pilot cũ có số lặp khác nhau giữa tasks. Với `N = 4*T*R`, hai marginal contrasts có trọng số từng run bằng `+2/N` hoặc `-2/N`. Theo cận Hoeffding và điều chỉnh Bonferroni cho hai khoảng:

```text
h_family = sqrt(2 * ln(4 / 0.05) / N)
N_min = ceil(2 * ln(80) / 0.15^2) = 390
T = 6; mỗi lượt qua đủ task và conditions có 4*6 = 24 runs
R = ceil(390 / 24) = 17
N = 24 * 17 = 408
h_family = 0.14656, tức khoảng ±14.7 điểm phần trăm
```

Tính toán này đã được đối chiếu với hàm `infer` và self-check của script ngày 15/11. Nó cần các runs độc lập conditional trên task/condition, cấu hình ổn định và đủ outcomes. Phiên sạch giảm nguy cơ chia sẻ trạng thái nhưng không chứng minh độc lập của provider. Các ngày/batch phải được lưu và bố trí đủ bốn điều kiện; nếu phụ thuộc hoặc drift đáng kể, báo giới hạn và phân tích độ nhạy. Không giữ lời hứa ±14,7 khi giả định không đáp ứng.

Bảng 288 mô phỏng cũ là sensitivity lịch sử; không phải 288 runs agent và không được dùng làm task count. Nhánh hypothetical-task-population trả lời câu hỏi khác, không phải suy luận chính cho sáu task này. Số 17 là số lặp tối thiểu theo mục tiêu và cận đã chọn; không chứng minh đây là phương pháp thống kê hiệu quả nhất. Không tuyên bố 80% power ở chênh lệch 10 điểm. Nếu đánh giá thêm bằng mô phỏng, phải dùng đúng estimator, missingness và giả định đã ghi [2].



Hồ sơ dưới đây giữ nguyên nội dung trước lần viết lại ngày 15/11/2026. Trạng thái, số lượt và thứ tự công việc trong hồ sơ chỉ mô tả phương án cũ. Phần hiện hành ở trên quyết định đề xuất mới.

# Kế hoạch thực nghiệm SmartKit

Cập nhật 15/11/2026. Giữ thiết kế 2 × 2 để khảo sát tổ chức mã và việc cung cấp preservation checks; joint success gồm tính năng mới đúng và hành vi cũ được giữ. Phần dưới đây là kế hoạch hiện hành. Hồ sơ sau đó giữ bằng chứng và phương án lịch sử, không phải queue phải thực thi.

## Việc trợ lý làm tiếp

| Thứ tự | Công việc | Đầu ra cụ thể và điều kiện hoàn tất |
|---|---|---|
| 1 | Xác minh runner đã thay đổi gì | Đã xác định chỉ thêm `-v` trong lệnh dọn container; còn kiểm tra vòng khởi tạo/dọn trên môi trường thử không model nếu dùng runner này. Ghi phiên bản và kiểm tra phần bị ảnh hưởng trước freeze mới; không chỉ thay digest cho khớp. |
| 2 | Kiểm tra hai ứng viên A03 và B03 | Card ngắn cho đổi mật khẩu và tiếp tục đơn pending: lý do sử dụng giả định, phần thiếu ở baseline, hành vi mới/cũ, liên hệ S/V và điểm cần kiểm tra runtime. Chỉ dựng full oracle sau khi khả thi; ghi cả ứng viên không đạt. |
| 3 | Đề xuất một pilot có mục tiêu hữu hạn | Một bảng task × bốn điều kiện × repetitions, lý do từng lượt, cap/attempts, dữ liệu cần thu và quyết định sau pilot. Dùng task đã qualify; không cần đợi toàn bộ main set. |
| 4 | Thu main sau khi thiết kế đã chốt | Tập main qua qualification, số task/repetitions và uncertainty phù hợp mục tiêu nghiên cứu; giữ cùng task set cho hai effects chính, interaction bổ sung. Chốt tất cả trước fresh main runs. |

[Registry](main-task-candidates-v1.md) có 11 candidates, chưa phải 11 task chính. A03/B03 chưa runtime qualification; U03 là bước discovery tiếp theo nếu chốt được contract quyền/session. Không tuyển task theo condition thắng, số file phải sửa hoặc nhu cầu lấp đủ số lượng. Giữ cả localized và cross-workflow tasks; mô tả overlap và giới hạn của V-gate hiện có.

## Pilot sẽ trả lời điều gì?

Mục tiêu là kiểm tra quy trình với **agent thực**: patch có được thu/chấm đúng contract, session/reset/logs có đầy đủ, agent dùng checks thế nào, và thời gian/token/timeout thực tế trong những task đã chọn. Đầu ra là outcomes acceptance/preservation/joint success theo task × condition, patch/trace và resource logs; không có tỷ lệ pass bắt buộc.

Pilot hoàn tất khi mọi slot đã chốt có outcome hoặc lý do missing được xử lý, artifacts đủ để kiểm tra và các lỗi instrument được ghi rõ. Agent fail trong môi trường đúng vẫn là kết quả, không phải lý do chạy lại. Không dừng hoặc thêm lượt theo bên thắng/all-pass/all-fail. Nếu phải đổi task/instrument sau exposure, áp dụng version/reuse policy ở §12. Pilot được báo riêng trong paper; không cộng các outcomes đó vào main hoặc suy ra hiệu ứng chính từ mẫu nhỏ.

## Vai trò của 16 phiên và việc tác giả cần quyết định

16 phiên (DP-02: 4; DP-03: 12) là **phương án giữ để xem xét, chưa triển khai**. Không tự đổi sang một số khác. DP-02 development-only; DP-03 giữ quyền chọn dùng lại task bằng fresh main sessions nếu đủ policy đã đặt. Cards, mục tiêu pilot, repetitions, tổng tài nguyên và trạng thái kỹ thuật phải được trình bày trong một đề xuất cụ thể trước model invocation.

Tác giả chưa cần cung cấp dữ liệu hoặc viết tests. Trợ lý hoàn thành kiểm tra kỹ thuật và chuẩn bị đề xuất; tác giả review một lần ở mức mục tiêu, task contract, số runs và nguồn lực khi hồ sơ đã cụ thể. Sự đồng ý sửa plan không được coi là author release cho model. Main sample và precision vẫn chưa chốt.

## Bằng chứng hiện có và kiểm tra ngày 15/11

[Qualification report](prepilot-2026-11-12/report.md) ghi DP-02/03 qua kiểm tra hai layouts: 212 visible suite runs, 124 final-evaluator runs, 26 fault/layout cases và tám rehearsals không model. Browser transient và thiếu review độc lập vẫn là giới hạn. Các lượt này không phải agent trials mới.

Đã đối chiếu `local-runtime.py`: khi bỏ riêng `-v` trong lệnh `docker rm` trên bản sao trong bộ nhớ, toàn bộ file khớp digest cũ. [Docker storage audit ngày 13/11](docker-storage-audit-2026-11-13.json) cũng ghi thay đổi dọn anonymous volumes tại file này. Vì vậy đã xác định khác biệt source; chưa chạy kiểm tra runtime cho thay đổi đó. Lượt này không sửa runner, allocation hoặc freeze manifest. Những ghi chú ngày 14/11 nói chưa biết nguyên nhân là trạng thái trước phép đối chiếu này.

## Hồ sơ phương pháp và các quyết định trước đây

Phần hiện hành ở trên thay thứ tự công việc và allocation cũ khi có khác biệt. Các quy tắc qualification, isolation, outcome-independent selection và tách pilot/main bên dưới tiếp tục áp dụng; nguồn và số liệu lịch sử được giữ nguyên.

**Hồ sơ quyết định 12/11/2026:** tác giả chọn DP-04 C
(hold/development-only, không sửa baseline), cho phép V1 có tiện ích hành vi độc lập
đường dẫn dùng auth/DB thật và xác nhận chính sách dùng lại DP-03 độc lập outcomes;
DP-02 development-only. Xem decision log. Hoàn tất screening trên giấy và registry
trước full oracle/P0–P3. Các kịch bản có DP-04 bên dưới chỉ còn là lịch sử đề xuất,
không phải queue đang hoạt động. Chưa có quyền gọi model từ cập nhật này.

## Hồ sơ screening V-gate trên giấy, trước qualification

Ngày 12/11/2026. Đây là expected detection từ source, **không có observed pass**.
Baseline là `layouts/feature` và `layouts/layered` trong manifest; clone SmartKit
hiện có history-filter development reference nên không dùng nó thay starting snapshot.
UI routes giữ nguyên giữa hai layouts; kiểm tra dưới đây dùng HTTP/browser + real
auth/DB, không import theo gold module list. V0 gồm upstream unit/component tests,
typecheck/build và các scripts đang được cung cấp, kể cả `test:billing`.

Static inventory: upstream tests ở `src/tests/features/billing` chỉ kiểm tra billing
helpers/components. PaymentSection mock auth-facing actions. Script billing scenario
8 kiểm tra composite DB predicate, không thực sự gọi `cancelOrder` với foreign session;
không được ghi là chứng minh authorization qua transport. Type/build có thể phát
hiện lỗi cú pháp/type nhưng không dự kiến phát hiện các probe hợp type dưới đây.
Không biến thiếu coverage trong source thành một observed V0 pass.

V1 proposed checks:

| ID | Check trên baseline chưa giải | Oracle / giới hạn |
|---|---|---|
| VP-A1 | Qua `/api/auth/update-user`, A cập nhật name hợp lệ; request riêng kèm foreign user ID phải không ghi B; email/role/verification/orders giữ nguyên | Auth route hiện có; real cookies + DB before/after. Không dùng boundary 1–80 mới. Với tampering, ignore hoặc reject đều được; không bắt buộc name A đổi nếu request bị reject. |
| VP-A2 | Anonymous POST update-user bị từ chối và DB không đổi; role/email/verification tampering của caller không nâng quyền hoặc sửa protected fields | Hai request tampering riêng, tránh email rejection che role mutation. Baseline behavior phải được xác minh runtime. |
| VP-A3 | Cập nhật name qua API cũ, áp dụng response cookies rồi GET Settings trong cùng cookie jar; name được render an toàn, identity đúng | Probe shared auth response/session path; không đòi form mới. Không yêu cầu một response status cụ thể ngoài contract. |
| VP-U1 | Non-admin và anonymous GET admin users không nhận account-directory data; admin được xem | Real auth cookies, direct URL, không chỉ kiểm tra sidebar. |
| VP-U2 | Admin GET **không có role query**: rows/total đúng; session counts 0/nhiều khớp DB; ngày tạo giảm dần | Giữ nghĩa hiện tại là count mọi session record, chưa đổi sang active-only. Dates khác nhau; controls/filter mới không nằm trong check. |
| VP-U3 | GET admin users không mutate user/order records và không render raw session token | Chỉ kiểm tra các business records; bỏ qua session touch/update-age hợp lệ của auth. |

V1 có thể chứa runner/fixtures nhưng không chứa reference implementation, acceptance
cho feature mới, assertions về module paths hay hidden fixtures. Cùng public contracts
ở V0/V1. Runtime/cost/reset/parity đều còn phải qualify. API cũ chỉ bảo vệ đường cũ:
VP-A1/A2 không tự kiểm tra được một action mới do agent thêm.

| Task / fault probe | V0 check dự kiến bắt | V1 baseline check dự kiến bắt | Phạm vi phát hiện / kết luận trên giấy |
|---|---|---|---|
| DP02-F1 bỏ filter | Không có semantic check | Không; VP-U2 chỉ dùng All | Acceptance mới ở final; không giúp V-gate |
| DP02-F2 hardcode role | Không có semantic check | VP-U2 nếu All cũng mất rows; không nếu chỉ sai filtered branch | Filtered branch là acceptance mới |
| DP02-F3 total sai | Không có semantic check | VP-U2 nếu total All sai; không nếu chỉ total sau lọc sai | Không đưa filtered total vào V1 |
| DP02-F4 bỏ requireAdmin nhưng giữ authentication | Không có admin-route test | VP-U1 với ordinary authenticated user | Plausible khi sửa admin query/page; dashboard layout chỉ chặn anonymous, không chặn ordinary user |
| DP02-F5 đếm sessions sai | Không có session-count test | VP-U2 với user có 0/2/3 records | Plausible khi ghép count với filtered users; count không phải logic mới |
| DP03-F1 chỉ client validation | Không có profile test | Không | Validation 1–80 là acceptance mới; final kiểm tra server bypass |
| DP03-F2 tin payload foreign ID | Không có profile-write test | VP-A1 **chỉ nếu lỗi ở shared existing API/config**; không nếu lỗi chỉ ở new action | Final phải exercise chính transport lời giải dùng |
| DP03-F3 lưu nhưng UI stale | Không có profile/session test | VP-A3 nếu sửa shared response/cookie path làm API cũ stale; không nếu chỉ form mới không refresh | Phân biệt regression cũ với acceptance same-session UI mới |
| DP03-F4 ghi thêm protected field | Không có profile-write test | VP-A1/A2 nếu shared API/config nới field input; không nếu chỉ new action | Ví dụ probe bỏ field protection trong config/hook dùng chung; không sửa dependency để tạo lỗi |
| DP03-F5 đếm UTF-16 sai | Không có Unicode name test | Không | New code-point boundary: final acceptance, không V1 |
| DP03-F6 shared auth handler làm mất response Set-Cookie khi bọc POST để thêm validation | Không có auth-response/session test | VP-A3: DB name đổi nhưng cached Settings name cũ | Regression liên quan trực tiếp task, trên API đã có; không chỉ một lỗi xa lạ để V1 thắng |

**Quyết định screening:** DP-02 `paper-feasible-runtime-pending` qua F4/F5.
DP-03 `paper-conditional-runtime-pending` qua shared-path F3/F4/F6 nếu reference
thực sự cần/được phép sửa shared path và probes được review là plausible.
Nếu reference/alternative chỉ thêm action biệt lập và không có regression cũ có
liên hệ hợp lý, các hàng đó không đủ căn cứ: ghi V-gate fail và chuyển discovery,
không làm rộng fault model chỉ để đạt gate. Việc cho phép tiện ích V1 giải quyết
khả năng chạy check trên baseline; nó không tự chứng minh fault coverage.

Ở thời điểm screening: **0 task non-lookup đã qua V-gate runtime**; một ứng viên
non-lookup ưu tiên còn conditional trên giấy. Không gọi đây là fail đã quan sát,
và chưa kết luận SmartKit đủ T=8–10. Registry mở rộng ghi candidates mới và lý do
hold. Vì bước 3 chưa chứng minh workload main đủ rộng, chưa dựng full oracle hoặc
chạy P0–P3 ở lượt screening này. Bước chuẩn bị tiếp theo là chốt rationale/fault
mapping của DP-03 và task cards của pool mới, rồi qualification nếu vẫn khả quan.
Nếu không có non-lookup task qua gates, dừng trước model, báo feasibility limit
và xác định lại phạm vi khám phá theo Q16; không báo candidate rejection là agent failure.

Ma trận này là hồ sơ để review trước khi khóa evaluator, chưa thay requirement-to-check
matrix đầy đủ của P1. Review phải bao gồm toàn public contract, allowed changes,
fixtures, acceptance/preservation assertions và limits của các transports thực dùng.

## Precision/power sensitivity đã chạy, 12/11/2026

Script [simulate-precision-power.py](simulate-precision-power.py) và output
[precision-power-scenarios.json](precision-power-scenarios.json) là phân tích
**giả định trước main**, không dùng hiệu ứng/variance quan sát trong pilot.
Có 288 kịch bản × 5.000 Monte Carlo replications: T=8/10/17/40/120/200;
R=3/10 mỗi cell/task; task-effect SD=0/0.05/0.10 probability units; global null,
S-only, V-only và cả hai effects=0.10; hai uncertainty targets riêng.

Mô hình sinh: b_t uniform quanh 0.5 với SD=0.05; hai marginal effects độc lập
uniform quanh giá trị đã đặt với SD tham số; centered additive four-cell risks,
interaction mặc định 0. Không clip probabilities: từ chối scenario có support
ngoài [0,1]. Repetitions độc lập conditional trên task; không model batch/missingness.
Finite-set scenarios dùng task pairs đối xứng để mean truth đúng giá trị đặt,
giữ nguyên task probabilities qua replications. Hypothetical population scenarios
redraw task probabilities mỗi replication. Đây không phải sampling frame thật.

- **Fixed tasks:** estimator task-balanced; Hoeffding bounds/test conservative,
  finite-sample dưới giả định độc lập. Marginal 95% halfwidth là
  `sqrt(2*log(2/alpha)/N)`; Bonferroni simultaneous halfwidth cho hai effects là
  `sqrt(2*log(4/alpha)/N)`. Bounds không bị co về 0 ở all-pass/all-fail.
- **Hypothetical task population:** task-contrast mean và t interval với T−1 df,
  variance từ task contrasts, **xấp xỉ**, cần xem null rejection/coverage. Khi variance
  0, giữ replication trong denominator, không reject và dùng halfwidth 2 bao phủ
  toàn miền effect khả dĩ [-1,1].
  Không gọi đây là inference đã qualify cho main hoặc sửa estimand finite-set.
- Hai primary p-values qua Holm ở alpha=.05. Family intervals dùng Bonferroni,
  không gọi chúng là Holm intervals. Báo coverage, global/partial-null family error,
  rejection từng effect và cả hai, width/halfwidth, degenerate cells và Wilson 95%
  Monte Carlo intervals. Anchor 10pp chỉ là mốc sensitivity, không equivalence margin.

Một lát cắt output, effect S=V=10pp, SD giữa tasks=10pp, R=3 (width là **toàn
khoảng marginal 95%**; power là bác bỏ S sau Holm):

| T | N=4TR | Fixed-task power / width pp | Hypothetical-population power / width pp |
|---:|---:|---:|---:|
| 8 | 96 | 0.023 / 55.4 | 0.073 / 48.1 |
| 10 | 120 | 0.026 / 49.6 | 0.103 / 41.2 |
| 17 | 204 | 0.054 / 38.0 | 0.183 / 30.2 |
| 120 | 1440 | 0.858 / 14.3 | 0.952 / 10.8 |
| 200 | 2400 | 0.986 / 11.1 | 0.997 / 8.3 |

Không dùng bảng này để chọn sample size: fixed bound cố ý conservative; task t
procedure chỉ approximate. Worst observed null-family rate trong grid là .0092
cho fixed (.0069–.0122 MC95) và .0570 cho task population (.0509–.0638 MC95).
Đây là maxima chọn qua nhiều scenarios; không chứng minh global calibration, cũng
không thể bỏ qua t-test approximation khi freeze. Kịch bản heterogeneous/correlated
batches hoặc task-family sampling khác sẽ cần DGP/inference riêng.

Đối chiếu [Khatri, published PDF §4.6](https://aclanthology.org/2026.realm-1.5.pdf):
17 tasks/3 repeats, 30pp chỉ phát hiện 57%; 10pp ở power 80% cần ~120–200 tasks.
Nghiên cứu đó dùng hai agents, ba context strategies và omnibus permutation/
task-clustered procedures; không phải cùng factorial contrast/DGP của script này.
Không phải replication con số của Khatri; không dùng 288 evaluated runs của họ làm
N tương đương cho SmartKit. Bài cũng nói bounds 10–15pp là descriptive và MDE >30pp.
Ở kịch bản hiện tại, T=8–10 cho khoảng rộng và power thấp; đây chỉ là minh họa
vì chưa có 8–10 task qualified thật. Scope/precision target vẫn chưa khóa.

Chạy từ workspace root:

```powershell
python research/execution/simulate-precision-power.py --self-check
python research/execution/simulate-precision-power.py --simulations 5000 --output research/execution/precision-power-scenarios.json
# N là TỔNG trials, không phải số lượt mỗi task/cell; phải chia hết 4*T.
python research/execution/simulate-precision-power.py --tasks 10 --N 400 --effect-sd 0 0.05 0.10 --output "$env:TEMP/smartkit-precision-N400.json"
```

Output lưu seed từng scenario, versions Python/NumPy/SciPy và script digest để
kiểm chứng; không đưa digest vào paper. Self-check kiểm tra Holm, contrast/interaction,
degenerate variance, unbalanced N rejection và tái lập seed. Source/workflow attribution
nằm trong `../paper-proposal/citation-evidence.md`, mục Planning-script provenance.

**Kết quả verify P0:** [DP-04 spike report](dp04-spike-2026-11-11/report.md) đã tái hiện trên cả hai layout việc API revoke xóa DB record nhưng request Settings kế tiếp vẫn authenticated khi victim giữ đủ cookie cache. Baseline không bị sửa, chưa có coding-agent runs mới. DP-04 chưa eligible/evaluation-ready; cần reference/scope resolution trước khi chạy. DP-02/DP-03 chưa được qualification trong spike này. Các mục quy trình bên dưới là kế hoạch, không phải kết quả đã hoàn tất.

Ngày cập nhật 12/11/2026. Trạng thái: tác giả đã xác nhận định hướng và phân công sau trao đổi grilling; chưa khóa protocol thực thi hoặc chạy pilot mở rộng. Tài liệu này mở rộng kế hoạch tác vụ v2 tại chính đường dẫn hiện có. Tác giả yêu cầu trợ lý tự đề xuất các task phù hợp cho pilot, không tiếp tục phỏng vấn từng business rule ở bước này. Các quy tắc dưới đây là constructed specifications do trợ lý đề xuất phục vụ nghiên cứu, không phải nhu cầu production hoặc xác nhận của tác giả về từng chi tiết.

Phạm vi review cập nhật gồm spike khả thi DP-04 trước khi đầu tư full oracle, DP-02 chạy một phiên/condition để kiểm tra runner/browser, DP-03 và DP-04 (nếu đủ chuẩn) chạy ba phiên/condition. Đề xuất mới là 16 hoặc 28 phiên High, thay cho bản đề xuất 24/36 trước review. Theo phản hồi tiếp theo của tác giả, giữ quyền chọn dùng lại DP-03 và có điều kiện cho DP-04, chưa gán evaluation-ready hay xác nhận từng contract. Cấu hình reasoning thấp hơn và repo thứ hai chưa được duyệt. Các con số dưới đây là giới hạn lập kế hoạch, không phải sample size đã được chứng minh đủ cho suy luận chính.

## Định hướng đã được tác giả xác nhận ngày 12/11/2026

Câu hỏi nghiên cứu là cách tổ chức mã theo tính năng hoặc vai trò kỹ thuật và việc cung cấp sẵn bộ kiểm tra hành vi ảnh hưởng thế nào đến khả năng coding agent thêm tính năng, bảo toàn hành vi và chi phí thực hiện. SmartKit là đối tượng thực nghiệm để tạo bằng chứng cho câu hỏi này. Kết luận thực nghiệm phải nêu phạm vi tác vụ, hệ thống, model/harness và ngân sách đã thử; câu hỏi chung không biến kết quả một hệ thống thành bằng chứng đại diện cho mọi repository.

Tác giả đã xác nhận các quyết định sau; xem lịch sử ở [decision log](author-decisions-2026-11-11.md):

- Đóng góp hướng tới bằng chứng hỗ trợ lựa chọn cách nhóm mã và cung cấp regression checks khi giao tác vụ mở rộng phần mềm cho agent. Extension hay replication còn cần đối chiếu các công trình/artifacts gần nhất; chưa có tuyên bố mới đầu tiên hoặc layout nào tốt hơn.
- Hai tác động trung bình của tổ chức mã và gói kiểm tra là mục tiêu chính. Các tác động theo từng điều kiện và tương tác là phân tích bổ sung; không coi nghiên cứu đã đủ chính xác để xác nhận tương tác. Acceptance và preservation cùng quyết định joint success; chi phí và failure patterns bổ sung diễn giải.
- Dùng chênh lệch tuyệt đối 10 điểm phần trăm về xác suất joint success làm mốc thảo luận ban đầu cho các kịch bản main-study planning. Đây chưa phải ngưỡng chính thức, effect kỳ vọng, equivalence margin, hoặc mục tiêu độ rộng khoảng bất định. Cần chọn riêng interval procedure và precision target trước main collection, không dùng chênh lệch pilot quan sát được để hợp thức hóa số mẫu.
- Sau pilot, ưu tiên discovery/qualification các loại tác vụ có rationale khác nhau trước khi tăng repetitions trên vài task. Giữ cả thay đổi cục bộ và thay đổi qua nhiều phần của ứng dụng; không ép số file, thêm độ khó nhân tạo hoặc chọn task theo condition thắng.
- Không dùng deadline hoặc số giờ/tuần của tác giả làm ràng buộc lập kế hoạch. Quyết định này không bỏ cap từng trial, giới hạn kỹ thuật của spike, trần số attempts, hoặc ràng buộc hạn mức Codex đã ghi. Không tự mở rộng model budget hay dùng paid API.
- Trợ lý tự đề xuất task, prompt, reference/alternative, ma trận và bộ chấm; tự tìm thông tin kỹ thuật thay vì tiếp tục hỏi tác giả từng business rule. Tác giả review bộ hồ sơ cụ thể ở cấp tổng thể: mục tiêu, rationale tác vụ, đầy đủ requirements và phạm vi chấm, nguồn lực và mức kết luận. Việc xác nhận định hướng chưa đồng nghĩa duyệt mọi specification DP-02/03/04.
- Giữ mốc review sau chuẩn bị/qualification DP-02/DP-03 và xử lý trạng thái DP-04, trước pilot mở rộng. Nếu thiếu task, áp dụng queue đã định trước. Không gọi model trials chỉ từ việc tác giả đồng ý bản chốt định hướng.

### Bốn việc cần hoàn tất và bằng chứng bàn giao

| Việc | Trợ lý chuẩn bị để tác giả review | Điều kiện trước bước tiếp |
|---|---|---|
| Làm rõ đóng góp | Đối chiếu intervention, outcome và phạm vi với các artifacts gần nhất; viết contribution statement có giới hạn | Giải thích được hiểu biết bổ sung hoặc mục đích replication; không lấy tên SmartKit hay thiết kế 2 × 2 làm điểm mới tự thân |
| Chọn tác vụ phù hợp | Registry/rationale/family và mô tả mã liên quan theo hai layouts; báo cả candidates không đạt | Tác vụ có mục đích sử dụng rõ và phần mới thực sự thiếu; dùng S metrics để mô tả, không làm cổng loại hoặc buộc lời giải theo gold file list |
| Kiểm chứng công cụ | Task prompts/cards, ma trận requirements–checks, reference/alternative/fault probes, logs browser/auth/DB, visible/final suites và packages | Qua P0–P3 cho từng task giữ lại; tác giả review tổng thể task card/matrix; chốt allocation và tổng runs thực tế trước invocation |
| Lập quy mô main study | Các kịch bản success rate, precision, task diversity và tài nguyên quanh mốc thảo luận 10 điểm phần trăm | Sau pilot mới chốt main tasks, configuration, số runs, interval/precision và stopping policy; giữ exploratory scope nếu chưa đạt độ chính xác cần thiết |

Hiện định hướng đã chốt; artifact-level contribution audit, qualification tác vụ mới và main precision plan vẫn chưa hoàn tất. DP-04 đang bị chặn theo spike report; DP-02/DP-03 chưa evaluation-ready. Số 16/28 bên dưới là kịch bản pilot có điều kiện, không phải sample size chính hay allocation sẵn sàng chạy. Cập nhật này chỉ ghi quyết định và bước bàn giao, không tạo thêm reference, qualification logs hoặc agent outcomes.

## Mục tiêu

Pilot giúp kiểm tra task có thực hiện/chấm được không, agent có dùng visible checks không, độ khó và chi phí trong cấu hình hiện tại. Không dùng một lượt mỗi cell để suy luận hiệu ứng layout/verification. Mỗi task bắt đầu từ cùng baseline riêng, không cộng dồn lời giải của task trước. Các nhiệm vụ và outcomes này được giữ trong development pool, không tự chuyển vào dữ liệu chính.

Task lịch sử đơn hàng đã smoke-pilot xong. Đề xuất thêm ba task dưới đây để có một ví dụ cục bộ và các thay đổi liên quan form/auth/session, thay vì tiếp tục toàn các biến thể billing lookup. Phân loại theo bề mặt hành vi dự kiến; không bắt buộc số file hoặc kiến trúc lời giải. Source anchors và giới hạn static inspection ở main-task-candidates-v1.md.

## DP-02 — Lọc vai trò trong danh sách quản trị

- **Nguồn liên hệ:** MT-U01, admin users page đã có read/permission/session-count query; chưa thấy UI role filter trong source đã đọc.
- **Specification đề xuất:** native GET dropdown All/User/Admin; thiếu, rỗng, sai hoặc lặp tham số role trở về All. URL/reload giữ lựa chọn; empty result giữ controls. Total là số tài khoản sau lọc. Session counts của từng user và thứ tự ngày tạo giảm dần giữ nguyên.
- **Preservation:** chỉ admin được xem, kể cả gọi URL trực tiếp; filter không đổi DB; không lộ session tokens; user/anonymous tiếp tục bị từ chối.
- **Vì sao đưa vào pilot:** tác vụ cục bộ, ít phụ thuộc ngoài, phù hợp kiểm tra lại harness với admin authorization. Pattern gần history filter nên chỉ là một development calibration case, không coi là một họ bằng chứng mới độc lập.
- **Qualification:** real admin/non-admin/anonymous sessions, users nhiều roles/0-nhiều sessions; browser submission cùng server-side checks. Baseline chưa có filter, reference phải qua cả hai layouts.

## DP-03 — Sửa tên hiển thị của chính mình

- **Nguồn liên hệ:** MT-A01, Settings đang hiển thị profile dạng read-only. Không tuyên bố backend auth thiếu khả năng update profile.
- **Specification đề xuất:** form sửa display name; trim khoảng trắng hai đầu; 1–80 Unicode code points sau trim; hỗ trợ tiếng Việt; server từ chối input trống/quá dài, không ghi thay đổi khi từ chối. Sau lưu, form/Settings hiển thị tên mới trong cùng phiên và lần tải trang mới. Email, role và verification không được thay đổi qua thao tác này.
- **Preservation:** caller chỉ cập nhật chính mình kể cả payload có user ID khác; không lộ dữ liệu profile khác; sign-in và order ownership giữ nguyên; render tên an toàn.
- **Vì sao đưa vào pilot:** thêm write path, validation và session-rendered UI ngoài bài toán lọc bảng. Đây là test khả năng phối hợp các phần của ứng dụng, chưa là claim task chắc chắn sửa nhiều file.
- **Qualification:** browser thật để kiểm tra submit/state, real auth và DB; input có dấu/trống/quá dài, payload giả mạo caller, reload và đăng nhập lại. Dùng API sẵn có nếu thích hợp; chấp nhận các implementation đúng khác nhau.

## DP-04 — Liệt kê và thu hồi một phiên đăng nhập khác

- **Nguồn liên hệ:** MT-A02, source đã export listSessions/revokeSession/revokeOtherSessions; Settings chưa có controls. Không mô tả phần API sẵn có là feature mới hoàn toàn.
- **Specification đề xuất:** Settings hiển thị các phiên còn hạn của chính mình, đánh dấu current session; cho thu hồi một other session, không cung cấp thao tác thu hồi current trong task này. Chỉ hiển thị thông tin tối thiểu như current marker, created/expiry time; không render raw token. Session bị thu hồi phải bị từ chối ở lần truy cập protected tiếp theo; session hiện tại và phiên của người khác vẫn hoạt động.
- **Preservation:** không đọc hoặc revoke session người khác; không đổi role/email/orders; session hết hạn không được hiển thị như active. Sau revoke, danh sách cập nhật đúng.
- **Vì sao đưa vào pilot:** kiểm tra thay đổi liên quan lifecycle và quyền truy cập qua nhiều request, bổ sung một trường hợp khó hơn render/query. Đây là thử thách công cụ và oracle, không phải thêm task để buộc một layout thất bại.
- **Rủi ro cần qualification trước agent:** auth có cookie cache. Phải xác nhận reference có thể đáp ứng immediate next-request invalidation mà không phá hợp đồng chung; nếu không, giữ task ở trạng thái chưa đủ điều kiện và báo nguyên nhân. Không âm thầm nới contract sau khi xem agent outcomes hoặc mock chính invalidation.
- **Qualification:** real browser hoặc cookie jars độc lập cho hai users, ít nhất hai sessions của một user; kiểm tra token bị revoke sau thao tác và current/foreign tokens vẫn hợp lệ. Browser UI cần được kiểm tra, không suy từ HTTP/DOM-only smoke evaluator cũ.

## Thứ tự và giới hạn

Theo cập nhật 14/11, thực hiện bảng công việc đầu tài liệu và discovery queue trong registry. DP-04 giữ hold; không chạy lại spike hoặc đổi baseline trong lượt này. DP-02/03 giữ qualification record, không lặp toàn bộ checks khi không có thay đổi liên quan. Trước model, đối chiếu runtime/freeze và hoàn thiện hồ sơ task/allocation cụ thể. Tác giả review tổng thể, không chọn từng file hoặc tự viết tests.

Cấu hình pilot đã chọn trước vẫn là ứng viên; thay model/budget/contract phải có lý do trước outcomes của đợt mới. Phân biệt backend đã có với behavior/UI mới; từng task bắt đầu từ baseline riêng, không tích lũy lời giải. Đồng ý sửa plan không tự mở model trials.

## 1. Pilot này cần trả lời điều gì?

Pilot cần cung cấp bằng chứng cho năm quyết định chuẩn bị nghiên cứu chính:

1. Tác vụ có thực sự thiếu ở baseline và thực hiện được bằng những thay đổi được phép không?
2. Bộ chấm có nhận lời giải đúng khác cấu trúc, phát hiện lỗi hợp lý và chạy lặp ổn định không?
3. Bốn gói điều kiện có chạy trong môi trường cô lập, cùng yêu cầu và cùng quyền công cụ không?
4. Thời gian, token usage, timeout và lỗi hạ tầng nằm trong phạm vi nào ở cấu hình phát triển này?
5. Main study cần điều chỉnh task discovery, thời hạn hay phạm vi kết luận nào trước khi khóa protocol?

Pilot có dữ liệu agent thực. Dữ liệu được lưu riêng là development, kể cả khi mọi task đều pass. Không chuyển các task/lượt đã dùng để sửa công cụ vào tập chính. Không dùng pilot để chọn tập task khiến layout hoặc package ưa thích thắng.

## 2. Thiết kế, số lượt và nguồn lực đề xuất

### Bốn điều kiện

| Điều kiện | Tổ chức mã | Gói kiểm tra được cung cấp |
|---|---|---|
| S0V0 | Layer-based, theo vai trò kỹ thuật | Basic checks đang có |
| S1V0 | Feature-based, theo tính năng | Basic checks tương đương |
| S0V1 | Layer-based | Basic checks và gói preservation bổ sung |
| S1V1 | Feature-based | Basic checks và gói preservation bổ sung tương đương |

Mọi điều kiện được đọc cùng yêu cầu chức năng, preservation và quy tắc input. V0 cũng được tự viết/chạy tests. V1 bổ sung checks cho các hợp đồng cũ có liên quan; không đưa gold solution hoặc acceptance suite của tính năng mới vào package. Các command, fixture và runtime của visible checks được ghi trong manifest. Không ép số checks giữa các task bằng nhau; chốt inventory của từng task sau qualification.

Đơn vị thực thi là một phiên agent mới, gắn với task × condition × repetition. Repetition là lượt thử khác trên cùng task, không phải một task độc lập. Một block gồm bốn conditions của cùng task và cùng repetition.

### Số lượt — phương án cũ để đối chiếu

Bảng dưới đây chỉ mô tả các kịch bản đã chuẩn bị. Không có phiên nào được xem là phải chạy cho tới khi task-frame review, contract review, artifact check và author release hoàn tất.

| Phạm vi | Task | Conditions | Phiên/cell/task | Phiên agent dự kiến | Trần wall time ở 15 phút/phiên |
|---|---:|---:|---:|---:|---:|
| DP-02 và DP-03 đủ chuẩn | 2 | 4 | DP-02: 1; DP-03: 3 | 16 | 4 giờ |
| Có thêm DP-04 đủ điều kiện | 3 | 4 | DP-02: 1; DP-03/04: 3 | 28 | 7 giờ |

DP-02 chỉ kiểm tra runner đã tổng quát hóa và browser scorer vì gần họ task cũ. Ba repetitions của các task còn lại là lựa chọn thực dụng để quan sát lặp lại và chi phí; chưa là power/precision justification. Không ước lượng độ biến thiên đáng tin cậy từ chỉ ba phiên mỗi cell. Khi thiếu task đủ chuẩn, chỉ dùng queue dự phòng và điều kiện kích hoạt ở P0 dưới đây; không âm thầm thay task theo outcomes.

### Báo riêng số task T và số lượt N

Với repetitions khác nhau theo task, `N = 4 × sum_t R_t`. Phương án ưu tiên là `T = 2, R_t = (1,3), N = 16`; phương án có DP-04 là `T = 3, R_t = (1,3,3), N = 28`. Bản trước dùng R=3 chung nên có N=24/36. Đếm thêm task families, attempts, completed outcomes và missing outcomes riêng; reference runs, mutation probes và các assertion của evaluator không làm tăng T hoặc N agent trials. Không gộp thô để task nhiều repetitions chiếm trọng số lớn hơn trong một estimand task-balanced.

T bằng hai hoặc ba chỉ hỗ trợ kiểm tra công cụ, coverage và các quan sát chi phí/độ khó ban đầu trên những task đó. Không fit random-task effect để coi đó là ước lượng đáng tin cậy của độ biến thiên hiệu ứng giữa các task; không suy rộng từ ba task sang toàn bộ SmartKit hoặc repository khác. Precision/resource planning dùng các kịch bản giả định được công bố rõ, thay vì cắm một variance estimate không ổn định từ pilot vào công thức main sample size.

Sau các repetitions đã đề xuất, ưu tiên discovery/qualification thêm task có rationale và contract khác nhau trước khi tăng repetitions. Tám phiên cắt khỏi DP-02 không tự được chuyển thành model runs khác; phần nguồn lực tiết kiệm ưu tiên việc chuẩn bị task. Chưa tăng task count hay ngân sách. Mở rộng task phải tính chi phí reference, browser/session fixtures và evaluator; chỉ thêm ID hoặc biến thể filter gần giống không giải quyết task diversity.

Đề xuất tối đa sáu replacement model attempts cho lỗi hạ tầng đã được adjudicate, tối đa một replacement/slot. Tổng trần là 22 hoặc 34 model attempts, tương ứng tối đa 5,5 hoặc 8,5 giờ wall time ở cap hiện tại. Đây là hard cap, không phải thời gian hoàn thành dự báo; chưa gồm chuẩn bị, build, qualification, setup, chấm và phân tích. Setup-only retries không gọi model được ghi riêng.

Các bảng 16/28 là các kịch bản allocation đã chuẩn bị trước task-frame revision, không phải quyết định task set hiện hành. Nếu queue discovery được kích hoạt trước release, tính lại `N=4×sum R_t` từ registry và công bố danh sách thực tế, không giữ nhãn 16 nếu số khác. Trần kỹ thuật cũ vẫn tối đa 28 scheduled sessions cộng sáu replacements, nhưng không tạo quyền gọi model; phải có task-frame review và author release trước. Queue không tự cho phép thêm trials, configuration hay scope vượt trần.

### Cơ sở thời gian và token từ smoke pilot

Bốn phiên history-filter cũ có tổng wall time 442,65 giây, trung bình 110,6625 giây, khoảng 99,66–141,27 giây/phiên. Nếu chỉ nhân trung bình này, 16 hoặc 28 phiên tương ứng khoảng 0,49 hoặc 0,86 giờ agent. Đây là ngoại suy minh họa từ một task đơn giản, không phải dự báo hay cận dưới cho task mới. Cap 4/7 giờ và ngoại suy phải được trình bày riêng.

Theo `pilot-2026-11-11/summary.json`, provider usage totals của bốn phiên là 1.330.159 input tokens, trong đó 1.190.272 cached input tokens, và 16.110 output tokens. Trung bình tương ứng 332.539,75 input, 297.568 cached input và 4.027,5 output tokens/phiên. Reasoning-output events có tổng 4.717; giữ nguyên định nghĩa provider, không cộng thêm nếu đây là tập con output. Không coi cached input là token ngoài tổng input, không suy ra API charges hoặc quota Plus còn lại từ các trường này. Workload mới, caching và số tool calls có thể thay đổi usage.

Hạn mức Codex, công chuẩn bị qualification và độ ổn định hạ tầng đều là ràng buộc. Lập effort log riêng cho spike, reference, oracle, browser/session fixtures, runner và debugging; ghi khi dùng LLM để tạo/sửa artifacts. Chấm lặp không gọi model nhưng vẫn tốn CPU, DB/browser runtime, lưu trữ và công chẩn đoán; không gọi là miễn phí.

### Cấu hình

- Dùng cấu hình development đã chọn: GPT-6 Luna (`gpt-6-luna`), High reasoning, Standard speed mặc định, cùng model/harness cho cả bốn cells.
- Cap 900 giây tính từ CLI invocation đến completion/timeout; giữ patch từng phần khi timeout. Smoke cũ chưa có token cap; đề xuất vòng pilot này tiếp tục wall-time cap và lưu token usage. Không mô tả là đã khống chế token budget. Main study phải chốt chính sách riêng.
- Dùng hạn mức Codex hiện có; không mua API hoặc credits. Nếu hết hạn mức thì ghi infrastructure interruption, giữ dữ liệu và tiếp tục theo allocation khi có thể. Không đổi model để chạy cho xong.
- Ghi CLI version, requested model, reasoning/speed, timestamps, image/dependency digests và metadata provider thực sự trả về. Không khẳng định model alias là snapshot weights bất biến.
- Kế thừa runner/container của smoke pilot làm nền, không gọi runner cũ để chạy task mới trực tiếp. Runner cũ đang gắn với history-filter; phải tổng quát hóa task manifest, repetition ID, browser evaluation và attempt policy trước.
- Chạy tuần tự, mỗi trial có workspace/DB/auth fixtures mới. Không tích lũy lời giải từ task trước, không dùng lịch sử hội thoại cũ.
- Quyền browser automation, nếu được qualification, được cung cấp tương đương trong cả bốn cells; final scorer tách riêng. V0 được tự kiểm tra bằng browser. Đây là đối chứng đúng cho câu hỏi về supplied package, dù có thể làm chênh lệch V nhỏ hơn. Không cắt công cụ của V0 để làm tăng tương phản. Tool/version và cách dùng browser phải có trong manifest trước invocation.
- Chưa bổ sung một bậc reasoning thấp hơn. Nếu sau qualification/pilot muốn khảo sát cấu hình đó, trước hết kiểm tra CLI/model thực sự hỗ trợ, tạo configuration/version riêng và cả bốn cells, chốt số lượt/budget trước khi chạy. Dữ liệu của nó không gộp với High và không tự làm cấu hình chính chỉ vì cho kết quả mixed.

## 3. Giai đoạn P0 — Kiểm tra baseline và tính khả thi

Trợ lý đọc lại snapshot thực giao agent, mapping của hai layout, schema và các auth APIs liên quan; đối chiếu với source anchors ở `main-task-candidates-v1.md`. Kiểm tra runtime để xác nhận UI còn thiếu theo task contract; phân biệt khả năng backend có sẵn với phần cần bổ sung.

Xác minh fixture/reset, truy cập admin/user/anonymous, session cache, browser runner và các command cơ bản. Source hiện có chưa khai báo Playwright hoặc browser automation dependency trong `package.json`; phải chọn và kiểm tra công cụ trình duyệt trước khi qualification các UI tasks. Nếu thêm test dependency, dùng cùng phiên bản/lockfile ở mọi cell và ghi đây là thay đổi hạ tầng chung. Browser engine và quyền dùng browser phải tương đương giữa các cells; hidden scorer luôn ở ngoài agent workspace.

Đối với DP-04, dùng nhiều sessions thật để xác định immediate next-request invalidation có thể đáp ứng mà không phải thay đổi baseline/auth behavior chung hay không. Nếu không, ghi task chưa đủ điều kiện và loại trước allocation; không âm thầm nới yêu cầu sau khi xem outcome.

Spike DP-04 chạy trước full oracle của DP-02/DP-03 và ghi giới hạn tối đa hai ngày làm việc như ở phần thứ tự. Đầu ra là luồng revoke tối thiểu tái tạo được, phiên current/other/foreign và kiểm tra request protected kế tiếp, ảnh hưởng cache, thay đổi cần thiết và quyết định feasible/pending/not-eligible. Không cam kết DP-04 là task khó nhất; đó là giả thuyết về workload, chưa có dữ liệu agent. Feasible spike chưa thay thế full qualification.

**Đầu ra:** baseline/environment manifest cập nhật, danh sách task eligible/pending và blocker có căn cứ. **Qua bước khi:** hai layout dùng chung nền đã ghi nhận, task khả thi hoặc có quyết định không đưa vào pilot. Chưa gọi model ở P0.

### Queue discovery trước allocation

[Registry](main-task-candidates-v1.md) và [CSV](main-task-candidates-v1.csv) là nguồn hiện hành về roles/shortlist. Rà cards/source A03 → B03 → U03; B04/U02/B01 reserve có overlap; DP-04/B02/U04 giữ hold. Queue U02 → B01 và mốc “hai eligible tasks” cũ không tự quyết định readiness.

Mỗi candidate ghi rationale, contract, qualification/V-gate, reuse và mô tả S trước outcomes. Bàn giao retained/pending/hold với coverage gaps, không đặt T tùy ý. Pilot cần qualify các task phục vụ câu hỏi feasibility cụ thể; main cần toàn bộ task được tuyển qualify và chốt precision/scope. Mọi rejection có lý do; không chọn theo condition thắng hoặc đổi fault model để V1 có lợi.

## 4. Giai đoạn P1 — Task cards và ma trận kiểm tra

Viết card riêng cho từng task đủ khả thi, gồm provenance `assistant-proposed constructed`, public requirements, starting-state hash, allowed changes, preservation, input policy, fixture rules và family. DP-02 ghi rõ gần họ lookup/filter đã dùng; đổi domain không biến nó thành bằng chứng độc lập về một loại vấn đề mới.

| Task | Acceptance tối thiểu | Preservation tối thiểu | Fault probes dự kiến |
|---|---|---|---|
| DP-02 | GET dropdown; URL/reload; All/User/Admin; invalid/repeated fallback; total sau lọc; empty result | Admin-only kể cả direct URL; per-user session counts và thứ tự; không đổi DB/không lộ tokens | Bỏ filter; hardcode role; total sai; bỏ requireAdmin; đếm sessions sai |
| DP-03 | Submit form thật; trim; 1/80 code points hợp lệ và 0/81 bị từ chối; tiếng Việt; same-session UI và reload | Chỉ đổi caller name; giữ email/role/verification/orders; anonymous bị từ chối; render an toàn | Chỉ client validation; tin payload user ID; lưu không cập nhật UI; ghi thêm field; đếm UTF-16 sai |
| DP-04 | Liệt kê own unexpired sessions; current marker; revoke other session; danh sách cập nhật; token bị revoke bị từ chối ở request tiếp theo | Current/foreign sessions còn hoạt động; không list/revoke foreign; không lộ token; không đổi user/order fields | Xóa record nhưng cookie còn dùng được; revoke nhầm current/foreign; list cả expired; render raw token |

Đây là nhóm yêu cầu, chưa phải số test đã có. Không đặt target 29 checks chỉ vì smoke cũ có 29. Payload tampering cần chấm qua endpoint/action/API mà lời giải thực sự dùng; không buộc agent tạo một endpoint hoặc đặt file theo gold implementation. Với DP-03, lệnh update gọi nhiều lần chỉ được đổi field được phép. Với DP-04, bảo đảm ca current/foreign có session thật và kiểm tra lại sau request, không mock phần invalidation cần đo.

Fixtures visible và hidden khác cấu trúc, không chỉ đổi tên/ID: phân bố roles/sessions, thứ tự ngày tạo, tên Unicode, users không có dữ liệu và các session states khác nhau. Fix thời gian hoặc đặt khoảng expiry có biên đủ xa để tránh flaky tests. Dùng fixture ngày tạo khác nhau khi contract chỉ quy định giảm dần mà chưa định nghĩa tie-break.

**Đầu ra:** task cards và requirement-to-check matrix có ID. **Qua bước khi:** mỗi assertion có public requirement; không có secret business rule hoặc đường dẫn lời giải bắt buộc. Chưa gọi model.

Trợ lý tự chuẩn bị toàn bộ quy tắc và ma trận thành hồ sơ dễ đọc để tác giả review tổng thể trước khi khóa evaluator; không phỏng vấn lần lượt từng business rule hoặc yêu cầu tác giả tự viết test. Mỗi hàng có requirement công khai, acceptance/preservation classification, assertion diễn giải bằng ngôn ngữ thường, fixtures, oracle source và giới hạn của phép đo. Tác giả có thể xác nhận toàn bộ hồ sơ và chỉ đánh dấu những chỗ chưa rõ/cần sửa; lưu nhận xét và bản matrix đã duyệt. Bước này chỉ xác nhận hợp đồng task khi hồ sơ đã review gồm rationale, toàn bộ public requirements, allowed changes, preservation, input/boundary policy và phiên bản task card; không chỉ một tập assertions con. Lưu task-card hash/version, matrix version, ngày và xác nhận, rồi cập nhật contract_status trong registry. Đây là bước đáp ứng yêu cầu author-confirmed contract ở decision log. Việc xác nhận mapping không chứng minh code assertion đúng và không được gọi là independent review.

Ghi provenance ai đề xuất task, ai viết/sửa reference, alternative, tests và ai kiểm tra; ghi hỗ trợ LLM ở mức thực tế thay vì mặc định tất cả artifacts cùng do một model viết. Methods/availability notes sau này mô tả việc dùng LLM và phần tác giả thực sự xác minh; không thay bằng một câu khai báo chung không có kiểm tra nội dung.

## 5. Giai đoạn P2 — Reference và qualification của bộ chấm

Cho mỗi task và mỗi layout:

1. Chạy baseline chưa giải: preservation phải pass, acceptance phải fail ít nhất một yêu cầu thực sự thiếu.
2. Tạo reference solution trên nhánh/snapshot riêng. Acceptance và preservation phải pass. Chứng minh thao tác UI bằng browser thật khi contract yêu cầu; dùng auth/DB thật cho quyền và persistence.
3. Tạo ít nhất một cách triển khai hợp lệ khác cấu trúc; bộ chấm vẫn chấp nhận. Khác biệt phải có ý nghĩa về cách xử lý, không chỉ đổi tên biến.
4. Tạo các lỗi hợp lý trong bảng P1. Từng lỗi phải bị assertion đúng phát hiện, không chỉ fail vì compile hoặc setup.
5. Chạy ba vòng ban đầu trên baseline, reference và valid alternative để xác nhận pattern pass/fail dự kiến. Sau đó chạy ít nhất 20 vòng đầy đủ của suite browser/session trên reference ở mỗi layout, reset sạch giữa vòng; valid alternative chạy lại cùng checks trọng yếu. Nâng lên 30 vòng trước freeze nếu có vấn đề timing/session cần xử lý. Mọi mismatch phải được điều tra; sau sửa giữ logs cũ và chạy lại validation trên version cuối, không bỏ các vòng lỗi khỏi denominator.
6. Chạy basic checks/build và kiểm tra fixture cleanup. Reference/gold patches không được tồn tại trong starting snapshot giao agent.
7. Khóa evaluator, visible package, fixtures, task requirements và reference hashes trước lượt agent đầu tiên.

### Cổng hợp lệ của can thiệp V: ma trận phát hiện

Đây là công việc trước model runs. Cho mỗi plausible fault probe trên reference, chạy basic V0, basic+visible V1 và final evaluator ở cả hai layouts. Ghi expected/observed outcomes cùng assertion IDs. Fault phải có quan hệ hợp lý với regression khi mở rộng task, không thêm một lỗi xa lạ chỉ để V1 thắng.

| Fault ID / hợp đồng / implementation version | Basic V0 bắt lỗi? | V1 bổ sung bắt lỗi? | Final acceptance/preservation nào bắt? | Loại phép đo / evidence |
|---|---|---|---|---|
| Điền sau khi dựng probe, chưa phải kết quả | Chưa đo | Chưa đo | Chưa đo | Log/fixture/check IDs |

Task chỉ được đưa vào workload factorial của pilot khi V1 có ít nhất một check chạy được trên baseline, gắn với hợp đồng preservation hợp lệ, và bắt một regression plausible mà basic V0 bỏ sót trên các bản probe. Giải pháp đúng/alternative phải qua V1 và final. Cổng này chứng minh cơ hội cung cấp feedback bổ sung, không chứng minh V1 sẽ tạo một hiệu ứng khác 0 khi agent dùng nó.

Cổng này định nghĩa một workload có điều kiện: các task có cơ hội phát hiện preservation regression bổ sung theo ma trận đã qualification. Cả ΔS và ΔV trong phép so sánh factorial dùng cùng tập eligible tasks. Không diễn giải ΔV là hiệu ứng trên mọi yêu cầu mở rộng SmartKit. Registry và Methods phải báo tất cả candidates, lý do không đủ điều kiện và endpoint scope; chỉ cập nhật manuscript sau khi chốt protocol, không gọi candidate bị loại là agent failure.

Đối với DP-03, phân biệt đường ghi đã tồn tại trong API với endpoint/UI mới. P0/P1 phải xác định V1 thực sự exercise được hành vi cũ nào bằng auth/DB thật. Không gọi check 1–80 code points là preservation nếu đó là yêu cầu mới mà baseline chưa đáp ứng. Security/input checks chỉ có thể exercise đường mới cần được đánh dấu đúng trong hidden acceptance/preservation matrix; không đưa yêu cầu mới vào V1 bằng cách âm thầm skip ở baseline chưa có feature. Nếu không có preservation contrast có căn cứ, task chưa đủ điều kiện cho factorial package study. Không âm thầm loại riêng task khỏi ΔV nhưng giữ trong ΔS; tập task chung hoặc các estimands khác phải được định nghĩa trước.

Nếu không đạt cổng, báo lý do và xem lại task/package/scope trước allocation, không dựng yêu cầu nghiệp vụ mới để hợp thức hóa contrast. Không được kết luận toán học rằng ΔV chắc chắn bằng 0 chỉ từ việc không bắt được các fault probes: package còn có thông tin và overhead, nhưng khi đó diễn giải hiệu ứng preservation-feedback chưa được chứng minh hợp lệ.

### Qualification riêng cho visible V1: feedback sai và thời gian chạy

Visible package được kiểm tra riêng với final scorer. Ở mỗi layout, chạy toàn bộ visible V1 ít nhất 20 vòng trên baseline chưa giải và 20 vòng trên reference, với reset/fixture cleanup như lúc agent gọi command. Ghi từng check, implementation, version, vòng chạy, expected/observed result và unexpected-result rate. Cả hai trạng thái đều phải pass; không thay bằng việc chỉ chấm final evaluator 20 lần. Khi có mismatch, chẩn đoán nguyên nhân, giữ logs cũ và lặp lại validation trên version cuối sau sửa; không cấp release chỉ nhờ bỏ các vòng fail.

Đo wall time của command visible từ khởi chạy tới exit, gồm fixture setup/reset/teardown mà agent thực sự trả trong budget; tách dependency/browser installation đã thực hiện ngoài model time. Ghi cold/warm runs, min/median/max và quantile mô tả, cùng tỷ lệ `suite_seconds/900`. Không coi quantile từ 20 vòng là một tail bound đáng tin cậy. Xác minh checks không làm hỏng task fixtures hoặc session state của agent sau khi chạy.

Đề xuất ngưỡng review kỹ thuật là một visible invocation vượt 90 giây, tức 10% cap 900 giây, trên baseline hoặc reference. Đây là ngưỡng quản lý budget để tác giả review, không phải ngưỡng hiệu ứng khoa học. Nếu vượt, chưa freeze package: kiểm tra chi phí setup, tối ưu mà giữ hợp đồng/check coverage rồi chạy lại qualification. Nếu vẫn vượt, phải quyết định và ghi trước model invocation việc giữ 900 giây với overhead được công bố, hay tăng cap đồng đều cho cả bốn cells và cập nhật tổng budget. Không tự gia hạn riêng V1 hoặc bỏ check khó chỉ để đạt runtime.

Flakiness của visible V1 có thể tạo feedback sai chỉ ở V1. Final evaluator dùng chung cũng không bảo đảm lỗi flaky phân bố đều theo condition nếu patches đi qua các đường mã khác nhau. Báo evidence cho từng suite; không giả định scorer error tự triệt tiêu khi so sánh.

### Mô tả cơ hội của tổ chức mã S, không dùng làm cổng loại

Từ hai reference patches được port theo cùng thay đổi logic và transformation manifest, ghi: số source files được sửa ở S0/S1; số parent directories chứa các files đó ở từng layout; số logical modules có relative path khác giữa hai layout; số changed framework-route files giữ nguyên vị trí. Loại test/scorer artifacts khỏi số source files hoặc báo riêng. Lưu định nghĩa path root, mapping IDs và patch hashes để tái tạo counts.

Với reference implementations khác tập module, báo rõ khác biệt implementation và counts riêng, không gán hết khác biệt cho layout. Dùng valid alternative như sensitivity mô tả khi có. Các trường trong registry để `not-measured` cho tới khi có reference và mapping; không điền 0 như thể đã đo.

Đây là biến mô tả, không phải tiêu chí loại task hoặc thước đo agent localization. Agent có thể đọc modules bị relocation mà không sửa chúng, nên zero relocated files trong reference không chứng minh ΔS bằng 0. Không ép agent sửa cùng file list của reference và không tự đặt threshold đủ phân kỳ khi chưa có căn cứ.

### Giới hạn của kiểm tra flakiness

Ghi số vòng dự kiến/thực tế và unexpected outcomes theo từng check, implementation và layout. Công thức phát hiện `1-(1-f)^k` giả định các vòng độc lập với flaky rate ổn định; cache/DB/timing tương quan có thể làm giả định này sai. Với f=5%, 20/30 vòng chỉ có khoảng 64,2%/78,5% cơ hội thấy ít nhất một fail. Zero failures không chứng minh flaky rate dưới 5%. Không gộp expected acceptance failures của baseline vào flaky errors. Chi phí các vòng scorer được báo riêng với model runs.

Đề xuất scoring timeout là 300 giây và startup readiness timeout là 180 giây cho mỗi attempt; qualification phải đo xem đủ không. Nếu cần đổi, chốt và ghi lại trước allocation, đồng đều giữa conditions của task. Thời gian setup/scoring được lưu riêng, không trộn vào agent wall time.

**Đầu ra:** qualification report/machine-readable results, reference/alternative/fault records và versioned inventories. **Qua bước khi:** mọi task giữ lại đạt đầy đủ các bước trên trên cả hai layout. Independent review hiện chưa có; báo đúng là self-check và assistant-assisted checking.

## 6. Giai đoạn P3 — Đóng gói, isolation audit và allocation

Tạo bốn package cho mỗi task từ starting snapshots chưa giải. Mỗi package có requirements giống nhau, basic tooling tương đương và layout instructions trung lập. V1 thêm visible preservation package tương ứng; hidden evaluator, gold, development notes và kết quả trước không được agent truy cập qua mounts, parent paths, repository history hoặc scripts.

Scorer chạy trên bản patch đã thu trong môi trường sạch. Agent sửa visible tests không đổi final criteria. Scorer dùng browser/DB phù hợp nhưng không gửi feedback về phiên agent. Kiểm tra archive không chứa credential values trước khi chuẩn bị public release.

File allocation đã được tạo để kiểm tra kỹ thuật, nhưng đang **held** và không phải author-release record. Sau task-frame review, nếu còn dùng allocation, phải xác định lại tập task, tính `N=4×sum R_t`, ghi seed `2026111102`, script/Python version và lịch xuất thực tế, rồi ghi author release nếu được duyệt. Randomize thứ tự bốn conditions trong mỗi task × repetition block; không thay thứ tự hoặc tập task theo outcomes.

Mỗi slot có ID dạng `DP02-R01-S0V0`, attempt ID riêng. Trong allocation cũ DP-02 có R01, DP-03 có R01–R03; chưa chốt số repetitions tiếp theo. Một thay đổi provider/model/harness phát hiện được tạo configuration/version mới; dừng để xem lại kế hoạch thay vì gộp âm thầm.

**Đầu ra:** package manifests, isolation report, allocation và protocol pilot đã khóa. **Qua bước khi:** có thể chỉ ra chính xác agent thấy gì, scorer thấy gì và slot nào sẽ chạy. Chưa gọi model.

## 7. Giai đoạn P4 — Chạy vòng đầu, rồi P5 — Hai vòng lặp bổ sung

### P4: repetition 1 nếu chọn lại phương án cũ

Chỉ bắt đầu sau khi task-frame gate, contract review, artifact verification và author-release record đều hợp lệ. Nếu còn DP-02 và DP-03, 8 phiên đầu là một development pilot có điều kiện; nếu task frame thay đổi thì allocation phải được tính lại trước invocation. Với mỗi slot: reset → readiness checks → agent trong 900 giây → thu patch/trace → chấm ở môi trường sạch → ghi outcome → cleanup.

Sau block đầu tiên, audit có đủ artifacts, fixture isolation và scorer behavior. Tiếp tục các block đã xếp nếu công cụ hoạt động. Một hoặc cả bốn agent fail vẫn là kết quả hợp lệ; không sửa prompt, cap, reference hay tests để làm chúng pass.

### P5: repetitions 2 và 3 của phương án cũ

Nếu chọn lại allocation cũ và không có lỗi instrument, các non-calibration tasks đã giữ chạy hai vòng còn lại; DP-02 không chạy thêm. Trong hai kịch bản chính, bổ sung 8 hoặc 16 phiên, tổng thành 16 hoặc 28; trường hợp queue dùng N đã tính và khóa trước invocation. Chạy tiếp không phụ thuộc condition nào đang thắng hoặc task nào đang cho kết quả đẹp.

Chưa áp dụng đề xuất dừng DP-03/DP-04 sau 4/4 pass/fail. Quy tắc đối xứng đó có thể dùng trong một pilot sàng lọc thích nghi nếu đặt trước, nhưng làm số lượt phụ thuộc outcome, cần đổi cách phân tích/report và chưa chứng minh bốn lượt có thông tin thấp. Bản đề xuất hiện tại tiết kiệm bằng vai trò task đã định trước. Nếu tác giả chọn adaptive screening, phải thay protocol/allocation/denominators trước bất kỳ model outcome mới nào; không gọi nó là main fixed-sample design.

Nếu P4/P5 phát hiện lỗi thực trong requirements/evaluator/runner: dừng các slot bị ảnh hưởng, lưu version cũ và nguyên nhân; không sửa tiếp giữa block rồi coi như cùng một thí nghiệm. Nếu lỗi chỉ nằm ở scorer, sửa version và chấm lại tất cả patch liên quan dưới cùng version, giữ cả scores cũ. Nếu prompt, starting state, visible package hoặc model exposure thay đổi, tạo pilot version khác và báo phạm vi chạy lại; không gộp dữ liệu hai versions. Không tự tăng tổng model budget của kế hoạch.

## 8. Chính sách lỗi, pause và replacement

| Trường hợp | Cách ghi và xử lý |
|---|---|
| Agent sai logic, không hoàn thành, tự bỏ cuộc, không dùng checks | Giữ patch; chấm như bình thường; không replacement |
| Agent chạm cap 900 giây trong môi trường đang hoạt động | Giữ patch từng phần; ghi timeout; chấm outcome có thể quan sát; không replacement |
| Patch của agent làm app/build hỏng | Joint failure theo contract; component không đo được ghi unassessable; không gọi là infrastructure để bỏ outcome |
| Setup lỗi trước model | Ghi setup-only attempt, logs và sửa readiness có version; chưa có agent outcome |
| Quota/auth/network/model-service interruption | Infrastructure interruption; outcome missing chờ adjudication, ghi mọi tài nguyên đã dùng; không tính như agent fail hoặc xóa attempt |
| Scorer/fixture hỏng không do patch | Giữ patch, phân loại evaluator error; chấm lại cùng patch sau sửa, không gọi model lại nếu không cần |
| Thiếu trace, patch hoặc provenance | Ghi incomplete record; kiểm tra trước khi đưa vào summary; không suy diễn dữ liệu thiếu |

Wall-time cap tính cả provider latency. Nếu CLI có telemetry tách model/tool/wait times, lưu theo định nghĩa thật của CLI; nếu thiếu thì để unavailable, không suy ra thời gian reasoning từ reasoning tokens hoặc lấy wall time trừ tổng tool times có thể chồng lấp. Chậm thông thường của provider trong môi trường hoạt động vẫn thuộc outcome dưới cap. Chỉ phân loại infrastructure interruption khi có bằng chứng service/transport/quota lỗi theo policy; không đổi nhãn timeout sau khi thấy patch fail. Ghi sensitivity/limitation cho các lần có độ trễ bất thường nhưng chưa đủ căn cứ adjudicate.

Replacement chỉ dùng sau adjudication có lý do, tối đa một lần/slot và sáu model attempts bổ sung toàn pilot. Lỗi hạ tầng hai lần liên tiếp thì dừng batch để chẩn đoán. Nếu hết replacement budget, giữ missing outcomes và báo pilot chưa hoàn tất; thay đổi giới hạn cần tác giả review. Không dừng pilot vì đã thấy đủ pass, không chạy thêm chỉ để tìm một outcome ngược lại.

## 9. Dữ liệu bắt buộc phải lưu

Mỗi record gồm task/family ID, condition, repetition, attempt/parent attempt ID, configuration version, starting snapshot/package/evaluator hashes, allocation position, ngày/batch, timestamps và termination reason.

Artifacts gồm prompt/instructions thực sự được tải, raw trace, patch, final source archive, setup/app/DB/scorer logs, browser evidence cho assertion liên quan, acceptance/preservation check results và machine-readable summary. Lưu wall time agent, setup time, scoring time, provider token events, check invocations và failure stage. Không tự quy đổi token thành tiền API hoặc hạn mức Plus còn lại.

Outcome gồm acceptance và preservation ở ba trạng thái pass/fail/unassessable; joint success cần cả hai pass. Agent-caused failures yield joint failure, kể cả component không thể đo. Infrastructure-only missing được giữ riêng. Báo denominators để không nhầm missing với fail hoặc âm thầm loại run không đẹp.

Đề xuất lưu một thư mục execution mới cho batch được duyệt, với protocol, allocation, manifests, qualification và runs/<task>/<repetition>/<condition>/<attempt>. Giữ nguyên thư mục smoke pilot cũ. Đây là cấu trúc dự kiến, chưa có artifacts mới được tạo theo kế hoạch.

## 10. Báo cáo pilot và tiêu chí hoàn tất

Báo cáo cần có:

1. Task nào qua/không qua qualification, lý do và phạm vi checks thực sự chạy.
2. Planned/started/completed/missing attempts theo task và cell; mọi replacement, timeout và exclusion có log.
3. Counts acceptance/preservation/joint success theo task × cell, kèm mẫu số; mọi raw outcomes giữ truy vết được.
4. Thời gian từng lượt, median/range mô tả theo task/cell, setup/scoring overhead và provider token usage. Với ba repeats, không coi phân bố quan sát là ổn định.
5. Visible check invocations và lỗi thường gặp có trace hỗ trợ. Không coi invocation là bằng chứng checks gây ra thành công; không gọi AI explanation là root cause đã xác nhận.
6. Instrument limitations, browser/session coverage và giới hạn do không có review độc lập.
7. Kế hoạch tiếp: main-task discovery/provenance, phạm vi tài nguyên khả thi, các kịch bản precision và lựa chọn exploratory nếu cần.

Pilot hoàn tất khi các task đã giữ đạt qualification, mọi slot có outcome hoặc missing/adjudication rõ ràng, archive đầy đủ và báo cáo mô tả tái tạo được từ records. Không yêu cầu agent phải pass một tỷ lệ cụ thể. Nếu thiếu coverage, scorer chưa ổn định hoặc tài nguyên không đủ, báo chưa sẵn sàng cho main study và chỉ rõ việc còn thiếu.

Không chạy significance test để chọn bên thắng từ pilot này. Precision planning sau pilot dùng nhiều kịch bản success rate, task heterogeneity và boundary cells; không lấy observed pilot difference làm effect size chắc chắn. Main tasks chưa bị dùng để tune instruments sẽ được tuyển và qualification riêng. Main configuration, sample, interval method, stopping/rerun policy và protocol phải chốt trước main outcomes.

Trong paper, pilot được mô tả ngắn ở Methods/feasibility hoặc phụ lục. Results chính dành cho main study. Bảng pilot của bản thảo làm việc hiện tại vẫn gắn nhãn development cho tới khi cập nhật bằng chứng chính.

### Quy tắc chẩn đoán và hành động khi gặp tín hiệu trần/sàn

Quy tắc dưới đây được ghi trước các model outcomes mới, không dùng để sàng lọc tự động theo tỷ lệ 20–80%.

**Hai loại lựa chọn khác nhau.** Có thể dùng thống kê calibration gộp/mù nhãn condition để đề xuất một workload hoặc configuration development mới: tỷ lệ pass gộp với trọng số bốn cells bằng nhau, phân bố runtime/timeout và resource feasibility, kèm rationale task/model cụ thể. Không dùng ΔS, ΔV, interaction, thứ hạng cells hoặc hướng chênh lệch để chọn task/configuration làm một bên thắng. Báo cáo phục vụ lựa chọn chỉ hiển thị summaries gộp; việc xem logs từng cell để chẩn đoán lỗi instrument được ghi riêng. Tính đối xứng không tự bảo đảm mọi suy luận sau selection đều không bias: giữ cả screening data, khai báo workload/configuration được chọn, tách fresh main runs và phạm vi estimand.

Mixed outcomes được phép là một tín hiệu về độ khó, không phải bằng chứng đủ rằng configuration đó thích hợp làm cấu hình chính hoặc đã có power. Khi mọi task bão hòa, bước tiếp theo là đánh giá feasibility, workload relevance, tool support và nguồn lực trên một phase development có protocol riêng. Không thay cấu hình giữa các cells và không chọn dựa trên contrast. Main configuration cuối cùng phải được khóa trước fresh main outcomes. Quy tắc này làm rõ câu trước đây về không chọn cấu hình chỉ vì mixed; không cấm mọi calibration dựa trên outcome gộp.

**Cách mô tả.** Với mỗi task, báo `k_sv/n_sv` của từng cell và cả số pass gộp trên bốn cells. Khi đủ số lượt cân bằng và không có missing, tỷ lệ gộp là trung bình mô tả của bốn điều kiện; nó không đại diện riêng cho S0V0 hoặc một xác suất chung bất biến. Khi thiếu outcome, báo cả planned/observed denominators, không để cell có nhiều dữ liệu hơn âm thầm có trọng số lớn hơn. Không dùng khoảng tin cậy nhị thức exact trên tổng gộp như thể mọi lượt có cùng xác suất pass. Suy luận cần giữ cấu trúc task, condition, batch và các giả định phụ thuộc.

**Nhãn quan sát.** Trong report development, chia task thành `observed-all-pass`, `observed-all-fail`, `mixed`, hoặc `incomplete`. Hai nhãn đầu chỉ dùng khi có đủ mọi slot đã lên kế hoạch: DP-02 có 4, DP-03/DP-04 có 12. Ghi rõ cỡ mẫu cạnh nhãn; 4/4 không có cùng mức thông tin với 12/12. Missing infrastructure/evaluator outcomes không được thay bằng fail. Vòng đầu của task có R=3 chỉ là cờ tạm thời. Nhãn mô tả kết quả quan sát, không khẳng định true probability bằng 0 hoặc 1. Giữ bảng từng cell để không che một chênh lệch điều kiện bằng tỷ lệ gộp.

| Tình huống | Hành động đã định trước |
|---|---|
| Vòng đầu cùng pass hoặc cùng fail | Gắn cờ, kiểm tra lỗi instrument dựa trên bằng chứng; DP-02 hoàn tất R=1, DP-03/DP-04 tiếp tục R=3 nếu công cụ đúng; không tự đổi lượt theo outcome |
| Task observed-all-pass sau đủ lượt | Giữ trong report development như nhóm quan sát bão hòa phía trên; không loại, sửa cho khó hơn hoặc chuyển vào main chỉ vì kết quả này |
| Task observed-all-fail sau đủ lượt | Giữ trong report development; đối chiếu reference/runtime/trace để phân biệt yêu cầu khả thi với thất bại agent. Nếu công cụ đúng, giữ failures; nếu có bug thật, áp dụng chính sách version ở P4/P5 |
| Một số task mixed, một số bão hòa | Báo riêng các nhóm và toàn bộ cells; không chỉ chọn nhóm mixed để trình bày, không kết luận pilot đã đủ power |
| Mọi task eligible đều cùng phía all-pass hoặc all-fail | Chưa khóa main study chỉ dựa trên pool/configuration này. Mở bước discovery/qualification workload đa dạng hơn hoặc đề xuất cấu hình khác với rationale cụ thể; protocol, budget và dữ liệu cấu hình mới được tách riêng để tác giả review |
| Thiếu outcome hoặc qualification không ổn định | Báo incomplete; xử lý missing/instrument trước khi dùng pilot cho quyết định main readiness |

Việc thay model, cap hoặc task contract không được thực hiện giữa các cells như phản ứng với pass/fail. Thay đổi sau pilot là một bước development mới có ngày, lý do và version; kết quả cũ vẫn được giữ. Không cố thêm consumer hoặc kéo dài yêu cầu chỉ để làm một layout thất bại. Task mới cần rationale sử dụng và contract độc lập với condition nào thắng.

Các nhóm quan sát trên là phân nhóm mô tả của pilot report, không phải strata đã được chứng minh cho main population. Task đã dùng để sửa công cụ vẫn là development-only; pilot outcomes của mọi task luôn tách khỏi main. DP-03/DP-04 chỉ có thể dùng cùng task cho fresh main runs theo quy tắc giữ quyền chọn ở §12. Nếu sau này muốn main study có các tầng độ khó, phải định nghĩa cách phân tầng, cách tuyển task, trọng số/estimand và nguồn screening riêng trước collection; không tái dùng labels hoặc pilot outcomes làm bằng chứng chính.

Nhiều task hơn giúp khảo sát khác biệt workload nhưng không tự tạo tính đại diện. Với task pool constructed/convenience, giả định suy rộng và task-family overlap vẫn phải được ghi rõ. Các kịch bản precision cho tập task cố định và cho một population tasks giả định được báo riêng; không tuyên bố pilot nhỏ đã ước lượng được population variance.

## 11. Phân công và thứ tự bàn giao để review

| Mốc | Trợ lý thực hiện | Tác giả review |
|---|---|---|
| Định hướng sau grilling | Đã ghi mục tiêu, ưu tiên tác vụ, hai tác động chính và phân công | Tác giả xác nhận ngày 12/11/2026; chi tiết task và protocol thực thi vẫn chờ hồ sơ cụ thể |
| Chuẩn bị pilot | Rà khung tác vụ, cards, qualification và câu hỏi feasibility | Shortlist, role và lý do số lượt; không mặc định R=1/3 |
| Trước model invocation | P0–P3, task cards, reference, qualification, packages và protocol cụ thể | Requirement-to-check matrix, eligibility, thay đổi đáng kể và tổng số lượt thực tế |
| Sau pilot | P4–P5 và báo cáo có provenance trong phạm vi kế hoạch đã duyệt | Ý nghĩa/giới hạn kết quả và phương án main study |
| Trước main study | Soạn protocol và precision/resource scenarios riêng | Scope, cấu hình, sample, stopping rules và mức kết luận |

Tác giả không cần chọn từng file sửa, tự viết test hoặc duyệt từng shell command. Việc review tập trung vào task frame, quyết định nghiên cứu và nguồn lực. Trong lượt soạn kế hoạch này chưa chạy agent mới, chưa sửa ứng dụng, chưa tiêu hạn mức model cho expanded pilot, và chưa khóa main protocol. Allocation tiếp theo cần lý do gắn với khung tác vụ và mục tiêu pilot. Workload hẹp phải được báo đúng giới hạn; không tự cấm một feasibility pilot đã có mục tiêu cụ thể. Nếu task được chọn chưa qualify, artifact/runtime chưa hợp lệ hoặc chưa có release thì chưa gọi model.

## 12. Quyền chọn dùng lại task và các lựa chọn phạm vi còn mở

### Có dùng lại task đã xuất hiện trong pilot cho main không?

Hướng đã ghi nhận từ phản hồi tác giả là giữ khả năng dùng lại DP-03; DP-04 có điều kiện vượt spike mà không đổi repaired baseline hiện tại. Đây là quyền chọn trước pilot, không phải task đã đủ chuẩn. Registry ghi `reuse-option-retained-pending-freeze` cho DP-03 và `reuse-option-conditional-unchanged-baseline-spike` cho DP-04. Không gán hồi tố evaluation-ready sau khi xem outcome.

Để chuyển một task từ quyền chọn sang `evaluation-ready`, hoàn tất trước lượt agent đầu tiên:

1. Tác giả xác nhận phiên bản task card và toàn bộ requirement-to-check matrix, gồm rationale, new behavior, preservation, allowed changes và input/edge policies. Lưu ngày/version/hash. Giữ quyền chọn chưa thay thế bước xác nhận hợp đồng.
2. Qua qualification baseline/reference/alternative/fault probes ở cả hai layouts; V-gate matrix hợp lệ; visible V1 ổn định và runtime đã review; S-reference metrics đã đo và ghi, không đặt ngưỡng S mới để loại task.
3. Khóa public spec, starting-state hashes, visible package, final evaluator, fixtures, reference hashes và execution cap của task; ghi manifest và version. Main task-discovery/analysis chưa được coi đã freeze chỉ vì task này đạt readiness.
4. Lưu quy tắc tuyển dưới đây và lịch sử exposure trước pilot. Nhãn task được chốt trước mọi agent outcomes mới.
5. DP-04 hoàn tất spike với baseline hiện tại. Nếu cần thay hành vi cache/auth nền, task không đủ điều kiện dùng lại theo quyền chọn này. Không sửa nền rồi giữ nguyên nhãn; muốn study release mới phải đề xuất riêng, đồng bộ cả hai layouts, requalification và review scope trước các trials của release đó.

**Quy tắc tuyển đặt trước:** mọi task được gán evaluation-ready trước pilot, hoàn tất pilot với các settings/instruments đã khóa và không cần substantive revision, được đưa vào eligible main pool bất kể pass/fail/time của pilot. Không loại task vì all-pass, all-fail, agent timeout hợp lệ hoặc contrast nhỏ/trái kỳ vọng. Mọi inclusion và exclusion có lý do và nguồn evidence. Nếu một lựa chọn về toàn bộ configuration/main scope khiến các task này không còn tương thích, báo thay đổi estimand/configuration và không lặng lẽ chỉ bỏ task bất lợi.

**Sau pilot exposure:** sửa substantive spec, starting snapshot, visible/final suites, fixture contract hoặc cap khiến task/version đó thành development-only. Giữ raw records và versions trước/sau; không đổi tên task để né lịch sử tuning. Sửa môi trường/evaluator error cũng phải qua version policy và review tác động; không tự coi nhãn ready còn nguyên khi measurement thay đổi. Pilot records tuyệt đối không trộn vào main dataset; main dùng fresh sessions, allocation và archive riêng sau main-protocol freeze.

**Calibration và prior exposure:** quyết định về configuration/cap sau pilot chỉ dùng summaries gộp mù condition theo §10 và rationale/resource constraints, không dùng ΔS/ΔV hay direction. Một cap mới vẫn làm mất khả năng dùng lại theo settings đã freeze của task; không dùng aggregate blinding làm ngoại lệ để giữ nhãn. Khai báo các traces/outcomes đã xem và vai trò LLM/author; main evidence là fresh runs trên task đã công bố, không phải chuyển sang task chưa từng thấy.

History-filter đã dùng để tune instruments và DP-02 dùng để generalize runner/browser tiếp tục development-only. Không dựa vào DP-03/DP-04 sống sót để hứa đủ T cho main: task discovery, budget và precision scenarios phải có phương án không dùng cả hai. Nếu chúng đạt đủ điều kiện thì cập nhật main registry trước main collection theo quy tắc đã đặt, không cộng pilot outcomes.

Hai task có primary functional families khác nhau: DP-03 là `profile-update`, DP-04 là `session-lifecycle`; cả hai có `shared_surface_group=settings` và phụ thuộc auth/session chung. Ghi grouping trước outcomes, không coi hai ID là bằng chứng độc lập về hai bối cảnh ứng dụng. Family/surface sensitivity chỉ thực hiện nếu dữ liệu và assumptions cho phép; với pilot hai/ba task chủ yếu báo mô tả, không fit variance component rồi suy rộng.

### Có thêm repository thứ hai không?

Chưa thêm. Phạm vi đã được tác giả đồng ý là một controlled SmartKit case study. Inventory sáu candidates ban đầu không phải giới hạn số task có thể discovery trong ứng dụng, nhưng chưa có bằng chứng đủ để hứa sẽ qualify được tám hay mười task khác nhau. Trước khi đầu tư thêm repository, lập task registry nêu new behavior, domain/family, rationale, dependencies và trạng thái qualification; kiểm tra có đủ workload trong scope hiện tại không.

Nếu workload SmartKit không đủ, báo rõ các lựa chọn: thu hẹp thành case study khám phá, mở thêm discovery, hoặc một replication repository có môi trường và preservation contracts riêng. Repository thứ hai tăng bề rộng bối cảnh nhưng không tự giải quyết task selection bias hoặc thiếu precision. Nó cần task frame, baseline, evaluator, budget và quyết định scope mới.

### Q15 và Registered Reports

Hiện giữ Q15: ưu tiên nghiên cứu hoàn chỉnh, chọn venue theo bằng chứng; không tự chuyển sang Registered Report. Nếu tác giả muốn hình thức này thì cần mở lại thời điểm chọn venue trước nghiên cứu chính và kiểm tra quy định nơi nộp. Cần phân biệt pilot với main collection: hướng dẫn [Registered Reports của COS](https://www.cos.io/initiatives/registered-reports) cho phép trình bày pilot results ở Stage 1; approval/IPA phải đi trước thí nghiệm chính theo protocol được duyệt. Vì vậy đã có development pilot không tự loại trừ Registered Reports, và không nên diễn đạt rằng mọi dữ liệu đều phải thu sau IPA. Chưa chọn track hoặc venue cụ thể trong plan này.

### Ngữ cảnh các mã Q và nguồn quyết định

Q16 là mã câu hỏi trong cuộc trao đổi giữa tác giả và trợ lý, không phải số mục của PDF hoặc một nguồn khoa học. Các xác nhận Q14–Q18 được ghi ở [author-decisions-2026-11-11.md](author-decisions-2026-11-11.md). Reviewers chỉ có PDF không thể tự xác minh những phiên trao đổi đó; khi gửi hồ sơ review, cung cấp decision log và phiên bản plan liên quan, phân biệt confirmed decisions với đề xuất chưa duyệt. Không trình bày lựa chọn mới trong bản plan này như thể tác giả đã xác nhận.

</details>

</details>
