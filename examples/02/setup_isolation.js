// 默认压本地模拟工单服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
// 本实验纯内存演示，不发任何请求，BASE 仅与其他脚本保持同一契约。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8898';

export const options = {
  vus: 2,
  iterations: 4,
};

console.log('[init] VU 初始化：本实验纯内存演示，不发请求');

export function setup() {
  console.log('[setup] 构造共享数据：count=0');
  return { count: 0 };
}

export default function (data) {
  data.count++;
  console.log(`[default] VU${__VU} 自己副本 count=${data.count}`);
}

export function teardown(data) {
  console.log(`[teardown] teardown 拿到的 count=${data.count}`);
}
