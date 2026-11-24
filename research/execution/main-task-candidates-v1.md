# Danh m?c task hi?n h?nh, 16/11/2026

**A01, A04, B05, B06, U02, U03**, m?i task 8 slots, t?ng 48. C? s?u task ?? ho?n t?t qualification/reliability tr?n hai layout: 48 tr??ng h?p baseline/reference/alternative/fault v? 24 di?n t?p capture/reset/score ??t. ??y l? ki?m ch?ng c?ng c?, kh?ng ph?i agent outcomes.

[Plan hi?n h?nh](../paper-completion-plan.md), [h?p ??ng v? protocol](main48/protocol.md), [audit readiness](main48/readiness.json). Technical freeze v? audit sau freeze ?? ??t; collection c?n start release ri?ng v? ki?m tra quota hi?n h?nh. Ch?a c? model invocation c?a ??t 48.

CSV gi? 14 candidates c?ng m?t history task ri?ng. C?c task ?? lo?i gi? b?ng ch?ng l?ch s?, allocation b?ng 0; kh?ng t? ??ng d?ng task d? ph?ng. M?u fault admin ???c d?ng chung ? U02/U03. Ph?m vi nghi?n c?u c? ??nh ? SmartKit v? c?u h?nh agent n?y; ch?a c? review ??c l?p.

<details>
<summary>Historical roster and qualification evidence</summary>

# Danh mục task SmartKit

> **Kết quả kiểm chứng 15/11:** sáu task × hai lời giải × hai layouts =24 trường hợp pass;12 fault/layout cases bị bắt đúng. Cả12 cặp task–implementation sửa0 relocated existing modules; imports vẫn khác. Đây là feasibility, chưa chứng minh ích lợi S/V hoặc đủ full qualification. [Báo cáo](task-feasibility-2026-11-15/report.md), [source mapping](task-feasibility-2026-11-15/source-evidence.json). Chưa khuyến nghị release48 cho claim thiết kế mạnh.

Cập nhật 15/11/2026 sau nghiên cứu nguồn. **Sáu task, 8 runs/task, tổng 48 runs mới**. Đề xuất thay **MT-B01 tìm mã đơn** bằng **MT-U03 admin đổi role** trước outcomes để giảm overlap với history development và bổ sung thao tác ghi có phân quyền. U03 đã qua phép thử runtime giới hạn với hai lời giải trên hai layouts; chưa đạt full qualification và không tự dùng task dự phòng nếu không đạt.

## Sáu task sẽ chuẩn bị

| STT | Mã | Tên task | Điều kiện | Lần/điều kiện | Runs | Trạng thái |
|---:|---|---|---:|---:|---:|---|
| 1 | MT-A01 / DP-03 | Sửa tên hiển thị | 4 | 2 | 8 | Đã tái kiểm tra hai lời giải trên hai layouts; chưa freeze mới |
| 2 | MT-A03 | Đổi mật khẩu | 4 | 2 | 8 | Đã qua feasibility trên hai layouts; full qualification còn thiếu |
| 3 | MT-B03 | Tiếp tục đơn pending | 4 | 2 | 8 | Đã qua feasibility trên hai layouts; full qualification còn thiếu |
| 4 | MT-B04 | Tải biên nhận JSON | 4 | 2 | 8 | Đã qua feasibility trên hai layouts; full qualification còn thiếu |
| 5 | MT-U02 | Admin xem chi tiết tài khoản | 4 | 2 | 8 | Đã qua feasibility trên hai layouts; full qualification còn thiếu |
| 6 | MT-U03 | Admin đổi vai trò tài khoản | 4 | 2 | 8 | Cache/role semantics đã thử; full qualification còn thiếu |
| | **Tổng** | | | | **48** | **0 task đã khóa cho main** |

Mọi use case đều là tình huống giả định do trợ lý đề xuất, chưa phải issue/PR hoặc nhu cầu production đã xác minh. Hai task mỗi nhóm auth/billing/admin mô tả roster; không phải quota đảm bảo đại diện. Mỗi task có starting snapshot độc lập, không cần lời giải của task khác. U03 phải có control độc lập trên directory baseline; không giả định U02 đã được làm trước.

## Ma trận hành vi, contract và phần dùng chung

| Task | Hành vi mới | Phần cần giữ / căn cứ | Shared surface |
|---|---|---|---|
| A01 | Form sửa name; trim; 1 đến 80 Unicode code points; server validation; cập nhật cùng phiên/reload | Chỉ đổi caller name; identity/role/email/verification/orders, safe rendering và sign-in. Kế thừa card đã qualify | Settings/auth/session; overlap A03 |
| A03 | Form current/new/confirmation; wrong current không ghi; new credential đăng nhập được, old không được | Policy password baseline; protected fields/orders; không thêm immediate revoke mọi phiên | Settings/auth/credentials; overlap A01 |
| B03 | Mở lại own pending order còn hạn, giữ ID/code/amount/expiry; không tạo/hủy record khi resume | Mua mới, status/cancel ownership, completion/idempotency; chốt behavior khi hết hạn trong lúc mở trang | History/checkout/payment; overlap B04 ở order reads |
| B04 | Tải JSON own completed order với code/plan/amount/completed time | Foreign/incomplete bị từ chối; read-only, không lộ dữ liệu khác; receipt không là hóa đơn thuế | History/orders/download; overlap B03 |
| U02 | Trang detail từ directory, cùng metadata được phép và tổng session records | Admin-only kể cả direct URL; count đúng nghĩa baseline; không raw token; missing target rõ ràng; directory còn đúng | Directory/auth/DB; overlap U03 |
| U03 | Admin đổi user/admin của tài khoản khác, giới hạn đường ghi mới như mục dưới | Quyền caller thật trên server; giữ identity/password/orders và semantics cache baseline | Directory/auth/session/role; overlap U02 và auth chung |

