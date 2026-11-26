# 城市口袋公园无障碍绕行标注

荫港公园维护局核验坡道和临时围挡，把可复核的步测绕行记录写入入口导视图。

## 现场工作与联系人

模拟客户为荫港公园维护局。入口设施凭证、障碍组合编码、绕行线路提报、地图图例签注；无替代坡道时只发布绕行提示。

- 入口设施核验 `entrances`，字段为 `park`（口袋公园）、`ramp`（坡道通行）、`tags`（障碍标记）、`condition`（核验状态）。模型约束位于 `backend/domain/entrances_model.py`，规则位于 `entrances_service.py`。
- 绕行偏好卡 `walk_profiles`，字段为 `park`（公园）、`avoid`（需避开标记）、`weights`（标记权重）、`minimum`（最低匹配分）。模型约束位于 `backend/domain/walk_profiles_model.py`，规则位于 `walk_profiles_service.py`。
- 绕行线路单 `detours`，字段为 `profile`（偏好卡）、`entrance`（终点入口）、`walk_m`（绕行距离 m）、`score`（匹配分）、`state`（状态）。模型约束位于 `backend/domain/detours_model.py`，规则位于 `detours_service.py`。
- 导视图签注 `map_notes`，字段为 `detour`（线路单）、`legend`（导视文本）、`edition`（图纸版本）。模型约束位于 `backend/domain/map_notes_model.py`，规则位于 `map_notes_service.py`。
- 权重对比试算 `weight_trials` / `trial_entries` / `trial_conclusions`，字段为 `profile`（偏好卡）、`weights_b`（候选权重）、`threshold`（放行门槛）、`judgment`（现场判定）、`score_a`/`score_b`（两套分）。模型约束位于 `backend/domain/trials_model.py`，规则位于 `trials_service.py`，续跑打分与结算位于 `trials_scoring.py`。两套权重共用同一批入口留档标记与同一放行门槛；现场判定与两套分都齐了才出结论；评分中断后再提交即可续跑，已算出的分接着用；复核员改判后两套误放行数一起更新，旧结论留在 `trial_conclusions` 可查；改判与算分并发时，晚回的分按新判定结算。

团队为模拟的9 人公园维护班，给小型公园步行图维护无障碍入口信息。

巡查照片、障碍清单和地图图例分开保管。多种障碍叠加时不好挑入口，坡道状态变化容易误发旧提报，走测距离和签注版本容易脱节。

入口现场查勘进入绕行提报，地图维护岗接收签注路线和不可达说明。

### 一天的业务操作

1. 08:10 查看柳瓦园 PK-E1 石阶和碎石记录。
2. 09:00 建立 PR-11，石阶权重 2，碎石权重 1。
3. 09:25 检索到 PK-E2 匹配分 1。
4. 11:05 员工步测 76 米，提报 DP-11。
5. 12:10 临时围挡占用 PK-E2 坡道。
6. 13:20 复核员以“绕行受阻”签出 NOTE-11。
7. 16:00 围挡撤除，独立提报 DP-12 并签发可通行图签。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18307`。FastAPI OpenAPI 在 `http://127.0.0.1:19307/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
本机开发时，在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 入口设施核验 | `/entrances` /entrances/inspect | `frontend/src/pages/entrances.js` |
| 绕行偏好卡 | `/walk_profiles` /walk_profiles/draft-profile，/walk_profiles/match-entrances | `frontend/src/pages/walk_profiles.js` |
| 绕行线路单 | `/detours` /detours/submit-detour，/detours/withdraw-detour | `frontend/src/pages/detours.js` |
| 导视图签注 | `/map_notes` /map_notes/publish-map | `frontend/src/pages/map_notes.js` |
| 权重对比试算 | `/trials` /trials/draft-trial，/trials/score，/trials/judge-entry，/trials/false-passes，/trials/conclusion-log | `frontend/src/pages/trials.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 MultiLabelBinarizer + 加权距离。标记以 MultiLabelBinarizer 编为 0/1，匹配分为 1-实际冲突权重/偏好总权重。结果按分值和坡道通行排序。

地点和步测均为演示数据。图签供维护员复制到外部制图工具。

[MIT](LICENSE)
