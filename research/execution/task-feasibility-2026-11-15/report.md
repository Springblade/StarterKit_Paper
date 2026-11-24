# Kiểm chứng bổ sung roster mới — 15/11/2026

**Ba task thay thế khả thi trong phạm vi thử; đã có bằng chứng phát hiện regression trên hành vi cũ. Chưa release 48 model runs.** Đây là kiểm tra phần mềm với PostgreSQL/Chromium thật, không phải agent trials.

| Phép thử | Kết quả |
|---|---|
| A04/B05/B06 × hai biến thể × hai layouts | 12 trường hợp pass runtime, basic suite và typecheck |
| Baseline ba task × hai layouts | 6 trường hợp giữ nghĩa vụ cũ nhưng chưa đáp ứng acceptance mới |
| Ba regression faults × hai layouts | 6 trường hợp pass basic/typecheck nhưng bị assertion bảo toàn bắt |
| Directory cũ trên baseline và reference U02/U03 × hai layouts | 6 trường hợp pass checker bảo toàn DP02 cũ |
| Sai role guard dùng chung trên reference U02/U03 × hai layouts | 4 trường hợp bị check directory cũ bắt, basic/typecheck vẫn pass; chỉ **một** fault template |
| Production build của overlay reference gộp A04/B05/B06 | Pass trên cả hai layouts; không phải build riêng từng task |
| Source integrity | 284 bản ghi baseline vẫn khớp manifest |

Basic suite là **4 files / 14 tests của package được cung cấp**, giữ nguyên snapshot, không phải mọi test upstream. Hai biến thể triển khai task mới có thuật toán gần nhau; khác biệt biểu thức chưa chứng minh oracle chấp nhận rộng các lời giải khác.

A04 được thử qua browser/API: biên 11/12/128/129, login mật khẩu cũ, invalid reset token và identity. Fault hạ trần 128 xuống 127 bị check bảo toàn bắt. B05 giữ mã chuẩn có chữ hoa/thường và `_`/`-`, kiểm tra marker/whitespace/ambiguity, webhook có chữ ký và processor integration; fault lowercase mã làm hỏng hành vi cũ. B06 kiểm tra quá hạn, đúng biên với clock kiểm soát, signed webhook, audit, live completion, mismatch/terminal/outbound/duplicate và năm cleanup races trong mỗi probe; fault từ chối cả đơn còn hạn bị bắt. U02/U03 giữ admin-only directory, rows/session counts, không lộ token và identity/orders qua checker cũ.

**Hai phát hiện phải đưa vào contract:**

1. B05 ban đầu chỉ cho chữ/số nhưng baseline dùng nanoid(8). Đã sửa đề xuất để nhận cả `_` và `-`, giữ case, thêm tests; không đổi generator/baseline.
2. Baseline có thể trả hai kết quả `completed` khi hai transaction IDs khác nhau đến đồng thời cho một đơn. Check này là **diagnostic**, không phải preservation. Chưa có bằng chứng cấp entitlement hai lần: entitlement hiện dựa trên một order row. Reference B06 dùng row lock và server decision time; public concurrency/response contract vẫn cần chốt trước freeze, không ép agent theo implementation này.

**Đánh giá G1–G4:** G1 có căn cứ tốt hơn vì ba task mới đổi quy tắc trong relocated shared modules; chưa có measured agent navigation/effect. G2 có bounded differential detection trên hành vi cũ, khác với fault acceptance mới của đợt trước; A01 dùng evidence cũ. G3 vẫn chưa đủ: chưa actual cron HTTP với nguồn SePay giả lập; direct module probes chưa chấm được mọi valid implementation; chưa tách V1 package/hidden evaluator, chưa reliability theo protocol và alternative đủ khác. G4 chỉ hỗ trợ tiếp tục chuẩn bị case study thăm dò, chưa bảo đảm effect hoặc công bố.

Trước 48 runs cần hoàn tất contract, actual-transport/independent oracle, reliability và exposure audit của 24 packages, đồng bộ manuscript, rồi author review/freeze. Không thêm pilot hoặc tăng runs. Production compile bổ sung ghi riêng trong `replacement-build-results.json`; đó là overlay reference gộp, không phải build riêng từng task.

[Ma trận đã assert và giới hạn](replacement-qualification.json), [raw replacement results](replacement-results-1794756305953791300.json), [raw admin results](admin-preservation-results-1794756417513119800.json). Scripts tái lập: `qualify-replacements.py`, `replacement-auth.cjs`, `replacement-billing.ts`, `qualify-admin-preservation.py`, `summarize-replacements.py`, `build-replacements.py`.

Các lượt development lỗi vẫn giữ logs, không tính là reliability: session browser bị redirect, thiếu shim server-only, import khác layout và TypeScript của probe. Một số fault overlay bị reset ghi đè; generator/logs cho phép tái tạo nhưng không phải exact archived fault snapshots. Chi tiết phạm vi/provenance ở JSON. Phần dưới là **báo cáo roster cũ**, không chuyển evidence sang task mới.

