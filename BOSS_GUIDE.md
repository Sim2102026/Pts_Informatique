# 关底门与史莱姆 Boss：安装和上传说明

基于 Sim2102026/Pts_Informatique 的 test 分支提交：
704994d4a5721cdd23051d83a1a42efd558a6c7e（2026-11-23）。
此代码包尚未提交到远程 GitHub。

## 游戏行为

- 原长地图第 156 列的终点换成 Kenney 门。站在门旁的地面上，按 ↑ 进入。
- 约 0.8 秒淡入淡出后进入独立石墙房间。进入时保留玩家血量和分数。
- 玩家向右走过房间 x=320 的触发线，Boss 才开始活动；房间镜头固定。
- 紫色史莱姆 3 格血：巡逻 → 蓄力（橙色）→ 冲刺 → 疲劳（绿色提示）。
- 仅在疲劳阶段，从上方下落踩头才扣血；踩中后玩家弹起。
- 侧面接触或在攻击阶段碰到 Boss 会伤害玩家，沿用原先的无敌时间和桃心动画。
- 击败 Boss 后出现奖杯，触碰奖杯才胜利，额外奖励 300 分。
- Boss 房间死亡后，在结束菜单选择 Rejouer，从该房间重新开始：玩家和 Boss 满血，分数回到进入房间时。
- 存档可以区分地面、Boss 房间和已击败 Boss。读取进行中的 Boss 战时，从房间入口满血重新战斗，不恢复战斗中间状态；已击败 Boss 的存档保留奖杯和分数。
- 音乐仍沿用团队当前代码；此包没有接入音乐。

## 先在电脑试运行

1. 下载 test 分支完整项目并解压；本更新包只有新增/修改文件，不能单独运行。
2. 解压本更新包，把里面的文件复制到项目根目录，按相对路径覆盖。
3. 在项目文件夹中打开终端：

```bash
python -m pip install -r requirements.txt
python main.py
```

macOS 若没有 python 命令，使用 python3。

直接试打 Boss（无需跑长地图）：

```bash
python demo_boss.py
```

左右箭头移动，空格或 ↑ 跳跃；靠近关底门时 ↑ 为进门；Esc 退出。
运行 main.py 后先选 Jouer，再选一个存档位。没有配置 PostgreSQL 时仍可开始新游戏，但不能持久保存。
requirements.txt 已补齐现有 db.py 需要的 psycopg[binary]；数据库需另行配置 DATABASE_URL，本次未连接真实数据库测试。

## 如何上传到 GitHub 网页（建议电脑操作）

仓库：https://github.com/Sim2102026/Pts_Informatique

1. 左上角分支选择器切换到 test。
2. 再打开分支选择器，输入 boss，选择 Create branch: boss from test。若 boss 已存在，换一个新名字，例如 zitong-boss。
3. 确认当前分支是 boss，在仓库根目录选择 Add file → Upload files。
4. 在电脑上解压 boss_update.zip，拖入解压后里面的所有内容：Assets 文件夹、tests 文件夹和根目录的 .py/.txt/.md 文件。
   不要直接上传 ZIP；GitHub 不会自动解压。
   不要把外层 boss_update 文件夹一起上传，否则代码会多嵌套一层。
5. 提交前核对：boss.py、porte.py、salle_boss.py、jeu.py、demo_boss.py 和 main.py 应处于同一层；图片应在 Assets/Boss/ 中。
6. Commit message 可写：Ajouter porte finale et boss slime Kenney。
7. Commit changes 后，创建 Pull request：base: test，compare: boss。
   标题：Porte finale + salle du boss + Roi Slime。
   描述：Ajout d'une porte en fin de niveau, d'une salle dédiée et d'un boss slime à trois vies. Checkpoint de combat et sauvegarde des scènes. Essai rapide : python demo_boss.py.
8. 让队友试打并审查，再合并到 test。不要将这包直接上传到 main；现有 main 与 test 仍有其他整合工作。

如果 test 在本包生成后又有新改动，尤其 jeu.py、niveau.py、menu.py、carte_longue.py，先对比差异，避免覆盖队友的新代码。

## 新代码分工

- porte.py：读取 Kenney 门的上下两块，检测玩家是否站在门边。
- boss.py：史莱姆 3 点血、状态计时、冲刺、踩头和受伤动画。
- salle_boss.py：单屏房间、战斗触发线、Boss 血条和奖杯。
- demo_boss.py：直接进入房间的测试入口。
- jeu.py：门的交互、场景切换、Boss 更新、重试、存档场景标记。
- niveau.py：识别 T 为门，并绘制门。
- carte_longue.py：把末尾 D 换为 T；自定义小地图的 D 仍可表示奖杯。
- menu.py：更新操作说明。
- requirements.txt：补齐数据库模块依赖。
- tests/test_boss.py：房间、实跳踩头、战斗、重试、存档场景的测试。
- 其他测试文件：更新旧菜单/地面终点的预期，适配现有存档菜单与新的门。

Kenney 图片取自用户提供的 New Platformer Pack 1.1，授权 CC0；原授权文件在 Assets/Boss/License.txt。
本包没有使用 Pixel Adventure 付费史莱姆，也没有使用 Nintendo 管道。

## 验证

运行：python -m pytest -q
本版测试结果：109 passed。
同时检查了门入口与 Boss 房间画面。Windows 本机运行尚未验证；真实 PostgreSQL 连接未验证（存读档场景使用测试替身验证）。
