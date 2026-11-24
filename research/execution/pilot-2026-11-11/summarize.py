"""Read-only audit of pilot outputs; writes an aggregate development report."""
from pathlib import Path
import hashlib
import json
import os
import re

root=Path(__file__).resolve().parent
allocation=json.loads((root/'allocation.json').read_text())['order']
qualification=json.loads((root/'qualification-complete.json').read_text())
assert qualification['hidden_evaluator_sha256']==hashlib.sha256((root/'final-check.cjs').read_bytes()).hexdigest()
auth=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json'
token_values=[value for value in json.loads(auth.read_text()).get('tokens',{}).values() if isinstance(value,str) and len(value)>60]
rows=[]; privacy_matches=[]
for cell in allocation:
    directory=root/'runs'/cell
    attempt=directory/'attempt.json'
    if not attempt.exists():rows.append({'cell':cell,'status':'pending'});continue
    data=json.loads(attempt.read_text())
    fields=['cell','status','model','reasoning','speed','cli_version','elapsed_seconds','returncode','timeout','acceptance','preservation','joint_success','usage_events']
    row={key:data.get(key) for key in fields}
    result=directory/'evaluation'/'result.json'
    if result.exists():
        r=json.loads(result.read_text());row['checks']=len(r['results']);row['failed_checks']=[item['name'] for item in r['results'] if not item['pass']]
        row['acceptance_checks']=len([item for item in r['results'] if item['kind']=='acceptance'])
        row['preservation_checks']=len([item for item in r['results'] if item['kind']=='preservation'])
    patch=directory/'patch.diff'
    if patch.exists():row['changed_paths']=re.findall(r'^diff --git a/(.*?) b/',patch.read_text(errors='replace'),re.M)
    events=[]
    if (directory/'events.jsonl').exists():
        raw=(directory/'events.jsonl').read_text(errors='replace')
        if any(token in raw for token in token_values):privacy_matches.append(cell)
        for line in raw.splitlines():
            try:
                event=json.loads(line)
                if isinstance(event,dict):events.append(event)
            except ValueError:pass
    commands=[event['item'].get('command','') for event in events if event.get('type')=='item.completed' and event.get('item',{}).get('type')=='command_execution']
    row['supplied_behavior_check_invocations']=sum('pnpm test:behavior' in command for command in commands)
    row['nested_agent_events']=sum(event.get('item',{}).get('type')=='collab_tool_call' for event in events)
    rows.append(row)
summary={'purpose':'development smoke pilot only; no main-study or comparative effect estimates',
         'allocation':allocation,'rows':rows,'credential_material_detected_in_events':privacy_matches,
         'setup_failures':[str(path.relative_to(root)) for path in (root/'runs').rglob('attempt-setup-failure-*.json')],
         'hidden_evaluator_unchanged_since_qualification':True}