---

# Kiểm chứng sáu task trước thực nghiệm

Ngày 15/11/2026. **Đã chạy kiểm tra cục bộ bằng Chromium và PostgreSQL thật, không gọi model thí nghiệm.** Cả sáu task có hai cách triển khai qua phép thử trên cả hai layouts. Tuy nhiên, kết quả chưa đủ để release thiết kế 48 runs cho mục tiêu so sánh ảnh hưởng của tổ chức mã và preservation checks.

## Kết quả đã chạy

| Task | Reference + alternative trên hai layouts | Hành vi đã kiểm tra |
|---|---|---|
| A01 / DP-03: sửa tên | 4 trường hợp pass | Dùng lại final evaluator/visible suite đã có; ghi tên, validation, quyền và preservation trong scope cũ |
| A03: đổi mật khẩu | 4 trường hợp pass | Form thật, current password sai, confirmation/độ dài sai, anonymous, đổi thành công, old/new sign-in, identity/orders |
| B03: tiếp tục đơn | 4 trường hợp pass | Đi từ history sang đúng pending order; reload không tạo đơn; foreign/terminal/expired bị chặn; mua mới, status ownership và cancel qua UI cũ |
| B04: biên nhận | 4 trường hợp pass | Tải file JSON thật, dữ liệu đúng, own/completed-only, foreign/anonymous/missing/non-completed bị chặn, read-only |
| U02: chi tiết account | 4 trường hợp pass | Link từ directory, metadata/session aggregate, no token, direct-route permission và missing account |
| U03: đổi role | 4 trường hợp pass | Form thật, promotion/demotion, current server role, stale-cookie caller bị chặn, fresh-login quyền đúng, self-demotion/input/CSRF và state bảo toàn |

**24 trường hợp triển khai đúng = 6 task × 2 cách triển khai × 2 layouts.** Mỗi trường hợp có browser/API/DB checks và typecheck. Unit tests/build có log cho từng candidate/layout; năm trường hợp feature-reference được bổ sung bằng lượt chỉ chạy basic checks trên cùng source. Đây là lượt kiểm tra phần mềm, không phải 24 agent runs hoặc phép lặp reliability.

**12 trường hợp lỗi cấy = 6 lỗi × 2 layouts**, đều bị assertion dự kiến phát hiện và vẫn typecheck:

- A03: bỏ kiểm tra confirmation.
- B03: bỏ ownership khi resume.
- B04: bỏ ownership khi download.
- U02: hạ guard từ admin xuống chỉ đăng nhập.
- U03: dùng role cache để cho phép ghi; bỏ self-demotion guard.

Các lỗi này thuộc hành vi tính năng mới; chưa chứng minh V1 preservation phát hiện được chúng. Một số lỗi làm sai state nên kéo theo assertion khác; giữ cả lỗi kế tiếp trong logs, không đếm thành các observations độc lập. Lỗi cấy không là lỗi agent đã tạo hoặc ước lượng tần suất lỗi thật.

## U03 đã kiểm chứng được gì?

Trên cả hai layouts, API baseline cho phép promotion/demotion; fresh login thấy quyền đúng. Cookie cũ vẫn có thể trả role `admin` trong dữ liệu session cache sau demotion, nhưng API admin có sẵn từ chối lệnh ghi bằng quyền cũ (HTTP403). Reference mới đọc quyền có thẩm quyền rồi ghi role; alternative dùng lại handler admin của auth sau kiểm tra task-specific. Cả hai từ chối caller đã bị demote.

API cũ cũng cho phép self-demotion. Vì vậy quy tắc chặn self-demotion trong task được giới hạn rõ ở feature mới, không được trình bày là đã tồn tại trên mọi endpoint. Không sửa auth config, cache hay dependency của baseline. Cảnh báo plugin order của baseline được giữ nguyên và ghi trong logs, không giả là zero warnings.

## Phát hiện có ảnh hưởng tới hướng nghiên cứu

**Toàn bộ 12 cặp task–implementation đang có đều sửa 0 module cũ đã được di chuyển giữa hai layouts.** Năm task mới được thực hiện bằng sửa/thêm các route App Router có cùng vị trí trong cả hai layouts. A01 thêm module theo layout nhưng cũng không sửa relocated existing code.

Imports tới các modules được di chuyển vẫn có, đặc biệt B03 dùng lại payment/auth/billing helpers. Do đó kết quả trên không chứng minh S không có tác động: agent có thể tìm/đọc các modules đó khác nhau. Nó là phản ví dụ với kỳ vọng rằng danh mục này buộc agent xử lý các thay đổi sâu trong tổ chức mã. Số file không được dùng làm quota hoặc bắt lời giải đi đường dài; workload cần nhu cầu nghiệp vụ có lý do trước khi chọn thay đổi.

