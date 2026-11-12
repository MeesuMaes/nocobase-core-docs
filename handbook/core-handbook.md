# NocoBase 3 Core 知识手册

> 面向答疑：先用本手册定位，再打开出处页核对细节与签名。只陈述文档已写明的事实，不编造 API、配置项或命令。文档站点：`https://meesumaes.github.io/nocobase-core-docs/<route>`，原文 Markdown：同路径加 `.md`。官方原文：https://docs.nocobase.com/zh-CN/core/。核对此镜像时，常用接口基线为 Core 修订 `015404ecd0db`（2026-10-26/27），插件清单另有 `db419f1d4`；以当前应用锁文件与本地类型为准。NocoBase 3 处于 beta，各包独立编号，主版本号不等于产品版本。

运行环境：Node.js 24+；pnpm 版本以应用 `package.json` 的 `packageManager` 为准（文档示例为 pnpm 11 / 11.11.0）。源码根目录用 `pnpm nocobase …`；部署产物用 `node dist/cli/index.js …`。创建应用：`PNPM_CONFIG_MINIMUM_RELEASE_AGE=0 pnpm create @nocobase/app@beta my-app --template-tag=beta`（该环境变量仅让此次创建可安装刚发布的包）。Windows 使用 WSL，命令在 POSIX shell 中执行。

## 如何答题

按问题类型打开对应页面；手册不够就读原文，并在回答中给出相对路由作为出处。接口输入、响应和权限以运行中应用的 `/api/swagger`、`/api/swagger/docs` 为准（受身份与权限约束，默认不向匿名用户开放）。路径相对于应用挂载前缀（如 `APP_BASE_PATH=/main` 时，`/api/users` 实际为 `/main/api/users`）。

| 问题类型 | 先打开 |
| --- | --- |
| 目录该放哪、生成文件能不能删 | `developing-apps/project-structure`，`reference/project-conventions`，`reference/faq` |
| 配置不生效、密钥、环境变量、公开给浏览器的配置 | `developing-apps/configuration-and-settings`，`reference/configuration` |
| 命令怎么写、开发/部署命令差异、JSON 输出 | `reference/cli`，`framework/runtime/cli`，`developing-apps/application-commands` |
| 页面、菜单、路由、登录要求、覆盖插件页 | `developing-apps/pages-routes-and-navigation`，`developing-apps/page-layouts` |
| UI、shadcn、主题、组件复用、UI Registry | `developing-apps/pages-and-interactions`，`developing-apps/themes-and-styles`，`extension-development/frontend-components` |
| 客户端请求、状态、远程 Repository | `developing-apps/data-requests-and-state`，`framework/http/api-client`，`reference/api` |
| 服务端接口、中间件、校验、错误 | `developing-apps/apis-and-services`，`developing-apps/request-validation-and-errors`，`framework/http/routes`，`framework/http/middleware`，`framework/http/validation` |
| 自动 CRUD 接口 | `framework/http/repository-routes`（建表不会自动开放 HTTP） |
| 认证、角色、数据范围、withPolicy | `developing-apps/authentication-and-permissions`，`using-plugins/authorization/*` |
| 建表、迁移、Seed、校验和、回退 | `developing-apps/data-models-and-migrations`，`framework/database/schema`，`framework/database/migrations`，`framework/database/seeds` |
| 查询、关联、聚合、事务 | `developing-apps/querying-data`，`framework/database/repositories`，`framework/database/relations`，`framework/database/transactions` |
| 多连接、已有库、换方言 | `developing-apps/multiple-databases`，`developing-apps/existing-databases`，`reference/compatibility`，`reference/database-configuration` |
| 后台任务、定时、队列 | `developing-apps/background-tasks`，`framework/background/jobs`，`framework/background/scheduling`，`framework/background/queues`，`using-plugins/automation/scheduler` |
| 工作流/状态机 | `developing-apps/business-workflows`（包 `@nocobase/lifecycle`） |
| 文件存储与上传访问 | `framework/file-storage`，`using-plugins/data-and-files/file-management` |
| 实时推送、WebSocket | `framework/realtime/topics`，`framework/realtime/websocket` |
| 缓存、日志、Snowflake ID | `framework/support/caching`，`framework/support/logging`，`framework/support/ids` |
| 多语言 | `developing-apps/localization`，`developing-apps/server-localization`，`using-plugins/application-support/i18n` |
| 装/卸/升级插件，为何没有页面 | `developing-apps/manage-plugins`，`using-plugins/overview`，`reference/plugins`，`reference/faq` |
| 某内置/商业插件怎么用 | `using-plugins/` 对应篇，包名见 `reference/plugins` |
| 该不该写插件、怎么创建 | `extension-development/when-to-write-a-plugin`，`extension-development/create-plugin`，`extension-development/plugin-structure`，`extension-development/plugin-declarations` |
| 升级 Core、包版本为何不同 | `developing-apps/upgrade-nocobase-core`，`reference/faq`，`reference/packages` |
| 部署、发布新版本、健康检查 | `deployment/choose-a-deployment-method`，`deployment/publish-app-release`，`tutorials/deploy-with-docker`，`tutorials/deploy-with-app-installer` |
| 多门户 / 多应用 / 多租户 | `architecture/overview`，再进 `architecture/multi-portal/*` 或 `architecture/multi-app/*` |
| 公开 API 速查、从功能找包名 | `reference/api`，`reference/packages` |
| 测试怎么写 | `developing-apps/testing-and-acceptance`，`extension-development/testing-and-verification` |

答题规则：包已安装 ≠ 已注册 ≠ 页面已接入 ≠ 迁移已执行。不要从依赖的 `src/` 或私有构建文件导入，只用 `package.json` 声明的公开入口。完整参数以所安装版本的类型声明为准。文档没写的 API 或配置项，直接说文档未记载。

---

## 1. 开发应用

NocoBase Core 与配套插件提供数据库、服务端、客户端、认证与权限等基础能力，业务代码专注功能本身。应用由客户端、服务端、数据库、插件和配置按需组合。可与 Agent 协作：先读项目 `AGENTS.md`、应用规则和随包 Skills。

### 目录约定

目录随模板与功能变化，不必为匹配目录树补齐空目录。`services/`、`commands/`、`packages/`、外部库 `metadata/` 均按需创建。

```text
my-app/
├── .agents/rules/          # 应用自有规则
├── .agents/skills/         # 从依赖同步的 Skills（可再生成）
├── cli/commands/           # 应用命令，调用为 pnpm nocobase app …
├── cli/plugins.ts
├── client/pages|layouts|components|hooks|locales|theme/
├── client/routes.ts        # 路由、菜单、权限
├── client/plugins.ts
├── client/runtime.ts
├── database/<连接名>/migrations|seeds|metadata/
├── database/<连接名>/collections/   # 生成快照，不手改，不作为迁移输入
├── packages/               # 可选本地插件/共享包/UI Registry
├── public/
├── server/routes|services|providers|config/
├── server/plugins.ts
├── server/runtime.ts
├── tests/
├── storage/                # 运行数据（库文件、上传、日志）；生成≠可删
├── dist/  node_modules/    # 可重建
├── AGENTS.md
├── config.example.yml      # 可提交示例
├── config.yml              # 含密钥，不提交 Git
├── components.json         # shadcn
├── package.json  pnpm-lock.yaml  pnpm-workspace.yaml
```

接入：页面 → `client/routes.ts`；HTTP → `server/routes/index.ts`；服务 → 各端 ServiceProvider 聚合入口；配置分区 → `server/config/index.ts`；插件按实际提供的入口写入三端 `plugins.ts`。`runtime.ts` 组装运行时。模板自带的布局、主题和运行时入口是应用源码，升级时保留业务定制。

