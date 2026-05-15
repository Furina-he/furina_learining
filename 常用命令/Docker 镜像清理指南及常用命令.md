# Docker 常用命令与镜像清理指南

> 适用环境：WSL Ubuntu-24.04 + Docker Desktop
> 项目路径：`D:\desk\Desktop\carview`
> ⚠️ 所有命令请在 **WSL 终端** 中执行，而不是 Windows PowerShell。

---

## 一、镜像清理指南

清理顺序：**容器 → 镜像 → volume → 网络**

### 1. 停止并移除容器（推荐用 compose）

在项目根目录 `D:\desk\Desktop\carview` 下执行：

```bash
# 停止并删除所有 profile 启动的容器、网络
docker compose --profile full down

# 如果想同时删除关联的 volume（会丢失 MySQL/Kafka 数据）
docker compose --profile full down -v

# 如果想顺便删除 compose 拉取的镜像
docker compose --profile full down --rmi all -v
```

### 2. 删除镜像

```bash
# 查看本项目相关镜像
docker images | grep -E "kafka|zookeeper|mysql|flink|hadoop|spark|superset"

# 按镜像名删除（精确）
docker rmi apache/kafka:3.7.0 \
           zookeeper:3.9 \
           mysql:8.0.31 \
           flink:1.20-scala_2.12-java17 \
           apache/hadoop:3 \
           apache/spark:3.5.0 \
           apache/superset:latest

# 按 IMAGE ID 删除
docker rmi <IMAGE_ID>

# 强制删除（即使有容器引用）
docker rmi -f <IMAGE_ID>
```

### 3. 清理 volume（持久化数据，慎重！）

```bash
# 列出所有 volume
docker volume ls | grep carview

# 删除指定 volume
docker volume rm carview_mysql-data carview_kafka-data carview_zk-data \
                 carview_hadoop-nn carview_hadoop-dn carview_superset-data

# 一键删除所有未被使用的 volume
docker volume prune
```

### 4. 一键大扫除（核武器级别）

```bash
# 删除：停止的容器 + 未被任何容器使用的镜像 + 悬空网络 + 构建缓存
docker system prune -a

# 加上 volume（会清空所有未挂载的 volume！）
docker system prune -a --volumes
```

### 5. 推荐工作流

| 场景           | 命令                                                |
| ------------ | ------------------------------------------------- |
| 只想重启服务       | `docker compose --profile core restart`           |
| 临时停止，保留数据    | `docker compose --profile full stop`              |
| 删除容器，保留镜像和数据 | `docker compose --profile full down`              |
| 彻底卸载本项目      | `docker compose --profile full down --rmi all -v` |
| 系统级清理（所有项目）  | `docker system prune -a --volumes`                |

### 6. 注意事项

- ⚠️ **WSL 提醒**：在 WSL Ubuntu-24.04 内运行 Docker，所有命令必须在 WSL 终端中执行。
- ⚠️ **数据丢失警告**：MySQL 表结构虽能通过 `sql/init/001_schema.sql` 重建，但 `vehicle_track`、`alarm_event` 等运行时数据一旦删除 volume 就没了。
- ⚠️ **先看磁盘占用**：执行清理前，用 `docker system df` 查看实际占用，再决定是否清理。

---

## 二、日常开发常用 Docker 命令

### 1. 容器生命周期

```bash
# 启动 / 停止 / 重启 / 删除容器
docker start <container>
docker stop <container>
docker restart <container>
docker rm <container>          # 已停止
docker rm -f <container>       # 强制删除（运行中也可删）

# 后台运行一个容器（常见参数组合）
docker run -d \
  --name myapp \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  -e ENV=prod \
  --restart unless-stopped \
  myimage:tag
```

### 2. 查看状态

```bash
docker ps                              # 当前运行中的容器
docker ps -a                           # 所有容器（含已停止）
docker ps -a --filter "name=carview"   # 按名称过滤
docker stats                           # 实时资源占用（CPU / 内存 / IO）
docker top <container>                 # 容器内进程
docker port <container>                # 容器端口映射
docker inspect <container>             # 完整元数据 JSON
docker system df                       # Docker 空间占用总览
docker system df -v                    # 按对象详细统计
```

### 3. 日志与调试

