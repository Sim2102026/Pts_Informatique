# Windows / Mac 启动完整 test 游戏

本包只添加启动器，不修改 main.py、jeu.py 或游戏逻辑。
默认启动 main.py（完整游戏，包括菜单、长地图和 Boss），不是只运行 Boss 演示。

## 添加到项目 / GitHub

解压 game_launchers.zip，把里面四个文件放在 test 分支的项目根目录，和 main.py、requirements.txt 放在一起：

- Lancer_Windows.bat
- Lancer_Mac.command
- lancer_jeu.py
- START_GAME.md

在 GitHub 网页：切换 test → Add file → Upload files → 上传以上文件 → Commit changes。
不要上传 ZIP 本身，不要把外层文件夹一起上传。
启动器还没有上传到 GitHub。

## 运行前

1. 电脑需要安装 Python 3.10 或更新版本；建议 Python 3.12。
   官方下载：https://www.python.org/downloads/
   Windows 安装时勾选 Add python.exe to PATH。
2. 下载 GitHub 的完整 test 项目并解压到电脑上的普通文件夹。
   如果是下载 ZIP，必须先解压，不能直接在 ZIP 里运行。
3. 不要仅下载这四个启动器：游戏 .py、Assets 和 requirements.txt 都需要保留。
4. 第一次启动需要联网下载依赖。之后依赖未变化时直接启动，不会每次重复安装。

## Windows

双击 Lancer_Windows.bat。
首次启动会创建 .venv-game 并安装 requirements.txt 里的依赖，然后自动打开完整游戏菜单。
出现报错时窗口会保留，截图最后的错误信息即可。

## macOS

双击 Lancer_Mac.command，会打开 Terminal 并启动游戏。
如果提示没有执行权限：

- 打开 Terminal，输入 chmod +x 后加一个空格；
- 把 Lancer_Mac.command 拖进 Terminal，再按 Enter；
- 回到 Finder，再双击该文件。

也可以在 Terminal 输入 bash 后加一个空格，拖入 Lancer_Mac.command，按 Enter 直接运行，无需修改权限。

从 GitHub 网页上传/重新下载可能丢失可执行权限，此时重复上面的步骤即可。

## 游戏操作

- 菜单：上下选择，Enter 确认。
- Jouer → 选择任意存档位开始。
- 左右箭头移动，空格/↑跳跃。
- 关底站在门旁，↑进入 Boss 房；向右走触发战斗。
- Boss 疲劳时踩头，击败后收集奖杯。
- Esc 退出。

## 可选终端命令

在项目文件夹打开终端。
Windows：

```bat
Lancer_Windows.bat
Lancer_Windows.bat --boss
Lancer_Windows.bat --check
```

Mac：

```bash
bash Lancer_Mac.command
bash Lancer_Mac.command --boss
bash Lancer_Mac.command --check
```

--boss 只用于直接试打；--check 安装并检查导入，不打开游戏窗口。

## 自动处理与限制

- 启动器自动切换到项目目录，支持路径含空格。
- 依赖和 Python 环境放在项目内的 .venv-game，不修改电脑全局 Python 包。
- requirements.txt 更新后，下次启动会重新安装依赖。
- .venv-game 是自动生成的本机环境，不要上传到 GitHub，也不要在 Windows 与 Mac 之间复制这个文件夹；每台电脑首次自行生成。
- 换系统或环境损坏时，只删除 .venv-game，再双击启动器重新生成。
- 只安装 Python 的包，不安装 PostgreSQL 服务。存档沿用现有 DATABASE_URL 配置。未配置时仍可开始游戏，但无法持久存档。
- 不需要安装 IDE / PyCharm。

## 验证范围

已在 Linux 的全新虚拟环境中验证：自动安装全部依赖、完整 main.py 实际渲染后正常退出、--boss 实际渲染后正常退出、从其他工作目录调用启动器、第二次启动不重复安装。
Mac 的 Bash 脚本语法已检查；Windows 批处理代码已检查，但本次没有 Windows 或 macOS 真机，双击启动和系统权限提示尚未在真机验证。