### 配置

合并顺序（后者覆盖前者）：`server/config/` 代码默认值 → `config.yml` → 已声明映射的环境变量。普通对象递归合并，数组和标量整体替换。YAML 中 `${NAME}` 是普通字符串，不会自动插值。环境变量须显式声明映射。`APP_CONFIG_FILE` 可改用另一份配置（相对路径相对应用根）。`dist/variables.json` 是部署配置元数据清单，不是密钥备份。`config init` 在已有配置时通常保持原文件，覆盖需 `--force`；已有应用应保留原密钥，不要靠重新初始化升级。改配置后部分服务需重启或自行处理 `reload()`。`users.initialAdmin` 只用于空用户库初始化，不重置已有账号。`client` 分区会写入页面；其他服务端分区仅 `defineAppConfig()` 的 `public` 叶子路径可公开。密码、密钥、邮件凭证不得放入 `client` 或公开路径。

`schemaManagement: managed` 表示框架可管理结构；`external` 限制框架结构变更，不是业务只读开关。默认 `DB_*` 只映射 `main` 连接。改方言或地址不会自动搬迁数据。SQLite 同时存在 `database` 与 `filename` 时 `database` 优先。

常用字段与环境变量见第 7 节。完整清单：`pnpm nocobase config variables --json`。

### 客户端

- 路由：`defineAppRoutes()`（`@nocobase/app-client` / `@nocobase/app-client/plugins`）。页面必填 `name`（同包内唯一，以字母或数字开头，可含点/下划线/连字符）、`path`、`componentLoader`；可选 `navigation`（`{ title, icon?, order? }`）、`breadcrumb`、`auth`、`authz`、`parent`（仅贡献根条目）、`children`。纯分组必填 `name`、`children`（可空数组）、`navigation`，不可设 `componentLoader` 与 `authz`，`path` 可选（作子路由前缀）。`auth` 顶层默认 `required`，子层继承。标题为字符串，图标为组件，不支持按用户执行配置回调。底层 React Router 的 `index`、`element`、`loader`、`action`、`errorElement` 不是该声明 API 的字段。`authz` 例：`{ resource: { type: 'page', id: 'projects' }, action: 'access' }` 或 `'skip'`。插件路由的 `parent` 可带包前缀。覆盖插件页：替换页面加载器，保留插件定义的路径、身份与权限元数据（`client/route-overrides.ts` 或插件提供的方式）。
- 路径规则：顶层路径以 `/` 开头；子路径追加到父层，`/new` 并不跳到根。不在 `path` 中写查询串、hash、`*`、可选参数 `?`、反斜杠或 `.`/`..` 段。页面地址在整个应用和所有插件之间唯一；冲突检查忽略静态段大小写和参数名（`/Projects` 与 `/projects` 冲突，`/:id` 与 `/:projectId` 冲突；`new` 与 `:projectId` 可共存）。不同包可同名，但地址不能相同。`/` 只能由应用提供；`/login`、`/register`、`/forgot-password`、`/reset-password` 必须 `auth: 'guest'`。

- UI：统一 shadcn，组件源码在应用中；页面连接数据与操作。品牌、侧栏、全局操作由应用外框管理；业务页组合已有容器、标题和内容区。主题用语义变量，改主题文件即可让列表/表单/弹窗一起适配；用户已保存的配色优先于 `client.app.defaultColorScheme`（`light`/`dark`/`system`）。`client.app.defaultTheme` 须在主题源码中存在。模块化区块优先参考 NocoBase UI Library（https://ui.nocobase.com/）。
- 请求：组件用 `useApiClient()`；`api.request<T>(options)` 返回完整响应体，不自动解包 `data`，泛型不做运行时校验。选项：`path`、`method`（默认 GET）、`query`、`headers`、`signal`、`credentials`（默认 `include`）；JSON 用 `json`，其他用 `body`，二者互斥。`api.stream()`、`api.repository(name)`（需服务端已开放对应接口；`name` 可以与 Collection 名不同；远程查询也走 POST，并自动解开 `data`）。失败为 `ApiClientError`。不要把浏览器缓存的权限当服务端授权依据。登录切换应清理旧身份状态。
- 多语言：`client/locales/` 与 `server/locales/` 独立加载；页面能翻译的 key，服务端仍需声明。
- 客户端服务：跨页面复用操作或应用级资源时用 ServiceProvider 注册到容器；`useService(token)` 只解析、不订阅变化，订阅需 `useSyncExternalStore` 等。React Provider ≠ ServiceProvider。

### 服务端

- 路由：`defineApiRoutes(factory)` 挂到 API 前缀（普通应用为 `/api`，还需考虑基础路径）；`defineRootRoutes()` 挂到应用根；`defineHttpMiddleware({ name, register })`；`apiValidator(target, schema)`；`throw new ApiError({ status, reason, domain, message })`，框架转为含 `error` 的失败响应。`message` 不能作为客户端分支条件；字段问题用 `fieldViolations`。自定义接口可统一 `{ data, meta }`。OpenAPI 辅助从 `@nocobase/app-server/router` 导入。路由工厂接收应用实例、返回 Hono Router，还须经应用或插件扩展入口接入。
- 服务：不必继承框架基类。HTTP、命令、后台任务复用同一服务。不要在单例字段保存当前用户、事务或本次输入。事务内用回调连接上的 Repository。邮件、HTTP、队列通常不随库回滚，放在 `afterCommit()` 或 Outbox。CLI/任务不能默认管理员权限。
- 认证与权限：认证、操作权限、数据范围职责分离。接口先认证再取当前用户；业务操作需注册，授权决策产生策略后 `withPolicy(policy)` 绑到 Repository。用户提交的过滤条件不是授权策略，只能缩小范围。页面权限与接口权限要分别配置和验证。不要把请求里的 `ownerId` 直接当当前用户。
- 后台：`JobExecutor` 先返回受理回执；`ScheduleExecutor` 按 Cron 或间隔触发。业务负责幂等与结果保存。需要管理页和执行记录时用定时任务插件。
- 工作流：基于状态机（`@nocobase/lifecycle`）定义状态、允许流转与条件，适合跨多次请求、由人员/自动/外部系统共同推进的流程。

### 数据库（应用侧）

应用资源在 `database/<连接名>/`。连接名对应目录，不是业务名。Examples 模板常用 `main` + 演示用 `analytics`。

- Migration：`defineMigration()`，`name` 必须与去扩展名的文件名一致，默认导出其返回值。必须有 `down()` 或 `irreversible: true`。已合入/发布的迁移不改内容（格式/注释也会改校验和），后续变化写新迁移。不要导入随应用变化的模型或服务。
- Seed：`defineSeed({ name, run, transaction?, sample? })`，必须默认导出，`name` 与文件名一致且在同一连接全部 Seed 来源中唯一。没有 `down()`、`shouldRun()` 或重复执行模式。用稳定业务键判断是否已存在再写入（或 `upsertOne`）。Seed 无 `builder`，结构须先由迁移建立。同一连接 Seed 按名称排序，位于迁移之后。`sample: true` 标记可选示例；普通 Seed 不会因记录“看起来像示例”而跳过。应用仅在连接首次安装且 `app.sampleData` 为 `true` 时自动执行 sample Seed（首次安装＝执行前没有迁移和 Seed 历史，或刚完成受管理结构重置）；否则记为 `skipped`，以后只打开配置也不会自动跑。开发可用 `pnpm nocobase db sample` 补载被跳过的示例（部署产物拒绝执行）。示例若必须调用其他插件业务服务，应使用 `sampleDataToken` 在应用就绪后生成，不能把业务服务塞进 Seed Context。迁移回退不删 Seed 历史。不要让迁移依赖同一次执行里尚未运行的 Seed。

