# Polaris 知识图谱系统

基于大模型驱动的智能知识图谱构建与问答系统。

## 项目概述

本项目旨在构建一个现代化的知识图谱系统，能够从多种格式的文档中提取知识，构建知识图谱，并支持智能问答交互。

### 核心功能

- 多格式文件处理（PDF、DOC、PPT、网页等）
- 智能知识图谱构建
- 基于知识图谱的问答系统
- 可视化知识图谱展示
- 用户友好的现代化交互界面

## 技术架构

- 前端：React + Ant Design + D3.js
- 后端：FastAPI (Python)
- 数据库：
  - PostgreSQL：结构化数据存储
  - Neo4j：图数据库存储
- 大模型：ChatGLM-6B
- 容器化：Docker

## 开发环境设置

### 后端设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 前端设置

```bash
cd frontend
npm install
npm start
```

### 数据库配置

- PostgreSQL
  - 端口：5432
  - 数据库名：polaris
  - 用户名：postgres

- Neo4j
  - 端口：7687
  - 数据库名：neo4j

## Docker 部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

## 项目结构

```
polaris/
├── backend/           # 后端服务
├── frontend/          # 前端应用
├── docs/             # 项目文档
├── docker/           # Docker配置
├── requirements.txt  # Python依赖
└── docker-compose.yml
```

## 团队

极星（Polaris）团队出品

## 许可证

MIT License
