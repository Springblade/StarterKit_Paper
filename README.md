> **Cập nhật 19/11/2026.** Next.js SaaS Starter và Makerkit Lite đã đạt kiểm chứng kỹ thuật trên ba tác vụ tài khoản. Thu thập dữ liệu chưa bắt đầu. Xem [kế hoạch hiện hành](research/paper-completion-plan.md) và [báo cáo kiểm chứng](research/execution/replacement-qualification-2026-11-19/README.md).

# Paper project - document map

| Purpose | Location |
|---|---|
| Current plan | [paper-completion-plan.md](research/paper-completion-plan.md) |
| Previous SmartKit progress | [paper-completion-tracker.csv](research/paper-completion-tracker.csv) |
| Previous SmartKit experiment protocol | [main48/protocol.md](research/execution/main48/protocol.md) |
| Manuscript draft | [LaTeX](research/paper-proposal/main-revised.tex), [PDF](research/paper-proposal/main-revised.pdf) |
| Manuscript history and instructions | [paper-proposal/README.md](research/paper-proposal/README.md) |
| Thesis | [LaTeX](latex/main.tex), [PDF](latex/main.pdf) |
| Application source | `research/SmartKit/` |
| Historical records | `archive/` |

## Execution files: keep, archive and restore

- `research/execution/main48/`: SmartKit instruments, packages, candidate solutions, qualification evidence and rehearsals from the previous design. Keep these paths intact.
- `research/execution/layouts/`, prepilot packages/solutions/checks and feasibility source overlays: read directly by current preparation/audit scripts. Keep these paths intact.
- Old pilot records, reports, logs and raw outcomes remain research evidence even when not read by the current runner. An old date alone is not a deletion criterion.
- The earlier manuscript `main.tex`/`main.pdf` remains a distinct historical draft and patch comparison baseline.

Cleanup on 16 November 2026:

1. Recycled 31 generated files (1.10 MiB): 16 Python cache files, 14 LaTeX auxiliary files and SmartKit's TypeScript cache. Preserved layout caches inside the experimental area.
2. Preserved the distinct PDF from the accidentally named `$paperBuildDir` as [main-revised-build.pdf](archive/research/paper-proposal/main-revised-build.pdf); removed the generated build directory.
3. Recycled 12 redundant historical `final-workspace/` extractions (1,732 files; 5.63 MiB) under pilot runs and prepilot rehearsals. Each source file matched its adjacent `final-workspace.tgz`; the only additional file was `.env`, reproducible from the corresponding runner's `env_text()` (with Windows line endings). All archives, outcomes, patches and logs were retained. To restore: extract the adjacent `.tgz` with Python `tarfile.extractall(..., filter='data')` into `final-workspace/`, then regenerate `.env` using `env_text()` in the old pilot's `pilot.py` or prepilot's `local-runtime.py`.

4. Archived the two historical qualification trees as ZIPs, then recycled their loose directories (2,027 files). Every archived entry was compared against the original file digest and ZIP integrity was checked. Archives: [prepilot qualification](archive/research/execution/prepilot-2026-11-12-qualification.zip) and [pilot qualification](archive/research/execution/pilot-2026-11-11-qualification.zip). Current `main48` does not read these two trees; their parent reports and summary records remain in place. Historical scripts or manual review that require loose evidence must restore the archives first. ZIP entries contain paths relative to this project root: run `Expand-Archive -LiteralPath <zip-path> -DestinationPath <project-root>` to restore original locations. Do not unpack into the qualification directory itself.

5. Final redundancy cleanup on 16 November 2026 recycled another 1,865 files (7.13 MiB) without creating new archives: completed `main48/rehearsal/*/final-workspace/` extractions, redundant `main48/qualification/*/solution/` copies, two layout TypeScript caches and Python bytecode. Rehearsal extractions matched their retained adjacent `.tgz` archives exactly; only completed, passed rehearsal records were selected. Qualification copies matched both the canonical `main48/solutions/<layout>/<task>/<variant>/` files and the solution-manifest binding recorded in their run summaries; historical mismatches were kept. Run logs, summaries, ledgers, source manifests and canonical solutions were retained. To restore a rehearsal extraction, extract its adjacent `.tgz` into `final-workspace/`. To restore a removed qualification `solution/`, copy the canonical variant identified by its `summary.json` only while its manifest still matches that summary's binding; otherwise restore from Recycle Bin. No existing study freeze included the removed paths. Current package/source audits were rerun after cleanup. The earlier statements about retaining all main48 extractions and layout caches describe the earlier cleanup stage and are superseded by this entry.

Recycled items can be restored through Windows Recycle Bin. Disk space is not reclaimed until the bin is emptied. The dated notes below record planning history; use the current plan and protocol for operational decisions.

---