- `collections/` 用 `pnpm nocobase collections generate` 更新（`--check` 只检查）。
- `schemaManagement: 'external'`：框架读已有结构并叠加应用元数据，不通过该连接跑迁移/Seed；`metadata/` 是源码，不能创建表。缺字段找结构维护方，不能给 external 连接加应用迁移来“修表”。元数据不能代替物理约束。增加连接或元数据不会自动开放 API。
- 取得数据库：`app.container.resolve(databaseManagerToken)`，再 `database.repository('orders')`。操作在服务端执行。

### 命令与插件管理

应用命令放在 `cli/commands/`，例如 `cli/commands/orders/sync.ts` → `pnpm nocobase app orders sync`。继承 `AppCommand`，可用 `withApp()`；不要在模块顶层连库。`cli link` / `cli build` 用于通过 HTTP 调用已运行应用的独立客户端（`@nocobase/app-cli-client`）。

管理插件：先查 `package.json`、锁文件和三端 `plugins.ts`，不要只根据 `node_modules` 推断已启用。`plugin register` / `update` / `unregister`（可 `--dry-run`）；`unregister` 不等于删除库中业务数据；省略名称的 `plugin update` 升级全部已注册插件并同步 Skills。`skills sync` 更新 `.agents/skills/`；维护插件 Skill 时改插件 `skills/` 源文件。`template-print` 仅分发 Skills，不必加入注册数组。`agents` 与 `knowledge` 在默认模板依赖中，但没有默认注册。扩展界面：优先插件公开 options/组件；需改源码则从 UI Library 安装由应用维护的副本。

升级 Core：先备份库、配置和密钥，保留锁文件；按文档逐项合并模板与依赖，同步 Skills，检查并执行迁移。回退代码不会自动撤销结构变更。不要用新模板覆盖原应用来“升级”。

测试：正常路径、权限拒绝、失败重试都要覆盖。迁移测试用 `@nocobase/app-testing/server` 的 `describeMigration()`。常用脚本：`pnpm dev`、`pnpm test`、`pnpm lint`、`pnpm typecheck`、`pnpm build`、`pnpm start`（以应用 `package.json` 为准）。

**出处：** `developing-apps/overview`，`project-structure`，`configuration-and-settings`，`testing-and-acceptance`，`pages-routes-and-navigation`，`pages-and-interactions`，`data-requests-and-state`，`page-layouts`，`localization`，`themes-and-styles`，`client-business-services`，`apis-and-services`，`server-business-services`，`request-validation-and-errors`，`authentication-and-permissions`，`background-tasks`，`business-workflows`，`server-localization`，`data-models-and-migrations`，`querying-data`，`transactions-and-consistency`，`multiple-databases`，`existing-databases`，`application-commands`，`plugin-commands`，`cli-client`，`manage-plugins`，`upgrade-nocobase-core`

---

## 2. 使用插件

先确认应用实际注册的插件与版本，再按篇接入。包已安装不等于已启用；部分插件还需应用组合工厂，或由应用声明业务数据、页面和权限。各篇 `/client`、`/server` 表示该包公开导出。使用文档四章：提供的能力、场景与示例、原理与实现、AI 开发约束与验证。

文档覆盖 21 个插件（主仓库核对 24 个应用插件 + 商业 2 个，见第 7 节）。按功能：

| 功能 | 路由 | 包（摘要） |
| --- | --- | --- |
| 用户 / 登录 / API Key | `using-plugins/authentication/users`，`sign-in`，`api-keys` | `app-plugin-users`（管理接口和页面）、`authentication`（登录与会话）、`api-keys`（内置） |
| 权限 / 默认范围 / 共享 / 限制 | `authorization/permissions`，`default-access`，`sharing-rules`，`restriction-rules` | `authorization`、`authz-default-access`、`authz-sharing-rules`、`authz-restriction-rules`（均内置） |
| 库浏览（只读） | `data-and-files/database-explorer` | `database-explorer`（内置） |
| 文件 | `data-and-files/file-management` | `file`（内置）；可编辑文件界面由 UI Library 提供 |
| 通知 / 渠道 / 站内信 / Web Push / 邮件 | `notifications/notification`，`providers`，`in-app`，`web-push`，`mail` | `notification*`（Web Push 非内置）；`mail`（内置） |
| Agents / 知识库 | `agents-and-knowledge/agents`，`knowledge` | 均在默认依赖中但默认不注册；`agent-sessions` 非内置 |
| 审批（商业） | `collaboration/approval` | `app-plugin-approval`；另有商业 `task-center` |
| 定时任务 / 模板打印 | `automation/scheduler`，`template-print` | `scheduler` 内置；`template-print` 仅 Skills |
| 多语言 / 应用底座 | `application-support/i18n`，`foundation` | 均内置 |

各插件文档中的开发约束（细节回各篇）：

- 用户：表单选项不能替代授权；接口仍检查 create 与 assign-role。邀请要区分“已创建账号”和“邮件投递失败”。删除不能当作物理清除用户历史。
- 登录：关闭注册后仍须检查直接注册请求；密码找回要验证实际投递与链接。业务接口在认证之后继续授权。
- API Key：管理密钥用登录会话，不能用 API Key 再管理其他密钥。无范围密钥 ≠ 只读；报表接口仍须落实操作和记录范围。轮换须立即使旧 secret 失效。
- 权限：先声明业务能力再授权；不能把未接入权限模型的查询当作已受保护。避免一个布尔 can 之后做无限制查询。Seed 角色时检查是否意外扩大现有用户权限。
- 默认数据范围：一个资源只维护一条默认规则；默认范围是追加范围，不是“仅无范围时生效的兜底”。规则只改变记录范围，不授予页面/操作/字段权限。
- 共享规则：按指定主体与记录保存；选择不支持 all，也不能顺带开放所有关联记录。
- 限制规则：选择表示仍允许的记录，多条取交集；删除规则可能扩大访问。
- 库浏览：只读；改表结构仍走迁移。展示连接摘要时不额外暴露主机、密码或数据库文件路径。第一页不是全部 Collection。
- 文件：检查内容路由和元数据接口各自的授权；默认 `accessPath` 不受 Repository policy 保护。上传只接受约定字段，业务归属由服务端处理，不信任客户端任意订单 ID。`deleteOne` 不等于物理清理。
- 通知：业务成功与投递分别处理；重试保留稳定事件标识，不能每次重试生成新幂等键。不能把用户 ID 当邮件地址。一次性凭据走 transient 路径，不能依赖其持久重试。
- 渠道：渠道名 ≠ `type`（`smtp` / `resend` 需原生邮箱与 subject 及 text 或 html；`feishu-webhook` / `dingtalk-webhook` 需 text，可选完整 HTTP(S) target URL）。YAML 不展开环境变量。不要为测试关闭提供方 Webhook 校验。该插件只有 Server 入口，无配置页。
- 站内信：接口使用当前登录身份，不能新增按任意 userId 的不受保护查询。实时事件只触发刷新，操作结果以 HTTP 为准。内部路径不能重复拼接 `/main`。
- 邮件：管理员邮箱概览不代替用户授权连接；participant 不扩大访问范围。结果未知时先核实 submission，避免重复发信。
- Web Push：不能每次启动生成新 VAPID 密钥；设备 API 不可暴露 endpoint 与加密密钥。URL 须指向应用内并含挂载前缀。`dedupeKey` 只替换可见通知，不替代事件幂等。排队成功 ≠ 已展示。
- 知识库：空间列表、读取与搜索使用同一访问边界；页面可进 ≠ 所有空间可读。写入携带预期版本，冲突时重新读取，不去掉版本检查强行覆盖。扫描件不可搜索不能伪造提取成功。
- 定时任务：声明计划 ≠ 已实现业务目标。不能把单进程 memory 验证当作分布式验收。`finalize` 仅使用完整清单，避免误停任务。
- 模板打印：包只提供开发指引（Skills），不得导入不存在的运行时入口或声称已有通用打印服务。下载接口须重新检查记录与字段权限。
- 审批：复用业务记录作为流程标识，不要维护脱节的第二份状态。可见按钮 ≠ 有权审批；服务端同时校验用户、记录、任务资格和内容版本。
- 多语言：语言选项由应用加载器决定，不另硬编码一份与资源不一致的列表。服务端回退不能被误认为浏览器切换已撤销。
- 应用底座：页面和接口保留 unrestricted 要求，不为让入口出现而放宽为“普通登录即可访问”。不能用底座统计代替业务测试。

