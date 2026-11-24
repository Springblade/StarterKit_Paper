# Chỉ số chi phí cho thí nghiệm starter-kit dùng agent cố định

Ghi chú nghiên cứu, không phải kết quả thực nghiệm. Đã đối chiếu phần phương pháp và bảng trong bốn bản toàn văn dưới đây; các giá trị minh họa là kết quả của nguồn, không phải kết quả starter-kit. Không cần đưa ngày lịch, hash hoặc commit ID vào bảng của manuscript. Hồ sơ giá, cấu hình và dấu vết kiểm chứng thuộc artifact.

## Bằng chứng trực tiếp từ paper

| Nguồn toàn văn | Vị trí đã kiểm tra | Định nghĩa, mẫu số và điều cần tránh |
| --- | --- | --- |
| [Yang et al., SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/html/2405.15793v3) | §4, đoạn “Metrics”; Table 1 | `Avg. Cost` là API inference cost trung bình **trên các instance giải thành công**. Có ngân sách mỗi instance và tự nộp bản sửa khi vượt ngân sách. Vì vậy không diễn giải cột này thành tổng chi phí tất cả lượt chạy chia số thành công. |
| [Xia et al., Agentless: Demystifying LLM-based Software Engineering Agents](https://arxiv.org/html/2407.01489v2) | §4, đoạn “Metrics”; Table 1; §5.1 | Báo cáo average inference cost và average input/output tokens. Dòng Agentless trên 300 bài có 96 bài thành công, $0.70 average cost và 78,166 average tokens. Phần định nghĩa không nói rõ mẫu số bằng cách tường minh như SWE-Effi; không suy ra quy tắc loại failure từ nhãn `average`. Kết quả baseline lấy từ nhiều nguồn, nên không mặc định mọi cột có cùng quy tắc hạch toán. |
| [Fan et al., SWE-Effi: Re-Evaluating Software AI Agent System Effectiveness Under Resource Constraints](https://arxiv.org/html/2509.09853v2) | §3.1–3.2; Tables 2–3; §5.4; Appendix §7.1 | Table 2 nói rõ trung bình trên **cả resolved và unresolved**; ghi riêng input/output tokens và requests. Table 3 phân tầng thành công/thất bại, cho thấy xu hướng failure tốn nhiều tài nguyên, không phải quy luật cho mọi cấu hình. CPU time tách khỏi inference. “Normalized inference time” là dự đoán từ mô hình hồi quy, không phải thời gian thực người dùng chờ. EuCB dùng đơn giá tham chiếu, không xác nhận hóa đơn thực trả. |
| [Guo et al., EET: Experience-Driven Early Termination for Cost-Efficient Software Engineering Agents](https://arxiv.org/html/2601.05777v2) | §4.5, “Evaluation Metrics” | Resolution rate là tỷ lệ task có patch vượt các test. API calls, input/output tokens và USD được định nghĩa là **tổng trên benchmark**, hỗ trợ báo cáo tài nguyên toàn bộ lần đánh giá thay vì chỉ các task thành công. Đây là bản arXiv đã đọc; không suy ra trạng thái phản biện từ nơi lưu trữ. |

## Bộ chỉ số tối thiểu đề xuất

Giữ acceptance và preservation là kết quả chính. Chi phí và thời lượng là kết quả phụ, giúp giải thích liệu cải thiện chất lượng có đi kèm thay đổi tài nguyên. Đây là đề xuất phương pháp cho starter-kit, không phải tuyên bố rằng cả bốn nguồn đều dùng cùng bộ chỉ số.

Ký hiệu: N là số lượt chạy đã bắt đầu theo thiết kế; A_i là acceptance; P_i là preservation; Q_i = A_i AND P_i nếu tiêu chí thành công đã được định trước như vậy; S = sum(Q_i). Không đổi định nghĩa acceptance hiện có chỉ để tính chi phí. Nếu acceptance đã bao hàm preservation thì Q_i = A_i. Phải công bố tiêu chí nào được dùng ở mẫu số.

| Chỉ số | Cách tính/đơn vị | Quy tắc |
| --- | --- | --- |
| Input và output tokens mỗi lượt chạy | sum(input_i)/N; sum(output_i)/N | Gộp mọi lời gọi trong lượt chạy, kể cả lặp sửa và test. Giữ hai loại riêng; có thể thêm tổng input+output để đọc nhanh. Chỉ tính khi đủ dữ liệu; nếu thiếu, báo độ bao phủ và mẫu số quan sát được. |
| Thời lượng mỗi lượt chạy | elapsed_seconds, đổi sang phút nếu thuận tiện | Báo mean và median [IQR] trên mọi lượt chạy; timeout giữ thời gian đã tiêu thụ đến khi dừng. Ghi rõ mốc bắt đầu/kết thúc và có tính setup/chấm độc lập hay không. Không gọi wall-clock là CPU time hoặc normalized inference time. |
| USD mỗi lượt chạy | sum(C_i)/N | Chỉ gọi là chi phí thực trả khi có chứng từ/API billing tương ứng. Trong thiết lập subscription hiện tại, chỉ có thể báo **ước tính theo đơn giá API tham chiếu**, nếu dữ liệu và đơn giá đã được xác minh. |
| USD cho mỗi kết quả đạt tiêu chí | sum(C_i)/S | Tử số bao gồm chi phí failure và timeout. Khác sum(C_i cho Q_i=1)/S, vốn chỉ là chi phí trung bình trong nhóm thành công. S=0 thì để “không xác định”, kèm tổng chi phí và 0/N thành công. |
| Lượt thất bại/timeout và độ phủ usage | số lượng/N | Phân loại lý do dừng; báo số lượt có usage hoàn chỉnh. Có thể phân tầng tài nguyên theo Q_i để giải thích failure, nếu cỡ mẫu đủ. |

Nếu có nhiều lần lặp cho cùng task, phải nói rõ “per run/attempt” hay “per unique task”. Chỉ số theo unique task phải cộng chi phí mọi attempt thuộc task theo một chính sách retry cố định. Không được dùng số task duy nhất làm mẫu số nhưng chỉ giữ chi phí attempt được chọn.

## Hạch toán tokens và USD trong thiết lập hiện tại

Theo thông tin kiểm tra mã do parent cung cấp: collector ghi `elapsed_seconds`, ghi `usage_events` khi nhận `turn.completed`; bộ phân tích cộng input, cached input và output. Đây là thông tin triển khai cần đối chiếu với artifact thực tế trước khi mô tả trong manuscript.

- Cached input thường được cung cấp như một phần của input: chỉ cộng `input + output` sau khi kiểm tra schema; không cộng cached input lần nữa. Báo cached-input tokens riêng hoặc tỷ lệ cache hit để giải thích chênh lệch ước tính USD. Nếu schema khác, theo schema thực tế.
- Nếu provider trả reasoning tokens là phần con của output, không cộng lần nữa; nếu không xuất trường này thì ghi “không quan sát riêng”, không coi bằng 0. Chỉ so sánh cùng agent/model/tokenizer như thiết kế hiện tại, không diễn giải tổng tokens thành lượng tính toán phổ quát.
- Timeout/crash trước `turn.completed` có thể đã dùng tokens nhưng chưa ghi usage. Đánh dấu missing/incomplete; không quy thành 0, không âm thầm loại khỏi trung bình. Nếu không khôi phục được, công bố coverage và chỉ gọi tổng quan sát được là tổng đã ghi nhận, không phải toàn bộ tiêu thụ.
- Subscription ChatGPT không cung cấp chi phí API thực trả cho từng task. Không chia tiền gói tháng cho task rồi gọi đó là marginal inference cost; cũng không gọi mức phí API giả định là hóa đơn. Không dùng paid API key chỉ để tạo một cột USD cho paper.
- Nếu cần ước tính USD, lưu đơn giá và quy tắc trong artifact: input không cache, cached input, output, cùng các loại phí thực sự áp dụng. Công thức tham chiếu chỉ hợp lệ sau khi xác nhận cached input nằm trong total input: C_i = (I_i-K_i)*p_input + K_i*p_cached + O_i*p_output, với đơn vị giá quy đổi nhất quán. Nếu có cache-write hay bậc giá khác thì hạch toán theo schema, không ép vào công thức này. Không tự điền đơn giá chưa kiểm chứng.

## Quyết định có thể áp dụng ngay

Với dữ liệu subscription hiện có, ưu tiên bảng gọn: acceptance, preservation, input tokens/run, output tokens/run, elapsed minutes/run, số timeout và coverage của usage. USD là tùy chọn có điều kiện; nếu chưa có đơn giá/schema/usage đầy đủ, để chưa báo cáo thay vì tạo độ chính xác giả. Khi đủ điều kiện, dùng nhãn “reference-price estimated USD/run” và “reference-price estimated USD/accepted outcome”, kèm định nghĩa mẫu số. Không đưa ngày lịch hay hash vào bảng này.

Các nguồn trên cung cấp tiền lệ về cách đo; chúng không chứng minh starter-kit làm giảm tokens, USD hoặc thời gian. Điều đó chỉ được kết luận từ các lượt chạy đối chứng có cùng agent, ngân sách và quy tắc dừng.

## Cần kiểm tra trước khi đưa vào paper

Xác nhận schema cached/reasoning tokens; usage của timeout; ranh giới đo elapsed_seconds; quy tắc lặp/retry và tập lượt chạy đưa vào mẫu số; acceptance có bao hàm preservation hay không. Nếu dùng USD, xác minh nguồn đơn giá và ghi rõ đây là ước tính tham chiếu, không phải khoản thanh toán thực tế.
