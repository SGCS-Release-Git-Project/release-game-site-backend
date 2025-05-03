from pathlib import Path, PurePosixPath
import base64, mimetypes
from langchain_mcp_adapters.client import MultiServerMCPClient


def mCall_CollectFiles(root: Path, remote_prefix="my_dir_name/"):
    files = []
    for p in root.rglob("*"):
        if p.is_file():
            remote_path = str(PurePosixPath(remote_prefix) / p.relative_to(root))
            
            raw = p.read_bytes()

            mime, _ = mimetypes.guess_type(p.name)
            try:
                if mime and mime.startswith("text/"):
                    files.append({"path": remote_path,
                                  "content": raw.decode("utf-8")})
                    continue
            except UnicodeDecodeError:
                pass

            files.append({
                "path": remote_path,
                "content": base64.b64encode(raw).decode(),
                "encoding": "base64"
            })
            
    return files


async def rCall_PushAndPR(my_dir_name:str, dir_name:str, branch_name:str, pr_title:str, pr_body:str, git_token:str) -> None:
    """
    my_dir_name = hyeonsang/
    dir_name    = 업로드할 디렉토리 이름
    branch_name = "feat/hyeonsang-test"
    pr_title    = "feat: 주차별 자료 업로드 (week1)"
    pr_body     = "MCP 서버를 이용해 **hyeonsang/week1/** 디렉터리를 추가했습니다."
    git_token = 개발자 세팅 깃 토큰
    """
    files       = mCall_CollectFiles(Path(dir_name), my_dir_name)

    async with MultiServerMCPClient({
        "github": {
            "command": "/usr/local/bin/github-mcp-server",
            "args": ["stdio"],   # stdio 서버 직접 실행
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": git_token},
            "transport": "stdio"
        }
    }) as client:

        tool_map = {t.name: t for t in client.get_tools()}
        create_branch         = tool_map["create_branch"]
        push_files_tool       = tool_map["push_files"]
        create_pull_request = tool_map["create_pull_request"]

        # 브런치 생성
        try:
            await create_branch.ainvoke({
                "owner": "SGCS-Release-Git-Project",
                "repo":  "release-collect-game",
                "branch": branch_name,
                "from_branch": "main"
            })
            print(f"브랜치 '{branch_name}' 생성 완료")
        except Exception:
            print(f"ℹ️  '{branch_name}' 브랜치가 이미 존재합니다. 계속 진행합니다.")

        
        # 파일 푸쉬
        try:
            await push_files_tool.ainvoke({
                "owner":  "SGCS-Release-Git-Project",
                "repo":   "release-collect-game",
                "branch": branch_name,
                "files":  files,
                "message": pr_title
            })
        except Exception as e:
            raise e

        # Pull Request 생성
        try:
            await create_pull_request.ainvoke({
                "owner":  "SGCS-Release-Git-Project",
                "repo":   "release-collect-game",
                "title":  pr_title,
                "body":   pr_body,
                "head":   branch_name,   # 내 브랜치
                "base":   "main"         # 병합 대상
            })
        except Exception as e:
            raise e
        
        return None