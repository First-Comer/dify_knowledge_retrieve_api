拉取下来的dify源码并添加并修改如下结构的代码：
dify-main/
├── api/                          # 你修改过的 Dify API 源码
│   ├── services/   
│   │    ├── workflow/                 
│   │    │    ├── dataset_retriever.py   # 修改此文件
│   ├── controllers/
│   │    ├── console/
│   │    ├── __init__.py                 # 修改此文件
│   │    │    ├── knowledge/         # 新建此文件包
│   │    │    ├── __init__.py          #新建自带
│   │    │    │    ├── rettiever.py    # 新建此文件
├── docker/
│   ├── Dockerfile                # 新建此文件
│   ├── docker-compose.yml      # 修改此文件


Docker部署
新建Dockerfile，本文以源代码为基础镜像，并将本地新增的代码复制到新容器中。 复制我的Dockerfile即可：

FROM langgenius/dify-api:1.3.1

COPY ../api /app/api
COPY ../api/core/workflow/nodes/knowledge_retrieval/knowledge_retrieval_node.py /app/api/core/workflow/nodes/knowledge_retrieval/knowledge_retrieval_node.py


修改源码部署方式，因为本次的开发只是对/api中的小模块进行API封装，所以我们只需要修改/api部分代码的部署即可。 复制我的docker-compose.yaml：


API封装代码


首先是路由注册： dify-main\api\controllers\console\_init_.py

from .knowledge.retriever import KnowledgeRetrieverApi

api.add_resource(
    KnowledgeRetrieverApi,
    "/workflow/knowledge-retriever/fetch-dataset",
    endpoint="workflow_knowledge_retriever_fetch"
)

还有两个代码一起给了。

# api/services/workflow/dataset_retriever.py


# api/controllers/console/knowledge/retriever.py


快速启动
启动 Dify 服务器的最简单方法是运行我们的 docker-compose.yml 文件。在运行安装命令之前，请确保您的机器上安装了 Docker 和 Docker Compose：

cd docker
cp .env.example .env
docker compose up -d
运行后，可以在浏览器上访问 http://localhost/install 进入 Dify 控制台并开始初始化安装操作。 ok了，非常方便，后面我们测试还需要一些参数在下一章。

参数规范
先给测试.txt，这个前提是部署的Dify有workflow或是chatflow，有上传和embedding好了的知识库。


1.user_id查询
1.1连接到 PostgreSQL 数据库 powershell
docker-compose exec db sh
psql -U postgres
 1.2查看数据库列表 sql

\l  # 列出所有数据库
\c dify  # 连接到 dify 数据库
\dt
SELECT id, email, name FROM accounts LIMIT 5;
  到这目的达到了 

2.tenant_id查询 同user_id查询，最后命令换为SELECT id, name FROM tenants;

3.app_id查询；  url里面有自己看。

4.dataset_ids 查询； 同app_id相同，都在url。

ok，大功告成，拿到你自己的id换上去测试就是200。

参考
本地Docker部署： [1] https://github.com/langgenius/dify
