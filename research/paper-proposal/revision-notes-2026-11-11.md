# Bản viết lại theo bố cục nghiên cứu, 11/11/2026

## Bản hiện hành

Đọc `main-revised.pdf`; chỉnh sửa ở `main-revised.tex`. Bản hiện hành có 15 trang, bảy mục chính, bảy hình và hai bảng. Đã đọc và biên tập toàn bộ bảy mục cùng abstract theo humanizer và AGENTS.md. Không có mục nào bị bỏ qua. `main-revised.patch` được cập nhật so với `main.tex`; bản trước vẫn được giữ ở `main.pdf`/`main.tex`.

Introduction mở bằng tình huống ứng dụng đã có trong bản gốc, dẫn đến acceptance/preservation và câu hỏi can thiệp. Giữ ví dụ order-search là hypothetical, không thêm tình huống giả định mới. Background tổng hợp nghiên cứu theo chủ đề. Method gộp thiết kế, setup và kế hoạch phân tích; Results tách bằng chứng đã thu khỏi công việc dự kiến; Discussion diễn giải phạm vi và giới hạn; Conclusion chỉ kết luận tính khả thi của development workflow.

Cập nhật cục bộ sau phản hồi về quyền dùng lại task: §4.3 ghi giữ quyền chọn cho profile editing và có điều kiện cho session revocation nếu spike không đổi baseline. Contract, checks, fixtures, reference hashes, cap và quy tắc inclusion phải freeze trước pilot; task hoàn tất unchanged vẫn eligible bất kể pilot pass/fail/time. Substantive post-exposure revisions làm task thành development-only; main phải dùng fresh sessions và khai báo prior exposure. Table 1 và đoạn trạng thái trong Results được sửa cho nhất quán, không thêm empirical outcomes. Registry vẫn ghi not-ready/pending contract và qualification; hai functional families khác nhau được gắn shared Settings surface. Đây là follow-up edit cục bộ, không phải một vòng kiểm chứng literature mới. PDF vẫn 15 trang; References nối sau Conclusion để tránh trang gần trống. Đã kiểm tra trang Method thay đổi và trang Conclusion/References; không mất citation occurrences hoặc thay phương trình.

## Bằng chứng và phân bổ nội dung

| Nội dung | Phân loại và vị trí | Bằng chứng / giới hạn |
|---|---|---|
| Hai layout qua cùng checks | Qualification, Results 5.1 | `../execution/layout-qualification.md`; giữ phạm vi các hợp đồng đã kiểm tra |
| Bộ chấm nhận lời giải đúng khác cấu trúc và loại ba bản lỗi | Qualification, Results 5.1 | `../execution/history-filter-qualification.md`; không chứng minh oracle đầy đủ |
| Bốn phiên qua 16 acceptance và 13 preservation checks | Necessary support cho tính khả thi, Results 5.2 và Table 2 | `../execution/pilot-2026-11-11/summary.json`, protocol và report; một task development, không đưa vào main outcomes |
| Thời gian và command invocations | Descriptive observations, Table 2 / Results 5.2 | Cùng `summary.json`; không suy ra lợi thế chi phí hay tác động của feedback |
| Setup failure, HTTP/DOM-only và stubs | Interpretation-changing qualification, giữ trong Results/Discussion | Pilot report; không che hạn chế trong phụ lục |
| Image IDs, hashes, attempts, token events và logs | Provenance detail, companion archive | Kho pilot hiện có; chưa phải artifact đã công bố |
| Hiệu ứng layout/package và uncertainty | Chưa có bằng chứng chính | Giữ định nghĩa/phương trình trong Method, không điền số vào Results |

Chuỗi bằng chứng chính là baseline/layout qualification → evaluator qualification → bốn smoke sessions được chấm sau phiên → giới hạn câu trả lời cho RQ1–RQ3. Các phép ước lượng chính/phụ vẫn là kế hoạch; chưa thực hiện phân tích mới hoặc tạo dữ liệu mới trong lượt viết lại.

Giữ đủ 22 citation keys và mọi lần xuất hiện citation, kiểm tra tự động với bản trước khi sửa. Bốn equation environments giữ nguyên. Các nhận định literature không được mở rộng quá phạm vi đã ghi ở `citation-evidence.md` và review trước; không xác minh lại toàn bộ bibliography trong lượt này.

## Biên tập và kiểm tra lặp ý