**出处：** `using-plugins/overview` 及上表各路径；清单与是否内置：`reference/plugins`

---

## 3. 开发插件

只服务当前业务、常随页面改的代码，直接放应用的 `client/`、`server/`、`database/`、`cli/`。需独立维护、提供扩展入口或供多应用接入时，再拆 `packages/app-plugin-<name>/`。本地插件随应用构建，不必先发 npm。

### 创建

```bash
pnpm create @nocobase/plugin@beta <name> --with <capability>
```

`--with` 是要生成的代码能力，不是安装已有插件。必须至少一种能力，或 `--empty` 只生成包结构。多个能力重复 `--with`，不用逗号拼接。

| `--with` | 生成 | 不会自动做的事 |
| --- | --- | --- |
| `client.routes` | 路由骨架与测试 | 不自动生成业务页面 |
| `client.components` | 示例组件与导出 | 需自己实现界面 |
| `client.service-providers` | 客户端 Provider 骨架 | 服务与生命周期 |
| `client.react-providers` | Context 与声明 | 状态与组合 |
| `client.locales` | 语言文件 | 实际译文 |
| `server.service-providers` | services/providers/tokens | 业务逻辑 |
| `server.routes` | 路由骨架 | 不自动生成 CRUD |
| `server.jobs` | 示例 Job 与执行器 Provider | 提交点、幂等、重试 |
| `server.locales` | 服务端语言文件 | 实际译文 |
| `database` | migrations/seeds 的 `.ts.example`、资源声明 | 改为 `.ts` 后才纳入任务 |
| `cli` | 示例 `info` 命令 | 实际命令 |
| `skills` | `skills/<名>/SKILL.md` 草稿 | 按真实实现完善后再同步 |

有任一项 client.*（除单独 components 的细则见原文）会推导 `client/index.ts`、`client/plugin.ts` 与 `./client` 导出；server 侧类似。不必写 `--with client` / `--with server`。带客户端时还会生成 `components.json` 与 `client/styles.css`。

创建后在应用中 `plugin register <包名>`（先 `--dry-run`），并检查三端注册文件。

### 结构与声明

插件按需提供 Client、Server、CLI、database、skills，不要求目录齐全。链路：

```text
client: pages → routes.ts → plugin.ts → index.ts → package.json 的 ./client → 应用 client/plugins.ts
server: routes/providers → plugin.ts → index.ts → ./server → server/plugins.ts
cli:    defineCliPlugin() 默认导出 → ./cli → cli/plugins.ts
```

```ts
// client/plugin.ts
import { defineClientPlugin } from '@nocobase/app-client/plugins';
export default defineClientPlugin({
  packageName: '@nocobase/app-plugin-announcements',
  routes,
  locales,
  // 还可贡献 serviceProviders、react-providers 等，以声明文档为准
});

// server/plugin.ts
import { defineServerPlugin } from '@nocobase/app-server/plugins';
export default defineServerPlugin({
  packageName: '@nocobase/app-plugin-announcements',
  baseDir: path.resolve(import.meta.dirname, '..'),
  serviceProviders,
  routes,
  locales,
  database: { migrations: './database/migrations', seeds: './database/seeds' },
});
```

跨插件调用必须走公开导出与原始 Token，并在依赖中声明该包；不能相对引用旁边插件的私有实现。UI 作为可编辑源码资产时，用独立 Registry 包（`registry/`、`registry.json`），构建 item JSON 后交给 `shadcn add`；本地不必启动 Registry 服务。资产不能依赖发布者私有路径。

`AGENTS.md` 面向维护插件源码的 Agent；`skills/` 面向在应用中使用该插件的 Agent。`.agents/skills/` 是同步副本。

### ServiceProvider

前后端都可用，容器各自独立。`register()` 同步注册；`boot()` / `start()` / `ready()` / `shutdown()` 为异步钩子。使用宿主 `app.container`，不要另建全局容器或销毁宿主共享的 DatabaseManager、Queue、Logging、Caching。工厂是同步的，异步准备放在生命周期里。

### 插件数据与命令

插件 `database/migrations`、`seeds` 经 `server/plugin.ts` 的 `database` 声明由宿主发现。同一连接上应用与插件迁移合并后按 **名称** 排序，插件注册顺序不是迁移顺序。重名会检查失败。构建后生成 `.manifest.json` 保留源校验和，不手改。命令命名空间通常由包名去掉 scope 与 `app-plugin-` 得到，冲突报错，不能靠注册顺序覆盖。开发命令（`devCommands`）只在源码环境保留。

发布、测试与 Skill 写法见 `publish-plugin`、`testing-and-verification`、`write-plugin-skills`。第一个完整示例见 `write-your-first-plugin`。

**出处：** `extension-development/when-to-write-a-plugin`，`plugin-development-guidance`，`create-plugin`，`plugin-structure`，`plugin-declarations`，`write-your-first-plugin`，`service-provider`，`client-services`，`server-services`，`server-apis`，`pages-and-menus`，`frontend-components`，`react-context-and-providers`，`database-and-migrations`，`background-jobs`，`extend-command-line`，`localization`，`server-localization`，`write-plugin-skills`，`publish-plugin`，`testing-and-verification`

---

## 4. 框架

应用组装客户端、服务端、CLI 运行时；插件通过公开入口扩展。两端服务契约相同，容器、实例与生命周期各自独立；共享 Token 不会共享内存，跨端走 API。依赖安装、运行端注册和最终业务接入须分别确认：客户端注册不自动启用服务端，服务端注册也不会给页面安装组件。导入插件声明时不应该读业务数据、启动任务或建立连接；声明选项只放稳定组装参数，部署凭据放服务端配置，不能放入客户端插件选项。`plugin inspect` 只读静态接入面，不能证明业务已工作。复用宿主实例：数据库 Token 来自 `@nocobase/db`，缓存/文件/任务等宿主 Token 来自 `@nocobase/app-server/*`。独立脚本才自行创建并 `destroy()`/`dispose()`，不要在每个请求里创建。

### 运行时

