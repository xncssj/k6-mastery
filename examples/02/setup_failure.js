import http from 'k6/http';

// 默认压本地模拟工单服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8898';

export const options = {
  vus: 1,
  iterations: 1,
};

export function setup() {
  console.log('[setup] 用错误密码登录，预期拿到 401');
  const res = http.post(
    `${BASE}/login`,
    JSON.stringify({ username: 'demo', password: 'wrong-password' }),
    { headers: { 'Content-Type': 'application/json' } },
  );
  console.log(`[setup] 登录状态=${res.status}，准备抛出异常`);
  throw new Error('鉴权失败示意');
}

export default function () {
  // setup 抛错后 default 不会执行，本行不应出现在输出里。
  console.log('[default] 本行不应出现');
}

export function teardown() {
  // setup 抛错后 teardown 不会执行，本行不应出现在输出里。
  console.log('[teardown] 本行不应出现');
}
