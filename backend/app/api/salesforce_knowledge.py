from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.knowledge import KnowledgeDocument, DocumentChunk
from app.services.salesforce_service import salesforce_service
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from app.core.config import settings

router = APIRouter()

# Configure Gemini for Embeddings
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_embedding(text: str) -> list[float]:
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return a zero-vector fallback or raise
        return [0.0] * 768

def sync_knowledge_background(db: Session):
    try:
        articles = salesforce_service.fetch_knowledge_articles()
        if not articles:
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
        )

        for article in articles:
            sf_id = article['salesforce_id']
            # Check if document already exists
            existing_doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == sf_id).first()
            
            # For simplicity in this demo, if it exists, we skip it. 
            # In production, we'd check 'LastModifiedDate' and update if changed.
            if existing_doc:
                continue

            # 1. Create Document
            new_doc = KnowledgeDocument(
                id=sf_id,
                title=article['title'],
                document_type=article['type']
            )
            db.add(new_doc)
            db.flush()

            # 2. Chunk text
            full_text = f"Title: {article['title']}\n\n{article['content']}"
            chunks = text_splitter.split_text(full_text)

            # 3. Embed and store chunks
            for chunk_text in chunks:
                embedding = generate_embedding(chunk_text)
                new_chunk = DocumentChunk(
                    document_id=sf_id,
                    chunk_text=chunk_text,
                    embedding=embedding
                )
                db.add(new_chunk)
            
            db.commit()
    except Exception as e:
        print(f"Failed to sync Salesforce Knowledge: {e}")
        db.rollback()

@router.post("/sync")
def sync_salesforce_knowledge(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers a background task to fetch Knowledge Articles from Salesforce,
    chunk them, generate embeddings via Gemini, and store in pgvector.
    """
    background_tasks.add_task(sync_knowledge_background, db)
    return {"message": "Salesforce Knowledge Sync started in the background."}

@router.get("/")
def list_knowledge_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    docs = db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()
    result = []
    for d in docs:
        result.append({
            "id": d.id,
            "title": d.title,
            "type": d.document_type,
            "chunks_count": len(d.chunks),
            "created_at": d.created_at
        })
    return result

@router.delete("/{document_id}")
def delete_knowledge_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(doc)
    db.commit()
    return {"message": "Document and all its vector chunks deleted successfully."}