> **Cập nhật thực thi 16/11/2026:** bộ hồ sơ chuẩn bị cho 48 slots nằm tại [main48](research/execution/main48/protocol.md). Đã dựng 24 packages, hợp đồng public, bộ chấm browser/auth/webhook/cron HTTP, runner có chốt start và phân tích prospective. Đang hoàn tất qualification toàn V0, reliability và 24 rehearsal; chưa technical freeze và chưa gọi model thí nghiệm. Không coi các probes trước đây là main admission. Trạng thái quyết định được tính lại bằng `main48/audit.py`; không chạy `collect.py run` trước freeze và start release.

> **Current roster revision (15 November 2026):** keep A01/U02/U03; replace A03/B03/B04 with A04 password policy, B05 payment-code recognition, B06 expiry enforcement. Still 48 held slots, no new pilot. Replacement tasks pass bounded runtime/fault checks on both layouts; full qualification remains incomplete. The 24 correct cases/12 fault cases below concern the old roster. Current CSV has 14 candidates plus one history task. [Current plan](research/paper-completion-plan.md) supersedes older roster/count statements below. Prospective manuscript sections have been synchronized; final readiness remains pending.

# Thesis và nghiên cứu paper SmartKit

**Model collection is on hold.** Feasibility probes pass, but G1 treatment reach, G2 preservation gate, G3 full task validity and G4 research value must pass before release of48 slots. [Current hold plan](research/paper-completion-plan.md).

[Kiểm chứng runtime sáu task](research/execution/task-feasibility-2026-11-15/report.md),15/11:24 reference/alternative/layout cases pass,12 seeded-fault/layout cases detected,0 agent trials. Source baseline giữ nguyên. Khả thi kỹ thuật đã có; chưa khuyến nghị release48 cho claim ảnh hưởng thiết kế mạnh vì treatment relevance còn yếu.

[Xác minh giá trị trước chạy](research/execution/research-direction-review/assessment.md), 15/11/2026: tiếp tục có điều chỉnh; chưa release48. Đã đối chiếu thêm nguồn gần nhất và tính sensitivity local; không có agent trial mới.

Cập nhật 15/11/2026 sau nghiên cứu nguồn. **Đề xuất vẫn là 6 task × 4 điều kiện × 2 lần = 48 runs trong một lịch**, không có pilot mới/chạy bù model. Roster mới thay tìm mã đơn B01 bằng admin đổi role U03 để thêm thao tác ghi có phân quyền; task này còn phải qua kiểm tra cache/contract và qualification. Chưa có main task hoặc lịch nào được release.

Bắt đầu tại [plan đọc nhanh](research/paper-completion-plan.md): ba điểm yếu và cách xử lý, sáu task, số runs, điểm dừng và sản phẩm cần cho paper. Đóng góp dự kiến gắn so sánh S/V với audit test trên toàn bộ mã agent đã lưu; phân tích bổ sung không làm tăng cỡ mẫu hay bảo đảm công bố.

## Tài liệu đang sử dụng