- Gộp Study design và Outcomes and analysis plan thành Method and experimental setup. Chuyển feasibility đã có bằng chứng sang Results, thay câu lỗi thời rằng chưa chạy pilot bằng setup và outcomes có hồ sơ.
- Nêu joint success trong Introduction để định hướng; định nghĩa ở Method; trình bày quan sát ở Results; Discussion chỉ giải thích khả năng suy luận. Không lặp toàn bộ thời gian/check counts trong Discussion hoặc Conclusion.
- Bảng task phân biệt historical candidates, development task đã chạy và expanded-pilot proposals chưa chạy. Hình inventory 5 billing/1 admin được giữ như hồ sơ lịch sử, không coi là main sample.
- Ghi rõ hiện chưa có independent review hoặc second coding, không coi assistant checks là review độc lập. Thêm exploratory fallback được chốt trước main collection và mục tiêu chuẩn bị public artifact có author review.
- Giảm câu dẫn theo khuôn, câu phòng thủ trùng ý và dấu gạch ngang dài trong prose. Giữ các phân biệt cần thiết về điều kiện kiểm tra, tính bất định và giới hạn suy luận.

| Mục / nhóm mục | Trước | Sau |
|---|---:|---:|
| Introduction | 486 | 437 |
| Related work → Background and related work | 800 | 663 |
| Research questions | 198 | 193 |
| Study design + Outcomes and analysis plan → Method and experimental setup | 2569 | 2869 |
| Feasibility and reproducibility → Results (chuyển phần artifact sang Method, bổ sung pilot thực có) | 407 | 605 |
| Discussion and threats to validity | 279 | 367 |
| Conclusion | 91 | 92 |

Đây là số đếm từ gần đúng trên nguồn LaTeX tiếng Anh, gồm headings/captions và một số identifiers, không phải word count dùng cho submission. Ba Results subsections mới lần lượt có 181, 273 và 105 từ theo cùng cách đếm; bản cũ chưa có Results subsections tương ứng. Phần phương pháp dài hơn vì bổ sung setup pilot đã thực hiện; phần Results dài hơn vì nay có outcomes có nguồn.

## Cần tác giả kiểm tra trước khi dùng bản này

- Tên tác giả, affiliation và quan hệ baseline có repairs với bản thesis đã bảo vệ vẫn chưa được xác nhận lại.
- Đóng góp extension/replication vẫn chờ artifact-level comparison; main-task inclusion, configuration, repetition count, precision/interval method và stopping policy chưa khóa.
- Đọc lại cách diễn giải acceptance/preservation và giới hạn HTTP/DOM/stubs để bảo đảm có thể giải thích bằng lời của mình. Public artifact mới là mục tiêu chuẩn bị, chưa được công bố.
- Khai báo hỗ trợ AI theo yêu cầu của cơ sở/venue; giữ bản nháp, decisions và execution logs. Trợ lý không thay thế trách nhiệm kiểm tra nội dung của tác giả.

BibTeX và repeated pdfLaTeX thành công; log cuối không có missing citations/references, box overflow hoặc underfull warnings. Đã render toàn bộ PDF và xem riêng bảng task, bảng pilot và trang Discussion/Conclusion. Không chạy thêm model, qualification hay main experiment trong lượt này.

## Hồ sơ bản sửa trước trong cùng ngày

Phần dưới mô tả bản sửa trước khi cập nhật smoke pilot và quyết định Q16–Q18. Các phát biểu trạng thái cũ được giữ như lịch sử, không thay thế mô tả bản hiện hành ở trên.

## Bản đã sửa

- Đọc `main-revised.pdf`; mã LaTeX ở `main-revised.tex`.
- Bản trước vẫn ở `main.pdf` và `main.tex`; bibliography `references.bib` giữ nguyên.
- Hình tổ chức mã của bản sửa dùng `figures/organization-revised.tex`; hình cũ không thay đổi.
- `main-revised.patch` ghi khác biệt của phần LaTeX chính.

Đây vẫn là discussion proposal. Không có dữ liệu mới về agent, không có sample size hoặc kết quả can thiệp được bổ sung.

## Tóm tắt thay đổi

1. **Title và Introduction.** Nêu rõ controlled SmartKit case study. Đóng góp dự kiến là ước lượng tác động của hai can thiệp cụ thể, với uncertainty/cost/failure patterns. Khẳng định novelty vẫn chờ đối chiếu artifact.
2. **Related work.** Phân biệt supplied project checks của đề xuất với behavioral arm trong nghiên cứu Mehta, nơi model tự viết test. Giữ các citation cũ và bổ sung liên kết lập luận bằng các key đã có.
3. **Method.** Mô tả hai qualification snapshots đã dựng, layer-based là role-first grouping thực tế. Giữ tool permissions chung; V0 được tự viết/chạy test. Baseline repairs thuộc cả hai layout, không thuộc treatment.
4. **Tasks và hình inventory.** Giữ số đếm lịch sử 5 billing/1 admin. Nêu một derivative history-filter task đã được dùng cho development, không tính thành main task. Làm rõ các task chung family có thể overweight một workflow.
5. **Feasibility và Conclusion.** Thay mô tả chưa dựng baseline/layout bằng bằng chứng kiểm tra có thật. Tách rõ 14 unit/component checks, 10 baseline integration checks và 15 checks có reference khỏi agent outcomes. Nêu ranh giới HTTP, SQL, session/cache stubs và production runtime.
6. **Hình organization.** Dùng ví dụ vị trí module có trong manifest thay cho tên tính năng giả định; không thể hiện đường dẫn như yêu cầu lời giải task.

