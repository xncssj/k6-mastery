import http from 'k6/http';
import { check } from 'k6';

// 默认压本地模拟工单服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8898';

export const options = {
  vus: 1,
  iterations: 2,
};

export default function () {
  const res = http.get(`${BASE}/`);
  check(res, { 'home status is 200': (r) => r.status === 200 });
}

export function handleSummary(data) {
  const iter = data.metrics.iterations.values.count;
  const reqs = data.metrics.http_reqs.values.count;
  const checkVals = data.metrics.checks.values;
  const p95 = data.metrics.http_req_duration.values['p(95)'];
  console.log(`[summary] 迭代数=${iter}`);
  const text = [
    '[summary] 自拼摘要（默认摘要已被 handleSummary 的 stdout 键替换）',
    `迭代次数=${iter}，HTTP 请求数=${reqs}，检查通过=${checkVals.passes} 失败=${checkVals.fails}`,
    `http_req_duration p(95)=${p95}ms`,
  ].join('\n');
  return {
    // 取舍说明：summary.json 只保留 metrics 里 iterations/http_reqs/checks/
    // http_req_duration 4 个字段，避免把全量 data 序列化成超大文件；
    // 自拼 stdout 文本不依赖 https://jslib.k6.io 远程导入，全程离线可跑。
    'summary.json': JSON.stringify(
      {
        iterations: data.metrics.iterations,
        http_reqs: data.metrics.http_reqs,
        checks: data.metrics.checks,
        http_req_duration: data.metrics.http_req_duration,
      },
      null,
      2,
    ),
    stdout: text,
  };
}
