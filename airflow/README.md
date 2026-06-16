# Airflow 本地环境搭建

基于 [官方教程](../cohorts/2022/week_2_data_ingestion/airflow/1_setup_official.md) 搭建的 Airflow Docker 环境。

## 前置要求

- Docker Desktop（内存分配 ≥ 5GB，推荐 8GB）
- Docker Compose v2.x+
- GCP Service Account JSON 文件（需要有 GCS 和 BigQuery 权限）

---

## 快速启动

### 第一步：准备 GCP 凭证

```bash
mkdir -p ~/.google/credentials/
cp /path/to/your-service-account.json ~/.google/credentials/google_credentials.json
```

### 第二步：配置环境变量

编辑 `.env` 文件，填入你的 GCP 信息：

```bash
GCP_PROJECT_ID=your-actual-project-id
GCP_GCS_BUCKET=your-actual-bucket-name
```

macOS/Windows 用户保持 `AIRFLOW_UID=50000` 即可。  
Linux 用户请运行：
```bash
echo "AIRFLOW_UID=$(id -u)" >> .env
```

### 第三步：构建 Docker 镜像

```bash
cd airflow/
docker compose build
```

> ⚠️ 首次构建会下载 gcloud SDK，可能需要 5~10 分钟。

### 第四步：初始化数据库

```bash
docker compose up airflow-init
```

### 第五步：启动所有服务

```bash
docker compose up -d
```

### 访问 Airflow UI

打开浏览器访问：http://localhost:8080  
默认账号：`airflow` / `airflow`

---

## 目录结构

```
airflow/
├── Dockerfile              # 自定义镜像（含 gcloud SDK）
├── docker-compose.yaml     # 服务编排配置
├── requirements.txt        # Python 依赖
├── .env                    # 环境变量（需手动填写 GCP 配置）
├── .gitignore
├── dags/                   # DAG 文件放这里
│   └── data_ingestion_gcs_dag.py   # 示例：NYC TLC 数据摄取
├── logs/                   # 运行日志（自动生成，已 gitignore）
├── plugins/                # 自定义插件（已 gitignore）
└── scripts/
    └── entrypoint.sh       # 容器启动脚本
```

---

## 停止服务

```bash
# 停止但保留数据
docker compose down

# 停止并清除数据库卷
docker compose down --volumes --remove-orphans
```

## 常见问题

### `File /.google/credentials/google_credentials.json was not found`

检查 `~/.google/credentials/google_credentials.json` 是否存在，文件名必须完全匹配。

### webserver 反复重启

Docker 内存不足，请在 Docker Desktop → Settings → Resources 里将内存调到至少 5GB。
