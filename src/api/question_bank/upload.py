import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from src.model.question import Question
from src.base.db import get_db

router = APIRouter()

@router.post("/upload")
def upload_excel(file: UploadFile, db: Session = Depends(get_db)):
    try:

        df = pd.read_excel(file.file)
        df.columns = df.columns.str.strip()  
        
        required_columns = {"Question", "A", "B", "C", "D"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {required_columns - set(df.columns)}"
            )

        uploaded_questions = []

        # Process each row in the DataFrame
        for _, row in df.iterrows():
            db_question = Question(
                text=row["Question"],
                A=row["A"],
                B=row["B"],
                C=row["C"],
                D=row["D"],
            )
            db.add(db_question)

            uploaded_questions.append({
                "question_text": row["Question"],
                "option_a": row["A"],
                "option_b": row["B"],
                "option_c": row["C"],
                "option_d": row["D"],
            })

        db.commit()  
        return uploaded_questions

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")



