import http from 'k6/http';

// 默认压本地模拟工单服务；换环境用 k6 run -e BASE_URL=... 覆盖，不改脚本。
const BASE = __ENV.BASE_URL || 'http://127.0.0.1:8898';

console.log('[init] 尝试在 init 上下文直接发请求（教学演示，预期被 k6 拒绝）');
http.get(`${BASE}/`);

export default function () {
  // default 是空函数：脚本在进入执行阶段前就会被 k6 拒绝。
}