(root/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
complete=[row for row in rows if row['status']=='complete']
text=['# Kết quả development smoke pilot, 11/11/2026\n',
      f'Đã hoàn tất {len(complete)}/4 phiên agent trên một tác vụ development. Đây là kiểm tra khả năng thực hiện và quy trình, không phải dữ liệu nghiên cứu chính. Không ước lượng hiệu ứng layout hay test package từ bốn lượt này.\n',
      '## Kết quả từng điều kiện\n',
      '| Điều kiện | Layout | Thời gian agent (giây) | Acceptance | Preservation | Kiểm tra cuối |',
      '|---|---|---:|---|---|---|']
for row in rows:
    layout='Theo tầng/vai trò' if row['cell'].startswith('S0') else 'Theo tính năng'
    text.append(f"| {row['cell']} | {layout} | {row.get('elapsed_seconds','—')} | {row.get('acceptance','chưa có')} | {row.get('preservation','chưa có')} | {row.get('checks','—')} |")
text += ['\nV0 có các checks cơ bản và scripts có sẵn; V1 bổ sung 10 preservation checks. Cả bốn có quyền công cụ thông thường và được tự viết tests. Model yêu cầu là GPT-6 Luna High, Standard mặc định, Codex CLI 0.166.0. Giới hạn 900 giây mỗi phiên. Model alias không chứng nhận một phiên bản weights bất biến.\n',
         '## Phạm vi đánh giá\n',
         'Bộ chấm cuối có 29 checks độc lập cho development pilot, gồm 16 acceptance và 13 preservation checks. Fixtures thưa theo người dùng, hai plans, nhiều orders cùng trạng thái và các ngày khác nhau; chúng khác cấu trúc với fixtures của bộ visible. Bộ chấm không có trong container agent và không trả kết quả để agent sửa tiếp. Chấm trong container sạch sau khi thu patch.\n',
         'HTTP/DOM checks không chạy tương tác/hydration trình duyệt. Bộ chấm cuối kiểm tra ownership/history/status và việc đọc không đổi orders; nó không tái kiểm tra trực tiếp cancellation qua browser/server-action transport. V1 có checks cancellation với session/cache stubs. Do đó preservation pass chỉ có nghĩa trong phạm vi final checks đã thực hiện, không bảo đảm mọi hành vi của ứng dụng. Cần mở rộng oracle phù hợp với từng main task.\n',
         'Trước model runs, cả hai unsolved baselines qua preservation và thất bại acceptance; cả hai reference implementations qua cả hai thành phần. Visible package qua 10/10 checks trên mỗi baseline chưa giải. Qualification không tiêu hạn mức model.\n',
         '## Hạ tầng, provenance và sự cố\n',
         'Từng phiên dùng container và PostgreSQL mới, không host bind mounts, Docker socket hay source history chứa lời giải. Auth ChatGPT được đặt ngoài application workspace, không dùng paid API key. Snapshot gốc và bản SmartKit của tác giả không bị agent sửa. File hashes và image IDs nằm trong manifests/isolation logs.\n',
         'Có một lần setup S1V0 lỗi trước khi gọi model. Record và migrate log cũ được giữ. Readiness ban đầu dùng Unix socket, có thể báo ready ở temporary init server trước khi PostgreSQL nhận TCP. Gate đổi sang TCP và thêm lưu log DB; đây là giả thuyết có căn cứ về failure, không có DB log cũ để chứng minh nguyên nhân SQL. Lần setup-only retry được adjudicate riêng. Không chạy lại một agent outcome thất bại để chọn kết quả tốt hơn. Bản runner trước sửa còn ở pilot-v1.py.txt; mọi package, model, task, allocation và timeout giữ nguyên.\n',
         '## Token và chi phí\n',
         'summary.json giữ nguyên các usage events do CLI báo. Input/cached/output là trường token của provider, không quy đổi thành tiền API hoặc số quota Plus còn lại. Có thể có prompt caching và nhiễu hạ tầng; một lượt mỗi cell chưa cho phép kết luận package nào rẻ hơn.\n',
         '## Bằng chứng và bước tiếp\n',
         'Xem protocol.md, allocation.json, qualification-results.json, qualification-complete.json và manifests. Mỗi runs/<cell> có attempt.json, events.jsonl, final-message.txt, patch.diff, final-workspace.tgz, isolation.json và evaluation/result.json. Raw traces cần rà privacy trước khi công khai. summary.json ghi audit xem trace có chứa credential strings hay không mà không in giá trị credential.\n',
         'Pilot này hỗ trợ quyết định tiếp tục kiểm tra Luna trên các development tasks đa dạng hơn. Nếu bốn cases đều pass, điều đó chỉ xác nhận một tác vụ mẫu có thể thực hiện trong cấu hình này; không chứng minh đủ năng lực cho mọi main task hoặc có khác biệt giữa điều kiện. Tiếp theo cần main task frame/provenance, oracle tương ứng và pilot precision/cost có repetitions phù hợp, rồi mới freeze protocol chính.\n']
(root/'report.md').write_text('\n'.join(text),encoding='utf-8')
print(json.dumps({'completed':len(complete),'cells':[{'cell':row['cell'],'status':row['status'],'joint_success':row.get('joint_success'),'seconds':row.get('elapsed_seconds')} for row in rows],'credential_matches':len(privacy_matches)},ensure_ascii=False))