Không chuyển interaction thành primary hypothesis. Hai marginal effects, estimand theo tập task cố định và các phương trình giữ nguyên. Không đổi số task, số lần lặp, budget hay model chưa được tác giả chốt.

## Thuật ngữ giữ nhất quán

| Thuật ngữ | Nghĩa trong bản sửa |
|---|---|
| feature-based organization | Grouping theo domain/tính năng trong snapshot S1 |
| layer-based organization | Role-first grouping của snapshot S0, không mặc định Clean Architecture |
| behavioral verification package | Gói checks cung cấp thêm, gồm cả thông tin thực thi và feedback |
| joint success | Cả acceptance và preservation đều pass trong phạm vi evaluator |
| qualification | Kiểm tra baseline/task/evaluator để chuẩn bị công cụ, không phải đo agent performance |

## Claim-evidence map

| Claim | Bằng chứng | Trạng thái |
|---|---|---|
| Hai layout qua cùng checks cục bộ | `../execution/layout-qualification.md`, manifest và logs | Supported trong phạm vi đã kiểm tra |
| Có một development task, oracle thử với faulty và valid alternative implementations | `../execution/history-filter-qualification.md`, mutation results | Supported cục bộ, chưa review độc lập |
| Supplied tests khác với thay tool capability/self-authored tests trong nguồn Mehta | Primary PDF lưu tại `../execution/research-direction-review/sources/verification-pdf.md`; giữ citation `mehta2026verification` | Supported cho khác biệt setting/intervention; không chứng minh novelty |
| Layout hoặc verification package giúp agent tốt hơn | Chưa có trials | Needs evidence, không được khẳng định trong bản sửa |
| Đóng góp khác đủ rõ so với toàn bộ literature | Có targeted comparison, chưa exhaustive artifact audit | Chưa xác lập; định vị extension/replication còn mở |

## Phân bổ bằng chứng và cấu trúc

Introduction đi từ bài toán mở rộng và preservation đến câu hỏi can thiệp cụ thể. Method mô tả thứ thay đổi giữa điều kiện. Feasibility giữ các qualification counts; đường dẫn, hashes và logs đầy đủ nằm trong companion artifacts. Kết quả agent tương lai chưa được điền vào Results. Các giới hạn định nghĩa phạm vi diễn giải, không thay thế dữ liệu.

## Cần tác giả kiểm tra

- Quan hệ giữa snapshot gốc, baseline có repairs và bản thesis đã bảo vệ; tên tác giả/affiliation giữ theo bản cũ, chưa xác nhận lại.
- Intended business contracts, provenance của main tasks và phạm vi kết luận dự kiến.
- Định vị contribution là extension hoặc purposeful replication sau đối chiếu artifact có phiên bản; không xem câu chữ mới là xác nhận novelty.
- Model/harness, API budget, task/repetition count, precision/analysis/stopping policy và venue vẫn chưa chốt.
- Main trial isolation và hidden evaluator chưa triển khai; không diễn đạt chúng là đã hoàn tất.
- Các nguồn cũ được giữ nguyên, không xác minh lại toàn bộ bibliography trong lượt biên tập này. Khác biệt liên quan Mehta dựa trên primary PDF đã đọc ở lượt review trước.

Không thêm ví dụ nghiệp vụ giả định mới. Ví dụ order-search ban đầu vẫn được ghi rõ hypothetical. Giữ ghi chú, bản nháp, logs và khai báo hỗ trợ AI theo quy định của cơ sở/venue khi nộp.

## Kiểm tra bản sửa

BibTeX và repeated pdfLaTeX thành công. PDF có 14 trang; không còn missing citations/references hoặc box-overflow warnings ở lần build cuối. Đủ 22 citation keys của bản gốc được giữ; các equation blocks không đổi. Đã xem contact sheet toàn PDF và kiểm tra riêng trang có hình organization. Đây là kiểm tra bản thảo và bố cục, không phải thêm một lượt kiểm chứng thực nghiệm.