- 客户端：`client/runtime.ts` → `resolveAppRuntime()` → `ClientApplication` → `app.start()` → `AppClientRoot`（Providers + routes）。宿主须等 `start()` 成功再渲染。
- 服务端：配置、Provider、路由、数据资源、插件由运行时接入。用 `app.paths` 解析路径。运行数据用持久位置，不写入可替换的构建目录。不要把“当前用户”写入单例。
- CLI：按 `package.json` 的 `nocobase.templateKind`（源码）或 `nocobase.buildTarget`（产物）识别；`NOCOBASE_APP_ROOT` 指定目标但不改 cwd。只有业务依赖完整生命周期时才 `app.start()`。面向程序的数据进 JSON `result`，进度走 stderr。
- 生命周期：按 Provider 钩子顺序启动与关闭；清理只关自己拥有的资源。`NOCOBASE_STRICT_STARTUP` 使启动失败严格退出。

### 服务容器

`createServiceToken<T>(name)` 每次创建新对象，字符串相同也不是同一 Token，必须导入提供方原始 Token。同一容器不能重复绑定。`instance` / `singleton`（同步工厂，可接收 resolver）/ `resolve`（缺失或循环依赖抛错）/ `has` / `resolveIfCreated`。工厂失败后绑定保留失败状态。无请求作用域。

客户端：`useService(token)`；服务端：`app.container.resolve(token)`。

### HTTP（框架层）

中间件用 `defineHttpMiddleware({ name, register })` 声明，应用组装阶段调用 `app.addHttpMiddleware(...)`，且应在启动和路由注册之前完成。`register` 收到应用根 Router，`/api/*` 是相对于应用的路径，宿主负责外部基础路径适配。先执行 `await next()` 前的代码，返回后再执行其后代码；拒绝时直接返回或抛 `ApiError`，不再调用后续。身份必须先于依赖身份的授权。避免把请求体消费两次（尤其流式上传）。进程内限流计数不是多实例全局计数。不要把未知异常包装成成功响应。

React Provider 用 `defineClientReactProviders([{ name, layer, component }])`（`layer` 如 `'extension'`），按 `layer` 与显式 `before`/`after` 从外到内排列。解析声明不会执行组件；`app.start()` 后渲染 `AppClientRoot` 才挂载。不要在 render 中新建共享连接。

Repository 数据接口用于“一个 Repository 操作即可完成”的列表/详情/字段编辑，须配置 `policy`；涉及复杂状态、多权限范围或副作用时用自定义路由。

```ts
import { defineRepositoryApiRoutes } from '@nocobase/app-server/router';
export default defineRepositoryApiRoutes({
  repositories: [{
    name: 'publicCategories',      // HTTP 名，亦为 api.repository(name)
    collection: 'categories',      // 省略则与 name 相同
    // connection 省略则用默认连接
    actions: { findMany: { maxLimit: 50 }, findOne: {}, count: {} },
    // 还可启用 exists、createOne、updateOne、deleteOne、aggregate、groupBy
    policy: { read: { scope: true, fields: ['id', 'title'] }, create: false, update: false, delete: false },
  }],
});
```

`policy` 也可按请求身份生成。`principal` 用于解析身份。HTTP 调用示例为 `POST /api/publicCategories/findMany`。流式响应一旦开始发送，不能再改成普通 JSON 错误。超时不自动撤销已提交的库操作。

### 数据库（框架层）

入口：DatabaseManager / Connection；CollectionBuilder；Repository；Query；Collections / SchemaInspector；Migrator / Seeder。业务通常从 Repository 开始。Migration 里用 Builder 改结构、用 Query 做集合式回填。底层驱动能力不自动成为各方言公共能力。

```ts
const database = app.container.resolve(databaseManagerToken);
const orders = database.repository('orders');
// db.connection(name?)、connect、builder（方法）、query、collections
// db.transaction(callback, name?)、destroy()
// CollectionBuilder 仅作类型导出，不要 new CollectionBuilder()
// connection.builder 是属性；db.builder() 是方法
```

`context` 查询选项是变量上下文，不是事务句柄。Builder 的 `transaction()` 当前不开真实事务。

**建模：** 框架不自动附加 `id`/`createdAt`/`updatedAt`。`increments()` 才是自增主键，字段仅名为 `id` 不会成为主键。`createCollection(name, callback | { fields, indexes, constraints })`，不能把字段数组当第二参数。字段：`string`/`text`/`boolean`/`integer`/`decimal`/`bigInt`（超安全整数用十进制字符串）/`date`/`time`/`datetime`/`datetimeTz`/`json`/`enum`/`char`/`float`/`double`/`blob`/`uuid`/`native`。默认值不回写旧记录。`alterCollection`/`alterField`/`addField`/`dropField`/`dropCollection`/`renameCollection`（有关系/外键/视图依赖时可能拒绝；不要用删建模拟重命名）。Builder 使用逻辑名；物理名由 `underscored`、`tablePrefix` 决定，不要向 Builder 填 `tableName`/`columnName`。`dryRun`/`previewSql` 的操作级预览 ≠ `db apply --dry-run`。`strict: true` 让能力警告变错误，不是删除确认。`ifNotExists`/`ifExists` 不校正已有对象结构。external 连接不能执行 Builder DDL。

**关联：** 必须显式指定键，不推断。`belongsTo`：`foreignKey`+`targetKey`；`hasOne`/`hasMany`：`sourceKey`+`foreignKey`；`belongsToMany`：`sourceKey`+`targetKey`+`through`+`foreignKey`+`otherKey`。关联声明不授权、不自动建中间表。只有 `constraints: true` 才自动建外键；已有显式外键时用 `constraints: false`。`belongsTo` 默认补索引，可用 `index: false`。`onDelete`/`onUpdate`：`restrict`/`cascade`/`set null`/`set default`/`no action`，能力因方言而异。

**Repository：** `findMany` 惰性，同一对象不要混合 await 与异步迭代或重复消费；`findOne` 不证明唯一；`updateOne`/`deleteOne` 必须恰好一条否则失败；`upsertOne` 筛选须唯一定位；批量写/删须筛选或 `all: true`。`createOne` 等从 `.record` 取记录。金额用精确字符串。`select` 限制字段；不设 select 通常读全部标量，仍不可泄漏密码。需要权限时 `withPolicy()`。

**Query：** 面向物理表与结果集，不读 Collection 字段映射或表前缀。`updateTable`/`deleteFrom` 要求条件，全表须 `allowAllRows()`。

**过滤、排序、分页：** 列表、计数和导出应基于同一授权范围。简单等值可写 `{ status: 'draft' }`；`{ amount: { gte: 100 } }` 不是当前等值简写。空筛选直接省略，不传空对象。复杂条件用 Filter Builder（`f.and`/`f.or`，`f.string('title').includes(q)` 等）或 JSON AST。须限制 page/pageSize（示例拒绝非安全整数或 pageSize>100）。列表与 `count` 是两次查询，不天然同一快照。`cursor` 是排序值的排他边界，不要求边界记录仍存在；必须显式排序，轴只能用非空直接标量字段，并含完整主键或唯一约束作决胜项；游标键须与最终排序轴一致，不能与 offset 同用。`direction: 'backward'` 取边界之前最近一页，返回仍按原 sort 顺序。返回没有自动 pageInfo/nextCursor。分页不保证跨请求快照。

**查询输入：** `@nocobase/repository-input` 的 `buildFilter`/`buildSelect`/`buildSort`/`buildAggregate` 把回调或 AST 物化为可序列化 JSON；也可 `buildCreateValues`/`buildUpdateValues`，远程请求用 API Client 的 `build*Options`。构造输入不连库、不验证字段权限。函数不能直接经 JSON 传输。日期转 ISO，bigint 转十进制字符串。不要使用 `internal/*`。服务端仍须核对 Collection、字段、关系深度、分页和策略。

