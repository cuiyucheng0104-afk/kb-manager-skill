// 交付就绪审计 · 可复用 Workflow 模板(Claude Code `Workflow` 工具)
// 用法:把它当模板改 —— 通过 args 传目标环境与要审的维度,或直接改 DEFAULT_AREAS。
//   Workflow({ scriptPath: ".../readiness-audit.workflow.js",
//              args: { base: "http://localhost:18770",
//                      auth: "Bearer <token>",
//                      root: "/abs/path/repo",
//                      areas: [ {key, prompt}, ... ] } })   // areas 可省,用默认四维
// 每个 agent **实测**(curl 运行中的服务 + 读源码定位)后给 ready/needs-config/blocked。
// 注意:脚本里不能用 Date.now()/Math.random()(会破坏 resume);时间戳在返回后再打。

export const meta = {
  name: 'delivery-readiness-audit',
  description: '交付就绪审计:并行实测各维度,给 ready/needs-config/blocked + 阻碍清单',
  phases: [{ title: 'Audit' }],
}

const A = (typeof args === 'object' && args) ? args : {}
const BASE = A.base || 'http://localhost:8080'
const AUTH = A.auth || ''
const ROOT = A.root || '.'

const COMMON = `
你在做「交付就绪审计」。被审系统运行中:服务基址 ${BASE}${AUTH ? `,鉴权头 Authorization: ${AUTH}` : ''}。源码根:${ROOT}。
你有 Bash(可 curl 实测运行中的服务)与 Read(可读源码)。**基于实测下结论,不要读代码猜。**
目标:判断这一块交付给客户后是否真能用,以及交付前必须先处理什么。
`

// 默认四维(能力多时把"功能真实性"拆成每个关键能力一个 agent)
const DEFAULT_AREAS = [
  { key: 'function-reality', prompt: '审【功能真实性】。对每个关键能力,实际调用运行中的端点看真实返回,判断是真接通(真模型/DB/服务/RAG)还是样板/占位/静默回落(如哈希向量、stub、内存表)。追代码到底层佐证。给出哪些实测能用、哪些是空/占位。' },
  { key: 'security-auth', prompt: '审【安全与登录/鉴权形态】。登录是否真门(还是假登录)?有无联调后门随包(dev 免签名 token 等)?默认弱口令?服务绑 0.0.0.0?身份/租户/角色是否 token 自报即信任?实测伪造凭据能否拿数据?生产鉴权(JWT/SSO)是否真被启用与使用。' },
  { key: 'clean-firststart', prompt: '审【干净目标机首次启动】。CI 只证明能打包≠客户机能起。核对首启链路:各依赖健康是否都纳入就绪门槛(某依赖没起却放行=能进但啥都不出)?建库/迁移/灌种是否幂等、失败会否毒化(半成品留着下次跳过)?打包依赖/二进制/离线模型是否齐?列出未在真机验证的风险点。' },
  { key: 'config-prereq', prompt: '审【配置与数据前提】。列全"没配就用不了"的项:大模型/密钥(是否在包内、掉线表现)、向量模型型号与库对齐、必须先导入并索引的数据、业务 seed/许可证、多份配置是否漂移。不满足时用户会以为"坏了"。' },
]
const AREAS = Array.isArray(A.areas) && A.areas.length ? A.areas : DEFAULT_AREAS

const READINESS = {
  type: 'object',
  properties: {
    area: { type: 'string' },
    verdict: { type: 'string', enum: ['ready', 'ready-with-config', 'blocked', 'unverified'] },
    works: { type: 'string', description: '实测确认能用的(附证据)' },
    blockers: { type: 'array', items: { type: 'string' }, description: '交付前必须处理的硬阻碍(具体可执行)' },
    evidence: { type: 'string', description: '关键实测证据:命令+结果摘要,或 file:line' },
  },
  required: ['area', 'verdict', 'works', 'blockers', 'evidence'],
}

phase('Audit')
const results = await parallel(AREAS.map(a => () =>
  agent(COMMON + '\n\n' + a.prompt, { label: 'audit:' + a.key, phase: 'Audit', schema: READINESS })
))
const rows = results.filter(Boolean)
return {
  areas: rows.map(r => ({ area: r.area, verdict: r.verdict, works: r.works, blockers: r.blockers, evidence: r.evidence })),
  blocked: rows.filter(r => r.verdict === 'blocked').map(r => r.area),
  needs_config: rows.filter(r => r.verdict === 'ready-with-config').map(r => r.area),
  all_blockers: rows.flatMap(r => (r.blockers || []).map(b => `[${r.area}] ${b}`)),
}
