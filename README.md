# tos-app-rustdesk-server

将原创应用 [RustDesk Server](https://github.com/ericbyz/rustdesk-server)（局域网 DNS 广告过滤，Apache-2.0）打包为 [铁威马 TOS](https://www.terra-master.com) 应用中心 **deb 类应用**（x86_64 + aarch64 双架构）。

**这是什么**：TOS deb 元数据壳 + 可复现构建脚本。RustDesk Server 为原创项目（冲原创档 200 元），本仓库只做 TOS 平台封装：按《TOS 7 应用开发指南》第 8 章规范，锁定源仓 Release 的静态二进制（CGO_ENABLED=0，Go 交叉编译）打包。

| 项目 | 值 |
|---|---|
| 应用 ID | `rustdesk-server` |
| 应用形态 | deb 类 · 悬浮窗（`type=iframe`, `exec=false`）· 端口模式 |
| 悬浮路由 | `http://<NAS>:8181/rustdesk-server/`（TOS nginx → 127.0.0.1:21116，前缀剥离） |
| DNS 服务 | `0.0.0.0:53`（systemd `AmbientCapabilities=CAP_NET_BIND_SERVICE`） |
| 面板端口 | 21116（**仅监听 127.0.0.1**，只能经 TOS 桌面悬浮窗访问，天然免鉴权） |
| 版本 | v0.1.0（见 [UPSTREAM](UPSTREAM) 锁定） |
| 许可证 | Apache-2.0（源仓与封装仓同许可） |
| 数据目录 | `/var/lib/rustdesk-server`（块表缓存 / 查询日志 JSONL / `rustdesk-server.yaml`） |

## 悬浮窗三要素（承接 dbx 实战结论）

1. `config.ini`：`"exec": false, "type": "iframe", "path": "/rustdesk-server/"`；
2. `nginx/rustdesk-server.conf`：`location /rustdesk-server/ { proxy_pass http://127.0.0.1:21116/; }`
   （**尾斜杠剥离前缀**——RustDesk Server 面板全相对路径，与 dbx 的保留前缀方案相反）；
3. 服务：systemd 单元加固同 dbx，`Restart=` 留空由平台管理生命周期。

## 目录结构

```
tos-app-rustdesk-server/
├── config.ini            # TOS 平台元数据（规范第 8 章）
├── rustdesk-server.lang           # 26 种语言（生成：scripts/make_lang.py）
├── rustdesk-server.env            # 服务环境变量（面板端口/DNS 监听/数据目录）
├── UPSTREAM              # 版本锁定（源仓 Release 资产 + SHA256）
├── DEBIAN/               # control + postinst/prerm/postrm
├── init.d/hbbs.service # systemd 单元（加固 + CAP_NET_BIND_SERVICE）
├── nginx/rustdesk-server.conf     # ⭐ 悬浮路由：/rustdesk-server/ → 127.0.0.1:21116/（剥前缀）
├── images/icons/rustdesk-server.svg
├── scripts/
│   ├── fetch_upstream.sh # 下载并校验源仓资产（SHA256 强制；支持 UPSTREAM_DIST_DIR 本地构建）
│   ├── build_deb.py      # 纯 Python 的 dpkg-deb 兼容打包器（确定性构建）
│   ├── validate.py       # TOS 审核规则校验
│   ├── make_lang.py      # 生成 rustdesk-server.lang
│   └── bump_upstream.sh  # 升级版本（UPSTREAM/config.ini/control 联动）
├── build.sh              # 一键构建 ./build.sh [x86_64|aarch64]
└── .github/workflows/    # CI：校验 + 双架构构建 + Release 发布
```

## 本地构建

依赖：bash、curl、tar、python3（任意平台；有 dpkg-deb 时自动优先）。

```bash
# 前置：源仓交叉编译产出（或等 v0.1.0 Release）
#   cd ../rustdesk-server && GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o dist/amd64/bin/rustdesk-server ./cmd/rustdesk-server
#   tar -czf dist/rustdesk-server_0.1.0_linux_amd64.tar.gz -C dist/amd64 bin   # arm64 同理
export UPSTREAM_DIST_DIR=Z:/business/company/twm/rustdesk-server/dist   # 本地 dist（免发布直接打）
./build.sh                # 双架构
./scripts/validate.py     # 元数据校验
```

产物：`build/output/rustdesk-server_<platform>.deb` + `.sha256`。

## 上架 Checklist（对应内部奖励计划 · 原创档 200 元）

1. ☐ 源仓 `ericbyz/rustdesk-server` 打 tag `v0.1.0`，CI 交叉编译双架构并发布 Release（含 `.sha256`）；
2. ☐ 用 Release 资产的 SHA256 更新本仓 `UPSTREAM`，重新 `./build.sh` 核对；
3. ☐ x86_64 与 ARM **分别创建应用**（独立 App ID、同一开发者账号、名称对应）；
4. ☐ 提交 Release 直链 + SHA256 + 上游源码仓（原创仓即上游）+ 本仓构建脚本；
5. ☐ 运行佐证：TOS 实机截图（悬浮窗 + 查询日志页 + 总览卡片）；
6. ☐ 《参与报名表》勾选**原创/创意档**，附仓库链接与差异说明（对比 AdGuard Home/Pi-hole：更轻、TOS 悬浮窗原生适配、中文优先、内置查询日志）；
7. ☐ 30 天内维护 Issues 响应。

> 提交前用查重工作台核对 `rustdesk-server` / `RustDesk Server` 无重名（2026-11-15 核验：adblock 品类仅 AdGuardHome 在架，Pi-hole/Blocky 未被提交）。

## 合规声明

- RustDesk Server 为**原创代码**（参考 Pi-hole/AdGuard Home 的产品形态与 esp32-c3-adblock 的思路，未复用其代码）；
- 运行时按需下载的第三方块表（StevenBlack/hosts 等）**不打包进安装包**，面板内声明来源；
- 安装包内容：源仓 Release 的静态二进制（SHA256 锁定）+ 本仓元数据，无其他二进制；
- 不收集任何用户数据；查询日志仅存储在 NAS 本地 `/var/lib/rustdesk-server/logs/`。