**聚合：** `aggregate()` 返回别名到数值的对象，不带 record 包装；`groupBy({ by, aggregate, having, sort })` 返回含分组字段与聚合别名的数组。先 filter，再分组，再 having。`count()` 空集为 0；`count(field)` 忽略 SQL NULL；`sum`/`avg` 对整数与 DECIMAL 保留精度字符串，浮点返回 number；`min`/`max` 保留逻辑类型；空集的 sum/avg/min/max 为 `null`。不要对金额或大整数使用 `Number()`。`by` 必须非空且不重复；聚合别名不能覆盖分组字段；having/sort 不能引用未分组字段。统计与明细使用同一权限范围。

**关联查询：** `select: (s) => s.fields(...).include('orders', (orders) => orders.fields(...).filter(...).sort(...).limit(10))`。关系局部 filter 只影响关联内容，不会移除没有匹配子记录的父行；筛父行需根级关系条件。belongsTo/hasOne 无匹配为 `null`，hasMany/belongsToMany 为 `[]`。不传 select 时默认读标量、不自动展开关系。`fields()` 无参数表示零个根字段。重复 include 同一关系会被拒绝。to-many 支持局部排序、limit、游标；to-one 不支持这些。关系 Builder 不可变，必须使用链式返回值。`combine()` 可在同一关系下分别返回记录、计数和求和，各分支条件与分页独立。局部 limit 不保证数据库只读取每个父记录的限定行数。关联不是绕过目标记录权限的通道。

**连接：** 一个管理器可含多个连接，各有方言、事务和模型解析。`db.repository('events', 'analytics')` 或 `db.connection('analytics')` 选命名连接。核心管理器不自动扫描方言包；独立代码须显式提供方言工厂或在 `drivers` 注册后用声明式配置。应用运行时按配置异步加载已安装官方方言。连接不是跨库事务协调器。不要在每次请求中创建连接池。

**事务：** 回调内必须用 `connection.repository()`，不要用外层 `db.repository()`。回调返回后连接结束。`afterCommit()` 在回滚时丢弃；其抛错不改变已提交结果。嵌套成功时回调并入最外层提交。需要可靠投递应持久化待发送记录。一个连接事务不覆盖其他连接或外部系统。

**迁移执行：** 只跑无成功历史的迁移，本次记入同一新批次，但各任务自有事务。`transaction: 'auto'`/`true` 使用连接事务；`false` 失败可能留下部分修改。不能假设所有方言 DDL 可回滚。`shouldRun` 在锁内、任务事务前执行，返回 `false` 不写成功历史；`--dry-run` 不执行该回调。`db rollback` 回退最新整批（可能含应用+插件），任一条不可逆则整批不能开始；非交互需 `--force`。`db redo` 回退后重做迁移与 Seed，重建表不等于已执行 Seed 会重装。`db reset` 删除受管理结构和历史后从空库安装，不调用 `down()`，只用于可丢弃数据。`db repair` 只修历史校验和，不跑迁移、不修结构。迁移 Context 的 `connection` 不是完整运行时连接；不要从外部 DatabaseManager 另取 Repository（会离开任务事务）。Context `container` 在应用层目前只允许 `idGeneratorToken`。迁移/Seed 写入不触发运行时 Repository 变更事件。

**Seed：** `name` 与文件名一致；执行历史与失败重试见原页。示例数据用 `sample: true` + `db sample`（仅开发）。

### 后台、实时与支撑

- Jobs（`jobExecutorServiceToken`，`@nocobase/app-server/jobs`）：`Job` 子类，`static jobName`；载荷须可 JSON 持久化，不要传连接、容器、函数、`Date`、`bigint`、`undefined`（日期用 ISO 字符串）。所有消费进程须在 `setup()` 前 `registerJob`。回执 ≠ 处理成功。开发可用 memory，跨进程用 Redis（配置名与 queue 的 `inMemory`/`redis` 不同）。任务提交不与业务库事务原子绑定。
- 调度：`getScheduleExecutor(scope)`，`cron`（五/六段，默认 UTC，应显式 `tz`）与 `every`（毫秒）二选一；`startDate`/`endDate`/`limit`/`immediately`。更名不会自动删除旧规则；`removeJob()` 不要在每次进程关闭时调用。
- Queue（`queueServiceToken`）：多数业务先用 Jobs；需通道、延迟、优先级、批量或限流再用队列。`producer(name).publish(channel, payload)` 回执 ≠ 消费完成。同进程处理器并行，任一失败可能整条重试。`withChannel()` 只筛选通道。不要在处理器里等待注销自身。
- Realtime（`realtimeServiceToken`）：先 `defineTopic`/`defineTopicFamily`；`audience: 'user'` 只投递给连接认证后的指定用户。`publishFor` 的用户 ID 须服务端已确认。事件断线不补发；权威状态在数据库和 API。默认 `inMemory` broker 仅当前实例，多进程用 Redis Pub/Sub。页面用 `useRealtimeRefresh(topic, refresh, { delayMs })` 或 `useRealtimeTopic()`；不要为每个组件建连接。路径内部为 `/ws`，对外可能含挂载前缀。
- Drive（`driveManagerToken`）：`drive.use()`/`use('local')`；驱动 `fs`（`location`、`visibility`、可选 `url`）、`s3`、`oss`。`visibility: 'private'` 不会自动配 OS 权限或保护公开 HTTP 目录；`url` 只参与 URL 生成。`put`/`get`/`delete`。多实例用本地盘需共享卷或改对象存储。
- Caching（`cachingToken`）：`getCache({ namespace, defaultTtl })`，`wrap`/`get`/`set`/`delete`/`take`。缓存不能当唯一数据源；键须覆盖租户/用户/权限维度。内置 `memory` 仅当前进程。不能只把配置改成 `redis` 就获得未安装的驱动。`wrap` 合并不是分布式锁。布隆过滤器可能误判存在。
- Logging（`loggingToken`）：`getLogger(source)` 写入 `logger` 字段，不自动分文件；默认文件名 `app`，目录 `storage/logs/`。文件始终 JSON Lines；`console.pretty` 只影响终端。一个日志目录由一个进程管理轮换。不要写密码、Cookie、Token、完整个人资料。
- Snowflake（`idGeneratorToken`）：`generate()` / `generateString()`。`workerId` 0–31（`snowflake.workerId` / `SNOWFLAKE_WORKER_ID`），多实例必须不同且不会自动协调。同秒序列用尽、时钟回退或超出安全整数会抛错，不静默重复。不要当会话密钥或 API Token。浏览器新 ID 应由服务端生成。

**出处：** `framework/overview`，`file-storage`，`runtime/client`，`runtime/server`，`runtime/cli`，`runtime/plugins`，`runtime/lifecycle`，`runtime/react-providers`，`services/container`，`services/tokens`，`services/integration`，`http/routes`，`http/middleware`，`http/validation`，`http/repository-routes`，`http/api-client`，`database/overview`，`database/connections`，`database/schema`，`database/relations`，`database/repositories`，`database/query-inputs`，`database/filtering-pagination`，`database/association-queries`，`database/aggregation`，`database/transactions`，`database/migrations`，`database/seeds`，`background/jobs`，`background/scheduling`，`background/queues`，`realtime/topics`，`realtime/websocket`，`support/caching`，`support/logging`，`support/ids`

---

## 5. 应用架构

多门户、多应用、多租户可组合：多入口共用一套应用与版本用**多门户**；要独立数据/配置/版本用**多应用**；面向多客户时可为每租户一个独立 App（租户 App 内仍可多门户）。统一登录 ≠ 拥有所有应用权限，也不会自动打通业务数据。多门户管理、门户生成器、多门户模板，以及多应用相关插件，属于商业能力。

