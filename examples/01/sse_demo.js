import http from 'k6/http';
import { check, sleep } from 'k6';

// 默认压本地模拟工单服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8898';

export const options = {
  vus: 1,
  duration: '5s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  // 先登录拿令牌：SSE 也是业务接口，同样要鉴权。
  const loginRes = http.post(
    `${BASE}/login`,
    JSON.stringify({ username: 'demo', password: 'demo123' }),
    { headers: { 'Content-Type': 'application/json' } },
  );
  check(loginRes, { 'login status is 200': (r) => r.status === 200 });
  const token = loginRes.json('token');

  // 收 SSE 事件流：本服务的 /events 把当前工单各推一条后主动收尾
  // （重启服务后为 5 条），标准 http.get 即可拿到完整响应体再断言。
  const res = http.get(`${BASE}/events`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const events = res.body ? res.body.match(/data: /g) || [] : [];
  check(res, {
    'sse status is 200': (r) => r.status === 200,
    'sse content type': (r) =>
      (r.headers['Content-Type'] || '').includes('text/event-stream'),
    'sse received 5 events': () => events.length === 5,
  });

  sleep(1);
}
