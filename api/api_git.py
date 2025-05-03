from fastapi import APIRouter, File, UploadFile , Form
from fastapi.responses import JSONResponse
import shutil, zipfile
from pathlib import Path
from uuid import uuid4

from modules.mcp_git import rCall_PushAndPR

TMP_ROOT = Path("/tmp/mcp_uploads")
TMP_ROOT.mkdir(exist_ok=True, parents=True)

rgRouter = APIRouter()

@rgRouter.post("")
async def Api_MCPGit(file: UploadFile = File(...), name:str = Form(...), token:str = Form(...)) :
    """유저 채팅 API"""
    
    uid = uuid4().hex
    work_dir = TMP_ROOT / uid
    zip_path = work_dir / "upload.zip"
    
    try:
        
        # 1. 디렉터리 준비
        work_dir.mkdir(parents=True, exist_ok=False)

        # 2. ZIP 파일 저장
        with zip_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        # 3. 압축 해제
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(work_dir)
            
        # 4. 압축 파일 삭제            
        zip_path.unlink(missing_ok=True)
        
        await rCall_PushAndPR(name, work_dir, name, name, name, token)
        
        return JSONResponse(
            status_code=200, 
            content={"detail": "Success"}
        )

    except Exception as e:
        
        return JSONResponse(
            status_code=500, 
            content={"detail": str(e)}
        )
        
    finally:
        # 5. 정리: ZIP + 작업 폴더 삭제
        if work_dir.exists():
            shutil.rmtree(work_dir)