- [Plan đọc nhanh](research/paper-completion-plan.md): sáu task, 8 runs/task, tổng 48; một đợt thu dữ liệu.
- [Plan thực nghiệm](research/execution/pilot-task-plan-v2.md): RQs, block allocation, phương pháp/denominators, trace codebook, audit V0/V1/hidden evaluator.
- [Registry](research/execution/main-task-candidates-v1.md), [CSV](research/execution/main-task-candidates-v1.csv): A01 A04 B05 B06 U02 U03; B01 ngoài đợt; qualification chưa hoàn tất.
- [Nguồn vừa đối chiếu](research/paper-proposal/citation-evidence.md#48-run-study-evidence-review--15-november-2026): SIGSOFT/Lakens và năm nghiên cứu gần nhất; những phần đã có và phần SmartKit dự kiến kiểm tra thêm.
- [Tracker](research/paper-completion-tracker.csv): preparation, một collection, audit toàn patches và hoàn thiện bài.
- Bản thảo hiện hành: [PDF](research/paper-proposal/main-revised.pdf), [LaTeX](research/paper-proposal/main-revised.tex), [BibTeX](research/paper-proposal/references.bib), [ghi chú](research/paper-proposal/README.md). PDF/LaTeX chưa cập nhật roster/RQs/audit mới; cần đồng bộ phần kế hoạch trước collection, giữ development results.
- Proposal [Word](research/smartkit-proposal.docx)/[Markdown](research/smartkit-proposal.md), [protocol v0](research/smartkit-study-protocol-v0.md), [audit v0](research/smartkit-task-audit-v0.csv): hồ sơ lịch sử, không là allocation hiện hành.
- [Bảng nguồn](research/evidence-ledger-v2.csv); `research/SmartKit/`: source tham chiếu.

12 task đã ghi nhận = 11 ứng viên + history task riêng. Chỉ history có 4 agent runs cũ, không cộng vào 48. DP-02 development-only, DP-04 hold. Trần mới 12 giờ agent; chấm offline tối đa 144 suite passes ban đầu, cộng preparation/qualification riêng. Runner source difference đã xác định là `docker rm -v`, runtime liên quan vẫn cần kiểm tra. Không gọi model hoặc thay application/freeze trong lượt research/viết plan.

## Thesis

- [PDF chính](latex/main.pdf), [source](latex/main.tex), [bibliography](latex/references.bib).
- `latex/thesis_cover.tex` và các file `.tex`/PDF trong `latex/figs/` được giữ để biên dịch thesis. Hai PDF hình được main.tex sử dụng trực tiếp.
- Log, cache và file phụ trợ LaTeX có thể được sinh lại khi biên dịch.

## Lịch sử lưu trữ

- [Khảo sát tài liệu](archive/research/research-landscape-v2.md): căn cứ, giới hạn và các hướng đã cân nhắc; kế hoạch hiện hành nằm trong protocol.
- `archive/research/scout-*.md`: ba ghi chú kiểm chứng nguồn chi tiết.
- `archive/research/`: cũng giữ định hướng boundaries và brief trước đây làm hồ sơ quá trình nghiên cứu.
- `archive/research/researchwrite/smartkit-proposal/`: hồ sơ bằng chứng, rà soát và script xuất Word của proposal; không phải kế hoạch nghiên cứu mới.
- `archive/thesis/main-build.pdf`: PDF trước nằm ở `latex/build/`, khác nội dung nhị phân với PDF chính; chưa xác định bản nào là bản bảo vệ cuối cùng.
- `archive/thesis/references.bib.backup`: có các mục riêng không còn trong bibliography hiện tại; giữ nguyên, chưa coi là nguồn đã xác minh.
- `archive/thesis/confound-taxonomy-table.tex`: bảng riêng chưa được main.tex gọi; giữ như bản nháp lịch sử.

Đợt dọn dẹp 2026-11-10 xóa 37 file biên dịch sinh tự động (2.13 MiB), chuyển 5 file lịch sử vào archive và giữ nguyên source thesis/SmartKit. Không chạy biên dịch hay thí nghiệm mới trong đợt này.

Sau đó chuyển thêm báo cáo khảo sát và ba ghi chú scout vào `archive/research/`; không xóa nội dung nghiên cứu.

Đợt dọn tiếp theo ngày 2026-11-10 xóa 56 file phụ trong `research/paper-proposal/` (9.79 MiB): ảnh render/preview, bản trích xuất văn bản từ PDF và file phụ LaTeX. Giữ PDF hiện hành, toàn bộ nguồn, hình được manuscript sử dụng, báo cáo rà soát và bằng chứng trích dẫn. Giữ log thực thi trong `research/execution/logs/` để đối chiếu kết quả; không thay đổi working tree SmartKit.

Đợt dọn ngày 2026-11-11 chuyển 2.803 file sinh tự động (1.182,74 MiB) vào Windows Recycle Bin: ba thư mục `.next` của SmartKit/hai layout, cache Python của runner và bảy file phụ/log biên dịch paper. Có thể khôi phục từ Recycle Bin; chưa giải phóng dung lượng ổ đĩa cho đến khi thùng rác được dọn. Giữ `node_modules`, source, PDF/bibliography/hình, các bản thảo có lịch sử riêng, scripts, snapshots, raw outcomes và logs thí nghiệm. Lần chạy Next.js hoặc LaTeX tiếp theo sẽ tạo lại cache/file phụ và có thể chậm hơn lần chạy dùng cache.

## Quy ước quản lý file

- Chỉ tạo file mới khi thật sự cần để hoàn thành công việc hoặc khi người dùng yêu cầu. Ưu tiên sửa file hiện có và trả lời trực tiếp trong chat; không tự tạo thêm báo cáo, ghi chú hay bản sao cho mỗi lần xử lý.
- Sửa trực tiếp bản hiện hành; tránh tạo các bản `final`, `revised` hoặc bản sao chỉ để xem trước.
- Ảnh render và văn bản trích xuất để kiểm tra PDF đặt trong thư mục tạm ngoài project; xóa sau khi kiểm tra. File phụ LaTeX có thể xóa sau khi hoàn tất biên dịch, giữ PDF để đọc.
- Giữ nguồn LaTeX/BibTeX, dữ liệu, script tái tạo hình và bằng chứng kiểm chứng. Không xóa log thí nghiệm đang được báo cáo viện dẫn.
- Chỉ đưa vào `archive/` tài liệu lịch sử có nội dung riêng cần giữ; không dùng archive để chứa cache hoặc ảnh preview. Cập nhật README hiện có thay vì tạo thêm báo cáo dọn dẹp riêng.
