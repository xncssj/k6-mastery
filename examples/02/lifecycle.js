import http from 'k6/http';
import { check, sleep } from 'k6';

// 默认压本地模拟工单服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8898';

export const options = {
  // 顶层 vus/iterations 是共享 iterations 执行器的快捷写法：
  // 2 个虚拟用户合计跑 6 次迭代，每次迭代由哪个 VU 执行由运行时调度。
  vus: 2,
  iterations: 6,
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

// 注意：init 上下文只有 __VU 可取，__ITER 尚未定义、不能引用。
// __VU 在 init 里的取值分两种：脚本首次加载（无 VU 归属）为 0，
// VU 初始化求值时为该 VU 的编号（从 1 起）；setup／teardown 上下文中恒为 0。
console.log(`[init] VU 初始化：init 上下文求值（当前 VU=${__VU}）`);

export function setup() {
  console.log('[setup] 全局一次：先登录拿令牌');
  const res = http.post(
    `${BASE}/login`,
    JSON.stringify({ username: 'demo', password: 'demo123' }),
    { headers: { 'Content-Type': 'application/json' } },
  );
  const token = res.json('token');
  console.log(`[setup] 登录状态=${res.status}，令牌=${token}`);
  return { token };
}

export default function (data) {
  const res = http.get(`${BASE}/tickets`, {
    headers: { Authorization: `Bearer ${data.token}` },
  });
  check(res, {
    'tickets status is 200': (r) => r.status === 200,
    'tickets total > 0': (r) => r.json('total') > 0,
  });
  console.log(`[default] VU${__VU} 第${__ITER + 1}次迭代`);
  sleep(0.5);
}

export function teardown(data) {
  console.log(`[teardown] 全局一次：令牌${data.token ? '已拿到' : '未拿到'}（${data.token}）`);
}