```bash
# 查看日志
docker logs <container>
docker logs -f <container>              # 持续追踪（类似 tail -f）
docker logs --tail 200 <container>      # 最后 200 行
docker logs --since 10m <container>     # 最近 10 分钟
docker logs -f --tail 100 <container>   # 组合用法（最常用）

# 进入容器
docker exec -it <container> bash
docker exec -it <container> sh             # 没有 bash 的镜像用 sh
docker exec -it <container> mysql -uroot -p
docker exec -u root -it <container> bash   # 以 root 进入

# 临时启动一次性容器调试
docker run --rm -it alpine sh
```

### 4. 文件传输

```bash
# 宿主机 → 容器
docker cp ./local-file.txt <container>:/tmp/

# 容器 → 宿主机
docker cp <container>:/var/log/app.log ./

# 复制目录
docker cp ./conf <container>:/etc/myapp/
```

### 5. 镜像管理

```bash
docker images                          # 本地镜像列表
docker images -a                       # 含中间层
docker pull mysql:8.0.31               # 拉取镜像
docker push myrepo/myimage:tag         # 推送镜像
docker tag src:tag target:tag          # 重新打标签
docker history <image>                 # 查看镜像分层

# 构建镜像
docker build -t myimage:1.0 .
docker build --no-cache -t myimage:1.0 .       # 不使用缓存
docker build -f Dockerfile.dev -t myimage .    # 指定 Dockerfile

# 镜像导入导出
docker save -o myimage.tar myimage:1.0
docker load -i myimage.tar
```

### 6. 网络管理

```bash
docker network ls                          # 查看网络
docker network inspect <network>           # 查看详情
docker network create mynet                # 创建网络
docker network connect mynet <container>   # 把容器加入网络
docker network disconnect mynet <container>
docker network prune                       # 清理未使用网络
```

### 7. Docker Compose 常用

```bash
# 启动 / 停止
docker compose up -d                       # 后台启动
docker compose up -d --build               # 重新构建后启动
docker compose down                        # 停止并删除容器
docker compose stop                        # 仅停止，保留容器
docker compose start                       # 启动已停止容器
docker compose restart <service>           # 重启某个服务

# 查看
docker compose ps                          # 服务状态
docker compose logs -f <service>           # 查看日志
docker compose top                         # 各服务进程

# 单服务操作
docker compose up -d <service>             # 只启动某个服务
docker compose build <service>             # 只构建某个服务
docker compose pull                        # 拉取所有镜像
docker compose exec <service> bash         # 进入运行中的服务
docker compose run --rm <service> <cmd>    # 一次性执行命令

# Profile 用法（本项目）
docker compose --profile core up -d        # 启动核心服务
docker compose --profile full up -d        # 启动全部服务
docker compose --profile full ps
```

### 8. Volume 管理

```bash
docker volume ls
docker volume create myvol
docker volume inspect myvol
docker volume rm myvol
docker volume prune                        # 清理未使用 volume

# 备份 volume
docker run --rm \
  -v myvol:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/myvol.tar.gz -C /data .

# 恢复 volume
docker run --rm \
  -v myvol:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/myvol.tar.gz -C /data
```

### 9. 常用清理速查

```bash
docker container prune       # 删除已停止容器
docker image prune           # 删除悬空镜像（<none>）
docker image prune -a        # 删除未被使用的所有镜像
docker volume prune          # 删除未使用 volume
docker network prune         # 删除未使用网络
docker builder prune         # 清理构建缓存
docker system prune          # 一键清理（不含未使用镜像/volume）
docker system prune -a       # 包含所有未使用镜像
docker system prune -a --volumes   # 终极清理
```

### 10. 实用排查命令

```bash
# 找出最占空间的容器
docker ps -s

# 找出最大的镜像（按体积排序）
docker images --format "{{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -h

# 一键停止所有容器
docker stop $(docker ps -q)

# 一键删除所有容器
docker rm -f $(docker ps -aq)

# 一键删除所有镜像（慎用！）
docker rmi -f $(docker images -q)

# 查看容器 IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>

# 查看健康检查状态
docker inspect --format='{{json .State.Health}}' <container>
```

---

## 三、本项目专用速查

```bash
# 启动核心服务
docker compose --profile core up -d

# 启动全部服务
docker compose --profile full up -d

# 查看 Kafka 日志
docker compose logs -f kafka

# 进入 MySQL
docker compose exec mysql mysql -uroot -p

# 重新初始化 MySQL（清空数据）
docker compose --profile full down -v
docker compose --profile full up -d mysql

# 查看磁盘占用
docker system df
```
