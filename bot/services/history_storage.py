"""
History storage for generated proposals with auto-cleanup
"""
import json
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
import aiofiles

from config import STORAGE_DIR, HISTORY_RETENTION_DAYS

logger = logging.getLogger(__name__)


@dataclass
class ProposalRecord:
    """Record of a generated proposal"""
    id: str
    user_id: int
    username: Optional[str]
    company_name: str
    tariff: str
    num_recruiters: int
    created_at: str
    pdf_path: str
    summary: str
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProposalRecord":
        return cls(**data)


class HistoryStorage:
    """Storage for proposal history with automatic cleanup"""
    
    def __init__(self):
        self.storage_dir = STORAGE_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.storage_dir / "index.json"
        self._lock = asyncio.Lock()
        
    async def _load_index(self) -> list[dict]:
        """Load index file"""
        if not self.index_path.exists():
            return []
        
        try:
            async with aiofiles.open(self.index_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            return []
    
    async def _save_index(self, records: list[dict]):
        """Save index file"""
        async with aiofiles.open(self.index_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(records, ensure_ascii=False, indent=2))
    
    async def add_record(self, record: ProposalRecord):
        """Add new proposal record"""
        async with self._lock:
            records = await self._load_index()
            records.append(record.to_dict())
            await self._save_index(records)
            logger.info(f"Added proposal record: {record.id}")
    
    async def get_user_history(self, user_id: int, limit: int = 10) -> list[ProposalRecord]:
        """Get user's proposal history"""
        records = await self._load_index()
        
        user_records = [
            ProposalRecord.from_dict(r) 
            for r in records 
            if r.get("user_id") == user_id
        ]
        
        # Sort by date descending
        user_records.sort(key=lambda x: x.created_at, reverse=True)
        
        return user_records[:limit]
    
    async def get_record_by_id(self, record_id: str) -> Optional[ProposalRecord]:
        """Get specific record by ID"""
        records = await self._load_index()
        
        for r in records:
            if r.get("id") == record_id:
                return ProposalRecord.from_dict(r)
        
        return None
    
    async def cleanup_old_records(self):
        """Remove records older than retention period"""
        async with self._lock:
            records = await self._load_index()
            cutoff = datetime.now() - timedelta(days=HISTORY_RETENTION_DAYS)
            cutoff_str = cutoff.isoformat()
            
            new_records = []
            deleted_count = 0
            
            for r in records:
                created_at = r.get("created_at", "")
                if created_at >= cutoff_str:
                    new_records.append(r)
                else:
                    # Delete PDF file
                    pdf_path = Path(r.get("pdf_path", ""))
                    if pdf_path.exists():
                        try:
                            pdf_path.unlink()
                            logger.info(f"Deleted old PDF: {pdf_path}")
                        except Exception as e:
                            logger.error(f"Failed to delete PDF {pdf_path}: {e}")
                    deleted_count += 1
            
            if deleted_count > 0:
                await self._save_index(new_records)
                logger.info(f"Cleaned up {deleted_count} old records")
            
            return deleted_count


async def start_cleanup_task():
    """Start background cleanup task"""
    storage = HistoryStorage()
    
    while True:
        try:
            await storage.cleanup_old_records()
        except Exception as e:
            logger.error(f"Cleanup task error: {e}")
        
        # Run cleanup every hour
        await asyncio.sleep(3600)


# Global storage instance
history_storage = HistoryStorage()
