# Kế hoạch thí nghiệm

## Quyết định ngày 19/11/2026

Giữ thiết kế hai kit. [Next.js SaaS Starter](https://github.com/nextjs/saas-starter) giữ vị trí đã có trong thiết kế và [Makerkit Lite](https://github.com/makerkit/nextjs-saas-starter-kit-lite) thay SmartKit. Cả hai kit đều do bên ngoài phát triển. Phạm vi suy luận giới hạn ở hai kit và các tác vụ được chọn có chủ đích.

Makerkit Lite là bản công khai theo giấy phép MIT, dùng Next.js App Router, TypeScript và Supabase trên PostgreSQL. Mã nguồn cho thấy biểu mẫu đăng ký kiểm tra ngưỡng 8 ký tự ở tầng ứng dụng, ô mật khẩu khi đăng nhập mặc định được che và menu tài khoản gọi thao tác đăng xuất trực tiếp. Cấu hình Supabase có xác nhận email và hộp thư thử cục bộ. Đây là căn cứ chọn Makerkit Lite để kiểm chứng cùng ba tác vụ tài khoản. Supabase phụ trách xác thực nên cần kiểm tra ngưỡng thực tế phía máy chủ, luồng email, phiên và reset trước khi kết luận ba tác vụ đủ điều kiện. [README](https://github.com/makerkit/nextjs-saas-starter-kit-lite/blob/9ff430df9c58516add0136bd01ed800ce551675e/README.md), [quy tắc mật khẩu](https://github.com/makerkit/nextjs-saas-starter-kit-lite/blob/9ff430df9c58516add0136bd01ed800ce551675e/packages/features/auth/src/schemas/password.schema.ts), [form đăng nhập](https://github.com/makerkit/nextjs-saas-starter-kit-lite/blob/9ff430df9c58516add0136bd01ed800ce551675e/packages/features/auth/src/components/password-sign-in-form.tsx), [luồng đăng xuất](https://github.com/makerkit/nextjs-saas-starter-kit-lite/blob/9ff430df9c58516add0136bd01ed800ce551675e/apps/web/components/personal-account-dropdown-container.tsx), [cấu hình Supabase](https://github.com/makerkit/nextjs-saas-starter-kit-lite/blob/9ff430df9c58516add0136bd01ed800ce551675e/apps/web/supabase/config.toml).

BoxyHQ đã có nút hiện/ẩn mật khẩu trên form đăng nhập. OpenStarterKit đã có hộp thoại xác nhận đăng xuất. Hai điểm xuất phát này làm giảm khả năng dùng cùng ba đặc tả hiện có. [Form đăng nhập BoxyHQ](https://github.com/boxyhq/saas-starter-kit/blob/abc9b686823cbfb4973c79bc36fea37a3244be6c/pages/auth/login.tsx), [hộp thoại OpenStarterKit](https://github.com/openstarterkit/nextjs-saas-starter-kit/blob/0a6534eb9b510c9c91b956165ec18ccd248c0055/src/components/dashboard/sign-out-dialog.tsx).

Ba [tác vụ hiện hành](execution/replacement-qualification-2026-11-19/task-cards.md) là chuẩn hóa tên hiển thị khi lưu, xác nhận đăng xuất và bật/tắt hiển thị mật khẩu khi đăng nhập. Tác giả đồng ý thay tác vụ đăng ký trước khi thu thập dữ liệu. Trong Supabase cục bộ, cấu hình ngưỡng mới chặn đăng ký bằng mật khẩu 11 ký tự đồng thời chặn đổi sang mật khẩu 11 ký tự, vốn được chấp nhận với cấu hình gốc. [Dữ liệu kiểm tra quy tắc mật khẩu](execution/replacement-qualification-2026-11-19/makerkit-password-policy.json).

**Đã đạt kiểm chứng kỹ thuật.** Cả hai kit đạt ma trận 72 ca, hai lượt diễn tập chấm lại và kiểm tra nội dung 24 cấu hình gói. Lịch ứng viên gồm 48 phiên với hai kit, ba tác vụ mỗi kit, bốn điều kiện và hai lần lặp. Thu thập dữ liệu chưa bắt đầu. [Báo cáo kiểm chứng](execution/replacement-qualification-2026-11-19/README.md), [lịch 48 phiên](execution/replacement-qualification-2026-11-19/allocation-candidate.json).

<details>
<summary>Hồ sơ chuẩn bị main48 trên SmartKit trước khi đổi starter kit</summary>

## Kế hoạch SmartKit cho 48 phiên

C?p nh?t 16/11/2026. B? ki?m ch?ng k? thu?t ?? ho?n t?t: **24 packages, 48 tr??ng h?p qualification v? 24 di?n t?p capture/reset/score ??u ??t**. Kh?ng c? phi?n model th?c nghi?m m?i; ch?a c? k?t qu? so s?nh S/V. **Technical freeze ?? ho?n t?t v? audit sau freeze ?? ??t.** H? s? t?i [readiness](execution/main48/readiness.json) v? [manifest](execution/main48/freeze.json).

| Task | Y?u c?u | Slots |
|---|---|---:|
| A01 | S?a t?n hi?n th? c?a ch?nh t?i kho?n | 8 |
| A04 | Ch?nh s?ch m?t kh?u ??ng k?/reset, gi? ??ng nh?p c? | 8 |
| B05 | Nh?n di?n m? thanh to?n, gi? n?i dung checkout chu?n | 8 |
| B06 | H?t h?n t?i th?i ?i?m ho?n t?t thanh to?n | 8 |
| U02 | Admin xem chi ti?t t?i kho?n | 8 |
| U03 | Admin ??i role v?i quy?n ghi hi?n h?nh | 8 |
| T?ng | 6 task ? 4 ?i?u ki?n ? 2 l?n | **48** |

H?p ??ng ??y ?? n?m trong [task cards](execution/main48/task-cards.json); [protocol](execution/main48/protocol.md) l? t?i li?u th?c thi hi?n h?nh. M?i task b?t ??u t? snapshot ri?ng, kh?ng ph? thu?c l?i gi?i task kh?c. C?c task l? use case nghi?n c?u ???c x?y d?ng, ch?a ph?i nhu c?u production ?? x?c minh.

C?c c?ng ?? ki?m ch?ng:

- **G1:** ??i chi?u c? 24 packages v? source hai layout; ba task A04/B05/B06 thay quy t?c ?ang d?ng trong shared modules. A01/U02/U03 c? th? c? m?c ti?p x?c v?i layout y?u h?n; gi? c? s?u task v? ph?n t?ch sensitivity ?? ??nh.
- **G2:** m?i fault/layout qua c? n?m l?nh V0 nh?ng b? ??ng ki?m tra preservation c?a V1 v? hidden b?t; baseline v? hai c?ch tri?n khai h?p l? ??t tr?n c? hai layout. Hai task admin d?ng chung m?t m?u fault, kh?ng ph?i hai lo?i l?i ??c l?p.
- **G3:** ?? reliability 20 l??t (A01: 30), alternative ba l??t, baseline hidden ba l??t; 24 di?n t?p l?u patch v? ch?m trong m?i tr??ng s?ch ??t. C?c l?n l?i c?ng c? v? ch?nh runtime ???c gi? trong h? s?.
- **G4:** ph?m vi ??ng g?p l? so s?nh factorial th?m d? v? audit b?o to?n tr?n s?u task SmartKit c? ??nh. Kh?ng suy ra khuy?n ngh? chung cho starter kits, kh?ng b?o ??m ph?t hi?n hi?u ?ng nh? ho?c c?ng b?. Ch?a c? reviewer ??c l?p; self-review c?ng c? ???c ghi r?.

Khi b?t ??u collection, d?ng m?t l?ch [allocation](execution/main48/allocation.json), GPT-6 Luna High/Standard, CLI ?? ghim, 900 gi?y/slot. Kh?ng pilot m?i, kh?ng ch?y b?, kh?ng thay task theo k?t qu?. Runner ki?m tra freeze v? quota tr??c m?i slot ch?a ch?y; khi h?t quota ch? ti?p t?c c?c slot ch?a ???c g?i sau khi ngu?n l?c h?i ph?c. Kh?ng th? b?o ??m tr??c quota ?? cho c? 48 l?i g?i. Snapshot t?i kho?n m?i nh?t ???c l?u ? [model preflight](execution/main48/model-preflight.json).

Technical freeze kh?ng t? kh?i ch?y collection. `collect.py run` c?n y?u c?u start release g?n ??ng freeze; vi?c chu?n b? n?y ch?a t?o release. Sau collection m?i t?ng h?p counts, contrasts, missing bounds, sensitivity v? chi ph? r?i vi?t main Results. Manuscript prospective ?? ??ng b? v? PDF bi?n d?ch s?ch; k?t qu? development c? ???c gi? nh?n ri?ng.

</details>

<details>
<summary>Previous hold plan, superseded roster</summary>

# Kế hoạch paper SmartKit

Cập nhật 15/11/2026 sau kiểm chứng không model. **Model collection đang hold.** Chưa chạy 48 phiên.

Kiểm chứng đã xác nhận sáu task có reference và alternative chạy được trên hai layouts, cùng 12 fault/layout probes bị bắt. Nó chưa xác nhận giá trị của phép so sánh S/V: cả 12 cặp task–implementation đều sửa 0 module cũ đã relocation, và các fault chính là lỗi feature mới. Vì vậy, khả thi kỹ thuật đã qua nhưng research-value gate chưa qua.

Phương án 48 runs vẫn được giữ làm allocation dự phòng: **6 task × 4 điều kiện × 2 lần = 48**. Không thêm runs. Chỉ release sau bốn cổng G1–G4.

## Bốn cổng trước khi chạy

| Cổng | Phải chứng minh | Bằng chứng cần lưu | Trạng thái |
|---|---|---|---|
| G1. Treatment reach | Task thực sự tiếp xúc với khác biệt về tổ chức mã hoặc đường tìm/tái sử dụng module | Ma trận public operation → route → logical modules → old obligations; reference/alternative trên cả hai layouts; phân loại route giữ nguyên, module mới và module relocation được đọc | **Chưa đạt** |
| G2. Preservation gate | V1 bắt được regression của hành vi cũ mà V0 bỏ sót | Baseline/reference/alternative/fault matrix trên hai layouts; fault thuộc old/shared behavior, không chỉ feature mới; reliability logs | **Chưa đạt** |
| G3. Task validity | Requirement và oracle kiểm tra đúng browser/API/DB transport, quyền, state và edge cases | Task cards, fixtures/reset, actual transport probes, valid alternative, hidden mapping, missingness policy | **Một phần đạt** |
| G4. Research value | Sau nghiên cứu, người dùng biết thêm điều gì hữu ích trong phạm vi SmartKit và cấu hình agent này | Contribution statement đối chiếu prior work, estimand, null/adverse interpretation, cost/effort boundary và scope | **Chưa đạt** |

G1 không yêu cầu agent phải sửa một số file định trước. Nếu workload vẫn chỉ thêm route/UI ở các đường giữ nguyên và không cho thấy organization exposure có ý nghĩa, phải thu hẹp claim S hoặc dừng thiết kế 2×2. Không tạo độ khó nhân tạo để cứu G1.

G2 không được dùng fault acceptance mới làm preservation evidence. Nếu V1 chỉ kiểm tra hành vi cũ nhưng không có fault hợp lý mà V0 bỏ sót, không được gọi package có tác dụng preservation.

## Task và runs dự phòng

| Mã | Task | Runs nếu G1–G4 đạt |
|---|---|---:|
| MT-A01 / DP-03 | Sửa tên hiển thị | 8 |
| MT-A03 | Đổi mật khẩu | 8 |
| MT-B03 | Tiếp tục đơn pending | 8 |
| MT-B04 | Tải biên nhận JSON | 8 |
| MT-U02 | Admin xem chi tiết tài khoản | 8 |
| MT-U03 | Admin đổi vai trò tài khoản | 8 |
| **Tổng** | **6 × 4 × 2** | **48** |

U03 thay B01 để bổ sung thao tác ghi có phân quyền. U03 đã có feasibility pass giới hạn, nhưng full qualification vẫn thiếu. B01 không phải fallback tự động. DP-02 development-only, DP-04 hold, task history có 4 runs cũ và không tính vào 48.

## Thứ tự tiếp theo

1. Hoàn thiện G1 map cho sáu task. Ghi rõ task nào thật sự buộc agent đọc hoặc gọi qua module mà hai layouts đặt khác nhau.
2. Hoàn thiện G2 cho từng task bằng old/shared behavior. Giữ acceptance và preservation riêng.
3. Hoàn thiện G3, gồm U03 cache/session contract, B03 expiry/concurrency scope và actual browser/API/DB transports.
4. Viết G4 contribution statement: câu hỏi, quyết định thực tế, tri thức bổ sung so với FeatBench/Precedent/SchrödingerRepo/TDAD/FeatureLoop/Code Cleanliness, và cách diễn giải null.
5. Review một bộ hồ sơ sáu task, 24 packages, 48 slots, codebook, missingness và resource cap. Chỉ sau review mới tạo author-release record.

Nếu bất kỳ cổng nào không đạt, không gọi model để “xem thử”. Dừng, thu hẹp estimand hoặc chuyển thành báo cáo feasibility/instrumentation. Không tăng runs và không chọn task theo outcome agent.

Bằng chứng kiểm chứng: [report](execution/task-feasibility-2026-11-15/report.md), [summary](execution/task-feasibility-2026-11-15/summary.json), [source evidence](execution/task-feasibility-2026-11-15/source-evidence.json), [value assessment](execution/research-direction-review/assessment.md), [primary-source review](paper-proposal/citation-evidence.md#pre-run-research-value-verification--15-november-2026).

</details>

<details>
<summary>Hồ sơ kế hoạch cũ: mở khi cần đối chiếu</summary>

Hồ sơ dưới đây giữ nguyên nội dung trước lần viết lại ngày 15/11/2026. Trạng thái, số lượt và thứ tự công việc trong hồ sơ chỉ mô tả phương án cũ. Phần hiện hành ở trên quyết định đề xuất mới.

# Kế hoạch hoàn thành paper SmartKit

**Cập nhật 14/11/2026:** giữ hai yếu tố S/V và phạm vi SmartKit. Thứ tự hiện hành là [khung tác vụ và registry](execution/main-task-candidates-v1.md) → rà source/cards và qualification của shortlist → pilot có mục tiêu nếu còn câu hỏi feasibility → hoàn thiện qualification toàn main cùng precision/resources → protocol → fresh main runs. [Plan chi tiết](execution/pilot-task-plan-v2.md) ghi sản phẩm và điều kiện chuyển bước.

DP-02/03 có qualification kỹ thuật đã lưu; DP-02 development-only, DP-03 giữ quyền chọn reuse theo policy đã đặt. Allocation 16 phiên tạm chưa triển khai; số lượt tiếp theo chưa chốt. Registry có 11 candidates, chưa có main task admitted. Các T=8–10 trong mô phỏng không phải task count thực tế. Pilot chỉ cần các task được chạy qua qualification, không cần đợi toàn bộ main set; mọi task main phải qualify trước main collection. DP-04 tiếp tục hold.

Đối chiếu file trong lượt chỉnh plan phát hiện `local-runtime.py` khác freeze manifest. Cần kiểm tra nguyên nhân/ảnh hưởng trước dùng runner; artifacts kỹ thuật giữ nguyên, chưa có model invocation mới.

Bản thảo hiện hành đã bổ sung Related Work và contribution có điều kiện; xem
[bảng đối chiếu](paper-proposal/citation-evidence.md). Script
[precision/power](execution/simulate-precision-power.py) và
[kịch bản đã chạy](execution/precision-power-scenarios.json) tách finite-task khỏi
hypothetical-task-population uncertainty, có Holm/global và partial nulls, cùng mốc
10pp chưa khóa. Các bằng chứng kỹ thuật là hồ sơ trước đây; lượt này sửa plan, registry và tracker, chưa qualification mới.

Ngày lập: 10/11/2026. Trạng thái: kế hoạch thực hiện, chưa chạy thí nghiệm chính. Tài liệu này hướng dẫn công việc; không phải phần nội dung sẽ đưa nguyên văn vào paper.

Mục tiêu là hoàn thành một nghiên cứu có thể kiểm tra và tái lập về ảnh hưởng của tổ chức repository và bộ kiểm chứng hành vi tới khả năng coding agent mở rộng SmartKit. Sản phẩm cuối gồm manuscript tiếng Anh bằng LaTeX, dữ liệu và artifact hỗ trợ, cùng báo cáo giới hạn nghiên cứu. Không đặt mục tiêu SmartKit phải thắng hoặc paper chắc chắn được nhận.

## 1. Xuất phát điểm và phạm vi

| Đã có bằng chứng | Còn phải hoàn thiện |
|---|---|
| Baseline đã sửa và hai layout qua các checks cục bộ | Phạm vi task chính, contracts và qualification từng task mới |
| History-filter smoke pilot bốn phiên; DP-02/03 qualification không model | Expanded pilot với mục tiêu cụ thể nếu cần; số lượt chưa release |
| Registry 11 candidates; 288 precision scenarios giả định | Shortlist khả thi, precision criterion và main sample size |
| Manuscript/proposal, nguồn và hồ sơ review | Prior-artifact audit còn thiếu, main data và kết luận phù hợp |

[Tracker 34 đầu việc](paper-completion-tracker.csv) ghi trạng thái cùng evidence. `done` chỉ xác nhận sản phẩm trong scope của hàng, không chứng minh main-ready hoặc runtime còn khớp freeze. P15 theo dõi runtime discrepancy. P19 ghi `unavailable` vì chưa có reviewer độc lập; trước freeze ghi giới hạn và phạm vi self-check, không giả là đã review. Tương ứng thesis cũ chưa được xác minh; dùng provenance repaired baseline đã ghi và khai báo giới hạn.

Phạm vi là controlled SmartKit case study với S (theo tầng/theo tính năng), V (basic/basic + preservation checks), joint success gồm acceptance và preservation. Hai effects dùng cùng tập task qua V-gate; không suy rộng thành mọi starter kit. Mỗi phiên bắt đầu sạch; không tích lũy lời giải qua tasks.

## 2. Thứ tự thực hiện và điểm kiểm tra

| Giai đoạn | Phụ thuộc | Sản phẩm để kiểm tra | Tiêu chí chuyển bước |
|---|---|---|---|
| G0. Chốt câu hỏi và đóng góp | Tài liệu hiện tại | Scope một trang; ma trận prior work | Có câu hỏi cụ thể và cách định vị trung thực |
| G1. Dựng baseline | G0 có phạm vi tạm thời | Environment manifest; baseline report | Build/runtime và hợp đồng nền kiểm tra được |
| G2. Làm một tác vụ xuyên suốt | G1 | Task card; evaluator; reference patches | Chứng minh tác vụ và bộ chấm có thể hoạt động |
| G3. Hoàn thiện bốn điều kiện | G1–G2 | Layout variants; treatment manifest | Điều kiện chỉ khác các can thiệp đã khai báo |
| G4. Xây tập tác vụ | G2–G3 | Khung tác vụ; shortlist; inclusion log | Tasks pilot qualify trước pilot; toàn main set hoàn thiện trước G6 |
| G5. Pilot và lập kế hoạch độ chính xác | G3; khung G4; tasks pilot đã qualify | Mục tiêu/decision table; pilot report nếu chạy; precision/resources | Không đổi lượt theo hướng outcomes; chốt sample từ task frame thực |
| G6. Khóa protocol | G0–G5 | Protocol v1 có ngày; cấu hình đã khóa | Không còn lựa chọn trọng yếu để quyết định sau outcomes |
| G7. Chạy chính và phân tích | G6 | Trial archive; analysis outputs | Đủ lần chạy theo kế hoạch và mọi quyết định xử lý có log |
| G8. Hoàn thiện paper và artifact | G7 | PDF, LaTeX, data, figures, reproducibility guide | Mỗi kết luận truy được về dữ liệu/nguồn |
| G9. Review và nộp bài | G8 | Revision log; submission package | Đạt yêu cầu venue và tác giả xác nhận nội dung |

G0 và chuẩn bị môi trường G1 có thể tiến hành song song. Tuy nhiên, chưa chi ngân sách lớn cho agent trước khi G2–G3 chứng minh tính khả thi. Có thể viết phần mô tả phương pháp trong lúc xây instrument, nhưng Results chỉ được viết từ dữ liệu đã thu.

## 3. G0 — Chốt câu hỏi, phạm vi và đóng góp

**Công việc**

1. Viết scope một trang: đối tượng nghiên cứu, can thiệp, đối chứng, endpoint, đơn vị thực nghiệm và giới hạn suy rộng.
2. Đối chiếu artifact của các nghiên cứu sát nhất: Precedent or Intent?, Constraint Decay, CodeThread, FeatureArc và nghiên cứu verification surface. Dùng [review khoa học](paper-proposal/scientific-review.md) làm điểm bắt đầu; không coi việc đọc abstract là đã kiểm tra artifact.
3. Lập ma trận: workload, yếu tố được thay đổi, loại feedback, acceptance/preservation, cách tuyển task, reset session và artifact công khai.
4. Viết một đoạn chỉ rõ phần nào kế thừa, phần nào được kiểm tra thêm, vì sao kiểm tra đó có ích. “Dùng SmartKit” hoặc “cũng có joint success” chưa đủ làm đóng góp.
5. Trao đổi với giáo sư để thống nhất hướng: extension có khác biệt cụ thể, replication có chủ đích, hoặc case study khám phá. Chọn nhóm venue phù hợp với loại bằng chứng có thể tạo ra; kiểm tra quy định chính thức khi có venue cụ thể.

**Đầu ra dự kiến:** `research/execution/scope.md`, `prior-work-matrix.csv`, `decision-log.md`.

**Đạt khi:** giải thích được câu hỏi còn cần trả lời mà không dựa vào tuyên bố “đầu tiên” chưa được xác minh. Nếu không có khác biệt đủ ý nghĩa, định vị replication hoặc sửa câu hỏi trước khi chạy lớn.

## 4. G1 — Dựng và kiểm tra baseline

**Công việc**

1. Xác nhận bản SmartKit sử dụng và quan hệ với bản thesis. Ghi revision chính xác vào artifact manifest, không chèn dãy hash vào phần thân paper.
2. Dựng môi trường sạch; ghi OS, runtime, dependency lock, DB và dịch vụ phụ trợ. Lưu toàn bộ lệnh và log cài đặt.
3. Chạy các kiểm tra có sẵn và production build; khởi động ứng dụng để kiểm tra những luồng liên quan tới task. Build pass không thay thế runtime checks.
4. Tạo fixture cục bộ cho người dùng thường, admin, nhiều chủ sở hữu đơn và các trạng thái cần thiết. Chỉ sử dụng dữ liệu/dịch vụ test.
5. Kiểm tra auth, quyền truy cập, history và order-state behavior trong phạm vi đã chọn. Nếu code và intended behavior mâu thuẫn, ghi vấn đề để tác giả xác nhận.
6. Phân loại lỗi có sẵn, lỗi môi trường và yêu cầu chưa rõ. Nếu phải sửa baseline, lưu patch riêng, kiểm tra lại và đóng băng bản sửa trước khi dựng treatment.
7. Chứng minh reset repository, DB và service state có thể lặp lại.

**Đầu ra:** `baseline-report.md`, `environment-manifest.json`, fixture/reset scripts, log build/test/runtime.

**Đạt khi:** biết baseline đáp ứng các hợp đồng nền nào và lỗi nào còn tồn tại. Chưa sử dụng baseline hỏng để tạo chênh lệch giữa các điều kiện.

## 5. G2 — Hoàn thành một tác vụ từ đầu đến cuối

Tác vụ mở đầu có thể là bộ lọc trạng thái trên trang lịch sử, nếu G1 xác nhận đủ điều kiện. Đây là lựa chọn để kiểm tra quy trình, chưa phải tác vụ đã được tuyển vào tập chính. Source hiện cho thấy action đã có tham số status, còn trang history dùng query riêng; phải đặc tả đúng phần giao diện và đường truy cập dữ liệu cần thay đổi.

**Task card cần có**

| Trường | Nội dung bắt buộc |
|---|---|
| ID và nguồn | Historical issue/PR hoặc constructed; URL/tài liệu nếu có |
| Starting state | Baseline, fixture và chức năng hiện có |
| New behavior | Hành vi quan sát được cần thêm, gồm trường hợp rỗng/lỗi |
| Preservation | Các yêu cầu cũ còn hiệu lực và căn cứ cho từng yêu cầu |
| Allowed changes | Những hành vi được phép đổi theo yêu cầu mới |
| Access policy | Ai được đọc/sửa dữ liệu nào |
| Reference | Giải pháp tham chiếu và một cách triển khai hợp lệ khác |
| Checks | Acceptance, preservation, build/runtime và cách reset |
| Eligibility | Vì sao task chưa có sẵn; điều kiện loại; trạng thái qualification |

**Thứ tự thực hiện**

1. Viết specification đủ rõ để người khác triển khai, không đưa gold patch hoặc danh sách file phải sửa.
2. Xác nhận với tác giả các lựa chọn nghiệp vụ còn mở: phân trang, exact/prefix search, batch atomicity, role policy… chỉ những lựa chọn liên quan tới task đã chọn.
3. Viết evaluator theo specification trước khi xem output agent.
4. Xây reference solution và alternative solution. Evaluator không được phạt giải pháp chỉ vì khác folder/style của reference.
5. Tạo các bản sai có chủ đích tương ứng với hợp đồng cần kiểm tra. Ghi lỗi nào do check nào phát hiện; chưa gọi đây là lỗi agent đã quan sát.
6. Chạy nhiều lần để phát hiện flakiness và lỗi reset; quy định số lần kiểm tra trong qualification plan, dựa trên môi trường và chi phí.

**Ma trận tối thiểu để qualification**

| Implementation | Acceptance | Preservation |
|---|---|---|
| Baseline chưa thay đổi | Chưa đáp ứng ít nhất một yêu cầu mới | Pass |
| Reference đúng | Pass | Pass |
| Alternative đúng | Pass | Pass |
| Bản thiếu chức năng | Bị check phù hợp phát hiện | Theo loại lỗi được cấy |
| Bản có regression | Theo chức năng đã triển khai | Bị check phù hợp phát hiện |

**Đầu ra:** task card hoàn chỉnh, reference/alternative patches, evaluator, fault variants, qualification report.

**Đạt khi:** phân biệt được đúng/sai theo hợp đồng và chạy lại được. Nếu chưa đạt, sửa instrument trước khi chạy agent. Tác vụ dùng nhiều để chỉnh instrument nên thuộc development set.

## 6. G3 — Dựng hai layout và bốn điều kiện

**Công việc**

1. Viết quy tắc layout theo tầng và theo feature; không thiết kế đối chứng theo hướng cố tình gây khó.
2. Refactor module/import/export bằng manifest có thể audit. Giữ domain logic, dependencies và hành vi đã đặc tả.
3. Chạy qualification checks trên cả hai layout; port reference/alternative solution và các bản sai cần thiết.
4. Định nghĩa V0 bằng inventory các checks cơ bản hiện có. V1 giữ nguyên V0 và thêm checks/fixtures đã mô tả.
5. Mỗi check bổ sung phải có contract và lý do phát hiện regression mà V0 còn thiếu. Không hạ chất lượng V0 để tăng hiệu ứng.
6. Tách hidden evaluator khỏi visible suite; tránh chỉ thay tham số của cùng một fixture rồi gọi đó là đánh giá độc lập.
7. Kiểm soát instructions: cùng requirements và domain facts, path mapping phù hợp layout, không để AGENTS.md của đối chứng ép agent viết theo layout treatment.
8. Kiểm tra parent rules, memory, mounts, git history và network access có thể làm lộ reference/hidden tests. Log chính xác exposure trong từng trial.

| Điều kiện | Layout | Visible checks |
|---|---|---|
| C00 | Theo tầng | V0 |
| C01 | Theo tầng | V0 + bộ bổ sung |
| C10 | Theo feature | V0 |
| C11 | Theo feature | V0 + bộ bổ sung |

**Đầu ra:** bốn fixtures có version, transformation manifest, treatment/exposure manifest, báo cáo equivalence trong phạm vi kiểm tra.

**Đạt khi:** mọi khác biệt giữa điều kiện đều giải thích được. Sự tương đương trên suite không được trình bày thành chứng minh tương đương ngữ nghĩa tuyệt đối.

## 7. G4 — Xây tập tác vụ chính

**Công việc**

1. Gán mỗi candidate vào role calibration, development, main hoặc discovery/hold trước khi xem agent outcomes.
2. Rà rationale/provenance và xác nhận behavior thực sự thiếu ở starting snapshot; constructed tasks phải ghi rõ đây là tình huống giả định.
3. Tách development set và main set trước mọi lựa chọn dựa trên kết quả agent. Không đưa task đã dùng để tune harness vào main mà không khai báo.
4. Gắn task family, shared surface và exposure mapping; nhiều biến thể một workflow không tự trở thành task độc lập.
5. Giữ cả localized và cross-workflow changes, nhưng không dùng số file, domain quota hoặc độ khó đoán trước làm cổng tuyển.
6. Mọi task dự kiến cho main phải qua ma trận qualification của G2 trên cả hai layout và có inclusion/exclusion reason.
7. Nhờ giáo sư hoặc người đọc độc lập rà specification/evaluator khi bố trí được; ghi rõ nếu không có review độc lập.

**Đầu ra:** task registry, task cards, inclusion/exclusion log, qualification matrix và provenance records.

**Đạt khi:** số task hợp lệ được xác định từ kiểm tra thực tế. Chưa ấn định số lượng “đủ” chỉ để có một con số đẹp trong paper; cỡ tập cuối phải phù hợp mục tiêu độ chính xác ở G5.

## 8. G5 — Pilot, chi phí và precision plan

Pilot có mục đích kiểm tra instrument và tính khả thi sau khi task frame đã được rà. Dữ liệu pilot phải có nhãn riêng, không được gộp âm thầm vào kết quả chính sau khi dùng để sửa thiết kế. Nếu chỉ còn calibration hoặc một candidate, ghi rõ giới hạn phạm vi và mục tiêu feasibility trước khi chọn allocation.

**Công việc**

1. Chọn cấu hình model/harness ứng viên theo khả năng truy cập, ghi log và tính phù hợp; không chọn chỉ vì từng cho chênh lệch thuận lợi.
2. Chạy các development tasks ở cả bốn điều kiện trong workspace/session sạch; ngẫu nhiên hóa thứ tự trong block task × model × repetition.
3. Đo thời gian, tokens/cost, tỷ lệ lỗi hạ tầng, hoàn chỉnh log, khả năng reset và độ ổn định evaluator.
4. Kiểm tra treatment có thực sự khả dụng không. Agent không chạy checks vẫn là outcome của điều kiện được gán, không phải lý do loại run.
5. Nếu task quá dễ/khó hoặc feedback không được sử dụng, điều tra cơ chế và specification. Giữ log sửa đổi; không chỉnh task chỉ để tạo hiệu ứng dương.
6. Lập các kịch bản precision với binary outcomes, các mức success rate hợp lý, task heterogeneity, cell toàn pass/toàn fail và batch dependence. Chọn mục tiêu độ rộng interval trước khi xem outcomes chính.
7. Chỉ sau khi biết task frame thực tế mới chốt số tasks, repetitions, model chính và ngân sách. Nếu interaction thiếu precision, giữ exploratory thay vì hứa xác nhận tương tác; nếu workload không đủ, thu hẹp claim hoặc tiếp tục discovery.

**Tính ngân sách**

Với T tasks, M cấu hình model/harness và R repetitions cho mỗi điều kiện, số trial chính là `N = 4 × T × M × R`, nếu thiết kế cân bằng. Tổng kinh phí gồm trial chính, pilot, qualification, lưu trữ và phần xử lý lỗi hạ tầng theo chính sách cố định.

Ví dụ số học giả định: T=20, M=2, R=5 tương ứng 800 trial. Đây không phải cỡ mẫu được khuyến nghị hoặc đã được chứng minh đủ. Dùng chi phí quan sát từ pilot để lập ngân sách, chưa gán một mức tiền khi chưa biết model và workload.

**Đầu ra:** pilot report, protocol deviations, bảng chi phí, precision report và cấu hình thí nghiệm đề xuất.

**Đạt khi:** biết nghiên cứu chính sẽ đo được gì trong giới hạn tài nguyên. Nếu không đạt precision cần thiết, điều chỉnh scope hoặc loại tuyên bố confirmatory; không gọi một pilot nhỏ là nghiên cứu kết luận.

## 9. G6 — Khóa protocol trước main runs

Tạo `protocol-v1.md` và cấu hình máy đọc được, có ngày và version. Các điểm bắt buộc phải giải quyết:

- Task IDs, family IDs, baseline, bốn fixtures, oracle version và exclusion criteria.
- Prompt, instructions thực sự được tải, model/harness, tool access, time/token limits và termination rule.
- Block allocation, thứ tự ngẫu nhiên và seed nếu công cụ hỗ trợ; không giả định seed bảo đảm tái lập model API.
- Joint success; acceptance/preservation có ba trạng thái pass/fail/unassessable; cách báo denominator.
- Hai hiệu ứng biên chính, các simple effects và interaction phụ; primary model/harness.
- Estimator task-balanced; cách tính interval cho tập task cố định; phân tích task-family/transfer nếu có và các giả định liên quan.
- Nếu kiểm định confirmatory: giả thuyết, test hợp lệ, family và kiểm soát multiplicity. Không chỉ ghi tên Holm mà bỏ phương pháp tính p-value gốc.
- Agent failure, evaluator failure và infrastructure failure; retry/adjudication, missingness, best/worst-case sensitivity bounds.
- Sample size, precision criterion, tổng budget, stopping rule và phương án provider/model thay đổi.
- Kế hoạch phân tích lỗi và phạm vi review độc lập.

**Đạt khi:** người đọc có thể biết trước cách xử lý mọi outcome chính. Có thể preregister nếu phù hợp, nhưng chỉ gọi preregistered khi thực sự đăng ký trước khi xem main outcomes. Sau freeze, mọi thay đổi có ngày, lý do và phạm vi ảnh hưởng; kết quả sau thay đổi không được giả làm kế hoạch ban đầu.

## 10. G7 — Thu dữ liệu và phân tích

**Thu dữ liệu**

1. Smoke-test hệ thống lưu artifact bằng trial development; kiểm tra không còn tác vụ main nào bị dùng để debug sau freeze mà không khai báo.
2. Chạy theo allocation đã khóa; mỗi trial có ID duy nhất và trạng thái kết thúc.
3. Lưu prompts, trace, patch, stdout/stderr, checks, resource logs, environment và adjudication ngay khi phát sinh.
4. Theo dõi sức khỏe hạ tầng và ngân sách; chưa dùng chênh lệch điều kiện để quyết định dừng sớm khi không có sequential design đã định trước.
5. Chạy hidden evaluation từ patch trong môi trường sạch. Không sửa tay patch rồi tính đó là output agent.
6. Giữ cả attempt lỗi và rerun; phân biệt parent attempt và replacement để tránh đếm đôi.

**Kiểm tra dữ liệu**

Đối chiếu số trial dự kiến/thực tế, ID trùng, metadata thiếu, model drift, task-condition cells trống, log không đầy đủ và missing outcomes. Tạo data-validation report trước khi diễn giải hiệu ứng. Không xóa outlier thời gian hoặc run thất bại vì “không giống các run khác”.

**Phân tích**

1. Tính từng cell từ counts có căn cứ; lấy trọng số bằng nhau giữa tasks như protocol.
2. Báo joint success và acceptance/preservation riêng, gồm unassessable và failure stages.
3. Ước lượng hai hiệu ứng chính; báo simple effects/interaction để phát hiện khác biệt bị trung bình che khuất.
4. Tính interval và các kiểm định đã khóa. Phân tích mới nảy sinh phải ghi exploratory.
5. Báo cost/time cho mọi attempts, không chỉ successful runs.
6. Làm sensitivity analysis theo kế hoạch: infrastructure missingness, task families, batch/model drift và các giới hạn evaluator được phát hiện.
7. Phân tích lỗi theo codebook; dùng traces để hỗ trợ giải thích, không biến suy đoán cơ chế thành phát hiện nhân quả.

**Đầu ra:** immutable raw archive, analysis dataset, data dictionary, scripts, kết quả chính/phụ và error-analysis report.

**Đạt khi:** mọi số đưa vào paper được tái tạo bằng script và mọi exclusion/rerun có dấu vết. Kết quả null với interval rộng không được gọi equivalence.

## 11. G8 — Chuyển proposal thành paper hoàn chỉnh

| Phần | Việc cập nhật sau dữ liệu |
|---|---|
| Title/Abstract | Viết theo đóng góp và bằng chứng thực tế; thêm con số đã kiểm tra |
| Introduction | Chốt khoảng trống hẹp và đóng góp thực sự đạt được |
| Related work | Đối chiếu kết quả với công trình sát nhất; cập nhật nguồn trước submission |
| Method | Thay “dự kiến” bằng quy trình đã làm; ghi rõ deviations |
| Experimental setup | Task provenance, qualification, model/harness, budget, allocation và sample counts |
| Results | Đi theo RQ, effect size, uncertainty và failure patterns; chỉ dùng dữ liệu mới có artifact |
| Discussion | Giải thích trong scope; xét giải thích thay thế và kết quả trái kỳ vọng |
| Threats | Nêu giới hạn thật của task selection, evaluator, tác giả kiêm thiết kế và một repository |
| Conclusion | Khẳng định vừa bằng chứng; không mở rộng sang human productivity chưa đo |
| Appendix/artifact | Chi tiết đủ tái lập, task cards, oracle validation, schema, logs và phụ phân tích |

**Bộ hình kết quả dự kiến, chưa có dữ liệu để vẽ**

- Joint success theo bốn điều kiện, có interval và số tasks/runs.
- Chênh lệch theo từng task/family, tránh chỉ báo một giá trị trung bình.
- Phân bố acceptance/preservation/failure stages, tách unassessable.
- Cost/time và quan hệ với success; giữ các lần thất bại.
- Ví dụ trace/patch đã ẩn dữ liệu nhạy cảm nếu giúp chứng minh một failure mode.

Không cần giữ tất cả bảy hình proposal trong main paper. Khi có results, chọn hình nào giúp trả lời câu hỏi; chuyển hình phụ và chi tiết inventory vào appendix nếu cần. Không vẽ đường/trụ từ số giả để “trông giống paper”.

**Đạt khi:** claim–evidence map cập nhật; mọi số, caption, bảng và text nhất quán với script outputs; citations giữ đúng phạm vi nguồn. Rà AGENTS.md và humanizer sau khi logic/evidence đã ổn định.

## 12. G9 — Review, tái lập và submission

1. Chạy lại pipeline phân tích trong môi trường sạch bằng dữ liệu đã khóa; đối chiếu những con số trọng yếu.
2. Nhờ một người không xây evaluator thử đọc task spec và tái lập một phần kết quả khi có thể. Báo đúng mức nếu chỉ có self-check.
3. Review khoa học: câu hỏi–thiết kế–kết quả–kết luận khớp nhau; không dùng nhiều citation để che thiếu bằng chứng.
4. Review toàn PDF bằng hình render: font, caption, màu, thứ tự hình, bảng, phương trình, bibliography và khoảng trắng. Clean compile log chưa đủ.
5. Kiểm tra venue chính thức: loại bài, giới hạn trang, anonymity, supplementary/artifact policy, license và khai báo AI.
6. Kiểm tra author list/contributions với giáo sư; không tự thêm đồng tác giả. Tác giả đọc và chịu trách nhiệm với toàn bộ nội dung.
7. Chuẩn bị source LaTeX, PDF, artifact README, availability statements và cover letter nếu venue yêu cầu. Loại credentials, dữ liệu cá nhân và lời giải không được phép công khai.
8. Chỉ nộp theo quyết định tác giả. Chấp nhận, revise hay reject là kết quả của quy trình phản biện, không nằm trong cam kết của kế hoạch này.

**Hoàn tất khi:** gói paper có thể review và nộp được, nguồn/data truy vết được, claims đúng phạm vi, tác giả đã xác nhận bản cuối. Nếu chưa có trial data, đầu ra vẫn là proposal/protocol, chưa đạt mục tiêu empirical paper.

## 13. Phân công giữa tác giả, giáo sư và trợ lý

| Vai trò | Trách nhiệm |
|---|---|
| Bạn, tác giả | Xác nhận intended behavior; quyết định câu hỏi, scope, budget và claims; đọc bản cuối; bảo đảm có thể giải thích nghiên cứu |
| Giáo sư/người hướng dẫn | Góp ý giá trị câu hỏi, đóng góp, tính khả thi và venue; quyết định authorship theo đóng góp thực tế |
| Trợ lý | Hỗ trợ audit nguồn/code, soạn task cards, dựng instrument/harness, phân tích có provenance, làm figure, LaTeX và kiểm tra nhất quán trong phạm vi được giao |
| Người review độc lập, nếu có | Kiểm tra một phần spec, oracle, error labels hoặc reproducibility; ghi đúng phần đã review |

Những phần cần tác giả quyết định không được thay bằng giả định âm thầm của trợ lý. Tuy nhiên, không cần xin phép lại cho từng thao tác đọc, sửa bản nháp hoặc kiểm tra có thể đảo ngược đã nằm trong phạm vi công việc được giao.

## 14. Lịch tham khảo và điều chỉnh

Khung dưới đây là lịch giả định ngày 10/11; quyết định 12/11 đã loại deadline/giờ làm hàng tuần khỏi ràng buộc. Lịch cũ giả định 4–5 ngày/tuần và môi trường khả dụng, chỉ giữ để tham khảo. Chưa phải dự báo đã được đo. Nếu làm bán thời gian hoặc gặp khó ở baseline, evaluator hay task discovery, thời gian sẽ dài hơn. Ước lượng lại sau G2 và G5.

| Khoảng thời gian giả định | Mục tiêu |
|---|---|
| Tuần 1 | G0 và G1: scope/prior work; dựng baseline; ghi vấn đề |
| Tuần 2 | G2: một tác vụ và evaluator xuyên suốt |
| Tuần 3 | G3: hai layout, bốn điều kiện, exposure control |
| Tuần 4–5 | G4: task qualification và review |
| Tuần 6 | G5: pilot, precision và budget |
| Tuần 7 | G6: khóa protocol; khắc phục việc còn thiếu |
| Tuần 8–9 | G7: main runs, kiểm tra dữ liệu và phân tích |
| Tuần 10–11 | G8: Results/Discussion, figures và artifact |
| Tuần 12 | G9: review, tái lập và chuẩn bị submission |

Đây là khung bố trí công việc 12 tuần, không phải hạn hoàn thành bắt buộc. Không rút ngắn task/evaluator qualification chỉ để giữ lịch. Nếu yêu cầu replication ngoài SmartKit trở thành bắt buộc, lập thêm kế hoạch sau khi đo được chi phí qualification.

## 15. Việc nên làm trong phiên tiếp theo

1. Dùng bảng 11 candidates trong registry để hoàn thiện cards nháp A03 rồi B03; U03 tiếp theo với câu hỏi cache/permission cụ thể.
2. Kiểm tra khả thi của shortlist trước full oracle; cập nhật retained/pending/hold, lý do và phần workload thiếu. Card/source mapping không phải runtime pass.
3. Đối chiếu thay đổi `local-runtime.py` với freeze; kiểm tra lại phần liên quan nếu cần, không cập nhật manifest chỉ để xóa mismatch.
4. Hoàn thiện card/matrix và qualification cho tasks dự kiến chạy; dùng bảng mục tiêu pilot trong plan chi tiết để chọn tasks, repetitions và bộ hồ sơ release.
5. Chốt toàn main set, uncertainty và tổng runs trước main; cập nhật manuscript sau các quyết định cụ thể, giữ pilot outcomes riêng.

Điểm bàn giao tiếp theo là task frame được review, không phải tự động là 16 model runs. Chưa cần chạy model hoặc tăng repetitions trước milestone này.

</details>