**多门户：** 同一应用内的业务入口，共享登录与运行环境，随应用统一升级；数据访问仍由权限控制，也可用多数据库连接。创建与开发见 `architecture/multi-portal/create-app`，`develop`，`access`，`manage`。

**多应用：** **Main** 是平台入口（工作台、应用管理、平台身份）；**子应用** 有自己的页面、API、数据库、配置和业务权限。平台决定能进哪些应用，子应用决定进去后能做什么。平台管理员不会自动成为子应用管理员。项目模板常把 Main 放根目录、默认子应用在 `apps/sub/`，共享依赖与锁文件，但分别开发、构建、部署；子应用也可在独立仓库。

平台中的**应用模板**管理某业务的部署版本；**版本**是一次构建的部署归档；**实例**是使用某版本运行的应用（如东/西门店）。发布新版本不会自动升级已有实例。托管应用由平台经 Releases 与 App Host 创建实例；独立接入则自行部署，平台提供入口和可选统一登录。源码位置不决定部署方式。托管时 Main 使用子应用部署归档，不直接跑其业务源码。

所需商业插件（项目模板不含实现也不提供授权）：`@nocobase/app-plugin-multi-app`（Main）、`@nocobase/app-plugin-identity-provider`（Main）、`@nocobase/app-plugin-platform-sso`（需平台登录的 NocoBase 子应用）。统一登录 Web 回调要求可信 HTTPS 和非回环主机名，不能用 `localhost`。启用平台身份后，新实例会登记登录客户端，但不会自动允许所有平台用户进入。只拥有应用访问资格不能因此管理实例。

运维要点：更新 Main 不会发布子应用；发布子应用版本也不会自动升级实例。实例「归档/恢复归档」是管理状态，不是数据库备份/恢复。代码回退不会自动撤销已执行迁移。不要只备份 Main 库。更换平台域名或挂载路径时，还要处理已保存的环境地址、回调、独立入口和身份绑定。外部应用接入 SSO 须支持授权码、PKCE S256、`client_secret_basic` 及标准 issuer/audience/签名校验；用户映射与业务权限由第三方负责。演练环境不要发生产通知或与生产争抢队列。

**出处：** `architecture/overview`，`architecture/multi-portal/create-app`，`develop`，`access`，`manage`，`architecture/multi-app/overview`，`quickstart`，`development`，`management`，`deployment`，`single-sign-on`，`external-apps`，`migration`

---

## 6. 部署与运维

适用自己的 Core 应用。Docker：容器 + 镜像与持久化挂载。PM2（app-installer）：Linux 上托管 Node 进程，安装器管理安装、配置、版本切换、备份和回退。源码留在开发机，服务器运行配置和业务数据独立于发布版本。两种方式都用独立生产配置、数据库和文件存储；构建前确定平台、数据库和存储。

构建产物含页面、接口、迁移和运行依赖，**不会**自动携带开发数据库、上传文件或运行密钥。首次用新库会执行迁移和必需种子；示例应用可能初始化角色，但不会复制开发环境中的商品、用户或角色分配。通过管理页创建的其他角色也不会自动迁入。`node dist/server/standalone.js` 只能检查产物，正式部署还需进程托管、配置管理与数据持久化。

构建指定平台（原生依赖不能简单跨系统复制）：

```bash
pnpm build --target linux-x64 --node-version 24 --tar
# 归档写入 storage/exports/dist.tar.gz；目标如 linux-arm64-musl
```

**Docker 要点：** 开发机构建匹配架构的镜像，如 `docker build --platform linux/amd64 -t my-app:1 .`。部署目录含 `docker-compose.yml`、`config.yml`、`storage/`。启动：`docker compose -p my-app up -d --wait --wait-timeout 180`。健康检查示例：`curl --fail http://<IP>:13000/main/api/healthz`（保留应用路径）。容器内 CLI：`docker compose -p my-app run --rm --no-deps app node dist/cli/index.js config check --connect`（以及 `db apply --dry-run --json` 等）。更新：构建新标签，改 Compose 镜像版本并 `--force-recreate`，保留配置和存储挂载。`down` 删除容器但可保留主机配置与数据。更新前备份 `config.yml`、`storage`、`docker-compose.yml`。

**PM2 / app-installer：** 命令使用 `@nocobase/app-installer@beta`（或固定版本），在服务器执行；开发机负责构建、打包、上传。示例：应用名、独立目录/端口/进程名、端口 `13000`、路径 `/main`。服务器需 Node 24、全局 PM2 4.3+。首次安装设置 origin/host/port/name 等；**升级用 `upgrade`，不再传这些首次参数**，保留原配置、密钥、库和上传。预检可能返回 `CONFIRMATION_REQUIRED`（此时尚未切换）；重复同包可为 `success-noop`。安装器自动备份可识别的 SQLite、`config.yml`、`app.env`；上传文件、外部库、对象存储须另行备份。`--backup-done` 只确认外部库已备份，不执行备份。若 `CHECKSUM_REPAIR_REQUIRED`，普通 `--yes` 不会授权修复，须按计划加 `--repair-checksums <token>`。错误：`PORT_IN_USE`（换端口并同步 origin，不要停无关进程）、`DRIVER_MISSING`（在源码加驱动并重建）、`START_FAILED`（看返回的日志路径和安装目录 `logs/`）。

发布新版本：沿用生产库、配置和文件存储；涉及结构变更时把新迁移随代码发布，保留已执行迁移；先备份，留存旧包或镜像。切回旧代码不一定能恢复数据库。先按升级 Core 文档完成框架升级再部署。

公网访问须先配域名、HTTPS 和反向代理，再登录管理员。文档中的 IP+HTTP 示例仅用于可信网络验证。

**出处：** `deployment/choose-a-deployment-method`，`deployment/publish-app-release`，`tutorials/deploy-with-docker`，`tutorials/deploy-with-app-installer`；升级另见 `developing-apps/upgrade-nocobase-core`

---

## 7. 参考

### 公开导入入口

| 入口 | 常用导出 |
| --- | --- |
| `@nocobase/app-client` | `createApp`、`defineClientPlugin`、`defineAppRoutes`、`useService`、`useApiClient` |
| `@nocobase/app-server` | `defineServerPlugin`、`defineServerPlugins` |
| `@nocobase/app-server/router` | `defineApiRoutes`、`defineRepositoryApiRoutes`、`defineRootRoutes`、`defineHttpMiddleware`、`apiValidator`、`ApiError` |
| `@nocobase/app-server/config` | `defineAppConfig`、`defaultAppConfigs`、`envString`、`envInteger`、`envBoolean` |
| `@nocobase/service-provider` | `ServiceProvider`、`ServiceContainer`、`createServiceToken` |
| `@nocobase/api-client` | `createApiClient`、`ApiClientError` |
| `@nocobase/db` | `createDatabaseManager`、`databaseManagerToken` |

数据库完整签名另见 Core 源码 `packages/libs/db/docs/api-reference/`（修订 `015404ecd0db`）。

### 命令速查

“两者”= 源码与部署产物均有。插件还会贡献命令，以 `commands` 输出为准。`dev`/`build`/`start` 等透传命令不统一支持 JSON。

