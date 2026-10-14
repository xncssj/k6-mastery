import http from 'k6/http';
import { check, sleep } from 'k6';

// 默认压本地模拟工单服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8898';

export const options = {
  vus: 1,
  duration: '5s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  // 第 1 步：登录拿令牌（每次迭代都登录，教学上先看懂链路；
  // 「登录一次全轮复用还是每次重来」的取舍留到下一篇讲脚本结构与生命周期时再拆）。
  const loginRes = http.post(
    `${BASE}/login`,
    JSON.stringify({ username: 'demo', password: 'demo123' }),
    { headers: { 'Content-Type': 'application/json' } },
  );
  check(loginRes, { 'login status is 200': (r) => r.status === 200 });
  const token = loginRes.json('token');
  const authHeaders = { headers: { Authorization: `Bearer ${token}` } };

  // 第 2 步：查工单列表。
  const listRes = http.get(`${BASE}/tickets`, authHeaders);
  check(listRes, {
    'list status is 200': (r) => r.status === 200,
    'list has tickets': (r) => r.json('total') > 0,
  });

  // 第 3 步：查 1 号工单详情。
  const detailRes = http.get(`${BASE}/tickets/1`, authHeaders);
  check(detailRes, { 'detail status is 200': (r) => r.status === 200 });

  // 第 4 步：建一张新工单，预期 201。
  const createRes = http.post(
    `${BASE}/tickets`,
    JSON.stringify({ title: `k6 跟练工单 ${Date.now()}` }),
    { headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` } },
  );
  check(createRes, { 'create status is 201': (r) => r.status === 201 });

  sleep(1);
}
