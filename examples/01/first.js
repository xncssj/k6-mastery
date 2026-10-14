import http from 'k6/http';
import { check, sleep } from 'k6';

// 默认压本地回显服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8899';

export const options = {
  vus: 1,
  duration: '5s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<2000'],
  },
};

export default function () {
  const res = http.get(`${BASE}/`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