| 命令 | 环境 | 要点 |
| --- | --- | --- |
| `dev` / `build` / `start` | 源码 | 开发、构建、启动产物 |
| `info` / `commands` | 两者 | `commands --json` 含参数与执行能力 |
| `config init` | 两者 | `--dialect`、`--config`；不安装驱动 |
| `config set` | 两者 | `key=value`；`--from-env` 把当前环境变量值写入文件（不是动态引用） |
| `config check` | 两者 | 默认尝试非 SQLite 连接；`--no-connect` 离线；`--connect` 也验证 SQLite；`--strict` 警告即失败；不执行迁移 |
| `config env` / `variables` | 两者 | 映射 / 部署清单；`variables --out` 写文件 |
| `db apply` | 两者 | 待运行迁移与初始数据；`--dry-run`；`--connection` 与 `--all` 互斥 |
| `db rollback` / `redo` | 两者 | 回退最近一批 / 回退后重做 |
| `db reset` | 两者 | 重置受管理表，删数据 |
| `db repair` | 两者 | 只修迁移校验和记录 |
| `db unlock` | 两者 | 处理残留锁；须先确认无迁移进程 |
| `db sample` | 仅开发 | 部署环境拒绝执行 |
| `collections generate` / `doctor` | 两者 | 生成快照 / 诊断；`doctor --fix` 会修改内容 |
| `locales check` | 两者 | 检查多语言资源 |
| `secrets status` / `rotate` | 两者 | `rotate --dry-run`、`--batch-size` |
| `plugin inspect/register/unregister/update` | 源码 | register/update 可 `--dry-run` |
| `package remove` | 源码 | 移除依赖及相关接入 |
| `skills sync` | 源码 | 可按包选择、`--dry-run` |
| `dist check` / `retarget` | 源码 | 检查/调整部署产物 |
| `cli build` / `cli link` | 源码 | 可分发业务 CLI / 本地链接 |

JSON 成功信封含 `schemaVersion`、`ok`、`command`、`status`、`result`、`warnings`。同时检查退出码、`ok`、`status`。`success-noop` 无需变更；`partial-success` 须看 warnings。`NOCOBASE_CONTENT_TYPE=json` 只对支持该模式的命令生效。

### 常用配置与环境变量

字段：`server.host`/`port`（模板代码默认 `127.0.0.1`/`13000`）、`server.startLog`、`app.publicOrigin`、`app.sampleData`、`database.default`（模板 `main`）、`database.connections.<name>`、`api.bodyLimit`/`timeout`/`rateLimit`、`secrets.keys`、`session`/`auth`、`users.initialAdmin`、`i18n.defaultLocale`、`logging`、`client.app.title`/`defaultColorScheme`/`defaultTheme`、`jobs`/`queue`/`caching`/`drive`，以及随插件出现的 `mail`/`notification`/`scheduler`/`knowledge`。局域网监听可改 `0.0.0.0`，但浏览器须用实际 IP；`pnpm dev` 可能还有独立前端端口。

环境变量映射（已核对清单，精确以 `config variables` 为准）：`APP_SERVER_HOST`/`PORT`/`START_LOG`，`APP_PUBLIC_ORIGIN`，`APP_SAMPLE_DATA`，`DB_DIALECT`/`HOST`/`PORT`/`DATABASE`/`FILENAME`/`USERNAME`/`PASSWORD`/`SSL`（仅 main），`API_BODY_LIMIT`/`TIMEOUT`，`SECRETS_KEYS`（`版本:密钥` 逗号分隔，第一项为当前密钥，轮换须保留旧项），`AUTH_SECRET`/`SESSION_SECRET`，`INITIAL_ADMIN_*`，`APP_DEFAULT_LOCALE`，`SNOWFLAKE_WORKER_ID`，`APP_VITE_DEV_URL`（`spa.viteDevUrl`），以及 mail/notification/scheduler 相关项。运行时另读：`APP_BASE_PATH`、`APP_CONFIG_FILE`、`NOCOBASE_STRICT_STARTUP`。会话优先用显式 `session.secret`，未设时才尝试从 Secrets 派生。

自定义分区示例：`defineAppConfig({ defaults, env: { ANNOUNCEMENTS_PAGE_SIZE: envInteger('pageSize', { description }) }, public: ['pageSize'], validate })`，在 `defaultAppConfigs({ … })` 中登记。`validate` 在启动、reload、`config check` 时运行，不要在其中发网络请求或写数据。

### 数据库方言

8 种方言；MariaDB 与 MySQL 共用 `mysql`，不要写成 `mariadb`。

| 数据库 | 包 | dialect | 要点 |
| --- | --- | --- | --- |
| SQLite | `@nocobase/db-sqlite` | `sqlite` | 默认模板已装；`database` 为文件路径，相对路径按 `storage/` 解析 |
| PostgreSQL | `@nocobase/db-postgres` | `postgres` | 可 `schema`、`ssl`；专用 CA 用 `ssl.ca` 填 PEM 内容而非路径 |
| MySQL / MariaDB | `@nocobase/db-mysql` | `mysql` | `charset` 如 `utf8mb4`；JSON 过滤需 MySQL ≥8.0.17 或 MariaDB ≥10.9 |
| SQL Server | `@nocobase/db-mssql` | `mssql` | `encrypt`、`trustServerCertificate` |
| Oracle | `@nocobase/db-oracle` | `oracle` | 用 `serviceName`（不是 SID，也不用 `database`） |
| 达梦（Pro，实验性） | `@nocobase/db-dameng` | `dameng` | 用 `schema`，初始化不生成 `database` |
| 人大金仓（Pro） | `@nocobase/db-kingbase` | `kingbase` | 须 `DB_MODE=pg`，仍用本方言与驱动 |
| OceanBase CE（Pro） | `@nocobase/db-oceanbase` | `oceanbase` | MySQL 兼容租户；TEXT 默认值由 Repository 在创建时填充，直接 SQL 插入须自行给值 |

商业驱动经 Pro registry：`pnpm login --registry="<url>" --scope=@nocobase`，令牌作密码，不写入文档/参数/Git。`config init --dialect … --json` 生成配置和密钥但不连库、不装驱动、不建账号。改已有 `config.yml` 时保留原密钥。集成测试曾用 PG16、MySQL 8.4、MariaDB 10.11、SQL Server 2022、Oracle Free 23，这不是完整兼容范围承诺。

### 包索引（按职责，非必装清单）

运行时：`app-client`、`app-server`、`app-cli`、`app-websocket`。基础库：`api-client`、`authorization`、`caching`、`config`、`db`、`drive`、`i18n`、`jobs`、`lifecycle`、`logging`、`mailer`、`queue`、`realtime`、`repository-input`、`secrets`、`service-provider`、`session`、`snowflake`、`document-extractor`、`markdown-mermaid`。工具：`app-skills`、`app-testing`、`db-testing`、`db-testkit`、`dev-config`、`create-app`、`create-plugin`。部署：`app-installer`、`app-host`、`app-host-docker`。Agent/远程命令：`acp-bridge`、`agent-protocol`、`agent-runner`、`app-cli-client`、`cli-envelope`。创建插件：`pnpm create @nocobase/plugin@beta`。

### FAQ 要点

功能写应用还是插件、安装后无页面、组件不必固定结构、不必为复用而发 UI Registry、本地 UI 资产不必启 Registry 服务、ServiceProvider 非服务端专用、config 不生效原因、初始管理员密码不改已有账号、命令与教程不符时先确认是 v3 且入口正确、建表不自动生成 API、校验和不一致时通常新增迁移、换方言不搬数据、包版本不必强行对齐、`storage/` 不能当构建缓存删、反馈问题时提供脱敏错误与包版本而不提供密钥。详见 `reference/faq`。

**出处：** `reference/api`，`cli`，`configuration`，`project-conventions`，`packages`，`plugins`，`compatibility`，`database-configuration`，`faq`
