# 文档地图

> 共 134 篇 · 7 个分组 · 约 675,235 字符

机器可读版：[llms.txt](https://meesumaes.github.io/nocobase-core-docs/llms.txt) ｜ 全量正文：[llms-full.txt](https://meesumaes.github.io/nocobase-core-docs/llms-full.txt) ｜ 官方原文：[https://docs.nocobase.com/zh-CN/core/](https://docs.nocobase.com/zh-CN/core/)

## 开发应用（26）

- [应用开发概览](/developing-apps/overview)：NocoBase Core 及配套插件提供开发业务应用所需的基础能力，包括数据库、服务端、客户端、认证与权限等。开发者可以直接使用这些能力，专注于业务功能的实现，而不必从零搭建基础设施。
- [项目结构](/developing-apps/project-structure)：目录会随模板版本和业务功能变化。packages/ 等可选目录按需创建，不必为了匹配目录树而补齐。
- [应用配置（config.yml）](/developing-apps/configuration-and-settings)：config.yml 保存当前应用环境的配置，例如应用标题、数据库连接、默认语言和日志级别。client/config/ 与 server/config/ 则定义代码默认值，以及需要通过代码构造的配置…
- [测试](/developing-apps/testing-and-acceptance)：一个功能开发完成后，需要确认它在正常操作、权限受限和执行失败时都能得到预期结果。例如商品管理功能，既要检查创建和发布能否成功，也要检查只读账号能否被阻止修改、保存失败后能否重试。

### 客户端

- [页面、路由与导航](/developing-apps/pages-routes-and-navigation)：使用 defineAppRoutes() 声明页面地址、组件、菜单和访问权限。[示例 App][app] 的启动和账号准备见运行环境与启动方式。
- [UI 组件与交互](/developing-apps/pages-and-interactions)：NocoBase 应用统一使用 shadcn 规范组织 UI。组件源码放在应用中，页面负责连接数据与操作，应用负责维护自己的组件和交互约定。
- [数据请求与状态管理](/developing-apps/data-requests-and-state)：客户目录示例展示搜索、翻页、查看详情和编辑时的数据流转：查询条件跟随 URL，读取结果来自服务端，未提交的字段留在表单中。示例使用真实数据库、应用权限和提交回执；慢请求、写入拒绝和响应丢失通过演示开关…
- [页面布局](/developing-apps/page-layouts)：业务页面通常只需要组合已有的页面容器、标题和内容区；品牌、侧边栏和全局操作由应用外框管理。这些组件都是应用持有的源码，基础交互遵循 shadcn 规范，组件添加方式见 UI 组件与交互。
- [多语言](/developing-apps/localization)：应用通过 client/locales/ 组织文案，沿用已有的翻译和语言切换机制，让菜单、表单、空状态和错误反馈保持一致。外观调整见主题与样式。
- [主题与样式](/developing-apps/themes-and-styles)：业务界面沿用应用已有的 shadcn 组件和语义主题变量。颜色、间距、字体和圆角在主题文件中调整，列表、表单、弹窗便能一起适配外观变化。NocoBase UI Library 的组件和业务区块也遵循这…
- [客户端服务](/developing-apps/client-business-services)：客户端服务用于在多个组件或页面之间复用操作、协调状态变化，或管理应用级资源。服务可以封装业务操作，也可以提供缓存、通知等通用能力；ServiceProvider 负责把它注册到应用容器。

### 服务端

- [HTTP 路由与接口](/developing-apps/apis-and-services)：应用可以直接返回 HTML、重定向和文件，也可以提供供页面或其他客户端调用的 JSON 接口。下面用 Product Catalog 示例展示这些用法；完整源码与启动方式见文末。
- [服务端服务](/developing-apps/server-business-services)：服务（Service）是封装可复用逻辑的类或对象，无需继承框架基类。例如，将订单确认和库存扣减放在订单服务中，HTTP 接口、应用命令和后台任务就能复用这些规则。简单查询或计算也可以保留为普通函数。
- [请求校验与错误处理](/developing-apps/request-validation-and-errors)：订单接口示例提供查询、新建和修改操作：请求参数先经过校验，业务服务再检查客户是否可用、订单是否允许修改。失败时返回统一错误，客户端可以定位字段或提示业务原因。示例源码与运行在文末。
- [认证、权限与数据范围](/developing-apps/authentication-and-permissions)：Customer Access 示例中，销售可以维护自己负责的客户，并为自己的订单更换客户；只读销售只能查看。接口使用真实的认证、授权和数据库，页面沿用默认模板的 shadcn 组件与用户、角色管理。…
- [后台任务与定时执行](/developing-apps/background-tasks)：通过 JobExecutor 在后台生成报表，让业务入口先返回受理结果；通过 ScheduleExecutor 按固定间隔或每天指定时间触发。业务代码负责生成报表、处理重复执行和保存结果。
- [工作流](/developing-apps/business-workflows)：工作流基于状态机定义业务记录的状态、允许的流转及其触发条件，适合需要跨越多次请求、持续较长时间，并由人员操作、自动处理或外部系统共同推进的业务流程。例如，订单可以等待用户付款、接收支付回调，再由人员确…
- [服务端多语言](/developing-apps/server-localization)：服务端生成的邮件、通知和导出内容使用 server/locales/。它与 client/locales/ 独立加载：页面上能翻译的 key，服务端仍需声明。

### 数据库

- [建表与数据初始化](/developing-apps/data-models-and-migrations)：在已有 NocoBase 应用中，可以用 Migration 创建状态字典，再用 Seed 安装默认值。下面的 appStatuses 保存稳定的状态编码和可编辑名称；后续升级为它增加说明字段。没有应…
- [查询与操作数据](/developing-apps/querying-data)：数据访问通常从 Repository 开始：它理解 Collection 的字段和关系，适合读取、创建和修改业务记录。Query 面向表和结果集，适合 Repository 不能表达的报表与聚合。两者…
- [事务与数据一致性](/developing-apps/transactions-and-consistency)：事务用于让同一数据库连接中的一组操作共同提交或回滚。它应围绕一个明确的业务结果组织，例如确认任务和目标项目都允许操作后，再保存归属。
- [多数据库连接](/developing-apps/multiple-databases)：一个应用可以使用多个数据库连接。Examples 模板用 main 保存应用数据，用 analytics 演示独立的分析数据；两者都由应用管理结构。连接名称对应 database/&lt;连接名>/，不是业…
- [接入已有数据库](/developing-apps/existing-databases)：如果数据库结构由 CRM、ERP 等其他系统维护，应用可以通过 schemaManagement: 'external' 接入。框架读取已有结构，再叠加应用维护的元数据；不通过这个连接运行迁移、See…

### 命令行

- [编写应用命令](/developing-apps/application-commands)：应用自己的命令放在 cli/commands/，适合导出数据、诊断或一次性维护。例如，在应用目录执行 pnpm nocobase app statuses export，读取状态字典并保存为文件。
- [接入插件命令](/developing-apps/plugin-commands)：插件通过 ./cli 入口提供命令，应用在 cli/plugins.ts 中选择接入哪些贡献。本篇关注应用侧的安装、注册与使用；命令实现和插件发布契约见命令行扩展。
- [为应用提供 CLI 客户端](/developing-apps/cli-client)：应用可以拥有一个独立的 CLI，例如 nocobase-examples。使用者在自己的电脑上登录应用，然后通过命令执行服务端业务操作；无需拿到应用源码或数据库配置。它也可以作为 Agent 调用业务…

## 使用插件（23）

- [插件使用概览](/using-plugins/overview)：NocoBase 提供用户、认证、权限、文件、通知、Agents 等插件，可用于构建应用中的常见功能。本章介绍各个插件的用途、配置方法，以及如何在应用中使用它们提供的页面、组件、接口、服务或 Skil…
- [管理插件](/developing-apps/manage-plugins)：默认模板已经包含多种插件。开发应用时，通常直接使用它们提供的认证、用户、权限、文件等能力；只有确认当前应用缺少所需能力时，才需要增加插件。任务和项目这类应用自己的业务代码仍放在应用目录，不必先拆成插件…
- [数据库浏览](/using-plugins/data-and-files/database-explorer)：@nocobase/app-plugin-database-explorer 用于查看应用已配置的数据库连接、Collection、字段及物理表结构，适合开发和排查数据模型问题。它不提供建表、改表或编…
- [文件](/using-plugins/data-and-files/file-management)：@nocobase/app-plugin-file 提供文件 Repository、上传接口构建工具和客户端服务，复用应用的数据库与 Drive 存储。应用可以据此实现头像、附件或资料库。
- [邮件](/using-plugins/notifications/mail)：@nocobase/app-plugin-mail 面向用户连接的邮箱，提供账户授权、邮件同步、阅读、撰写、发送、草稿、附件及发送记录。系统验证码和业务通知的邮件投递使用通知渠道；需要读取用户邮箱或以…
- [Agents](/using-plugins/agents-and-knowledge/agents)：@nocobase/app-plugin-agents 为应用提供 AI 对话、模型配置、业务 Skills 和机器 Agent。你可以给业务页面加一个聊天面板，让 Agent 按团队规范处理内容，或…
- [知识库](/using-plugins/agents-and-knowledge/knowledge)：@nocobase/app-plugin-knowledge 提供知识空间、目录、Markdown 文档、文件、版本、搜索及修改建议。基础知识库可以独立使用，不要求启用 Agents 或语义检索。
- [审批](/using-plugins/collaboration/approval)：@nocobase/app-plugin-approval 将人工审批接入围绕业务记录推进的工作流，管理审批参与人、任务、操作记录与内容快照。适合请假、采购、合同等需要人工确认的业务。它是商业插件，安…
- [定时任务](/using-plugins/automation/scheduler)：@nocobase/app-plugin-scheduler 用于在代码中声明计划任务，将调度交给宿主 Jobs，并记录每次触发结果。适合定期同步、汇总报表和业务巡检。
- [模板打印](/using-plugins/automation/template-print)：@nocobase/app-plugin-template-print 提供模板打印的 Agent Skills 与参考实现，帮助应用从 Office 模板和业务数据生成文档，并按需要处理图片、二维码…
- [多语言](/using-plugins/application-support/i18n)：@nocobase/app-plugin-i18n 提供应用运行时语言切换接口与 hooks。翻译资源、命名空间和翻译机制由框架负责；本插件负责让用户选择语言并同步服务端偏好。
- [应用底座](/using-plugins/application-support/foundation)：@nocobase/app-plugin-foundation 提供应用能力概览，帮助管理员了解当前应用接入了哪些 Core 能力、已有何种使用证据，以及业务模块与这些能力的关系。

### 用户与认证

- [用户管理](/using-plugins/authentication/users)：@nocobase/app-plugin-users 提供用户查询、账号管理、邀请和个人偏好能力。登录身份、密码和会话由身份认证提供，用户管理复用这些数据；角色与操作权限由权限管理及应用业务定义。
- [身份认证](/using-plugins/authentication/sign-in)：@nocobase/app-plugin-authentication 将 Better Auth 接入应用，提供登录身份、会话、认证客户端和服务端认证中间件。它回答“当前是谁”；该用户能进行哪些操作…
- [API 密钥](/using-plugins/authentication/api-keys)：@nocobase/app-plugin-api-keys 为脚本和外部系统提供 API 密钥认证。请求使用 x-api-key，以密钥所属用户的身份执行；带范围的密钥还会受到自身范围限制。

### 权限与数据访问

- [权限管理](/using-plugins/authorization/permissions)：@nocobase/app-plugin-authorization 提供应用授权服务、权限集、页面和设置项权限，以及数据库字段、记录和关联访问策略。适合控制“谁能打开某个页面、执行某个业务操作、访问…
- [默认数据范围](/using-plugins/authorization/default-access)：@nocobase/app-plugin-authz-default-access 默认数据范围为已经拥有某个操作权限的主体，增加一份共同可访问的记录范围。它与权限集自己的范围合并，不是只有“未设置范…
- [共享规则](/using-plugins/authorization/sharing-rules)：@nocobase/app-plugin-authz-sharing-rules 共享规则为指定用户、团队等主体追加记录范围。它适合交接、跨团队协作或指定记录的临时共享；接收方仍需拥有相关业务操作权限…
- [限制规则](/using-plugins/authorization/restriction-rules)：@nocobase/app-plugin-authz-restriction-rules 限制规则收窄指定主体已经取得的记录范围。规则中的选择表示“仍然允许访问的记录”，而不是需要屏蔽的记录；多条匹配…

### 通知

- [通知](/using-plugins/notifications/notification)：@nocobase/app-plugin-notification 是通知投递运行时，负责消息校验、持久化、队列、幂等处理、投递状态和有限重试。具体发送方式由通知渠道、站内信、浏览器推送等插件提供。
- [通知渠道](/using-plugins/notifications/providers)：@nocobase/app-plugin-notification-providers 为通知提供 SMTP、Resend、飞书机器人和钉钉机器人渠道。它只有 Server 运行时入口，不提供配置页面…
- [站内信](/using-plugins/notifications/in-app)：@nocobase/app-plugin-notification-in-app 提供 in-app 通知渠道及当前用户的收件箱，支持未读数、已读/未读、全部已读和删除消息。
- [浏览器推送](/using-plugins/notifications/web-push)：@nocobase/app-plugin-notification-web-push 将通知发送到已订阅的浏览器设备，提供 VAPID 配置、设备订阅、Service Worker 和可复用设备设置组…

## 开发插件（20）

- [什么时候写插件](/extension-development/when-to-write-a-plugin)：在 NocoBase 中，插件把一项功能封装为独立的包，由 App 按需接入。编写插件主要有两个原因：代码复用和模块化组织代码。两者满足其一，就可以考虑使用插件。
- [创建插件](/extension-development/create-plugin)：先按创建应用准备一个 App 并完成依赖安装。插件会生成在这个 App 的 packages/ 下，与应用一起开发和构建。
- [插件结构](/extension-development/plugin-structure)：本篇以 create-app 创建的 App 为前提，说明本地插件的文件放在哪里、各自负责什么，以及怎样接入应用。插件位于 App 的 packages/ 下，目录随所选能力变化，不要求每个插件都具备…
- [插件开发指引（AGENTS.md）](/extension-development/plugin-development-guidance)：插件的 AGENTS.md 面向维护源码的 Agent：让它知道这个插件负责什么，修改一项能力时需要检查哪些文件，以及如何验证结果。指引应记录跨任务仍然有效的约定，并随插件源码维护。
- [编写第一个插件](/extension-development/write-your-first-plugin)：本篇实现一个“公告栏插件”：在 App 菜单中打开公告栏，页面请求插件提供的接口并显示公告列表。这个例子同时用到 Client 和 Server，能直观看到插件如何为应用增加功能。
- [插件声明与公开入口](/extension-development/plugin-declarations)：插件内部的页面、接口、服务和命令，需要通过插件声明汇总，再由应用接入。允许应用或其他插件直接使用的组件、类型和服务，还需要从包的公开入口导出。
- [数据库资源与迁移](/extension-development/database-and-migrations)：插件通过 Server 声明提供迁移和 Seed，由安装它的应用统一执行。下面以 notice-data 插件的公告分类字典为例；建模、Context 和执行规则与应用共用，详细用法见数据表与字段、数…
- [命令行扩展](/extension-development/extend-command-line)：插件可以给 App 增加自己的命令，用于诊断、生成文件或一次性维护。本篇添加 notice-cli preview，在终端检查文本并输出预览结果；它不启动应用服务，也不写入数据库。
- [插件 Skill](/extension-development/write-plugin-skills)：插件 Skill 是给使用插件的 Agent 的说明：有哪些已经实现的能力、从哪个公开入口调用、由谁维护数据，以及如何判断操作成功。它不负责实现功能，也不会自动注册插件。
- [测试与验证](/extension-development/testing-and-verification)：插件检查通过、App 注册成功和用户实际能用，是三个不同的结果。验证应该沿着本次变化的边界进行：先检查插件本身，再检查接入 App 后的行为，涉及发布时再检查包的内容。
- [构建与发布](/extension-development/publish-plugin)：插件不发布，也可以一直在 App 中使用。 本地插件放在 packages/ 下，通过工作区依赖和运行时注册接入应用。App 构建会构建依赖的本地包，将需要交付的插件产物收集到 dist/vendor…

### 客户端

- [页面、路由与菜单](/extension-development/pages-and-menus)：插件通过路由声明把页面接入 App，菜单也来自这些声明。本篇实现一个“帮助中心”：侧边栏只有一个入口，页面内可切换“使用指南”和“常见问题”，刷新或分享链接都能保留当前内容。
- [组件与样式](/extension-development/frontend-components)：开发应用和插件时，前端组件可以自由编写和组织，唯一约束是基础组件使用 shadcn。构建模块化界面时，优先参考 NocoBase UI Library 中的组件和区块。
- [React Context 与 Provider](/extension-development/react-context-and-providers)：本篇为公告页面提供紧凑显示偏好，重点说明 contexts.ts、Provider 组件和 react-providers/ 怎样连接。状态由 React 树维护，不需要数据库、HTTP 接口或 Se…
- [客户端服务](/extension-development/client-services)：当多个页面需要协作刷新公告列表时，可以由插件提供一个变更通知服务。它负责发布“已保存”的通知，页面负责请求数据和显示反馈。本例只维护当前浏览器应用实例中的版本号，不实现保存接口、请求缓存或跨浏览器同步…
- [客户端多语言](/extension-development/localization)：插件管理自己的文案，App 决定界面提供哪些语言以及用户当前选择的语言。本篇维护 client/locales/；请求和后台消息的文案见服务端多语言。两端分别声明资源，使用相同的插件包名作为命名空间。

### 服务端

- [路由与 HTTP 接口](/extension-development/server-apis)：插件的服务端接口负责接收请求、检查输入和访问权限，再调用业务逻辑。本篇实现一个公告文本预览接口：接收文本，去掉两端空白，返回文本和字符数，不保存数据。
- [业务服务与 ServiceProvider](/extension-development/server-services)：本篇为公告插件提供文本预览服务，让 HTTP、CLI 或其他插件复用同一实现。services/ 放业务实现，tokens.ts 定义公开契约，providers/ 把实现注册到应用容器。这里不访问数…
- [后台任务与执行器](/extension-development/background-jobs)：本篇让公告插件异步生成文本摘要，说明 server/jobs/ 与 Provider、应用 Jobs 服务如何配合。示例只截取前 80 个 Unicode 码点并记录到日志，不使用 AI、不写数据库，…
- [服务端多语言](/extension-development/server-localization)：插件在 server/locales/ 维护服务端文案，通过 server/plugin.ts 的 locales 接入应用。客户端页面使用独立的 Client 语言资源，注册 Client 插件不会…

## 框架（37）

- [框架概览](/framework/overview)：本章介绍应用和插件共同使用的框架机制，以及 @nocobase/ 核心包的职责、使用方式和运行边界。需要实现页面、接口或插件时，可以从开发应用和开发插件开始，遇到具体机制再回到这里查阅。
- [缓存](/framework/support/caching)：@nocobase/caching 提供带命名空间的缓存、计数器和布隆过滤器。应用使用 @nocobase/app-server/caching 的 cachingToken 复用宿主实例；缓存用于加…
- [文件存储与驱动](/framework/file-storage)：@nocobase/drive 统一文件存储驱动，宿主通过 @nocobase/app-server/drive 的 driveManagerToken 提供管理器。文件插件在它上面提供文件记录、上传…
- [消息队列](/framework/background/queues)：@nocobase/queue 提供消息生产与消费。大多数后台业务可先用Jobs；需要通道、延迟、优先级、批量投递或限流控制时，再直接使用队列。
- [日志](/framework/support/logging)：@nocobase/logging 提供结构化日志、来源标记、输出和轮换。应用通过 @nocobase/app-server/logging 的 loggingToken 取得服务。
- [ID 生成](/framework/support/ids)：@nocobase/snowflake 生成带时间顺序的 JavaScript 安全整数 ID。应用通过 @nocobase/app-server/id-generator 的 idGenerator…

### 运行时与扩展机制

- [客户端运行时](/framework/runtime/client)：客户端运行时把配置、服务、插件、路由与 React 扩展组合成一个浏览器应用。应用与插件都向同一套运行时提供声明，最终的页面布局与组件由应用决定。
- [服务端运行时](/framework/runtime/server)：服务端运行时负责配置、资源路径、服务生命周期以及 HTTP 和 WebSocket 接入。它将业务应用与监听端口的宿主分开，使同一应用可以用于独立服务、命令或测试。
- [命令行运行时](/framework/runtime/cli)：@nocobase/app-cli 将框架命令、应用业务命令与插件命令组成一棵命令树。它根据应用清单识别源码工作区或部署产物，加载对应入口。
- [应用启动与生命周期](/framework/runtime/lifecycle)：生命周期把服务声明、异步初始化、消费者启动和清理放在明确阶段。应用与插件共用这个顺序，因此可在使用依赖前知道它已经完成哪一阶段。
- [插件加载与扩展](/framework/runtime/plugins)：插件通过公开入口声明贡献，由目标应用显式组装。依赖安装、运行端注册和最终业务接入是三个需要分别确认的步骤。
- [React Provider 的注册与挂载](/framework/runtime/react-providers)：React Provider 为页面树提供上下文，例如表单状态、主题或共享交互。它是接收 children 的 React 组件，和注册应用服务的 ServiceProvider 各有职责。

### 服务容器与依赖注入

- [服务容器](/framework/services/container)：服务容器将服务的使用者与创建方式分开。调用方依赖接口和 Token，应用在组装时决定使用哪个实现。客户端和服务端都采用这套机制，但各自拥有实例。
- [服务契约与 Token](/framework/services/tokens)：服务契约描述调用方能够做什么；Token 用来在容器中找到实现。将接口与 Token 放在公开模块，可以让应用、插件和测试使用同一约定，而无需引用内部类。
- [ServiceProvider 与服务生命周期](/extension-development/service-provider)：ServiceProvider 把插件提供的服务接入 App 的容器，并管理服务需要的启动与清理工作。前端和后端使用相同的基本机制，但运行在不同环境，容器和实例互不共享。
- [前后端服务接入](/framework/services/integration)：@nocobase/service-provider 为应用和插件提供同一套容器、Token 与生命周期机制。浏览器和服务端各自拥有容器；“共享契约”不表示共享跨网络的实例。

### HTTP 与 API

- [路由与请求上下文](/framework/http/routes)：HTTP 接口通过路由贡献接入应用，路由工厂在应用启动期间取得服务，处理器在每次请求到达时读取输入和身份。
- [中间件](/framework/http/middleware)：中间件处理多个接口共用的请求行为，例如身份解析、请求约束和响应头。它应围绕明确的路径与顺序注册，业务流程仍留在服务中。
- [请求校验与响应处理](/framework/http/validation)：接口在业务逻辑之前验证外部输入，并用稳定的响应结构报告结果。TypeScript 类型只约束开发代码，无法代替运行时校验。
- [Repository 数据接口](/framework/http/repository-routes)：defineRepositoryApiRoutes() 把指定 Collection 的 Repository 操作声明为 HTTP 接口。客户端通过 api.repository(name) 调用，…
- [API Client](/framework/http/api-client)：API Client 统一处理应用的 HTTP 地址、凭证和请求格式。应用组件优先取得运行时已经配置的客户端，避免在每个页面重新拼接服务端地址。

### 数据库

- [数据库概览](/framework/database/overview)：@nocobase/db 提供逻辑数据模型、数据读写、结构演进与事务。方言包负责连接具体数据库，应用运行时负责配置、资源发现和生命周期。
- [连接与数据库方言](/framework/database/connections)：连接将逻辑数据库能力绑定到具体数据库和命名空间。一个管理器可以包含多个连接，每个连接有自己的方言、事务和模型解析。
- [数据表与字段](/framework/database/schema)：CollectionBuilder 把逻辑集合定义转换为数据库结构，并同步模型所需的元数据。应用和插件都在 Migration 的 up(\{ builder \})、down(\{ builder \})…
- [关系与关联](/framework/database/relations)：关联让 Repository 按逻辑模型读取和写入相关记录。以下示例在迁移的 up(\{ builder \}) 中执行，使用数据表与字段中的 orders：包含自增 id 和可空整数 customerI…
- [Repository 与数据操作](/framework/database/repositories)：Repository 按 Collection 的逻辑字段和关系读写数据，处理字段编解码、查询输入和绑定的策略。取得 Repository 不会创建表，也不会替调用方完成身份认证。
- [过滤、排序与分页](/framework/database/filtering-pagination)：Repository 用 filter 选记录、sort 定顺序，再应用分页。列表、计数和导出应基于同一授权范围，避免显示越权数量或产生无效页码。
- [关联查询](/framework/database/association-queries)：关联查询通过已声明的关系读取相关记录，避免调用方手工拼接物理表名。每一级关联都需要对应元数据，数据策略也必须允许相关读取。
- [聚合与统计](/framework/database/aggregation)：聚合在数据库端计算计数、求和、平均值和极值，适合总览和报表。统计也会暴露信息，应使用与明细相同的权限范围。
- [事务](/framework/database/transactions)：事务让同一个数据库连接上的一组操作共同提交或回滚。业务服务负责定义事务范围，Repository、Query 和 Builder 必须使用回调提供的事务连接。
- [数据库迁移](/framework/database/migrations)：Migration 记录一次固定的结构或历史数据变更。应用与插件使用同一个 defineMigration() API；文件位置和资源接入分别见建表与数据初始化和插件数据库资源。
- [初始数据](/framework/database/seeds)：Seed 安装应用或插件所需的初始记录，例如默认状态、分类。建表和升级中的历史数据回填属于 Migration，用户日常创建的订单等记录由业务服务处理。
- [查询输入与构造器](/framework/database/query-inputs)：@nocobase/repository-input 提供可在前后端使用的查询输入契约。构造器将代码表达转换为可序列化数据，数据库执行和授权仍在服务端完成。

### 后台任务与调度

- [后台任务与执行器](/framework/background/jobs)：耗时处理可以交给 @nocobase/jobs，让请求只负责接收任务。宿主的 jobExecutorServiceToken 位于 @nocobase/app-server/jobs；通过它取得按插件…
- [周期调度](/framework/background/scheduling)：ScheduleExecutor 按 Cron 或固定间隔触发任务，适合应用代码声明的清理、汇总和同步任务。需要可操作的定时任务列表、启停控制和执行记录时，接入定时任务插件。

### 实时通信

- [实时消息与主题订阅](/framework/realtime/topics)：@nocobase/realtime 将业务变更推送到订阅页面。应用通常复用 @nocobase/app-server/realtime 的 realtimeServiceToken，组件复用客户端运…
- [WebSocket 协议与适配](/framework/realtime/websocket)：@nocobase/app-websocket 定义宿主和应用共用的 WebSocket 接口，以及 Node HTTP Server 的升级适配。普通页面实时刷新优先使用实时主题；需要自定义宿主或其…

## 应用架构（13）

- [概览](/architecture/overview)：多门户、多应用与多租户分别解决业务入口、应用拆分和客户隔离的问题，可以组合使用。多个业务共用一个应用时，可以按门户组织入口；需要独立管理数据、配置和版本时，可以拆成多个应用；面向多个客户时，可以为每个…

### 多门户

- [创建多门户应用](/architecture/multi-portal/create-app)：创建并启动一个多门户应用，为后续业务门户提供运行环境。模板已经接好多门户插件、工作台和门户管理，但不包含预装的业务门户或示例数据。
- [开发门户](/architecture/multi-portal/develop)：准备一个已配置并能正常启动的多门户应用，保持商业包源登录有效，并使用具有 unrestricted 权限的管理员账号完成以下操作。
- [门户访问与权限](/architecture/multi-portal/access)：在已创建并安装门户的应用中，让 Agent 结合现有权限体系实现门户访问控制。下面以开发门户中的门户 1、概览（Overview）和示例列表（Examples）页面为例，将以下需求交给应用项目中的开发…
- [管理门户](/architecture/multi-portal/manage)：使用具有 unrestricted 权限的管理员账号登录，打开 系统设置 → 门户管理。

### 多应用

- [概述](/architecture/multi-app/overview)：当多个业务系统需要独立管理数据、配置和发布版本，同时又希望提供统一入口与登录体验时，可以采用多应用架构。
- [快速开始](/architecture/multi-app/quickstart)：准备 Node.js 24 或更新版本、pnpm 11.11.0，以及多应用商业插件的许可和下载权限。要体验平台统一登录，还需要一个由可信证书保护的 HTTPS 域名。
- [应用开发](/architecture/multi-app/development)：Main 和子应用都是普通的 NocoBase 3 应用。页面、API、数据库和测试沿用应用开发的方式；这里只说明多个应用一起开发时的区别。
- [管理模板与应用实例](/architecture/multi-app/management)：以下操作适用于由 App Host 托管的应用，需要相应管理页面、操作和数据范围权限。只拥有应用访问资格的用户不能因此管理实例。外部系统的部署和启停由其负责人处理，见接入独立应用。
- [统一登录与访问授权](/architecture/multi-app/single-sign-on)：用户登录平台后，可以进入自己获准访问的子应用。平台会话有效时，浏览器完成认证跳转，无需再次输入平台密码；子应用随后建立自己的会话。
- [接入独立应用](/architecture/multi-app/external-apps)：独立接入适用于继续使用原部署环境的应用。平台登记入口并按所选方式提供登录，不创建 Host 实例，也不接管原应用的数据库、升级或备份。
- [从单应用迁移](/architecture/multi-app/migration)：已有 NocoBase 3 应用可以保留原部署接入平台，也可以迁入平台托管，或在原系统中增加主应用能力。这里不涉及 NocoBase 2 到 3 的迁移。
- [部署与运维](/architecture/multi-app/deployment)：Main 和子应用沿用普通应用的部署方式。服务器准备、配置初始化、进程管理及版本更新见 Docker 部署或 PM2 部署，本篇补充多应用的部署分工与托管要求。

## 部署与运维（5）

- [选择部署方式](/deployment/choose-a-deployment-method)：应用开发并通过测试后，可以在自己的服务器上使用 Docker 或 PM2 独立部署到生产环境。Docker 通过容器运行应用；PM2 托管 Node.js 进程，由 app-installer 完成安…
- [发布应用新版本](/deployment/publish-app-release)：发布应用新版本，就是把验证通过的代码重新构建，再通过 Docker 或 PM2（app-installer）更新已有的生产应用。沿用生产环境的数据库、运行配置和文件存储，应用地址通常也不需要改变。
- [使用 Docker 部署](/tutorials/deploy-with-docker)：以下直接通过 IP 和 HTTP 访问的示例仅用于可信网络中的部署验证。通过公网或不可信网络访问时，先配置域名、HTTPS 和反向代理，再登录管理员账号。
- [使用 PM2 部署（app-installer）](/tutorials/deploy-with-app-installer)：app-installer 将部署包安装到服务器，由 PM2 管理应用进程，并负责后续的版本切换、备份和回退。应用源码保留在开发机，服务器上的运行配置和业务数据独立于发布版本保存。
- [升级 NocoBase Core](/developing-apps/upgrade-nocobase-core)：本文介绍如何升级当前应用使用的 NocoBase Core 及相关依赖。升级在应用源码项目中进行；完成验证后，再按照原来的方式部署应用。

## 参考（9）

- [API 参考](/reference/api)：本页按调用场景列出常用公开 API、返回值和使用约束。完整参数、重载和辅助类型以所安装版本的类型声明为准；数据库的专题参考见本文末尾。应用开发过程见开发应用，共享机制见框架。
- [命令行参考](/reference/cli)：本页说明应用的 nocobase 命令。创建应用、创建插件和生产安装由独立工具完成，分别见创建应用、创建插件和使用 PM2 部署。
- [配置项参考](/reference/configuration)：配置由应用及已接入模块共同定义。本页列出默认模板中的常用字段；已安装应用的完整配置元数据通过 pnpm nocobase config variables --json 查询。配置开发流程见应用配置（…
- [项目目录与文件约定](/reference/project-conventions)：第一次认识项目时阅读项目结构。本页按路径查找职责和维护方式；目录中的文件名是约定示例，按实际模板和功能增减。
- [核心包与工具包索引](/reference/packages)：本页用于从功能找到包名和公开源码。它是包索引，不是每个应用都需要安装的依赖清单；应用实际依赖以 package.json 和锁文件为准。插件清单见插件索引，常用接口见 API 参考。
- [插件索引](/reference/plugins)：本页列出已核对源码中的应用插件：主仓库 24 个、商业仓库 2 个。清单按包名字母顺序排列，公开源码通过包名链接提供。
- [数据库支持与版本兼容](/reference/compatibility)：NocoBase 提供 8 种数据库方言。方言是连接配置中 dialect 的取值，用于选择对应的数据库驱动；MariaDB 与 MySQL 共用 mysql 方言。
- [使用不同数据库创建应用](/reference/database-configuration)：数据库服务可以部署在本机、独立服务器或云平台上，无需使用 Docker。为新应用准备独立的空数据库或 schema，账号需能连接、读写数据，并在应用使用的范围内创建和修改表、索引等对象。网络数据库应允…
- [常见问题](/reference/faq)：只服务当前业务、需要经常随页面调整的代码，可以直接放在应用的 client/、server/、database/ 或 cli/。需要独立维护、提供明确扩展入口或供多个应用接入时，再考虑拆成 packa…