**Khả thi triển khai đã được chứng minh trong phạm vi thử; khả năng tạo bằng chứng cho cả S và V vẫn chưa được xác lập.** Các lỗi nổi bật của năm task mới nằm trên feature mới. V1 theo thiết kế chỉ có checks chạy được trên baseline chưa giải. Không được đưa acceptance mới vào V1 rồi gọi đó là preservation, hoặc cấy lỗi xa task chỉ để V1 thắng.

Vì vậy, đánh giá hiện hành là **chưa chạy đợt48 như một nghiên cứu nhằm khuyến nghị hai lựa chọn thiết kế**. Có thể giữ đây là workload bổ sung UI/endpoint để khảo sát thăm dò với scope hẹp, nhưng việc đó không tự đáp ứng kỳ vọng về đóng góp nghiên cứu mạnh. Không tăng số runs và không đổi câu hỏi hay roster âm thầm. Bước quyết định tiếp theo phải là workload/câu hỏi có quan hệ thực với can thiệp, thay vì tiếp tục lặp tests trên bộ task này để lấy đủ số.

## Phạm vi chưa đạt, không gán là đủ qualification

- Các probes mới dùng routes/labels của candidate: chưa phải hidden evaluator frozen chấp nhận arbitrary agent solutions/transports.
- Chưa có V0/V1 preservation matrix hoàn chỉnh cho năm task mới; chưa làm reliability20/30 rounds hoặc main package/exposure qualification.
- B03 chưa chứng minh toàn bộ concurrent completion/cancel, session expiry trong lúc mở trang hoặc idempotency dưới races; các phần này còn ngoài evidence vừa chạy.
- Không có actual agent trace hoặc effect estimate mới. Reference imports không thay bằng chứng agent thật đã đọc mã.
- Chưa có reviewer con người độc lập hoặc quyết định rằng48 có precision hữu ích cho claim mạnh. Kết quả sensitivity trước đó vẫn còn hiệu lực trong assumptions đã ghi.

## Môi trường và tính toàn vẹn

Image cũ không còn trên máy. Đã dựng `smartkit-feasibility:20261115` từ lockfile được lưu, Node24.22.2, pnpm11.7.0 và Playwright1.58.2/Chromium145.0.7632.6. Image mới không cài Codex CLI hoặc mang credentials tài khoản; nó không được giả là đúng image cũ. Mỗi case dùng container/DB riêng, không host research mounts hoặc Docker socket, dữ liệu synthetic cục bộ; baseline source snapshots giữ nguyên.

Đối chiếu **284 bản ghi manifest của hai layouts đều khớp**. `local-runtime.py` chỉ khác freeze cũ ở `docker rm -v`; đã kiểm tra vòng start/stop và xác nhận anonymous volume của từng DB thử được xóa. Không sửa freeze cũ để xóa mismatch. Không dọn các containers/volumes của dự án khác.

Tổng có **47 invocations kiểm chứng**, gồm31 passed,12 detected và4 lượt lỗi phát triển được giữ log: một lỗi quote của version-probe; một candidate U03 chưa đúng types; một probe U03 chờ URL quá sớm làm state kiểm tra chồng; một candidate/probe U02 thiếu null guard và chờ navigation. Đã sửa nguyên nhân trước các lượt pass cuối. Đây không phải bằng chứng47 lần liên tiếp không flaky; các phiên bản development phải tách khỏi reliability cuối.

## Hồ sơ và chạy lại

- [summary.json](summary.json): bảng case/log, mọi trạng thái và giới hạn.
- [source-evidence.json](source-evidence.json): paths/modules theo layout và kết quả manifest.
- `runs/`: logs, results, screenshot và source candidate được lưu ở các lượt sau khi bổ sung provenance; một số phiên bản lỗi đầu chưa có source archive, không phục dựng giả.
- [verify.py](verify.py), [probe.cjs](probe.cjs), [task-probe.cjs](task-probe.cjs): kiểm tra có assert, không có model client.
- [build-references.py](build-references.py), [build-alternatives.py](build-alternatives.py): tạo candidate trong thư mục riêng; không viết vào baseline.

```powershell
python -X utf8 research/execution/task-feasibility-2026-11-15/source-check.py
python -X utf8 research/execution/task-feasibility-2026-11-15/summarize.py
# Chỉ khi cần tái kiểm tra runtime; mỗi invocation tạo thư mục log mới:
python -X utf8 research/execution/task-feasibility-2026-11-15/verify.py --layout feature --task U03 --phase reference
```

Các forms trong candidate dùng label, POST và server-side validation theo guide `forms` của modern-web-guidance: “Never treat browser constraints as a data integrity defense.” Có screenshot trình duyệt để kiểm tra hiển thị; đây không phải vòng polish giao diện production.