Reference/alternative ở hai layouts phải có logical-module mapping để mô tả thao tác nào đọc/tái dùng/sửa phần mã đã chuyển vị trí. Đây không phải gold path list hoặc điều kiện buộc nhiều files. Agent không sửa relocated module vẫn có thể đọc nó; dùng traces mới kết luận hành vi truy cập mã đã quan sát. Phân biệt việc path được gọi với việc assertion kiểm tra đúng nghĩa vụ [E48-M2, E48-P3 và P4 trong bảng nguồn](../paper-proposal/citation-evidence.md#48-run-study-evidence-review--15-november-2026).

<a id="u03-contract"></a>

## U03: hợp đồng đề xuất và phép thử khả thi

Mục đích giả định: admin giao hoặc thu lại vai trò quản trị của tài khoản khác. Baseline đã có backend role API; phần mới là luồng UI có quy tắc public và kiểm tra đúng actual write transport, không gọi API sẵn có là feature backend mới.

- Trên directory baseline, admin chọn tài khoản khác và role `user` hoặc `admin`, submit rồi thấy giá trị persisted sau reload. Input role khác bị từ chối. Self-demotion qua feature mới bị từ chối server-side, không chỉ giấu nút; không mở yêu cầu sửa mọi API admin có sẵn.
- Anonymous/ordinary user không được ghi. Caller đã bị demote nhưng giữ cookie cache admin cũ cũng không được ghi qua đường mới: quyền ghi phải kiểm tra theo trạng thái có thẩm quyền trên server. Không tin role/user ID của caller trong payload.
- Đổi role không đổi email/name/password/verification/orders hay quyền của tài khoản không được chọn. UI không lộ raw token. Target sau đăng nhập mới được phép hoặc bị từ chối admin directory đúng role mới; kiểm tra cả promotion và demotion.
- Phiên cũ có thể giữ dữ liệu cached theo baseline. Public card phải nêu phạm vi này; kiểm tra runtime riêng old session/fresh session, không tuyên bố immediate invalidation hay tắt cookie cache toàn cục. Không sửa baseline hoặc dependency để đạt task.

Static evidence ngày 15/11: SmartKit config có `admin()` và cache 300 giây; directory hiện read-only. Installed Better Auth 1.6.25 `dist/plugins/admin/routes.mjs` dùng `getAuthoritativeSessionFromCtx` trong middleware, kiểm tra `user:set-role`, rồi cập nhật role; hàm authoritative ở `dist/api/routes/session.mjs` bỏ cache khi có server store. `requireAdmin` của SmartKit dùng cached `getSession`. Source này và [Admin docs](https://www.better-auth.com/docs/plugins/admin), [Session docs](https://www.better-auth.com/docs/concepts/session-management) chỉ hỗ trợ thiết kế kiểm tra; Runtime mới xác nhận cache/read và authoritative write trong phạm vi thử; xem báo cáo bên dưới.

Trước full oracle, chạy phép thử không model trên fixtures tách biệt: promotion/demotion persisted và fresh-login access; unauthorized/new-path write; demoted caller với cookie cũ; self-demotion; bảo toàn identity/orders; old-session behavior theo declared scope. Ghi interface thật dùng và version. Sau đó reference/alternative/faults phải qua hai layouts cùng V-gate. Nếu không chứng minh được contract thì U03 chưa đủ chuẩn và toàn lịch chưa release; không âm thầm bỏ trường hợp khó, đổi yêu cầu sau agent outcomes hoặc trở lại B01.

## Sáu task ngoài đợt này

| Mã | Task | Runs mới | Lý do |
|---|---|---:|---|
| DEV-HISTORY-STATUS-01 | Lọc trạng thái lịch sử | 0 | Đã có 4 development runs; chưa có mã DP-01 chính thức |
| MT-U01 / DP-02 | Lọc role | 0 | Development-only; dùng kiểm tra công cụ, không có pilot mới |
| MT-A02 / DP-04 | Thu hồi session | 0 | Giữ hold theo quyết định trước; không đổi baseline |
| MT-B01 | Tìm đơn theo mã | 0 | Bỏ khỏi roster trước outcomes vì gần history task; thay bằng permission-write U03 |
| MT-B02 | Hủy nhóm pending | 0 | Workflow nhiều pending chưa có rationale phù hợp |
| MT-U04 | Ban/unban | 0 | Cache semantics chưa rõ; không thêm vào đợt này |

11 ứng viên trong CSV = 6 được chọn chuẩn bị + 5 ngoài đợt. Cộng task history riêng = **12 task đã ghi nhận**. Mới có 1 task/4 agent runs development; đề xuất mới là 6 task/48 runs. B01 không là fallback tự động. Đổi roster là đề xuất trong lượt nghiên cứu này, chưa phải tác giả đã xác nhận từng contract.

## Tuyển task và đo lường

Giữ qualification/V-gate cũ: baseline thiếu feature nhưng giữ behavior cũ; reference và valid alternative pass; faults hợp lý bị check đúng bắt; V1 có check trên baseline bắt regression cũ mà V0 bỏ sót ở cả hai layouts. Cả S/V chỉ suy luận trên cùng tập đủ điều kiện đó. Không tuyển dựa trên agent outcomes, số files hoặc làm yếu baseline để tạo effect.

Trước runs, map từng obligation thành old behavior, new behavior hoặc shared invariant với old/new checks riêng. Ghi acceptance/preservation cố định và public scope. Bộ chấm phải exercise transport thực của lời giải, không cố định gold endpoint; unsupported transport ghi chưa chấm được và điều tra, không mặc định agent fail. Khi audit toàn bộ final patches, old-test pass/new-feature fail không tự là regression escape. Chi tiết denominators và codebook ở [plan thực nghiệm](pilot-task-plan-v2.md).

Tập task này mở rộng loại hành vi trong SmartKit, không mở rộng số repository hay chứng minh độc lập. So sánh theo task và báo leave-one-task/domain-out sensitivity, không dùng thống kê để biến constructed pool thành mẫu đại diện. Chưa có review độc lập; author review nhãn diễn giải không phải independent replication.

## File máy đọc và bằng chứng

[CSV](main-task-candidates-v1.csv) giữ qualification/contract/V-gate và metrics đã đo. `collection_role` mô tả roster mới; `planned_conditions=4`, `planned_repetitions_per_condition=2`, `planned_agent_runs=8` cho mỗi task được chọn; ngoài đợt là 0. `planned_behavior` và `selection_reason` ghi lý do trước outcomes. Readiness không được nâng bởi việc sửa plan. Cột `status` cũ tiếp tục là bằng chứng screening kỹ thuật, không thay allocation hiện hành.

Bằng chứng cũ giữ nguyên: [DP02/03 cards](prepilot-2026-11-12/task-cards.md), [qualification report](prepilot-2026-11-12/report.md), [reference metrics](prepilot-2026-11-12/reference-metrics.json), [DP04 spike](dp04-spike-2026-11-11/report.md). Runner đã biết source đổi `docker rm -v`; runtime liên quan vẫn phải kiểm tra trước freeze. Đã làm kiểm tra khả thi không model; chưa hoàn tất qualification để thu agent data.


**Feasibility pass không phải main admission.** Report cho thấy 24 correct candidate/layout cases và 12 seeded-fault detections; treatment reach và V-gate còn mở.

<details>
<summary>Cards, source mapping và lịch sử tuyển task trước lần viết lại</summary>

Hồ sơ dưới đây giữ nguyên nội dung trước lần viết lại ngày 15/11/2026. Trạng thái, số lượt và thứ tự công việc trong hồ sơ chỉ mô tả phương án cũ. Phần hiện hành ở trên quyết định đề xuất mới.

# Registry tác vụ ứng viên SmartKit

Cập nhật 14/11/2026: tác giả đồng ý giữ thiết kế 2 × 2 và xây phạm vi tác vụ trước khi quyết định pilot. Đây là sàng lọc từ source và hồ sơ hiện có, chưa phải danh sách main đã tuyển. Cả 11 ứng viên đều do trợ lý đề xuất, với tình huống sử dụng giả định; chưa có provenance issue/PR được xác minh. DP-02/03 có qualification kỹ thuật đã ghi nhận; các ứng viên bổ sung chưa có kiểm chứng runtime. Số lượt pilot mới chưa chốt; allocation 16 phiên được lưu làm phương án cũ, không tự kích hoạt model.

## Phạm vi khảo sát và quy tắc chọn

Giữ hai lựa chọn thiết kế: tổ chức theo tầng/theo tính năng và cung cấp/không cung cấp thêm preservation checks. Hai hiệu ứng trung bình lên joint success vẫn là chính trên **cùng tập task đủ điều kiện**; chi phí, navigation và tương tác là bổ sung. V-gate hiện có giới hạn tập này vào các task có cơ hội preservation-feedback đã được qualification; không tự đổi thành mọi yêu cầu mở rộng SmartKit.

Khung tác vụ (*task frame*) gồm rationale/provenance, phần mới, hành vi phải giữ, family/surface dùng chung và mã liên quan. Lập khung trước outcomes, giữ cả thay đổi cục bộ và qua nhiều luồng. Không yêu cầu sửa nhiều file, sửa module đã di chuyển hoặc tạo chênh lệch giữa conditions. Nhiều ID chung workflow không tự tăng độ bao phủ.

Qualification kỹ thuật, vai trò pilot và khả năng tuyển main là các trạng thái riêng. DP-02 tiếp tục development-only theo quyết định trước. DP-03 giữ quyền chọn reuse nếu đủ §12 của plan trước pilot và không sửa substantive materials sau exposure; main cần phiên mới. Không tuyển candidate chỉ vì có reference hoặc pilot pass.

## Bảng tác vụ và câu hỏi cần xác minh

Cột S mô tả quan hệ với tổ chức mã, không dự đoán layout thắng. Cột V mô tả hành vi cũ mà checks có thể bảo vệ. Với ứng viên chưa qualify, đây là rationale cần xác minh, không phải kết quả thực nghiệm.

| ID / tác vụ | Vai trò và lý do sử dụng giả định | Phần mới cần thêm | Quan hệ với S | Hành vi cũ liên quan V | Bằng chứng và việc tiếp theo |
|---|---|---|---|---|---|
| MT-U01 / DP-02: lọc role | Calibration; admin xem một nhóm tài khoản | GET dropdown, filtered rows/total | Reference/alternative sửa một route giữ nguyên đường dẫn; auth imports khác vị trí | Admin-only access, counts/order, không ghi dữ liệu/lộ tokens | Qualification/V-gate đã ghi ở hai layouts; development-only, chưa chạy model |
| MT-A01 / DP-03: sửa tên | Development, giữ quyền chọn main; sửa tên mà giữ identity | Form, validation, persistence và hiển thị cùng phiên | Reference thêm hai module theo layout, không sửa relocated existing module; mã đọc/tái sử dụng vẫn có thể khác vị trí | Safe rendering, identity, sign-in, order ownership | Qualification/V-gate đã ghi; card chưa được xác nhận, chờ rà scope và runtime |
| MT-A03: đổi mật khẩu | Discovery 1; đổi credential khi đang đăng nhập | Form current/new/confirmation và lưu credential | Settings → auth client/config/session; chung Settings/auth với DP-03 | Sign-in, protected fields/orders; map plausible regression của API cũ | Source Settings chỉ liên kết reset-password; kiểm tra password/session policy trước full oracle |
| MT-B03: tiếp tục đơn pending | Discovery 2; quay lại đúng đơn còn hạn | Resume own order, giữ code/amount/expiry; không tạo/hủy khi resume | History → billing page → PaymentSection/polling/status/auth; modules theo layout khác vị trí | Mua mới, status/cancel ownership và completion/idempotency trong scope đã chốt | Source createOrder hủy pending cũ rồi tạo mới; kiểm tra luồng resume, expiry/transport trước full oracle |
| MT-U03: admin đổi role | Discovery 3; phân quyền tài khoản khác | Admin write user↔admin; chặn self-demotion trong đề xuất | Admin route → permission/session/config; chung admin surface DP-02 | Admin guard, identity, protected fields/orders | Cached-role timing chưa chốt; kiểm tra trước qualification, hold nếu cần đổi baseline |
| MT-B04: tải receipt | Reserve; lưu thông tin own completed order | Download JSON đúng đơn đủ điều kiện | History/order read và ownership; gần họ lookup | Own history/status, read-only, không lộ dữ liệu khác | Chưa qualification; chốt nội dung download và đánh giá overlap |
| MT-U02: chi tiết account | Reserve; admin xem một tài khoản | Detail route, metadata/session counts được phép | List → detail → auth/DB; chung admin surface | Admin-only direct access, không lộ token, list/count cũ | Chưa chốt metadata/count semantics; không dùng lấp task count |
| MT-B01: tìm mã đơn | Reserve; tra mã đã biết | GET search, empty/no-match policy | Gần history smoke task; đổi input không tạo family mới | Own orders, thứ tự và read-only | Matching policy và qualification còn mở |
| MT-A02 / DP-04: revoke session | Hold/development-only | UI list/revoke other session | Settings/auth/session; chung surface DP-03 | Current/foreign sessions, tokens | Spike ghi DB record đã xóa nhưng cached cookie còn authenticated; giữ baseline |
| MT-B02: hủy nhóm pending | Hold do rationale | Batch cancellation | Order lifecycle, atomic/partial chưa chốt | Ownership/status/completion | createOrder hủy pending cũ; chưa xác nhận workflow nhiều pending |
| MT-U04: ban/unban | Hold do cache semantics | Admin control khóa/mở account | Admin/auth/session, overlap U03 | Identity/orders/access theo contract | Hiệu lực với cache chưa rõ; không allocation |

Bằng chứng DP-02/03: [task cards](prepilot-2026-11-12/task-cards.md), [report](prepilot-2026-11-12/report.md), [reference metrics](prepilot-2026-11-12/reference-metrics.json). Source anchors nằm trong [CSV](main-task-candidates-v1.csv), layout mapping ở [manifest](layout-manifest.json). Metrics mô tả một cách giải, không phải gold file list hay giới hạn mã agent phải đọc.

Mapping ví dụ đã ghi: auth `src/features/auth/lib/auth.ts` ↔ `src/lib/auth/auth.ts`; billing `src/features/billing/components/PaymentSection.tsx` ↔ `src/components/billing/PaymentSection.tsx`; actions/hooks có mapping tương ứng. Đây là đường mã có thể cần tìm hiểu; chưa có agent trace của candidates mới để xác nhận thực sự được đọc.

## Lượt khảo sát tiếp và điều kiện kết thúc

1. Hoàn thiện card nháp A03 rồi B03: rationale, thiếu sót baseline, allowed changes, acceptance/preservation và dependencies. Bảng trên là đầu vào, chưa xác nhận từng business rule.
2. Kiểm tra điểm có thể làm task không khả thi trước full oracle: password/session policy của A03; expiry và đường resume của B03. Ghi nguồn và kết quả thực; source inspection không phải runtime pass.
3. Xét U03 với câu hỏi cached-role timing. B04/U02/B01 là reserve có overlap khai báo; A02/B02/U04 giữ hold. Không chọn theo outcomes vì chưa có outcome mới.
4. Bàn giao retained/pending/hold, rationale và phần workload chưa bao phủ. Không có ngưỡng 2/8/10 task tự chứng minh main-ready. Nếu chỉ đủ vài task, báo giới hạn và mục tiêu hẹp trước chọn allocation.

Qualification sâu dành cho shortlist có rationale. Pilot không cần chờ toàn bộ main set, nhưng **mọi task chạy pilot** phải qualify, có card/instrument version, mục tiêu feasibility và allocation khóa trước. Trước main, toàn bộ task được tuyển phải qualify và protocol phải chốt. Lượt này cập nhật tài liệu; chưa chạy các bước runtime mới trên.

## Trạng thái hiện hành

Có 11 candidates, hai development tasks có qualification đã ghi, trong đó DP-03 là non-lookup. **Chưa có task mới admitted main.** Các T mô phỏng không chứng minh đã có từng ấy task đủ chuẩn. Qualification DP-02/03 là bằng chứng lịch sử; `local-runtime.py` hiện khác manifest và cần đối chiếu trước lần chạy mới. Không sửa digest để bỏ qua xác minh.

Trong CSV, `proposed_repetitions` trống là chưa chốt lượt tiếp theo; 0 là chưa cấp lượt cho discovery/hold. Giá trị 1/3 cũ vẫn được giữ trong allocation và bảng lịch sử. `paper_V_gate_status` là screening cũ; `V_gate_status`/`qualification_status` ghi evidence runtime mới hơn. Rationale mới không tự nâng readiness.

## Hợp đồng ứng viên để khảo sát; chưa được duyệt cho main

Mọi use case dưới đây là **giả định phục vụ constructed task**, chưa có issue/PR
hoặc nhu cầu production được xác nhận. Anchors thuộc `layouts/feature`; dùng
layout manifest để đối chiếu S0, không dùng clone SmartKit có development reference
làm baseline. Các policies sau là đề xuất, chưa phải author-confirmed contract.

- **MT-A03, đổi password với current password:** Settings chỉ liên kết reset-password;
  thư viện đã có `/change-password`. Giả định người dùng đang đăng nhập muốn thay
  credential mà không đi qua email reset. Đề xuất form current/new/confirmation;
  wrong-current không ghi, new password giữ policy auth hiện có 8–128; sau đổi,
  new credential đăng nhập được, old credential không được. Giữ email/role/verification/
  orders và ownership; không thêm yêu cầu revoke mọi phiên ngay lập tức. V1 có thể
  kiểm tra sign-in đúng/sai và wrong-current qua API đã có, nhưng phải map plausible
  regression khi sửa UI/shared auth. Không gọi backend API có sẵn là feature mới.
- **MT-B03, tiếp tục own pending payment:** Billing GET với `plan` hiện gọi
  `createOrder`, hàm này hủy pending cũ rồi tạo đơn mới. Giả định người dùng quay lại
  muốn tiếp tục đúng payment code đang còn hạn. Đề xuất Resume từ history qua own
  order ID, giữ code/amount/expiry; resume không tạo/cancel record. Foreign, missing,
  non-pending hoặc expired không hiển thị payment controls. Giữ luồng mua mới,
  ownership của status/cancel, entitlement và webhook idempotency. Chỉ ra đây là
  tiếp tục transaction workflow, không chỉ thêm filter. V1 kiểm tra status/cancel
  trên đường cũ với real sessions; billing script DB-only không thay transport test.
  Không mô tả mọi race là đã được contract xử lý; chốt expiry/concurrency trước oracle.
- **MT-U03, admin đổi role tài khoản khác:** admin directory hiện read-only, admin
  plugin/schema có role. Giả định hỗ trợ phân quyền vận hành. Đề xuất admin đổi
  user↔admin cho tài khoản khác, chặn self-demotion trong task này, non-admin và
  anonymous không được ghi; không đổi identity/password/orders. Timing quyền của
  session đã cache là unresolved: cần kiểm tra semantics, không hứa immediate
  demotion hoặc lặp lại workaround đổi nền của DP-04. Nếu không chốt được contract
  phù hợp baseline thì hold. V1 dự kiến admin-only directory và existing auth field
  protection; chưa chứng minh đủ regression contrast.
- **MT-B04, tải receipt:** giả định caller cần lưu biên nhận của own completed
  order; đề xuất download JSON chứa code, plan, amount, completed time; không raw
  token/email người khác, không mutate DB, không tuyên bố là hóa đơn thuế. Foreign/
  incomplete không export receipt. Có output/download behavior nhưng vẫn gần họ
  read/ownership, nên không dùng nó để tự tuyên bố đủ diversity. V1 dự kiến giữ own
  history/status; mapping regression còn pending.
- **MT-U04, ban/unban:** schema/plugin đã có banned/banReason/banExpires, chưa có
  control trên admin directory đã đọc. Giả định chặn account lạm dụng. Hold vì
  hiệu lực đối với cookies đang cache chưa rõ; không tự áp immediate enforcement,
  không xóa user/orders, không tính như task đủ chuẩn để bù DP-04.

CSV tách contract, V-gate giấy, qualification runtime, readiness, reuse và surface.
S-reference metrics của DP-02/03 đã có; các candidates còn lại vẫn `not-measured`. Không đặt ngưỡng file/module để tuyển task.

## Bối cảnh lịch sử ngày 11/11/2026

Giữ contracts ban đầu và allocation cũ để đối chiếu. Bảng hiện hành/CSV quyết định thứ tự tiếp theo; task cards DP-02/03 đã qualification thay cho những chi tiết còn mở trong các mô tả ban đầu.

## Lịch sử allocation đề xuất; chưa phải queue hiện hành

| Candidate / pilot alias | Vai trò | Repetitions/cell đề xuất | Reuse status | Điều kiện |
|---|---|---:|---|---|
| MT-U01 / DP-02 | Runner/browser calibration | 1 | Development-only, đề xuất | Contract + qualification + V gate |
| MT-A01 / DP-03 | Profile workflow | 3 | Giữ quyền chọn; chưa ready | Author-confirmed contract + qualification + V gate + freeze |
| MT-A02 / DP-04 | Session lifecycle | 3 | Giữ quyền chọn có điều kiện; chưa ready | Spike không đổi baseline, rồi cùng gates/freeze |
| MT-U02 | Dự phòng 1, admin account detail | 3 nếu được giữ | Chưa gán | Kích hoạt trước allocation khi thiếu task đủ chuẩn |
| MT-B01 | Dự phòng 2, history lookup | 3 nếu được giữ | Chưa gán | Ghi near-clone family, không coi tự động là workload mới |
| MT-B02 | Hold, chưa là task dự phòng hoạt động | 0 | Chưa gán | Cần xác nhận use case nhiều pending trước mọi qualification |

Bảng này giữ lịch sử allocation trước task-frame revision. Queue hiện hành ở đầu registry chỉ dùng discovery/cards, không tự kích hoạt model. Kết thúc sàng lọc phải báo khoảng trống workload; không có ngưỡng task-count mặc định. Quyết định pilot dựa vào câu hỏi feasibility và tasks đã qualify; quyết định main dựa thêm vào scope, precision và toàn bộ main qualification.

## Các trường trạng thái và chỉ số cần hoàn thiện

CSV ghi contract/qualification/V-gate/reuse/readiness riêng. Contract thành confirmed khi tác giả xác nhận card/matrix cụ thể. DP-03 có qualification đã ghi nhưng đang chờ rà phạm vi, xác nhận card và đối chiếu runtime; DP-04 hold/development-only. Quyền chọn reuse không đồng nghĩa main admission. Chỉ chuyển evaluation-ready sau đủ điều kiện đã đặt trước model invocation.

Mọi task được gán evaluation-ready trước pilot, hoàn tất pilot mà không cần sửa substantive spec/snapshot/checks/fixtures/cap, vào eligible main pool bất kể pilot pass/fail/time. Pilot/main raw outcomes tách riêng và main dùng fresh sessions theo protocol khóa trước main collection. Substantive revisions sau exposure chuyển task/version thành development-only và giữ lịch sử, không gán nhãn hồi tố. Xem quy tắc chi tiết ở §12 của plan. Không tính trước DP-03/04 vào mục tiêu T tối thiểu; task discovery có phương án không dùng chúng.

Functional family của DP-03 vẫn là `profile-update`, DP-04 là `session-lifecycle`. Ghi thêm shared_surface_group=`settings` vì cả hai nằm trên Settings và có auth/session dependencies chung. Đây là grouping trước outcomes, không khẳng định độc lập giữa hai task. Family/surface sensitivity cần đủ dữ liệu và assumptions; không fit population variance từ hai task này.

Các trường reference_source_files_S0/S1, reference_parent_dirs_S0/S1, relocated_logical_modules, unchanged_route_files và reference_metrics_version đã ghi cho DP-02/03; các candidates khác vẫn chưa đo. Đếm bằng source files/reference patches đã port và logical-module mapping, loại hoặc báo riêng tests. Parent directories tính relative với source root đã ghi, không đo theo độ sâu cây thư mục. Nếu references sửa khác logical modules, khai báo khác biệt implementation; không coi toàn bộ chênh lệch counts là layout effect. Đây là mô tả, không phải cổng loại hoặc tiêu chí chấm agent.

V gate định nghĩa eligible workload có cơ hội preservation-feedback bổ sung, không phải mọi extension của SmartKit. Ghi false/fail/pending cùng lý do thay vì bỏ hàng khỏi registry. Hai marginal effects factorial dùng cùng task set đã chốt; nếu muốn target khác phải định nghĩa trước.

## Nguyên tắc chọn

Đóng góp và phạm vi đã được tác giả đồng ý là đo hai lựa chọn thiết kế cụ thể trong SmartKit, gồm chức năng mới, preservation và chi phí. Pool phải giúp quan sát cả thay đổi cục bộ và thay đổi qua nhiều luồng, nhưng domain count không phải quota và candidate count không phải sample size. Mỗi task phải được gắn role (calibration, development, main hoặc discovery/hold) trước outcomes; các biến thể gần cùng family không tự tạo thêm task độc lập.

Nguồn của các đề xuất là kiểm tra source và đề xuất của trợ lý cho tác giả xác nhận. Chúng chưa phải nhu cầu người dùng, issue/PR hay sự cố production có thật. Đường dẫn dưới đây thuộc feature snapshot; layout đối chứng được đối chiếu bằng manifest khi qualification.

Classification là dự kiến theo yêu cầu và bề mặt hành vi, không bắt buộc agent sửa nhiều file. Không thưởng phạt đường dẫn, layer hay số module. Họ tác vụ được ghi trước outcomes; các biến thể chung workflow không được coi là task mẫu độc lập chỉ vì có ID khác nhau. DEV-HISTORY-STATUS-01 và bốn smoke-pilot outcomes vẫn nằm ngoài main dataset.

## MT-A01 — Sửa tên hiển thị của chính mình

- **Miền / họ / loại dự kiến:** auth; profile update; nhiều luồng (form, validation, auth persistence, session-rendered profile).
- **Bề mặt source:** `src/app/dashboard/settings/page.tsx` chỉ hiển thị name/email/role; `src/features/auth/client.ts`, `auth.config.ts`, `src/database/schema/user.ts`. Chưa thấy form sửa tên trong UI đã đọc. Chưa kết luận backend auth thiếu khả năng cập nhật profile.
- **Giá trị sử dụng giả định:** người dùng tự sửa tên hiển thị mà giữ nguyên danh tính đăng nhập.
- **Hành vi mới đề xuất:** form sửa name trên Settings; validate phía server, lưu và hiển thị lại đúng tên. Tiêu chí độ dài/normalization chờ Q12.
- **Cần giữ:** chỉ đổi tài khoản hiện tại; không đổi email, role, trạng thái xác minh hoặc các đơn hàng; tên được render an toàn; đăng nhập vẫn hoạt động.
- **Chấm dự kiến:** browser form + real auth session + DB; thử caller giả mạo user ID, input trống/dài và hai user. Không chỉ chấm component render hoặc gọi mock.
- **Chưa chốt:** giới hạn độ dài; trim; thời điểm session/UI phải thấy tên mới; nguồn nhu cầu thực tế nếu có.

## MT-A02 — Quản lý các phiên đăng nhập của chính mình

- **Miền / họ / loại dự kiến:** auth; session lifecycle; nhiều luồng.
- **Bề mặt source:** `src/features/auth/lib/auth.ts` đã export `listSessions`, `revokeSession`, `revokeOtherSessions`; `src/database/schema/session.ts`; Settings chưa có danh sách/controls này trong phần UI đã đọc. Auth config có cookie cache, cần kiểm tra semantics khi revoke.
- **Giá trị sử dụng giả định:** nhận biết phiên đăng nhập và kết thúc phiên trên thiết bị khác.
- **Hành vi mới đề xuất:** danh sách phiên của chính mình, đánh dấu phiên hiện tại, thu hồi một phiên khác.
- **Cần giữ:** không đọc/thu hồi phiên người khác; không lộ raw token; không nhầm current session; không đổi role/email/order state.
- **Chấm dự kiến:** nhiều cookie jars và database thật; thao tác UI rồi kiểm tra lại truy cập của phiên bị thu hồi. API/token không chỉ được giả lập.
- **Chưa chốt:** có cho tự thu hồi phiên hiện tại không; hiển thị metadata nào; hiệu lực ngay hay theo cache TTL. Không mặc định semantics của thư viện là yêu cầu nghiệp vụ của tác giả.

## MT-B01 — Tìm đơn theo mã trong lịch sử cá nhân

- **Miền / họ / loại dự kiến:** billing; history lookup; cục bộ.
- **Bề mặt source:** history page hiện đọc own orders; `list-orders.ts` có filter status nhưng không phải UI/code-search; `payment-content.ts` dùng order code trong thanh toán. History reference của development không có trong baseline giao agent.
- **Giá trị sử dụng giả định:** tra cứu một đơn đã biết mã.
- **Hành vi mới đề xuất:** GET search theo order code trong lịch sử của caller; empty query trở về lịch sử đầy đủ của caller.
- **Cần giữ:** ownership, thứ tự hiển thị, dữ liệu đơn và quy tắc mã thanh toán; tìm kiếm không mutate orders.
- **Chấm dự kiến:** hai user có mã gần giống nhau, nhiều ngày/trạng thái; browser submission hoặc HTTP form theo contract; test SQL wildcard/control input nếu contract cần literal matching.
- **Chưa chốt:** exact/prefix/substring; case sensitivity; trim và empty/no-match semantics.
- **Rủi ro family:** gần development history filter và các biến thể lookup khác. Phải gắn nhãn, không gọi đây là họ bằng chứng hoàn toàn mới; có thể chuyển reserve nếu tập chính quá thiên về history lookup.

## MT-B02 — Hủy nhiều đơn pending đã chọn

- **Miền / họ / loại dự kiến:** billing; order lifecycle; nhiều luồng.
- **Bề mặt source:** `cancel-order.ts` hỗ trợ một own pending order; history chỉ là bảng; `create-order.ts` hiện tự hủy các pending orders cũ của caller khi tạo đơn mới. Không giả định bình thường luôn có nhiều pending orders trong UI.
- **Giá trị sử dụng giả định:** dọn một nhóm đơn bỏ dở, chỉ hợp lý nếu tác giả xác nhận có workflow tạo nhóm pending như vậy. Nếu không có lý do nghiệp vụ, loại ứng viên thay vì dựng dữ liệu để hợp thức hóa.
- **Hành vi mới đề xuất:** chọn nhiều đơn và yêu cầu hủy cùng lúc; phải chốt atomic/partial semantics trước khi viết oracle.
- **Cần giữ:** không hủy đơn người khác/non-pending; không làm thay đổi payment completion và entitlements ngoài yêu cầu; single cancellation vẫn đúng.
- **Chấm dự kiến:** browser selections, real action transport và DB, nhóm trộn quyền/trạng thái; transaction checks nếu chọn atomic. Không mock chính transaction cần đo.
- **Chưa chốt:** nhu cầu nhóm pending có thật trong intended workflow; partial hay all-or-nothing; giới hạn batch; concurrent state changes.

## MT-U01 — Lọc vai trò trong danh sách quản trị

- **Miền / họ / loại dự kiến:** admin; account-directory lookup; cục bộ.
- **Bề mặt source:** `src/app/dashboard/admin/users/page.tsx` gọi `requireAdmin`, đọc tất cả user, đếm sessions và hiển thị bảng. Chưa thấy role filter trong UI/query đã đọc.
- **Giá trị sử dụng giả định:** admin tìm nhóm user/admin khi danh sách lớn.
- **Hành vi mới đề xuất:** role filter qua URL; total và session counts phản ánh đúng tập hiển thị theo contract.
- **Cần giữ:** non-admin không đọc danh sách; filter không thay đổi tài khoản; không trả session token; thông tin và thứ tự còn hiệu lực được bảo toàn.
- **Chấm dự kiến:** admin/user/anonymous sessions, mixed roles, users có 0/nhiều phiên, URL/input edge cases và browser control.
- **Chưa chốt:** default/invalid/repeated-role policy; total là tổng toàn hệ thống hay tổng sau lọc.
- **Rủi ro family:** gần pattern filter của development dù là workflow khác. Không dùng đổi domain làm lý do tự động coi các task độc lập; có thể reserve để tránh near-clone domination.

## MT-U02 — Trang chi tiết tài khoản cho admin

- **Miền / họ / loại dự kiến:** admin; account inspection; nhiều luồng (list, detail route, permissions, session aggregates).
- **Bề mặt source:** admin users page hiện đã hiển thị account metadata và session counts; auth `requireAdmin`; user/session schema. Chưa thấy trang detail riêng trong các routes đã liệt kê.
- **Giá trị sử dụng giả định:** admin xem một tài khoản và trạng thái phiên tổng hợp khi hỗ trợ vận hành.
- **Hành vi mới đề xuất:** mở detail từ một user trong danh sách; hiển thị name/email/role/email-verification/created-at cùng số phiên theo contract. Không thêm quyền quản trị đơn hoặc đổi role như một phần ngầm của task này.
- **Cần giữ:** admin-only kể cả gọi URL trực tiếp; không lộ raw session token; user không tồn tại xử lý rõ; list/search/count cũ không bị phá.
- **Chấm dự kiến:** direct-route authorization, users có các trạng thái/phiên khác nhau, thiếu user và điều hướng thực qua browser.
- **Chưa chốt:** chỉ đếm phiên đang còn hạn hay cả record; metadata nào được phép thấy; missing-user response; phạm vi hỗ trợ admin mong muốn.

## Điều kiện để tuyển một ứng viên

1. Tác giả xác nhận lý do sử dụng và business contract, hoặc ứng viên bị loại với lý do.
2. Kiểm tra runtime để xác nhận phần extension thực sự thiếu; không gọi API đã có là backend feature mới.
3. Chốt specification độc lập với gold file list và cách triển khai.
4. Reference và valid alternative qua evaluator trên cả hai layouts; plausible faulty variants bị đúng checks phát hiện.
5. Mapping visible V0/V1 và hidden checks không đưa yêu cầu bí mật hoặc clone fixtures.
6. Runtime tests ở mức cần thiết, gồm browser hoặc transaction/session invalidation khi contract yêu cầu. HTTP/DOM-only evaluator của smoke task không tự qualification các task này.
7. Chốt domain/family/locality classification, inclusion/exclusion và scope trước main outcomes; không chọn task theo điều kiện nào thắng.

Chưa chốt số task, tỷ lệ local/cross-flow hay repetitions. Một solution có thể thay đổi ít file hơn dự kiến và vẫn đúng. Không thiết kế tác vụ để cố làm layout đối chứng khó sử dụng. Cần review chất lượng của cả hai baseline và ghi giới hạn nếu chỉ có self-check.

</details>

</details>
